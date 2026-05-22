import React from 'react';
import type { RoadmapResponse } from '../../types';
import { PhaseSection } from './PhaseSection';
import { ExportButton } from './ExportButton';

interface RoadmapTimelineProps {
  roadmap: RoadmapResponse;
  userName?: string;
}

export const RoadmapTimeline: React.FC<RoadmapTimelineProps> = ({ roadmap, userName }) => {
  const { milestones } = roadmap;

  // Group by phase
  const phases = milestones.reduce<Record<number, typeof milestones>>((acc, m) => {
    if (!acc[m.phase]) acc[m.phase] = [];
    acc[m.phase].push(m);
    return acc;
  }, {});
  const sortedPhases = Object.keys(phases).map(Number).sort((a, b) => a - b);

  // Summary stats
  const totalMonths   = Math.max(...milestones.map((m) => m.target_month));
  const totalScenarios = milestones.reduce((s, m) => s + m.scenario_count, 0);
  const totalAssessments = milestones.reduce((s, m) => s + m.assessment_count, 0);
  const totalInterviews = milestones.reduce((s, m) => s + m.mock_interview_count, 0);

  let globalIndex = 0;

  return (
    <section id="roadmap-output" className="animate-fadeIn">

      {/* ── Header bar ───────────────────────────────── */}
      <div className="border border-[#1f1f1f] bg-[#0a0a0a] mb-0">
        <div className="flex flex-col sm:flex-row sm:items-center gap-4 px-6 py-5 border-b border-[#1a1a1a]">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
              <span className="font-mono text-[11px] text-[#52525b] uppercase tracking-widest">Generated</span>
            </div>
            <h2 className="text-xl font-semibold text-white">
              {userName ? `${userName}'s` : 'Your'} Career Execution Plan
            </h2>
          </div>

          {/* Stat chips */}
          <div className="sm:ml-auto flex flex-wrap items-center gap-2">
            {[
              { label: 'Milestones', value: '7' },
              { label: 'Timeline', value: `${totalMonths}mo` },
              { label: 'Scenarios', value: String(totalScenarios) },
              { label: 'Assessments', value: String(totalAssessments) },
              { label: 'Interviews', value: String(totalInterviews) },
            ].map((s) => (
              <div key={s.label} className="flex items-center gap-1.5 px-3 py-1.5 bg-[#111111] border border-[#1f1f1f] rounded">
                <span className="font-mono text-sm font-semibold text-white">{s.value}</span>
                <span className="text-[11px] text-[#52525b]">{s.label}</span>
              </div>
            ))}
            <ExportButton elementId="roadmap-output" userName={userName} className="ml-1" />
          </div>
        </div>

        {/* Certainty legend */}
        <div className="flex flex-wrap items-center gap-x-6 gap-y-2 px-6 py-3">
          <span className="font-mono text-[10px] text-[#a1a1aa] uppercase tracking-widest">Certainty</span>
          {[
            { bars: 4, color: '#22c55e', label: 'High — Clear & immediate' },
            { bars: 3, color: '#84cc16', label: 'Good — Defined direction' },
            { bars: 2, color: '#f59e0b', label: 'Medium — Projected outcome' },
            { bars: 1, color: '#6366f1', label: 'Low — Long-range vision' },
          ].map((item) => (
            <div key={item.bars} className="flex items-center gap-1.5">
              <div className="flex gap-0.5">
                {[1,2,3,4].map((b) => (
                  <div
                    key={b}
                    className="w-1 h-2.5 rounded-sm"
                    style={{ backgroundColor: b <= item.bars ? item.color : '#232323' }}
                  />
                ))}
              </div>
              <span className="text-[10px] text-[#a1a1aa]">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Phase sections ────────────────────────────── */}
      <div className="border-l border-r border-[#1f1f1f]">
        {sortedPhases.map((phase) => {
          const phaseMilestones = phases[phase];
          const startIndex = globalIndex;
          globalIndex += phaseMilestones.length;
          return (
            <PhaseSection
              key={phase}
              phase={phase}
              milestones={phaseMilestones}
              globalStartIndex={startIndex}
            />
          );
        })}
      </div>

      {/* ── Footer ───────────────────────────────────── */}
      <div className="border border-t-0 border-[#1f1f1f] bg-[#0a0a0a] px-6 py-4 flex flex-wrap items-center justify-between gap-3">
        <span className="font-mono text-[11px] text-[#71717a]">
          roadmap.generated · {new Date().toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' })}
        </span>
        <span className="font-mono text-[11px] text-[#71717a]">
          {sortedPhases.length} phases · 7 milestones
        </span>
      </div>
    </section>
  );
};
