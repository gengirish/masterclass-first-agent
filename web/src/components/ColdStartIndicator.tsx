"use client";

import { useEffect, useState } from "react";
import { COLD_START_FRAMES, COLD_START_FRAME_MS } from "@/lib/api";

/**
 * Rotates progress copy while a request is pending. The copy is theatrical
 * (we don't actually know which stage the backend is in), but it's tied to
 * the realistic ~30s wake-up cadence so it lands at the right moments.
 */
export function ColdStartIndicator({
  active,
  startedAt,
  compact = false,
}: {
  active: boolean;
  startedAt: number;
  compact?: boolean;
}) {
  const [frame, setFrame] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!active) {
      setFrame(0);
      setElapsed(0);
      return;
    }
    const tick = () => {
      const ms = Date.now() - startedAt;
      setElapsed(ms);
      const idx = Math.min(
        Math.floor(ms / COLD_START_FRAME_MS),
        COLD_START_FRAMES.length - 1,
      );
      setFrame(idx);
    };
    tick();
    const id = setInterval(tick, 200);
    return () => clearInterval(id);
  }, [active, startedAt]);

  if (!active) return null;

  const message = COLD_START_FRAMES[frame];
  const seconds = Math.floor(elapsed / 1000);

  if (compact) {
    return (
      <p className="flex items-center gap-2 text-sm text-foreground-muted" aria-live="polite">
        <span
          className="inline-block h-3 w-3 rounded-full border border-foreground-faint border-t-foreground spin-slow"
          aria-hidden
        />
        {message}
      </p>
    );
  }

  return (
    <div className="reveal flex items-center gap-3 rounded-md border border-border bg-surface px-4 py-3 font-mono text-sm">
      <span
        className="inline-block h-3 w-3 rounded-full border border-foreground-faint border-t-foreground spin-slow"
        aria-hidden
      />
      <span className="flex-1 text-foreground" aria-live="polite">
        {message}
      </span>
      <span className="tabular-nums text-foreground-faint text-xs">{seconds}s</span>
    </div>
  );
}
