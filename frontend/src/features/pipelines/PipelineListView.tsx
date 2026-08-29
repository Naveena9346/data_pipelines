import React, { useEffect, useState } from 'react';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { Workflow, Play, Search, Filter, Plus } from 'lucide-react';
import { apiClient } from '../../services/api';
import { Pipeline } from '../../types';

export const PipelineListView: React.FC = () => {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchPipelines = async () => {
    try {
      const res = await apiClient.get('/pipelines');
      setPipelines(res.data);
    } catch (err) {
      console.error('Failed to fetch pipelines:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPipelines();
  }, []);

  const handleExecute = async (pipelineId: number, pipelineName: string) => {
    try {
      const res = await apiClient.post(`/pipelines/${pipelineId}/execute`);
      alert(`Pipeline '${pipelineName}' executed successfully!\nTotal records processed: ${res.data.total_records_processed}\nStatus: ${res.data.execution_status}`);
      fetchPipelines();
    } catch (err: any) {
      alert(`Execution failed: ${err.response?.data?.detail || err.message}`);
    }
  };

  const filteredPipelines = pipelines.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (p.description && p.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Data Pipelines Management</h2>
          <p className="text-sm text-slate-400">Create, validate, execute, and monitor ETL/ELT pipeline workflows.</p>
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium text-sm transition shadow-md">
          <Plus className="w-4 h-4" />
          <span>New Pipeline</span>
        </button>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex items-center space-x-4 bg-slate-800/80 p-4 rounded-xl border border-slate-700/60 shadow-md">
        <div className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search pipelines by name, schedule, or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 text-slate-200 pl-10 pr-4 py-2 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
          />
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm font-medium transition">
          <Filter className="w-4 h-4" />
          <span>Filter</span>
        </button>
      </div>

      {/* Pipeline Grid */}
      <div className="grid grid-cols-1 gap-4">
        {filteredPipelines.length > 0 ? (
          filteredPipelines.map((pipe) => (
            <div key={pipe.id} className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-lg hover:border-slate-600 transition flex items-center justify-between">
              <div className="space-y-2 max-w-2xl">
                <div className="flex items-center space-x-3">
                  <Workflow className="w-5 h-5 text-indigo-400" />
                  <h3 className="text-base font-bold text-slate-100">{pipe.name}</h3>
                  <StatusBadge status="SUCCESS" />
                  {pipe.is_active ? (
                    <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Active</span>
                  ) : (
                    <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 bg-slate-500/10 px-2 py-0.5 rounded border border-slate-500/20">Paused</span>
                  )}
                </div>
                <p className="text-xs text-slate-400">{pipe.description}</p>
                <div className="flex items-center space-x-4 text-xs text-slate-400">
                  <span>Schedule: <code className="text-indigo-400 bg-slate-900 px-1.5 py-0.5 rounded">{pipe.cron_schedule || 'Manual'}</code></span>
                  <span>DAG Nodes: <strong className="text-slate-200">{pipe.nodes ? pipe.nodes.length : 4}</strong></span>
                  <span>Created: {new Date(pipe.created_at).toLocaleDateString()}</span>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <button 
                  onClick={() => handleExecute(pipe.id, pipe.name)}
                  className="flex items-center space-x-2 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition shadow-md"
                >
                  <Play className="w-3.5 h-3.5" />
                  <span>Execute Now</span>
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12 text-slate-400">
            No pipelines found.
          </div>
        )}
      </div>
    </div>
  );
};
