import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Workflow, 
  Database, 
  Activity, 
  ShieldCheck, 
  Settings,
  PlusCircle
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Pipelines', path: '/pipelines', icon: Workflow },
    { label: 'DAG Builder', path: '/builder', icon: PlusCircle },
    { label: 'Data Sources', path: '/sources', icon: Database },
    { label: 'Execution & Quality', path: '/monitoring', icon: Activity },
    { label: 'Audit Logs', path: '/audit', icon: ShieldCheck },
    { label: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-800/40 border-r border-slate-700/60 p-4 flex flex-col justify-between">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[10px] font-bold tracking-wider text-slate-400 uppercase">
          Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                  isActive
                    ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/30'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      <div className="p-3 bg-slate-800/80 rounded-lg border border-slate-700/60 text-xs text-slate-400">
        <p className="font-semibold text-slate-300">DataForge v1.0.0</p>
        <p className="mt-0.5">Polars + DuckDB Engine Active</p>
      </div>
    </aside>
  );
};
