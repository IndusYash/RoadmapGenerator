import React, { useState } from 'react';
import type { KeyboardEvent } from 'react';

interface TagInputProps {
  id: string;
  label: string;
  helper: string;
  tags: string[];
  onChange: (tags: string[]) => void;
  placeholder?: string;
}

export const TagInput: React.FC<TagInputProps> = ({
  id,
  label,
  helper,
  tags,
  onChange,
  placeholder = 'python, sql, react...',
}) => {
  const [input, setInput] = useState('');

  const addTags = (raw: string) => {
    const newTags = raw
      .split(',')
      .map((s) => s.trim().toLowerCase())
      .filter((s) => s.length > 0 && !tags.includes(s));
    if (newTags.length > 0) onChange([...tags, ...newTags]);
    setInput('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); addTags(input); }
    else if (e.key === 'Backspace' && input === '' && tags.length > 0) onChange(tags.slice(0, -1));
  };

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
        <div
          className="min-h-[38px] w-full px-3 py-2 bg-[#0d0d0d] border border-[#1f1f1f] border-l-0 hover:border-[#2a2a2a] focus-within:border-[#2e2e2e]
            flex flex-wrap gap-1.5 items-center transition-colors duration-150 cursor-text"
          onClick={() => document.getElementById(id)?.focus()}
        >
          {tags.map((tag) => (
            <span key={tag} className="inline-flex items-center gap-1 px-2 py-0.5 bg-[#161616] border border-[#252525] font-mono text-[11px] text-[#a1a1aa]">
              {tag}
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); onChange(tags.filter((t) => t !== tag)); }}
                className="text-[#52525b] hover:text-[#a1a1aa] transition-colors ml-0.5 leading-none"
              >
                ×
              </button>
            </span>
          ))}
          <input
            id={id}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={() => input && addTags(input)}
            placeholder={tags.length === 0 ? placeholder : ''}
            className="flex-1 min-w-[100px] bg-transparent font-mono text-sm text-[#e4e4e7] placeholder-[#52525b] outline-none"
          />
        </div>
      </div>
      <p className="text-[11px] text-[#71717a] font-mono">Enter or , to add · Backspace to remove</p>
    </div>
  );
};
