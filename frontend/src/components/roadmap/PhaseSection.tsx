import React from 'react';
import type { Milestone } from '../../types';
import { MilestoneCard } from './MilestoneCard';

interface PhaseSectionProps {
  phase: number;
  milestones: Milestone[];
  globalStartIndex: number;
}

const phaseInfo: Record<number, { label: string; tag: string; description: string; accent: string }> = {
  1: { label: 'Phase 01', tag: 'Foundation',     description: 'Establish baseline and core technical skills',  accent: '#10b981' },
  2: { label: 'Phase 02', tag: 'Specialisation', description: 'Deep-dive into your target domain',             accent: '#38bdf8' },
  3: { label: 'Phase 03', tag: 'Application',    description: 'Build projects and enter the market',           accent: '#a78bfa' },
  4: { label: 'Phase 04', tag: 'Execution',      description: 'Land your target role',                        accent: '#f87171' },
};

export const PhaseSection: React.FC<PhaseSectionProps> = ({ phase, milestones, globalStartIndex }) => {
  const info = phaseInfo[phase] ?? phaseInfo[1];

  return (
    <div className="mb-2">
      {/* Phase header — full-width bar */}
      <div className="flex items-center gap-4 px-5 py-3 border-t border-b border-[#1a1a1a] bg-[#0a0a0a] mb-0">
        <div
          className="w-px h-8 flex-shrink-0"
          style={{ backgroundColor: info.accent }}
        />
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold tracking-widest text-[#a1a1aa] uppercase">
            {info.label}
          </span>
          <span className="text-sm font-semibold text-[#e4e4e7]">{info.tag}</span>
          <span className="hidden sm:inline text-xs text-[#71717a]">—</span>
          <span className="hidden sm:inline text-xs text-[#a1a1aa]">{info.description}</span>
        </div>
        <div className="ml-auto font-mono text-[11px] text-[#71717a]">
          {milestones.length} milestone{milestones.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Milestone cards — no gap, border-separated */}
      <div className="divide-y divide-[#161616]">
        {milestones.map((milestone, i) => (
          <MilestoneCard
            key={milestone.code}
            milestone={milestone}
            index={globalStartIndex + i}
          />
        ))}
      </div>
    </div>
  );
};
