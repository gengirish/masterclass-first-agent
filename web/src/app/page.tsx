import Link from "next/link";
import { ChatInterface } from "@/components/ChatInterface";

const STACK = [
  { label: "FastAPI", href: "https://fastapi.tiangolo.com/" },
  { label: "OpenRouter", href: "https://openrouter.ai/" },
  { label: "ChromaDB", href: "https://www.trychroma.com/" },
  { label: "Tavily", href: "https://tavily.com/" },
  { label: "Fly.io", href: "https://fly.io/" },
  { label: "Next.js", href: "https://nextjs.org/" },
];

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Masthead */}
      <header className="border-b border-border">
        <div className="mx-auto flex w-full max-w-3xl items-center justify-between px-6 py-5">
          <div className="flex items-baseline gap-3">
            <span className="font-display text-xs uppercase tracking-[0.2em] text-foreground-faint">
              IntelliForge
            </span>
            <span className="text-foreground-faint/40">/</span>
            <span className="font-display text-xs uppercase tracking-[0.2em] text-foreground">
              First Agent
            </span>
          </div>
          <a
            href="https://github.com/gengirish/masterclass-first-agent"
            target="_blank"
            rel="noopener noreferrer"
            className="font-display text-xs uppercase tracking-[0.16em] text-foreground-muted hover:text-foreground transition-colors"
          >
            Source &rarr;
          </a>
        </div>
      </header>

      {/* Main */}
      <main className="flex-1">
        <div className="mx-auto w-full max-w-3xl px-6 py-16 sm:py-24">
          {/* Hero: type as anchor — JetBrains Mono display, generous gaps */}
          <section className="mb-20 flex flex-col gap-8">
            <h1 className="font-display text-4xl sm:text-6xl font-semibold leading-[1.02] tracking-tight text-foreground">
              A small agent
              <br />
              <span className="text-foreground-muted">that does its homework.</span>
            </h1>
            <p className="max-w-xl font-sans text-base sm:text-lg leading-relaxed text-foreground-muted">
              It decides whether to call a calculator, search the IntelliForge FAQ,
              or hit a live web search before it answers. Built in three hours.
            </p>
          </section>

          {/* Live agent surface */}
          <ChatInterface />

          {/* How it works */}
          <section className="mt-24 border-t border-border pt-16 flex flex-col gap-8">
            <h2 className="font-display text-[11px] uppercase tracking-[0.18em] text-foreground-faint">
              How it works
            </h2>
            <div className="grid gap-8 sm:grid-cols-3">
              <Step
                index="01"
                title="Tool-calling loop"
                body="Asks the LLM what to do next, runs the tool, appends the result, repeats."
              />
              <Step
                index="02"
                title="RAG over docs"
                body="The IntelliForge FAQ was chunked and embedded into ChromaDB at build time."
              />
              <Step
                index="03"
                title="Multi-provider"
                body="Chat and embeddings route through OpenRouter; one env-var swaps in Groq or NIM."
              />
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-4 px-6 py-8 sm:flex-row sm:items-center sm:justify-between">
          <p className="font-display text-[11px] uppercase tracking-[0.18em] text-foreground-faint">
            Built in 3 hours &middot; IntelliForge masterclass
          </p>
          <ul className="flex flex-wrap gap-x-3 gap-y-2 font-display text-[11px] uppercase tracking-[0.14em]">
            {STACK.map((s) => (
              <li key={s.label}>
                <Link
                  href={s.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-foreground-muted hover:text-foreground transition-colors"
                >
                  {s.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </footer>
    </div>
  );
}

function Step({
  index,
  title,
  body,
}: {
  index: string;
  title: string;
  body: string;
}) {
  return (
    <div className="flex flex-col gap-3">
      <span className="font-display text-[11px] uppercase tracking-[0.18em] text-foreground-faint">
        {index}
      </span>
      <h3 className="font-display text-base font-medium text-foreground">{title}</h3>
      <p className="font-sans text-sm leading-relaxed text-foreground-muted">
        {body}
      </p>
    </div>
  );
}
