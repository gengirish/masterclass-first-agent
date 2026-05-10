"use client";

import clsx from "clsx";

const SAMPLES = [
  {
    label: "Bootcamp duration & cost",
    question: "How long is the IntelliForge bootcamp and what does it cost?",
    tag: "RAG",
  },
  {
    label: "Placement assistance",
    question: "Do you offer placement assistance after the bootcamp?",
    tag: "RAG",
  },
  {
    label: "Quick math",
    question: "What is 17% of 4,829?",
    tag: "calculator",
  },
  {
    label: "Live web search",
    question: "What is OpenRouter and how does it differ from the OpenAI API?",
    tag: "tavily",
  },
] as const;

export function SampleQuestions({
  onPick,
  disabled,
}: {
  onPick: (q: string) => void;
  disabled: boolean;
}) {
  return (
    <div className="flex flex-col gap-3">
      <p className="font-display text-[10px] uppercase tracking-[0.18em] text-foreground-faint">
        Try
      </p>
      <div className="flex flex-wrap gap-2">
        {SAMPLES.map((s) => (
          <button
            key={s.question}
            type="button"
            disabled={disabled}
            onClick={() => onPick(s.question)}
            className={clsx(
              "group cursor-pointer flex items-center gap-2",
              "rounded-md border border-border bg-surface px-3 py-1.5",
              "text-left text-sm text-foreground-muted hover:text-foreground",
              "hover:bg-surface-2 hover:border-border-strong",
              "transition-all duration-150 active:scale-[0.97]",
              "disabled:opacity-40 disabled:cursor-not-allowed disabled:active:scale-100",
            )}
          >
            <span className="font-sans">{s.label}</span>
            <span className="font-display text-[10px] uppercase tracking-[0.14em] text-foreground-faint">
              {s.tag}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
