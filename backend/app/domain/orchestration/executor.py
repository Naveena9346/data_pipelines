import time
from typing import Dict, Any, List
import polars as pl
from app.models.execution import ExecutionStatusEnum
from app.domain.orchestration.dag_compiler import DAGCompiler
from app.domain.ingestion.extractors import IngestionExtractor
from app.domain.transformation.operators import apply_transformation_operator
from app.domain.validation.validator import DataQualityValidator
from app.core.exceptions import PipelineExecutionError


class PipelineExecutor:
    """Synchronous & Celery execution engine for DataForge pipelines."""

    @staticmethod
    def execute_pipeline_dag(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
        topological_order = DAGCompiler.compile_and_toposort(nodes, edges)
        node_map = {n["node_key"]: n for n in nodes}

        execution_results = {}
        memory_buffers: Dict[str, pl.DataFrame] = {}
        total_records_processed = 0

        for node_key in topological_order:
            node_cfg = node_map[node_key]
            node_type = node_cfg["node_type"]
            config = node_cfg.get("config_json", {})
            start_time = time.time()

            try:
                # 1. Extractor Nodes
                if "EXTRACTOR" in node_type:
                    file_path = config.get("file_path", "")
                    format_type = config.get("format_type", "CSV")
                    if file_path:
                        df = IngestionExtractor.extract_file(file_path, format_type)
                    else:
                        # Fallback sample data for testing execution
                        df = pl.DataFrame({
                            "id": [1, 2, 3, 4, 5],
                            "category": ["A", "B", "A", "C", "B"],
                            "amount": [100.0, 250.5, 300.0, 450.0, 50.0],
                            "status": ["ACTIVE", "ACTIVE", "INACTIVE", "ACTIVE", "ACTIVE"]
                        })
                    memory_buffers[node_key] = df
                    input_rows = 0
                    output_rows = df.height

                # 2. Transformer Nodes
                elif "TRANSFORM" in node_type:
                    # Find parent node output from edges
                    parent_keys = [e["source_node_key"] for e in edges if e["target_node_key"] == node_key]
                    input_df = memory_buffers.get(parent_keys[0]) if parent_keys else list(memory_buffers.values())[-1]
                    input_rows = input_df.height
                    
                    df = apply_transformation_operator(input_df, config)
                    memory_buffers[node_key] = df
                    output_rows = df.height

                # 3. Validator Nodes
                elif "VALIDATOR" in node_type:
                    parent_keys = [e["source_node_key"] for e in edges if e["target_node_key"] == node_key]
                    input_df = memory_buffers.get(parent_keys[0]) if parent_keys else list(memory_buffers.values())[-1]
                    input_rows = input_df.height

                    rules_cfg = config.get("rules", [
                        {"rule_type": "NOT_NULL", "column": input_df.columns[0]}
                    ])
                    val_report = DataQualityValidator.run_validation(input_df, rules_cfg)
                    memory_buffers[node_key] = input_df
                    output_rows = input_df.height

                    if val_report["failed_rules"] > 0 and config.get("fail_on_error", True):
                        raise PipelineExecutionError(node_key, f"Data Quality Validation failed ({val_report['failed_rules']} rules broken).")

                # 4. Loader / Sink Nodes
                elif "LOADER" in node_type:
                    parent_keys = [e["source_node_key"] for e in edges if e["target_node_key"] == node_key]
                    input_df = memory_buffers.get(parent_keys[0]) if parent_keys else list(memory_buffers.values())[-1]
                    input_rows = input_df.height
                    output_rows = input_rows

                else:
                    input_rows = 0
                    output_rows = 0

                duration_ms = round((time.time() - start_time) * 1000, 2)
                total_records_processed += output_rows

                execution_results[node_key] = {
                    "node_name": node_cfg["name"],
                    "status": ExecutionStatusEnum.SUCCESS,
                    "input_rows": input_rows,
                    "output_rows": output_rows,
                    "duration_ms": duration_ms,
                    "error": None
                }

            except Exception as e:
                execution_results[node_key] = {
                    "node_name": node_cfg["name"],
                    "status": ExecutionStatusEnum.FAILED,
                    "input_rows": 0,
                    "output_rows": 0,
                    "duration_ms": round((time.time() - start_time) * 1000, 2),
                    "error": str(e)
                }
                raise PipelineExecutionError(node_key, str(e))

        return {
            "status": ExecutionStatusEnum.SUCCESS,
            "topological_order": topological_order,
            "total_records_processed": total_records_processed,
            "node_results": execution_results
        }
