import React, { useState } from 'react';
import { useAuthStore } from '../../store/useAuthStore';
import { ShieldCheck, Lock, Mail } from 'lucide-react';

export const LoginView: React.FC = () => {
  const [email, setEmail] = useState('admin@dataforge.io');
  const [password, setPassword] = useState('password123');
  const { setAuth } = useAuthStore();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setAuth(
      {
        id: 1,
        email,
        full_name: 'Lead Data Engineer',
        role_id: 1,
        role_name: 'SUPER_ADMIN',
        is_active: true,
        is_superuser: true,
        created_at: new Date().toISOString(),
      },
      'demo_jwt_token_dataforge_2026'
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">
      <div className="max-w-md w-full bg-slate-800/90 border border-slate-700/80 rounded-2xl p-8 shadow-2xl backdrop-blur-xl space-y-6">
        <div className="text-center space-y-2">
          <div className="h-12 w-12 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-2xl text-white shadow-lg mx-auto">
            DF
          </div>
          <h2 className="text-2xl font-bold text-slate-100">DataForge Platform</h2>
          <p className="text-sm text-slate-400">Enterprise Data Engineering & Pipelines Platform</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-slate-100 pl-10 pr-4 py-2.5 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-slate-100 pl-10 pr-4 py-2.5 rounded-lg text-sm focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-semibold text-sm transition shadow-lg flex items-center justify-center space-x-2"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Sign In to Platform</span>
          </button>
        </form>
      </div>
    </div>
  );
};
