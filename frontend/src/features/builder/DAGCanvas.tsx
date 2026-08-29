import React from 'react';
import { Database, Filter, ShieldCheck, HardDrive, Play, CheckCircle } from 'lucide-react';

export const DAGCanvas: React.FC = () => {
  const nodes = [
    { id: '1', name: 'Extract Orders CSV', type: 'Extractor (File)', icon: Database, color: 'border-cyan-500/50 bg-cyan-950/40 text-cyan-400' },
    { id: '2', name: 'Polars Column Mutator', type: 'Transformer', icon: Filter, color: 'border-indigo-500/50 bg-indigo-950/40 text-indigo-400' },
    { id: '3', name: 'Schema & Quality Check', type: 'Validator', icon: ShieldCheck, color: 'border-emerald-500/50 bg-emerald-950/40 text-emerald-400' },
    { id: '4', name: 'Load to PostgreSQL Data Lake', type: 'Sink / Loader', icon: HardDrive, color: 'border-purple-500/50 bg-purple-950/40 text-purple-400' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Visual DAG Pipeline Builder</h2>
          <p className="text-sm text-slate-400">Design directed acyclic workflows with interactive nodes and dependencies.</p>
        </div>
        <div className="flex items-center space-x-3">
          <button 
            onClick={() => alert("DAG topology verified: Acyclic (No cycles detected). Topo order: Extract -> Transform -> Validate -> Load")}
            className="flex items-center space-x-2 px-3.5 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 text-sm font-medium rounded-lg transition"
          >
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>Validate DAG Topology</span>
          </button>
          <button 
            onClick={() => alert("Pipeline Execution Started via Polars/DuckDB Async Execution Runner")}
            className="flex items-center space-x-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition shadow-md"
          >
            <Play className="w-4 h-4" />
            <span>Run Pipeline</span>
          </button>
        </div>
      </div>

      {/* Canvas Workspace */}
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl h-[520px] p-8 relative overflow-hidden flex items-center justify-center bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:24px_24px]">
        <div className="flex items-center space-x-12">
          {nodes.map((node, index) => {
            const Icon = node.icon;
            return (
              <React.Fragment key={node.id}>
                <div className={`w-56 p-5 rounded-xl border ${node.color} shadow-xl backdrop-blur-md relative group hover:scale-105 transition transform cursor-pointer`}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] uppercase font-bold tracking-wider opacity-80">{node.type}</span>
                    <Icon className="w-5 h-5" />
                  </div>
                  <h4 className="font-bold text-slate-100 text-sm leading-snug">{node.name}</h4>
                  <div className="mt-3 pt-3 border-t border-slate-700/50 flex items-center justify-between text-[11px] text-slate-400">
                    <span>Node ID: #{node.id}</span>
                    <span className="text-emerald-400 font-mono">READY</span>
                  </div>
                </div>

                {index < nodes.length - 1 && (
                  <div className="flex items-center text-slate-500">
                    <div className="w-10 h-0.5 bg-indigo-500/60 relative">
                      <div className="absolute right-0 -top-1 w-2 h-2 border-t-2 border-r-2 border-indigo-400 transform rotate-45"></div>
                    </div>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};
