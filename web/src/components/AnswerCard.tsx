import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = {
  question: string;
  answer: string;
  durationMs: number;
  compact?: boolean;
};

export function AnswerCard({ question, answer, durationMs, compact = false }: Props) {
  const seconds = (durationMs / 1000).toFixed(1);

  return (
    <article className={compact ? "reveal flex flex-col gap-3" : "reveal flex flex-col gap-4"}>
      <div className="flex items-baseline justify-between gap-4 border-b border-border pb-2">
        <h2 className="font-display text-[10px] uppercase tracking-[0.18em] text-foreground-faint">
          Question
        </h2>
        <span className="font-display text-[10px] uppercase tracking-[0.14em] text-foreground-faint tabular-nums">
          {seconds}s
        </span>
      </div>
      <p
        className={
          compact
            ? "font-sans text-sm leading-relaxed text-foreground"
            : "font-sans text-lg leading-relaxed text-foreground"
        }
      >
        {question}
      </p>

      <div className="mt-2 flex items-baseline gap-3 border-b border-border pb-2">
        <h2 className="font-display text-[10px] uppercase tracking-[0.18em] text-foreground-faint">
          Answer
        </h2>
      </div>
      <div className={compact ? "markdown markdown-compact" : "markdown"}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{answer}</ReactMarkdown>
      </div>
    </article>
  );
}
