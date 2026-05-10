"use client";

import { useRef, useState } from "react";
import { ask, AgentRequestError, AskResponse } from "@/lib/api";
import { QuestionInput } from "./QuestionInput";
import { AnswerCard } from "./AnswerCard";
import { ColdStartIndicator } from "./ColdStartIndicator";
import { SampleQuestions } from "./SampleQuestions";
import { StatusDot } from "./StatusDot";

type Status = "idle" | "asking" | "ready" | "error";

type Result = {
  question: string;
  answer: string;
  durationMs: number;
};

export function ChatInterface() {
  const [draft, setDraft] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [requestStartedAt, setRequestStartedAt] = useState(0);
  const abortRef = useRef<AbortController | null>(null);

  const submit = async (questionOverride?: string) => {
    const question = (questionOverride ?? draft).trim();
    if (!question || status === "asking") return;

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setStatus("asking");
    setError(null);
    setResult(null);
    const startedAt = Date.now();
    setRequestStartedAt(startedAt);

    let response: AskResponse;
    try {
      response = await ask({ question }, controller.signal);
    } catch (err) {
      if ((err as Error).name === "AbortError") {
        setStatus("idle");
        return;
      }
      const msg =
        err instanceof AgentRequestError
          ? err.message
          : "Something went wrong. Try again.";
      setError(msg);
      setStatus("error");
      return;
    }

    setResult({
      question: response.question,
      answer: response.answer,
      durationMs: Date.now() - startedAt,
    });
    setStatus("ready");
  };

  const handleSamplePick = (q: string) => {
    setDraft(q);
    void submit(q);
  };

  return (
    <div className="flex w-full flex-col gap-8">
      <div className="flex items-center justify-between gap-3">
        <p className="font-display text-[11px] uppercase tracking-[0.18em] text-foreground-faint">
          /ask &mdash; live agent
        </p>
        <StatusDot status={status} />
      </div>

      <QuestionInput
        value={draft}
        onChange={setDraft}
        onSubmit={() => void submit()}
        onCancel={() => abortRef.current?.abort()}
        busy={status === "asking"}
      />

      <SampleQuestions onPick={handleSamplePick} disabled={status === "asking"} />

      {status === "asking" && (
        <ColdStartIndicator active startedAt={requestStartedAt} />
      )}

      {status === "error" && error && (
        <div
          role="alert"
          className="reveal flex items-start gap-3 rounded-md border border-accent-error/40 bg-accent-error/5 px-4 py-3"
        >
          <span
            className="mt-1.5 inline-block h-1.5 w-1.5 flex-shrink-0 rounded-full bg-accent-error"
            aria-hidden
          />
          <div className="flex-1 font-mono text-sm text-foreground">
            {error}
          </div>
        </div>
      )}

      {result && (
        <AnswerCard
          question={result.question}
          answer={result.answer}
          durationMs={result.durationMs}
        />
      )}
    </div>
  );
}
