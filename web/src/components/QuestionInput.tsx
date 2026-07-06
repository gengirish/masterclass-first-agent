"use client";

import { FormEvent, KeyboardEvent, useRef } from "react";
import clsx from "clsx";

type Props = {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  busy: boolean;
  onCancel?: () => void;
  compact?: boolean;
  placeholder?: string;
  autoFocus?: boolean;
};

export function QuestionInput({
  value,
  onChange,
  onSubmit,
  busy,
  onCancel,
  compact = false,
  placeholder = "Ask anything about the IntelliForge bootcamp\u2014or any quick fact.",
  autoFocus = true,
}: Props) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!busy && value.trim()) onSubmit();
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      handleSubmit(e);
    }
    if (e.key === "Enter" && !e.shiftKey && !e.metaKey && !e.ctrlKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (compact) {
    return (
      <form onSubmit={handleSubmit} className="flex items-end gap-2">
        <label htmlFor="question" className="sr-only">
          Ask the agent a question
        </label>
        <textarea
          ref={textareaRef}
          id="question"
          name="question"
          rows={1}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={busy}
          placeholder={placeholder}
          className={clsx(
            "min-h-[36px] flex-1 resize-none rounded-md border border-border bg-surface px-3 py-2",
            "text-sm text-foreground placeholder:text-foreground-faint",
            "focus:border-border-strong focus:outline-none disabled:opacity-50",
          )}
          autoFocus={autoFocus}
        />
        {busy && onCancel ? (
          <button
            type="button"
            onClick={onCancel}
            className="flex-shrink-0 rounded-md px-2 py-2 text-xs text-foreground-muted hover:text-foreground"
          >
            Stop
          </button>
        ) : (
          <button
            type="submit"
            disabled={busy || !value.trim()}
            className={clsx(
              "flex-shrink-0 rounded-md bg-accent-ready px-3 py-2 text-sm font-medium text-background",
              "disabled:cursor-not-allowed disabled:opacity-30",
              "hover:bg-accent-ready/90",
            )}
          >
            Send
          </button>
        )}
      </form>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div
        className={clsx(
          "group relative flex flex-col rounded-md border bg-surface transition-colors",
          "border-border focus-within:border-border-strong",
        )}
      >
        <label htmlFor="question" className="sr-only">
          Ask the agent a question
        </label>
        <textarea
          ref={textareaRef}
          id="question"
          name="question"
          rows={3}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={busy}
          placeholder={placeholder}
          className={clsx(
            "w-full resize-none bg-transparent text-foreground",
            "placeholder:text-foreground-faint",
            "focus:outline-none disabled:opacity-50",
            "px-4 py-4 text-base font-sans leading-relaxed",
          )}
          autoFocus={autoFocus}
        />
        <div className="flex items-center justify-between gap-3 border-t border-border px-3 py-2">
          <kbd className="hidden sm:inline-flex font-display text-[10px] uppercase tracking-[0.16em] text-foreground-faint">
            <span>Enter</span>
            <span className="mx-1.5 text-foreground-faint/50">to send</span>
            <span>Shift+Enter</span>
            <span className="mx-1.5 text-foreground-faint/50">for newline</span>
          </kbd>
          <span className="sm:hidden font-display text-[10px] uppercase tracking-[0.16em] text-foreground-faint">
            Enter to send
          </span>
          <div className="flex items-center gap-2">
            {busy && onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className={clsx(
                  "cursor-pointer font-display text-xs uppercase tracking-[0.14em]",
                  "rounded-md border border-border px-3 py-1.5",
                  "text-foreground-muted hover:text-foreground hover:bg-white/5",
                  "transition-all duration-150 active:scale-[0.97]",
                )}
              >
                Cancel
              </button>
            )}
            <button
              type="submit"
              disabled={busy || !value.trim()}
              className={clsx(
                "cursor-pointer font-display text-xs uppercase tracking-[0.14em]",
                "rounded-md bg-accent-ready px-4 py-1.5 text-background",
                "transition-all duration-150 active:scale-[0.97]",
                "disabled:opacity-30 disabled:cursor-not-allowed disabled:bg-foreground/30",
                "hover:bg-accent-ready/90",
              )}
            >
              {busy ? "Asking\u2026" : "Ask"}
            </button>
          </div>
        </div>
      </div>
    </form>
  );
}
