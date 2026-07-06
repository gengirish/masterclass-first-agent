import { ChatInterface } from "@/components/ChatInterface";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-border">
        <div className="mx-auto flex w-full max-w-2xl items-center justify-between px-6 py-4">
          <span className="text-sm font-medium text-foreground">First Agent</span>
          <a
            href="https://github.com/gengirish/masterclass-first-agent"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-foreground-muted hover:text-foreground transition-colors"
          >
            Source
          </a>
        </div>
      </header>

      <main className="flex-1">
        <div className="mx-auto w-full max-w-2xl px-6 py-12">
          <ChatInterface />
        </div>
      </main>
    </div>
  );
}
