import React from 'react';

interface SelectFieldProps {
  id: string;
  label: string;
  helper: string;
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
}

export const SelectField: React.FC<SelectFieldProps> = ({
  id,
  label,
  helper,
  value,
  onChange,
  options,
}) => {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-baseline justify-between">
        <label htmlFor={id} className="text-xs font-bold text-white uppercase tracking-wider">
          {label}
        </label>
        <span className="text-[11px] text-[#a1a1aa]">{helper}</span>
      </div>
      {/* Notebook margin strip wrapper */}
      <div className="relative border-l-2 border-l-[#1e3a8a]/50 focus-within:border-l-[#3b82f6] transition-colors duration-150">
        <select
          id={id}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 bg-[#0d0d0d] border border-[#1f1f1f] border-l-0 text-[#e4e4e7] text-sm font-mono
            appearance-none cursor-pointer
            focus:outline-none focus:border-[#2e2e2e]
            hover:border-[#2a2a2a] transition-colors duration-150"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-3 flex items-center">
          <svg className="w-3 h-3 text-[#52525b]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );
};
