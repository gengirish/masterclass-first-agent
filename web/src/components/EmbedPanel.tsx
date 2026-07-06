"use client";

import { ChatInterface } from "@/components/ChatInterface";

function closeEmbed() {
  if (window.parent !== window) {
    window.parent.postMessage("intelliforge-chat-close", "*");
  }
}

export function EmbedPanel() {
  return (
    <div className="embed-shell flex h-full min-h-0 flex-col">
      <header className="embed-header flex flex-shrink-0 items-center justify-between gap-3 border-b border-border px-4 py-3">
        <div className="min-w-0">
          <p className="font-display text-[10px] uppercase tracking-[0.2em] text-foreground-faint">
            IntelliForge
          </p>
          <h1 className="truncate font-sans text-sm font-semibold text-foreground">
            Bootcamp Assistant
          </h1>
        </div>
        <button
          type="button"
          onClick={closeEmbed}
          className="embed-close flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-md border border-border text-foreground-muted transition-colors hover:bg-surface-2 hover:text-foreground"
          aria-label="Close chat"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden>
            <path
              d="M2 2l10 10M12 2L2 12"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </header>

      <div className="embed-body min-h-0 flex-1 overflow-y-auto px-4 py-4">
        <ChatInterface variant="embed" />
      </div>

      <footer className="embed-footer flex-shrink-0 border-t border-border px-4 py-2">
        <p className="text-center font-display text-[9px] uppercase tracking-[0.14em] text-foreground-faint">
          AI answers &middot;{" "}
          <a
            href="https://upskill.intelliforge.tech/"
            target="_blank"
            rel="noopener noreferrer"
            className="underline underline-offset-2 hover:text-foreground-muted"
          >
            upskill.intelliforge.tech
          </a>
        </p>
      </footer>
    </div>
  );
}
