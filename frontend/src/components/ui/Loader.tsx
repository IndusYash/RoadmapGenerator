import React from 'react';

export const Loader: React.FC = () => {
  const steps = [
    'Analyzing career profile...',
    'Mapping skill requirements...',
    'Computing phase distribution...',
    'Generating milestone titles...',
    'Estimating salary tiers...',
    'Building unlock statements...',
    'Validating roadmap schema...',
  ];

  const [step, setStep] = React.useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setStep((s) => (s < steps.length - 1 ? s + 1 : s));
    }, 320);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="py-12 px-6 font-mono animate-fadeIn">
      {/* Top bar */}
      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-[#1a1a1a]">
        <div className="flex gap-1.5">
          <div className="w-2 h-2 rounded-full bg-[#232323]" />
          <div className="w-2 h-2 rounded-full bg-[#232323]" />
          <div className="w-2 h-2 rounded-full bg-[#232323]" />
        </div>
        <span className="text-[11px] text-[#71717a] tracking-widest uppercase">AI Pipeline — Running</span>
        <div className="ml-auto flex gap-0.5">
          {[0,1,2].map((i) => (
            <div
              key={i}
              className="w-1 h-3.5 bg-[#e4e4e7]"
              style={{ animation: `dotBounce 1.2s ease-in-out ${i * 0.2}s infinite` }}
            />
          ))}
        </div>
      </div>

      {/* Pipeline steps */}
      <div className="space-y-2">
        {steps.map((s, i) => (
          <div key={i} className="flex items-center gap-3">
            <span className="text-[#52525b] text-[11px] w-5 text-right flex-shrink-0">{String(i + 1).padStart(2,'0')}</span>
            <div className={`flex-1 text-[13px] transition-all duration-200 ${
              i < step ? 'text-[#52525b]' : i === step ? 'text-[#e4e4e7]' : 'text-[#232323]'
            }`}>
              {i <= step ? (
                <>
                  <span className={`mr-2 ${i < step ? 'text-green-500' : 'text-[#e4e4e7]'}`}>
                    {i < step ? '✓' : '›'}
                  </span>
                  {s}
                  {i === step && <span className="ml-1 animate-blink text-[#e4e4e7]">_</span>}
                </>
              ) : (
                <span className="text-[#1f1f1f]">{'·'.repeat(s.length + 2)}</span>
              )}
            </div>
          </div>
        ))}
      </div>

      <p className="mt-6 pt-4 border-t border-[#1a1a1a] text-[11px] text-[#71717a] tracking-wide">
        AI is building your personalized roadmap — this may take a few seconds
      </p>
    </div>
  );
};
