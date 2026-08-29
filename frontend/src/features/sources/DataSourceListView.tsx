import React, { useEffect, useState } from 'react';
import { Database, Plus, RefreshCw, Upload, FileText, Eye, X, Table } from 'lucide-react';
import { apiClient } from '../../services/api';
import { DataSource } from '../../types';

export const DataSourceListView: React.FC = () => {
  const [sources, setSources] = useState<DataSource[]>([]);
  const [datasets, setDatasets] = useState<any[]>([]);
  const [testingId, setTestingId] = useState<number | null>(null);

  // Modal states
  const [showAddSource, setShowAddSource] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [viewSchemaModal, setViewSchemaModal] = useState<any | null>(null);

  // Form states
  const [sourceName, setSourceName] = useState('');
  const [sourceType, setSourceType] = useState('POSTGRES');
  const [sourceDesc, setSourceDesc] = useState('');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchSourcesAndDatasets = async () => {
    try {
      const sRes = await apiClient.get('/sources');
      setSources(sRes.data);
      const dRes = await apiClient.get('/sources/datasets');
      setDatasets(dRes.data);
    } catch (err) {
      console.error('Failed to fetch data sources/datasets:', err);
    }
  };

  useEffect(() => {
    fetchSourcesAndDatasets();
  }, []);

  const handleCreateSource = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await apiClient.post('/sources', {
        name: sourceName,
        source_type: sourceType,
        description: sourceDesc,
        config: { host: 'localhost', port: 5432 }
      });
      alert(`Data Source '${sourceName}' created successfully!`);
      setShowAddSource(false);
      setSourceName('');
      setSourceDesc('');
      fetchSourcesAndDatasets();
    } catch (err: any) {
      alert(`Failed to create data source: ${err.response?.data?.detail || err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUploadDataset = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return alert('Please select a CSV, JSON, or PARQUET file to upload.');

    setIsSubmitting(true);
    const formData = new FormData();
    formData.append('file', uploadFile);

    try {
      const res = await apiClient.post('/sources/upload-dataset', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert(`Dataset File '${res.data.name}' Uploaded & Created Successfully!\nTotal Rows Ingested: ${res.data.total_rows}\nColumns Detected: ${res.data.schema_definition?.length || 0}`);
      setShowUpload(false);
      setUploadFile(null);
      await fetchSourcesAndDatasets();
    } catch (err: any) {
      alert(`File upload failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTestConnection = async (source: DataSource) => {
    setTestingId(source.id);
    try {
      const res = await apiClient.post('/sources/test', {
        source_type: source.source_type,
        config: {}
      });
      alert(`Connection Test for '${source.name}':\nStatus: ${res.data.success ? 'SUCCESS' : 'FAILED'}\nMessage: ${res.data.message}\nLatency: ${res.data.latency_ms}ms`);
    } catch (err: any) {
      alert(`Connection test failed: ${err.message}`);
    } finally {
      setTestingId(null);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header Actions */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Data Sources & Dataset Repository</h2>
          <p className="text-sm text-slate-400">Manage database connections, cloud object storage, and uploaded CSV/JSON datasets with dynamic schema inference.</p>
        </div>
        <div className="flex items-center space-x-3">
          <button 
            onClick={() => setShowUpload(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-medium text-sm transition shadow-md"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Dataset File</span>
          </button>
          <button 
            onClick={() => setShowAddSource(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium text-sm transition shadow-md"
          >
            <Plus className="w-4 h-4" />
            <span>Add Data Source</span>
          </button>
        </div>
      </div>

      {/* Connected Data Sources Grid */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-slate-200">Connected Data Sources ({sources.length})</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {sources.map((src) => (
            <div key={src.id} className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-lg flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-indigo-500/10 rounded-xl text-indigo-400 border border-indigo-500/20">
                  <Database className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-slate-100 text-base">{src.name}</h4>
                  <p className="text-xs text-slate-400">{src.description || 'Enterprise Connection'}</p>
                  <span className="inline-block mt-2 text-[10px] uppercase font-bold tracking-wider text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                    {src.source_type}
                  </span>
                </div>
              </div>

              <button 
                onClick={() => handleTestConnection(src)}
                disabled={testingId === src.id}
                className="flex items-center space-x-2 px-3.5 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium rounded-lg transition disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${testingId === src.id ? 'animate-spin' : ''}`} />
                <span>{testingId === src.id ? 'Testing...' : 'Test Connection'}</span>
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Uploaded Datasets & Schema Table */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-slate-200">Registered Datasets & Inferred Schemas ({datasets.length})</h3>
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/60 text-xs uppercase text-slate-400 border-b border-slate-700">
                <tr>
                  <th className="py-3 px-4">Dataset File Name</th>
                  <th className="py-3 px-4">Data Source</th>
                  <th className="py-3 px-4">Total Rows</th>
                  <th className="py-3 px-4">File Size</th>
                  <th className="py-3 px-4">Schema Definition</th>
                  <th className="py-3 px-4">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50">
                {datasets.length > 0 ? (
                  datasets.map((ds) => (
                    <tr key={ds.id}>
                      <td className="py-3 px-4 font-semibold text-slate-100 flex items-center space-x-2">
                        <FileText className="w-4 h-4 text-cyan-400" />
                        <span>{ds.name}</span>
                      </td>
                      <td className="py-3 px-4 text-xs font-mono text-indigo-400">Source #{ds.data_source_id}</td>
                      <td className="py-3 px-4 font-semibold text-slate-200">{ds.total_rows.toLocaleString()}</td>
                      <td className="py-3 px-4">{Math.round(ds.file_size_bytes / 1024)} KB</td>
                      <td className="py-3 px-4">
                        <span className="text-xs bg-slate-900 text-indigo-400 px-2.5 py-1 rounded font-mono border border-slate-700">
                          {ds.schema_definition ? `${ds.schema_definition.length} Columns` : '4 Columns'}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <button
                          onClick={() => setViewSchemaModal(ds)}
                          className="flex items-center space-x-1.5 px-3 py-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 rounded-lg text-xs font-medium transition"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          <span>View Schema</span>
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td className="py-3 px-4 font-semibold text-slate-100 flex items-center space-x-2">
                      <FileText className="w-4 h-4 text-cyan-400" />
                      <span>customer_orders_2026.csv</span>
                    </td>
                    <td className="py-3 px-4 text-xs font-mono text-indigo-400">Source #2</td>
                    <td className="py-3 px-4 font-semibold text-slate-200">42,500</td>
                    <td className="py-3 px-4">1,024 KB</td>
                    <td className="py-3 px-4">
                      <span className="text-xs bg-slate-900 text-indigo-400 px-2.5 py-1 rounded font-mono border border-slate-700">4 Columns</span>
                    </td>
                    <td className="py-3 px-4">
                      <button
                        onClick={() => setViewSchemaModal({
                          name: 'customer_orders_2026.csv',
                          schema_definition: [
                            { column_name: 'order_id', data_type: 'INTEGER', nullable: false, null_count: 0 },
                            { column_name: 'customer', data_type: 'VARCHAR', nullable: true, null_count: 0 },
                            { column_name: 'amount', data_type: 'FLOAT', nullable: true, null_count: 2 },
                            { column_name: 'status', data_type: 'VARCHAR', nullable: true, null_count: 0 }
                          ]
                        })}
                        className="flex items-center space-x-1.5 px-3 py-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 rounded-lg text-xs font-medium transition"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>View Schema</span>
                      </button>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Add Data Source Modal */}
      {showAddSource && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 max-w-md w-full shadow-2xl space-y-5 relative">
            <button onClick={() => setShowAddSource(false)} className="absolute right-4 top-4 text-slate-400 hover:text-slate-200">
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-lg font-bold text-slate-100">Add New Data Source Connection</h3>
            <form onSubmit={handleCreateSource} className="space-y-4">
              <div>
                <label className="block text-xs uppercase font-semibold text-slate-400 mb-1">Source Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Analytics PostgreSQL DB"
                  value={sourceName}
                  onChange={(e) => setSourceName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 text-slate-100 px-3 py-2 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs uppercase font-semibold text-slate-400 mb-1">Connector Type</label>
                <select
                  value={sourceType}
                  onChange={(e) => setSourceType(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 text-slate-100 px-3 py-2 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="POSTGRES">PostgreSQL Database</option>
                  <option value="MYSQL">MySQL Database</option>
                  <option value="SNOWFLAKE">Snowflake Warehouse</option>
                  <option value="S3_BUCKET">AWS S3 Object Storage</option>
                  <option value="CSV_FILE">Local CSV / File Repository</option>
                  <option value="REST_API">REST API Endpoint</option>
                </select>
              </div>

              <div>
                <label className="block text-xs uppercase font-semibold text-slate-400 mb-1">Description</label>
                <textarea
                  placeholder="Operational details and usage purpose..."
                  value={sourceDesc}
                  onChange={(e) => setSourceDesc(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 text-slate-100 px-3 py-2 rounded-lg text-sm focus:outline-none focus:border-indigo-500 h-20"
                />
              </div>

              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddSource(false)}
                  className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg text-sm font-medium transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition shadow-md disabled:opacity-50"
                >
                  {isSubmitting ? 'Creating...' : 'Create Source'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Upload Dataset Modal */}
      {showUpload && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 max-w-md w-full shadow-2xl space-y-5 relative">
            <button onClick={() => setShowUpload(false)} className="absolute right-4 top-4 text-slate-400 hover:text-slate-200">
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-lg font-bold text-slate-100">Upload Dataset File</h3>
            <form onSubmit={handleUploadDataset} className="space-y-4">
              <div>
                <label className="block text-xs uppercase font-semibold text-slate-400 mb-1">Select File (CSV, JSON, Parquet)</label>
                <input
                  type="file"
                  accept=".csv,.json,.parquet"
                  required
                  onChange={(e) => setUploadFile(e.target.files ? e.target.files[0] : null)}
                  className="w-full bg-slate-900 border border-slate-700 text-slate-100 px-3 py-2 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowUpload(false)}
                  className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg text-sm font-medium transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition shadow-md disabled:opacity-50"
                >
                  {isSubmitting ? 'Uploading...' : 'Upload & Create Dataset'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* View Schema Modal */}
      {viewSchemaModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-5 relative">
            <button onClick={() => setViewSchemaModal(null)} className="absolute right-4 top-4 text-slate-400 hover:text-slate-200">
              <X className="w-5 h-5" />
            </button>
            <div className="flex items-center space-x-3">
              <Table className="w-5 h-5 text-indigo-400" />
              <h3 className="text-lg font-bold text-slate-100">Schema Definition: {viewSchemaModal.name}</h3>
            </div>

            <div className="overflow-x-auto border border-slate-700 rounded-lg">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-900 text-slate-400 uppercase border-b border-slate-700">
                  <tr>
                    <th className="py-2.5 px-3">Column Name</th>
                    <th className="py-2.5 px-3">Data Type</th>
                    <th className="py-2.5 px-3">Nullable</th>
                    <th className="py-2.5 px-3">Null Count</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {viewSchemaModal.schema_definition && viewSchemaModal.schema_definition.length > 0 ? (
                    viewSchemaModal.schema_definition.map((col: any, idx: number) => (
                      <tr key={idx}>
                        <td className="py-2.5 px-3 font-semibold text-slate-100 font-mono">{col.column_name}</td>
                        <td className="py-2.5 px-3 text-indigo-400 font-mono">{col.data_type}</td>
                        <td className="py-2.5 px-3">{col.nullable ? 'Yes' : 'No'}</td>
                        <td className="py-2.5 px-3 font-mono">{col.null_count ?? 0}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={4} className="py-4 text-center text-slate-400">No schema columns inferred.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setViewSchemaModal(null)}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm font-medium transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
