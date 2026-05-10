import clsx from "clsx";

type Status = "idle" | "asking" | "ready" | "error";

const TONE: Record<Status, { color: string; pulse: boolean; label: string }> = {
  idle:    { color: "bg-foreground-muted",  pulse: false, label: "ready" },
  asking:  { color: "bg-accent-warming",    pulse: true,  label: "thinking" },
  ready:   { color: "bg-accent-ready",      pulse: false, label: "answered" },
  error:   { color: "bg-accent-error",      pulse: false, label: "error" },
};

export function StatusDot({ status }: { status: Status }) {
  const tone = TONE[status];
  return (
    <div className="flex items-center gap-2 font-display text-[11px] uppercase tracking-[0.14em] text-foreground-faint">
      <span
        className={clsx(
          "h-1.5 w-1.5 rounded-full",
          tone.color,
          tone.pulse && "pulse-soft",
        )}
        aria-hidden
      />
      <span>{tone.label}</span>
    </div>
  );
}
