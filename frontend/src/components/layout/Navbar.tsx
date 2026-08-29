import React from 'react';
import { useAuthStore } from '../../store/useAuthStore';
import { LogOut, User as UserIcon, ShieldAlert } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <header className="h-16 bg-slate-800/90 border-b border-slate-700/80 px-6 flex items-center justify-between sticky top-0 z-30 backdrop-blur-md">
      <div className="flex items-center space-x-3">
        <div className="h-9 w-9 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-lg text-white shadow-md">
          DF
        </div>
        <div>
          <h1 className="font-bold text-slate-100 text-base leading-none">DataForge Platform</h1>
          <span className="text-xs text-indigo-400 font-medium">Enterprise Data Engineering</span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-700/40 border border-slate-600/50">
          <ShieldAlert className="w-4 h-4 text-emerald-400" />
          <span className="text-xs text-slate-300 font-medium">
            Role: <span className="text-indigo-400 font-semibold">{user?.role_name || 'DATA_ENGINEER'}</span>
          </span>
        </div>

        <div className="flex items-center space-x-2 border-l border-slate-700 pl-4">
          <div className="text-right">
            <p className="text-xs font-semibold text-slate-200">{user?.full_name || 'Lead Engineer'}</p>
            <p className="text-[10px] text-slate-400">{user?.email || 'admin@dataforge.io'}</p>
          </div>
          <button
            onClick={logout}
            className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-700/50 transition"
            title="Log out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
