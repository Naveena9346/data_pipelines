export type RoleType = 
  | 'SUPER_ADMIN' 
  | 'ADMIN' 
  | 'DATA_ENGINEER' 
  | 'DATA_ANALYST' 
  | 'DEVELOPER' 
  | 'VIEWER';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role_id: number;
  role_name: RoleType;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export type SourceType = 
  | 'POSTGRES' 
  | 'MYSQL' 
  | 'SQLITE' 
  | 'SNOWFLAKE' 
  | 'CSV_FILE' 
  | 'JSON_FILE' 
  | 'PARQUET_FILE' 
  | 'EXCEL_FILE' 
  | 'S3_BUCKET' 
  | 'REST_API';

export interface DataSource {
  id: number;
  name: string;
  description?: string;
  source_type: SourceType;
  is_active: boolean;
  created_by_id: number;
  created_at: string;
}

export type NodeType = 
  | 'EXTRACTOR_DB' 
  | 'EXTRACTOR_FILE' 
  | 'EXTRACTOR_API' 
  | 'TRANSFORM_POLARS' 
  | 'TRANSFORM_DUCKDB' 
  | 'TRANSFORM_SQL' 
  | 'VALIDATOR_SCHEMA' 
  | 'VALIDATOR_QUALITY' 
  | 'LOADER_DB' 
  | 'LOADER_FILE' 
  | 'ALERT_NOTIFICATION';

export interface PipelineNode {
  id?: number;
  node_key: string;
  name: string;
  node_type: NodeType;
  config_json: Record<string, any>;
  position_x: number;
  position_y: number;
}

export interface PipelineEdge {
  id?: number;
  edge_key: string;
  source_node_key: string;
  target_node_key: string;
  condition_expression?: string;
}

export interface Pipeline {
  id: number;
  name: string;
  description?: string;
  cron_schedule?: string;
  is_active: boolean;
  max_retries: number;
  retry_delay_seconds: number;
  timeout_seconds: number;
  created_by_id: number;
  created_at: string;
  updated_at: string;
  nodes: PipelineNode[];
  edges: PipelineEdge[];
}

export type ExecutionStatus = 
  | 'PENDING' 
  | 'QUEUED' 
  | 'RUNNING' 
  | 'SUCCESS' 
  | 'FAILED' 
  | 'CANCELLED';

export interface PipelineExecution {
  id: number;
  pipeline_id: number;
  status: ExecutionStatus;
  trigger_type: string;
  triggered_by_id?: number;
  started_at?: string;
  finished_at?: string;
  duration_seconds: number;
  total_records_processed: number;
  error_summary?: string;
}

export interface DashboardMetrics {
  total_pipelines: number;
  running_pipelines: number;
  successful_pipelines: number;
  failed_pipelines: number;
  total_records_processed: number;
  average_execution_time_seconds: number;
  overall_error_rate_percentage: number;
  active_data_sources: number;
  data_quality_pass_rate_percentage: number;
  recent_executions: PipelineExecution[];
}
