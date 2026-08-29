import React from 'react';
import { ShieldCheck, UserCheck, Settings as SettingsIcon, Database, Server } from 'lucide-react';
import { useAuthStore } from '../../store/useAuthStore';

export const SettingsView: React.FC = () => {
  const { user } = useAuthStore();

  const rolesMatrix = [
    { role: 'Super Admin', desc: 'Full system control, credentials & user management', permissions: 'ALL PERMISSIONS' },
    { role: 'Admin', desc: 'Administrative control of pipelines, users & data sources', permissions: 'ALL PERMISSIONS' },
    { role: 'Data Engineer', desc: 'Create, configure, execute & maintain data pipelines', permissions: 'Pipeline CRUD, Data Source CRUD, Execution' },
    { role: 'Data Analyst', desc: 'Execute pipelines, inspect data quality & view analytics', permissions: 'Pipeline Read/Execute, Quality Reports' },
    { role: 'Developer', desc: 'Develop, test & validate pipeline DAG operators', permissions: 'Pipeline CRUD, Test Connections' },
    { role: 'Viewer', desc: 'Read-only access to pipeline status & dashboards', permissions: 'Pipeline Read, Dashboard Read' },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">System Settings & Role Security</h2>
        <p className="text-sm text-slate-400">Configure role-based permissions, execution worker pools, and system parameters.</p>
      </div>

      {/* Active Session Info */}
      <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-indigo-600/20 rounded-xl text-indigo-400 border border-indigo-500/30">
            <UserCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-slate-100 text-lg">{user?.full_name || 'Lead Data Engineer'}</h3>
            <p className="text-xs text-slate-400">{user?.email || 'admin@dataforge.io'}</p>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xs uppercase font-bold tracking-wider text-indigo-400 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/30">
            Role: {user?.role_name || 'SUPER_ADMIN'}
          </span>
        </div>
      </div>

      {/* RBAC Matrix */}
      <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg space-y-4">
        <h3 className="text-base font-semibold text-slate-200 flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <span>Role-Based Access Control (RBAC) Permissions Matrix</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/60 text-xs uppercase text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">Role Title</th>
                <th className="py-3 px-4">Scope Description</th>
                <th className="py-3 px-4">Granted Permissions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {rolesMatrix.map((r, idx) => (
                <tr key={idx}>
                  <td className="py-3 px-4 font-semibold text-slate-100">{r.role}</td>
                  <td className="py-3 px-4 text-xs text-slate-400">{r.desc}</td>
                  <td className="py-3 px-4">
                    <span className="text-xs bg-slate-900 text-indigo-400 px-2 py-1 rounded font-mono">
                      {r.permissions}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
