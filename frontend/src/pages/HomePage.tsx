import React from 'react';
import { useRoadmap } from '../hooks/useRoadmap';
import { InputField } from '../components/ui/InputField';
import { TagInput } from '../components/ui/TagInput';
import { UrgencySlider } from '../components/ui/UrgencySlider';
import { SelectField } from '../components/ui/SelectField';
import { Button } from '../components/ui/Button';
import { Loader } from '../components/ui/Loader';
import { RoadmapTimeline } from '../components/roadmap/RoadmapTimeline';

const ICP_OPTIONS = [
  { value: 'ICP-A', label: 'ICP-A — High Wage (₹8 LPA+)' },
  { value: 'ICP-B', label: 'ICP-B — Low Wage (Below ₹8 LPA)' },
];
const LANGUAGE_OPTIONS = [
  { value: 'en', label: 'English' },
  { value: 'hi', label: 'Hindi' },
];

export const HomePage: React.FC = () => {
  const { form, updateField, loading, roadmap, error, submit, reset } = useRoadmap();

  React.useEffect(() => {
    if (loading) {
      setTimeout(() => {
        document.getElementById('output-panel')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    }
  }, [loading]);

  React.useEffect(() => {
    if (roadmap) {
      setTimeout(() => {
        document.getElementById('roadmap-output')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 80);
    }
  }, [roadmap]);

  const isReady = form.name.trim().length > 0 && form.target_role.trim().length > 0;

  return (
    <div className="min-h-screen text-[#e4e4e7]">

      {/* ── NAV ──────────────────────────────────────────── */}
      <nav className="border-b border-[#1a1a1a] bg-[#080808]/95 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-8xl mx-auto px-6 h-12 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-[#e4e4e7]" />
            <span className="font-mono text-sm font-semibold tracking-tight text-[#e4e4e7]">
              roadmap.ai
            </span>
            <span className="text-[#232323] font-mono text-sm">/</span>
            <span className="font-mono text-xs text-[#52525b]">career-planner</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden sm:inline font-mono text-[11px] text-[#3f3f46]">v1.0.0</span>
            <div className="flex items-center gap-1.5">
              <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
              <span className="font-mono text-[11px] text-[#52525b]">AI Pipeline Ready</span>
            </div>
          </div>
        </div>
      </nav>

      {/* ── HERO ─────────────────────────────────────────── */}
      <div className="border-b border-[#1a1a1a]">
        <div className="max-w-8xl mx-auto px-6 py-14">
          <div className="max-w-3xl">
            <div className="flex items-center gap-2 mb-4">
              <span className="font-mono text-[11px] text-[#52525b] uppercase tracking-widest">Career Intelligence</span>
              <span className="font-mono text-[#2e2e2e]">·</span>
              <span className="font-mono text-[11px] text-[#52525b]">AI-Powered</span>
            </div>

            <h1 className="text-4xl sm:text-5xl font-bold text-[#e4e4e7] mb-5 leading-tight tracking-tight">
              AI Career Roadmap<br />
              <span className="text-[#52525b]">Generator</span>
            </h1>

            <p className="text-[#d4d4d8] text-base leading-relaxed max-w-xl">
              Generate personalized milestone-based career execution plans powered by AI.
              7 milestones across phased timelines with salary targets and practice scenarios.
            </p>

            {/* Quick facts */}
            <div className="flex flex-wrap gap-4 mt-8">
              {[
                { k: '07', v: 'Milestones' },
                { k: '04', v: 'Phases' },
                { k: '~', v: 'AI + Fallback' },
                { k: 'EN/HI', v: 'Language' },
              ].map((f) => (
                <div key={f.k} className="flex items-center gap-2 border border-[#1f1f1f] px-3 py-2 bg-[#0d0d0d]">
                  <span className="font-mono text-sm font-semibold text-[#e4e4e7]">{f.k}</span>
                  <span className="font-mono text-xs text-[#52525b]">{f.v}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── MAIN LAYOUT ──────────────────────────────────── */}
      <div className="max-w-8xl mx-auto px-6 py-10">
        <div className="grid grid-cols-1 xl:grid-cols-[380px_1fr] gap-8 items-start">

          {/* ── LEFT: INPUT FORM ────────────────────────── */}
          <div className="xl:sticky xl:top-20">
            {/* Form header */}
            <div className="flex items-center gap-2 mb-3 pb-3 border-b border-[#1a1a1a]">
              <span className="font-mono text-[11px] text-[#a1a1aa] uppercase tracking-widest">Input Profile</span>
              <span className="ml-auto font-mono text-[11px] text-[#a1a1aa]">9 fields</span>
            </div>

            <div className="border border-[#1a1a1a] bg-[#0a0a0a] divide-y divide-[#141414]">

              {/* SECTION: Identity */}
              <div className="px-4 py-3 bg-[#0d0d0d]">
                <span className="font-mono text-[10px] text-[#a1a1aa] uppercase tracking-widest">Identity</span>
              </div>
              <div className="px-4 py-4 space-y-4">
                <InputField id="name" label="Name" helper="Full name" value={form.name}
                  onChange={(v) => updateField('name', v)} placeholder="Aisha Sharma" />
                <SelectField id="icp_type" label="ICP Type" helper="Profile category" value={form.icp_type}
                  onChange={(v) => updateField('icp_type', v as 'ICP-A' | 'ICP-B')} options={ICP_OPTIONS} />
                <InputField id="location" label="Location" helper="City / Region" value={form.location}
                  onChange={(v) => updateField('location', v)} placeholder="Bengaluru" />
              </div>

              {/* SECTION: Career */}
              <div className="px-4 py-3 bg-[#0d0d0d]">
                <span className="font-mono text-[10px] text-[#a1a1aa] uppercase tracking-widest">Career</span>
              </div>
              <div className="px-4 py-4 space-y-4">
                <InputField id="current_role" label="Current Role" helper="Present situation" value={form.current_role}
                  onChange={(v) => updateField('current_role', v)} placeholder="Final-year Student" />
                <InputField id="target_role" label="Target Role" helper="Desired position" value={form.target_role}
                  onChange={(v) => updateField('target_role', v)} placeholder="AI Engineer" />
                <InputField id="experience_months" label="Experience" helper="Months of work exp." type="number"
                  value={form.experience_months} onChange={(v) => updateField('experience_months', Number(v))}
                  placeholder="0" min={0} />
              </div>

              {/* SECTION: Plan */}
              <div className="px-4 py-3 bg-[#0d0d0d]">
                <span className="font-mono text-[10px] text-[#a1a1aa] uppercase tracking-widest">Plan</span>
              </div>
              <div className="px-4 py-4 space-y-4">
                <UrgencySlider id="urgency_months" label="Urgency" helper="Target timeline"
                  value={form.urgency_months} onChange={(v) => updateField('urgency_months', v)} />
                <SelectField id="language" label="Language" helper="Output language" value={form.language}
                  onChange={(v) => updateField('language', v as 'en' | 'hi')} options={LANGUAGE_OPTIONS} />
                <TagInput id="skills" label="Skills" helper="Known skills" tags={form.skills}
                  onChange={(tags) => updateField('skills', tags)} />
              </div>

              {/* CTA */}
              <div className="px-4 py-4 bg-[#0d0d0d]">
                {error && (
                  <div className="mb-3 px-3 py-2 border border-red-900/40 bg-red-950/20 font-mono text-[12px] text-red-400">
                    <span className="text-red-500 mr-2">ERR</span>{error}
                  </div>
                )}
                <div className="flex gap-2">
                  <Button id="generate-roadmap-btn" onClick={submit} loading={loading} disabled={!isReady} className="flex-1">
                    {loading ? 'Generating...' : '→ Generate Roadmap'}
                  </Button>
                  {roadmap && (
                    <Button id="reset-btn" onClick={reset} variant="secondary">Reset</Button>
                  )}
                </div>
                {!isReady && (
                  <p className="mt-2 font-mono text-[11px] text-[#71717a]">
                    Name and Target Role required
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* ── RIGHT: OUTPUT PANEL ─────────────────────── */}
          <div id="output-panel" className="min-h-[300px]">
            {!loading && !roadmap && (
              <div className="border border-[#1a1a1a] bg-[#0a0a0a] h-full min-h-[500px] flex flex-col items-center justify-center gap-4 text-center px-8">
                {/* Diagram placeholder */}
                <div className="w-full max-w-md font-mono text-[12px] text-[#232323] leading-6 text-left">
                  <div>{'┌──────────────────────────────────┐'}</div>
                  <div>{'│  Input Profile                   │'}</div>
                  <div>{'│  ─────────────────────────       │'}</div>
                  <div>{'│  name, role, skills, urgency     │'}</div>
                  <div>{'└──────────────┬───────────────────┘'}</div>
                  <div>{'               │'}</div>
                  <div>{'               ▼'}</div>
                  <div>{'┌──────────────────────────────────┐'}</div>
                  <div>{'│  AI Pipeline                     │'}</div>
                  <div>{'│  ─────────────────────────       │'}</div>
                  <div>{'│  Claude Sonnet → Fallback Gen    │'}</div>
                  <div>{'└──────────────┬───────────────────┘'}</div>
                  <div>{'               │'}</div>
                  <div>{'               ▼'}</div>
                  <div>{'┌──────────────────────────────────┐'}</div>
                  <div>{'│  RoadmapResponse                 │'}</div>
                  <div>{'│  ─────────────────────────       │'}</div>
                  <div>{'│  7 milestones · 4 phases         │'}</div>
                  <div>{'│  salary_tier · blur_level        │'}</div>
                  <div>{'│  scenarios · assessments         │'}</div>
                  <div>{'└──────────────────────────────────┘'}</div>
                </div>
                <p className="font-mono text-[12px] text-[#71717a] mt-2">
                  Fill in the profile and click Generate Roadmap
                </p>
              </div>
            )}

            {loading && (
              <div className="border border-[#1a1a1a] bg-[#0a0a0a]">
                <Loader />
              </div>
            )}

            {roadmap && !loading && (
              <RoadmapTimeline roadmap={roadmap} userName={form.name} />
            )}
          </div>
        </div>
      </div>

      {/* ── FOOTER ───────────────────────────────────────── */}
      <div className="border-t border-[#1a1a1a] mt-8">
        <div className="max-w-8xl mx-auto px-6 py-4 flex items-center justify-between">
          <span className="font-mono text-[11px] text-[#71717a]">roadmap.ai · Career Intelligence Platform</span>
        </div>
      </div>
    </div>
  );
};
