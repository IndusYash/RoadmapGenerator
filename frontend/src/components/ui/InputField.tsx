import React from 'react';

interface InputFieldProps {
  id: string;
  label: string;
  helper: string;
  type?: 'text' | 'number' | 'email';
  value: string | number;
  onChange: (value: string) => void;
  placeholder?: string;
  min?: number;
  max?: number;
}

export const InputField: React.FC<InputFieldProps> = ({
  id,
  label,
  helper,
  type = 'text',
  value,
  onChange,
  placeholder,
  min,
  max,
}) => {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-baseline justify-between">
        <label htmlFor={id} className="text-xs font-bold text-white uppercase tracking-wider">
          {label}
        </label>
        <span className="text-[11px] text-[#3f3f46]">{helper}</span>
      </div>
      {/* Notebook margin strip wrapper */}
      <div className="relative border-l-2 border-l-[#1e3a8a]/50 focus-within:border-l-[#3b82f6] transition-colors duration-150">
        <input
          id={id}
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          min={min}
          max={max}
          className="w-full px-3 py-2 bg-[#0d0d0d] border border-[#1f1f1f] border-l-0 text-[#e4e4e7] placeholder-[#3f3f46] text-sm font-mono
            focus:outline-none focus:border-[#2e2e2e]
            hover:border-[#2a2a2a]
            transition-colors duration-150"
        />
      </div>
    </div>
  );
};
