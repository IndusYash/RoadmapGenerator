import React from 'react';

interface ButtonProps {
  id?: string;
  children: React.ReactNode;
  onClick: () => void;
  loading?: boolean;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'ghost';
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  id,
  children,
  onClick,
  loading = false,
  disabled = false,
  variant = 'primary',
  className = '',
}) => {
  const isDisabled = disabled || loading;

  const base = 'inline-flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-medium font-mono transition-colors duration-150 select-none disabled:cursor-not-allowed';

  const variants = {
    primary:   'bg-[#e4e4e7] text-[#09090b] hover:bg-white disabled:bg-[#3f3f46] disabled:text-[#71717a]',
    secondary: 'bg-transparent border border-[#2e2e2e] text-[#a1a1aa] hover:border-[#3f3f46] hover:text-[#e4e4e7] disabled:opacity-40',
    ghost:     'bg-transparent text-[#71717a] hover:text-[#a1a1aa] disabled:opacity-40',
  };

  return (
    <button
      id={id}
      type="button"
      onClick={onClick}
      disabled={isDisabled}
      className={`${base} ${variants[variant]} ${className}`}
    >
      {loading && (
        <svg className="animate-spin h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      )}
      {children}
    </button>
  );
};
