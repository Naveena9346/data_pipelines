import React, { useState } from 'react';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { Workflow, Play, CheckCircle, Search, Filter, Plus } from 'lucide-react';

export const PipelineListView: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const samplePipelines = [
    {
      id: 1,
      name: 'Customer Orders ETL Pipeline',
      description: 'Ingests CSV order logs, applies Polars filter & schema validation, loads to PostgreSQL',
      cron_schedule: '0 * * * *',
      is_active: true,
      nodes_count: 4,
      last_status: 'SUCCESS',
      created_at: '2026-08-28'
    },
    {
      id: 2,
      name: 'Financial Transactions ELT Sync',
      description: 'Executes DuckDB SQL analytical transformations on daily transaction datasets',
      cron_schedule: '0 0 * * *',
      is_active: true,
      nodes_count: 5,
      last_status: 'RUNNING',
      created_at: '2026-08-27'
    },
    {
      id: 3,
      name: 'Clickstream Data Quality Validator',
      description: 'Enforces regex pattern matching, non-null rules, and anomaly thresholds',
      cron_schedule: '*/15 * * * *',
      is_active: false,
      nodes_count: 3,
      last_status: 'FAILED',
      created_at: '2026-08-25'
    }
  ];

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
        {samplePipelines.map((pipe) => (
          <div key={pipe.id} className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-lg hover:border-slate-600 transition flex items-center justify-between">
            <div className="space-y-2 max-w-2xl">
              <div className="flex items-center space-x-3">
                <Workflow className="w-5 h-5 text-indigo-400" />
                <h3 className="text-base font-bold text-slate-100">{pipe.name}</h3>
                <StatusBadge status={pipe.last_status} />
                {pipe.is_active ? (
                  <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Active</span>
                ) : (
                  <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 bg-slate-500/10 px-2 py-0.5 rounded border border-slate-500/20">Paused</span>
                )}
              </div>
              <p className="text-xs text-slate-400">{pipe.description}</p>
              <div className="flex items-center space-x-4 text-xs text-slate-400">
                <span>Schedule: <code className="text-indigo-400 bg-slate-900 px-1.5 py-0.5 rounded">{pipe.cron_schedule}</code></span>
                <span>DAG Nodes: <strong className="text-slate-200">{pipe.nodes_count}</strong></span>
                <span>Created: {pipe.created_at}</span>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button 
                onClick={() => alert(`Executing pipeline: ${pipe.name}`)}
                className="flex items-center space-x-2 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition"
              >
                <Play className="w-3.5 h-3.5" />
                <span>Execute</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
