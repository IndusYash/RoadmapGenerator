import React from 'react';
import type { Milestone } from '../../types';

interface MilestoneCardProps {
  milestone: Milestone;
  index: number;
}

// blur_level is job-clarity metadata, not a visual effect
const clarityConfig = {
  0: { label: 'High Certainty',    bars: 4, color: '#22c55e', textColor: 'text-green-400' },
  1: { label: 'Good Visibility',   bars: 3, color: '#84cc16', textColor: 'text-lime-400' },
  2: { label: 'Projected',         bars: 2, color: '#f59e0b', textColor: 'text-amber-400' },
  3: { label: 'Long-Range Vision', bars: 1, color: '#6366f1', textColor: 'text-indigo-400' },
} as const;

const phaseColors = {
  1: { accent: '#10b981', bg: 'bg-emerald-500/8', border: 'border-emerald-500/20', text: 'text-emerald-400' },
  2: { accent: '#38bdf8', bg: 'bg-sky-500/8',     border: 'border-sky-500/20',     text: 'text-sky-400'     },
  3: { accent: '#a78bfa', bg: 'bg-violet-500/8',  border: 'border-violet-500/20',  text: 'text-violet-400'  },
  4: { accent: '#f87171', bg: 'bg-red-500/8',     border: 'border-red-500/20',     text: 'text-red-400'     },
} as const;

export const MilestoneCard: React.FC<MilestoneCardProps> = ({ milestone, index }) => {
  const clarity = clarityConfig[milestone.blur_level as keyof typeof clarityConfig] ?? clarityConfig[0];
  const phase = phaseColors[milestone.phase as keyof typeof phaseColors] ?? phaseColors[1];

  return (
    <div
      className="group relative border border-[#1f1f1f] bg-[#0d0d0d] hover:border-[#2e2e2e] hover:bg-[#101010] transition-colors duration-150 animate-fadeIn"
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {/* Left accent bar */}
      <div
        className="absolute left-0 top-0 bottom-0 w-[2px]"
        style={{ backgroundColor: phase.accent, opacity: 0.7 }}
      />

      <div className="pl-5 pr-5 py-5">
        {/* ── TOP ROW ─────────────────────────────────── */}
        <div className="flex flex-wrap items-start gap-x-6 gap-y-3 mb-4">
          {/* Milestone ID */}
          <div className="flex items-center gap-3 min-w-0">
            <span className="font-mono text-[11px] font-600 tracking-widest text-[#71717a] select-none">
              {String(index + 1).padStart(2, '0')}
            </span>
            <code className="font-mono text-sm font-semibold text-[#a1a1aa] bg-[#161616] border border-[#252525] px-2 py-0.5 rounded">
              {milestone.code}
            </code>
            <span className={`text-xs font-medium px-2 py-0.5 rounded border ${phase.bg} ${phase.border} ${phase.text}`}>
              Phase {milestone.phase}
            </span>
            {/* Certainty indicator */}
            <div className="flex items-center gap-1.5 ml-1">
              <div className="flex gap-0.5">
                {[1,2,3,4].map((bar) => (
                  <div
                    key={bar}
                    className="w-1.5 h-3 rounded-sm transition-opacity"
                    style={{
                      backgroundColor: bar <= clarity.bars ? clarity.color : '#27272a',
                      opacity: bar <= clarity.bars ? 1 : 1,
                    }}
                  />
                ))}
              </div>
              <span className={`text-[10px] font-medium ${clarity.textColor}`}>{clarity.label}</span>
            </div>
          </div>

          {/* Right side metadata */}
          <div className="flex items-center gap-4 ml-auto text-right flex-shrink-0">
            <div className="text-right">
              <div className="text-[10px] text-[#a1a1aa] uppercase tracking-widest font-mono">Target</div>
              <div className="text-xs font-mono font-medium text-[#e4e4e7]">Month {milestone.target_month}</div>
            </div>
            <div className="text-right">
              <div className="text-[10px] text-[#a1a1aa] uppercase tracking-widest font-mono">Duration</div>
              <div className="text-xs font-mono font-medium text-[#e4e4e7]">{milestone.estimated_duration_weeks}w</div>
            </div>
          </div>
        </div>

        {/* ── TITLE ───────────────────────────────────── */}
        <h3 className="text-[15px] font-semibold text-white mb-2 leading-snug">
          {milestone.title}
        </h3>

        {/* ── UNLOCK STATEMENT ────────────────────────── */}
        <p className="text-sm text-[#d4d4d8] leading-relaxed mb-5 max-w-3xl">
          {milestone.unlock_statement}
        </p>

        {/* ── DATA GRID ───────────────────────────────── */}
        <div className="border-t border-[#1a1a1a] pt-4 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">

          {/* Salary tier — spans more */}
          <div className="sm:col-span-2 flex flex-col gap-1">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#a1a1aa]">Salary Tier</span>
            <span className="text-xs text-white font-medium">{milestone.salary_tier}</span>
          </div>

          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#a1a1aa]">Expected By</span>
            <span className="text-xs text-[#d4d4d8]">{milestone.expected_completion}</span>
          </div>

          {/* Divider (hidden on small) */}
          <div className="hidden lg:block border-l border-[#1f1f1f] self-stretch" />

          {/* Stats */}
          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#a1a1aa]">Scenarios</span>
            <span className="font-mono text-sm font-semibold text-white">{milestone.scenario_count}</span>
          </div>

          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#a1a1aa]">Assessments</span>
            <span className="font-mono text-sm font-semibold text-white">{milestone.assessment_count}</span>
          </div>

          <div className="flex flex-col gap-1">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#a1a1aa]">Interviews</span>
            <span className="font-mono text-sm font-semibold text-white">{milestone.mock_interview_count}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
