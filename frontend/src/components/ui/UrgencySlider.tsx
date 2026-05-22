import React from 'react';

interface UrgencySliderProps {
  id: string;
  label: string;
  helper: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
}

export const UrgencySlider: React.FC<UrgencySliderProps> = ({
  id,
  label,
  helper,
  value,
  onChange,
  min = 0,
  max = 12,
}) => {
  const pct = ((value - min) / (max - min)) * 100;

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-baseline justify-between">
        <label htmlFor={id} className="text-xs font-bold text-white uppercase tracking-wider">
          {label}
        </label>
        <span className="text-[11px] text-[#a1a1aa]">{helper}</span>
      </div>
      {/* Notebook margin strip wrapper */}
      <div className="border-l-2 border-l-[#1e3a8a]/50 pl-3">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <input
              id={id}
              type="range"
              min={min}
              max={max}
              value={value}
              onChange={(e) => onChange(Number(e.target.value))}
              className="urgency-slider w-full"
              style={{
                background: `linear-gradient(to right, #e4e4e7 ${pct}%, #232323 ${pct}%)`,
              }}
            />
          </div>
          <div className="flex-shrink-0 text-center px-3 py-1 bg-[#111111] border border-[#1f1f1f] font-mono text-sm font-semibold text-[#e4e4e7] min-w-[64px]">
            {value}mo
          </div>
        </div>
        <div className="flex justify-between font-mono text-[10px] text-[#71717a] mt-1">
          <span>0</span>
          <span>12 months</span>
        </div>
      </div>
    </div>
  );
};
