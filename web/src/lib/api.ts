export const AGENT_BASE_URL =
  process.env.NEXT_PUBLIC_AGENT_BASE_URL ?? "https://masterclass-first-agent.fly.dev";

export type AskRequest = {
  question: string;
  max_iterations?: number;
};

export type AskResponse = {
  question: string;
  answer: string;
};

export class AgentRequestError extends Error {
  status?: number;
  constructor(message: string, status?: number) {
    super(message);
    this.name = "AgentRequestError";
    this.status = status;
  }
}

/**
 * Tied to the real ~30s cold-start the user actually experiences when Fly's
 * auto-stopped machine has to wake. Each frame is shown for ~3 seconds. After
 * the last frame we just sit on it until the response lands.
 */
export const COLD_START_FRAMES = [
  "Waking the machine in Mumbai\u2026",
  "Loading the Chroma index\u2026",
  "Embedding your question\u2026",
  "Calling the model\u2026",
  "Synthesizing the answer\u2026",
] as const;

export const COLD_START_FRAME_MS = 3000;

export async function ask(req: AskRequest, signal?: AbortSignal): Promise<AskResponse> {
  let response: Response;
  try {
    response = await fetch(`${AGENT_BASE_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: req.question,
        max_iterations: req.max_iterations ?? 4,
      }),
      signal,
    });
  } catch (err) {
    if ((err as Error).name === "AbortError") throw err;
    throw new AgentRequestError(
      "Network request failed. Check your connection and try again.",
    );
  }

  if (!response.ok) {
    let body = "";
    try {
      body = (await response.text()).slice(0, 200);
    } catch {
      /* ignore */
    }
    throw new AgentRequestError(
      `Agent returned HTTP ${response.status}. ${body}`,
      response.status,
    );
  }

  return (await response.json()) as AskResponse;
}
