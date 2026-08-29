import React, { useEffect, useState } from 'react';
import { Database, Plus, RefreshCw, HardDrive } from 'lucide-react';
import { apiClient } from '../../services/api';
import { DataSource } from '../../types';

export const DataSourceListView: React.FC = () => {
  const [sources, setSources] = useState<DataSource[]>([]);
  const [testingId, setTestingId] = useState<number | null>(null);

  const fetchSources = async () => {
    try {
      const res = await apiClient.get('/sources');
      setSources(res.data);
    } catch (err) {
      console.error('Failed to fetch data sources:', err);
    }
  };

  useEffect(() => {
    fetchSources();
  }, []);

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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Data Sources & Connectors</h2>
          <p className="text-sm text-slate-400">Manage database connections, cloud object storage, and API data sources.</p>
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium text-sm transition shadow-md">
          <Plus className="w-4 h-4" />
          <span>Add Data Source</span>
        </button>
      </div>

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
              className="flex items-center space-x-2 px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium rounded-lg transition disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${testingId === src.id ? 'animate-spin' : ''}`} />
              <span>{testingId === src.id ? 'Testing...' : 'Test Connection'}</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
