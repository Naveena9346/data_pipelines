import pytest
from app.domain.orchestration.dag_compiler import DAGCompiler
from app.domain.orchestration.executor import PipelineExecutor
from app.core.exceptions import DAGCycleError


def test_dag_cycle_detection():
    nodes = [
        {"node_key": "N1", "name": "Extract"},
        {"node_key": "N2", "name": "Transform"},
        {"node_key": "N3", "name": "Load"}
    ]
    # Cyclic edge: N3 -> N1 creates a cycle
    cyclic_edges = [
        {"source_node_key": "N1", "target_node_key": "N2"},
        {"source_node_key": "N2", "target_node_key": "N3"},
        {"source_node_key": "N3", "target_node_key": "N1"}
    ]

    with pytest.raises(DAGCycleError):
        DAGCompiler.compile_and_toposort(nodes, cyclic_edges)


def test_pipeline_dag_full_execution():
    nodes = [
        {"node_key": "ext1", "name": "Extract Orders CSV", "node_type": "EXTRACTOR_FILE", "config_json": {}},
        {
            "node_key": "tr1",
            "name": "Filter Tech Orders",
            "node_type": "TRANSFORM_POLARS",
            "config_json": {"operator_type": "FILTER", "column": "status", "operator": "==", "value": "ACTIVE"}
        },
        {"node_key": "load1", "name": "Load to Data Lake", "node_type": "LOADER_FILE", "config_json": {}}
    ]
    edges = [
        {"source_node_key": "ext1", "target_node_key": "tr1"},
        {"source_node_key": "tr1", "target_node_key": "load1"}
    ]

    res = PipelineExecutor.execute_pipeline_dag(nodes, edges)
    assert res["status"] == "SUCCESS"
    assert len(res["node_results"]) == 3
    assert res["topological_order"] == ["ext1", "tr1", "load1"]
