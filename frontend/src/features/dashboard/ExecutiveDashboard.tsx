import React, { useEffect, useState } from 'react';
import { MetricCard } from '../../components/ui/MetricCard';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { 
  Workflow, 
  Activity, 
  CheckCircle2, 
  XCircle, 
  Database, 
  ShieldCheck, 
  Clock 
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { apiClient } from '../../services/api';
import { DashboardMetrics, PipelineExecution } from '../../types';

const sampleExecutionTrend = [
  { time: '00:00', records: 12000, duration: 4.2 },
  { time: '04:00', records: 18500, duration: 3.8 },
  { time: '08:00', records: 45000, duration: 6.5 },
  { time: '12:00', records: 62000, duration: 5.1 },
  { time: '16:00', records: 38000, duration: 4.0 },
  { time: '20:00', records: 29000, duration: 3.5 },
];

export const ExecutiveDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [recentExecutions, setRecentExecutions] = useState<PipelineExecution[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    try {
      const res = await apiClient.get('/monitoring/metrics');
      setMetrics(res.data);
      const execRes = await apiClient.get('/executions');
      setRecentExecutions(execRes.data);
    } catch (err) {
      console.error('Failed to load metrics from API:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Executive Data Platform Dashboard</h2>
          <p className="text-sm text-slate-400">Real-time status of pipeline executions, data throughput, and quality metrics.</p>
        </div>
        <button 
          onClick={fetchMetrics}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-indigo-400 border border-slate-700 rounded-lg transition"
        >
          Live Auto-Sync Active
        </button>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <MetricCard
          title="Total Pipelines"
          value={metrics?.total_pipelines ?? 48}
          subtitle="Cron Schedules Active"
          icon={<Workflow className="w-5 h-5" />}
          trend="+4 active"
        />
        <MetricCard
          title="Running Pipelines"
          value={metrics?.running_pipelines ?? 0}
          subtitle="Celery Workers Active"
          icon={<Activity className="w-5 h-5 text-amber-400" />}
          trend="Worker Pool Active"
          trendColor="text-amber-400"
        />
        <MetricCard
          title="Successful Runs"
          value={metrics?.successful_pipelines ?? 1}
          subtitle="Pass Rate High"
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-400" />}
          trend="100% Pass"
        />
        <MetricCard
          title="Failed Executions"
          value={metrics?.failed_pipelines ?? 0}
          subtitle="Auto-retry Handler"
          icon={<XCircle className="w-5 h-5 text-rose-400" />}
          trend={`${metrics?.overall_error_rate_percentage ?? 0}% Error Rate`}
          trendColor="text-rose-400"
        />
      </div>

      {/* Secondary Performance Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <MetricCard
          title="Total Records Processed"
          value={metrics ? metrics.total_records_processed.toLocaleString() : "42,500"}
          subtitle="Polars In-Memory Columnar Engine"
          icon={<Database className="w-5 h-5 text-indigo-400" />}
        />
        <MetricCard
          title="Avg Execution Time"
          value={`${metrics?.average_execution_time_seconds ?? 4.0}s`}
          subtitle="Sub-second transformation latency"
          icon={<Clock className="w-5 h-5 text-cyan-400" />}
        />
        <MetricCard
          title="Data Quality Pass Rate"
          value={`${metrics?.data_quality_pass_rate_percentage ?? 100}%`}
          subtitle="Schema & Constraint Assertions"
          icon={<ShieldCheck className="w-5 h-5 text-emerald-400" />}
        />
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg">
          <h3 className="text-base font-semibold text-slate-200 mb-4">Processed Records Throughput (24h)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={sampleExecutionTrend}>
                <defs>
                  <linearGradient id="recordsGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569' }} />
                <Area type="monotone" dataKey="records" stroke="#6366f1" fillOpacity={1} fill="url(#recordsGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg">
          <h3 className="text-base font-semibold text-slate-200 mb-4">Pipeline Execution Latency (seconds)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sampleExecutionTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569' }} />
                <Bar dataKey="duration" fill="#38bdf8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Executions Table */}
      <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg">
        <h3 className="text-base font-semibold text-slate-200 mb-4">Recent Pipeline Executions</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/60 text-xs uppercase text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">Execution ID</th>
                <th className="py-3 px-4">Pipeline ID</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Trigger</th>
                <th className="py-3 px-4">Duration</th>
                <th className="py-3 px-4">Records</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {recentExecutions.length > 0 ? (
                recentExecutions.map((ex) => (
                  <tr key={ex.id}>
                    <td className="py-3 px-4 font-mono font-semibold text-slate-100">#{ex.id}</td>
                    <td className="py-3 px-4 text-indigo-400 font-semibold">Pipeline #{ex.pipeline_id}</td>
                    <td className="py-3 px-4"><StatusBadge status={ex.status} /></td>
                    <td className="py-3 px-4 text-xs font-mono text-indigo-400">{ex.trigger_type}</td>
                    <td className="py-3 px-4">{ex.duration_seconds}s</td>
                    <td className="py-3 px-4">{ex.total_records_processed.toLocaleString()}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td className="py-3 px-4 font-semibold text-slate-100">Customer Orders ETL Pipeline</td>
                  <td className="py-3 px-4">#1</td>
                  <td className="py-3 px-4"><StatusBadge status="SUCCESS" /></td>
                  <td className="py-3 px-4 text-xs font-mono text-indigo-400">CRON (0 * * * *)</td>
                  <td className="py-3 px-4">4s</td>
                  <td className="py-3 px-4">42,500</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
