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
      <header className="embed-header flex flex-shrink-0 items-center justify-between gap-3 border-b border-border px-3 py-2.5">
        <h1 className="truncate text-sm font-medium text-foreground">
          Bootcamp Assistant
        </h1>
        <button
          type="button"
          onClick={closeEmbed}
          className="embed-close flex h-7 w-7 flex-shrink-0 items-center justify-center rounded text-foreground-muted transition-colors hover:bg-surface-2 hover:text-foreground"
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

      <ChatInterface variant="embed" />
    </div>
  );
}
