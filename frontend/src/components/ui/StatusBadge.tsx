import React from 'react';
import { ExecutionStatus } from '../../types';

interface StatusBadgeProps {
  status: ExecutionStatus | string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getBadgeStyle = (st: string) => {
    switch (st.toUpperCase()) {
      case 'SUCCESS':
      case 'ACTIVE':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'RUNNING':
      case 'QUEUED':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30 animate-pulse';
      case 'FAILED':
      case 'CANCELLED':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'PENDING':
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getBadgeStyle(status)}`}>
      {status}
    </span>
  );
};
