export type SampleQuestion = {
  label: string;
  question: string;
  tag: string;
};

export const DEMO_SAMPLES: SampleQuestion[] = [
  {
    label: "Bootcamp duration & cost",
    question: "How long is the IntelliForge bootcamp and what does it cost?",
    tag: "RAG",
  },
  {
    label: "Placement assistance",
    question: "Do you offer placement assistance after the bootcamp?",
    tag: "RAG",
  },
  {
    label: "Quick math",
    question: "What is 17% of 4,829?",
    tag: "calculator",
  },
  {
    label: "Live web search",
    question: "What is OpenRouter and how does it differ from the OpenAI API?",
    tag: "tavily",
  },
];

export const UPSKILL_SAMPLES: SampleQuestion[] = [
  {
    label: "Pricing",
    question: "What does the 12-week IntelliForge bootcamp cost?",
    tag: "FAQ",
  },
  {
    label: "Build-alongside",
    question: "What is build-alongside and who qualifies?",
    tag: "FAQ",
  },
  {
    label: "Credential",
    question: "What is the verifiable credential and how do recruiters check it?",
    tag: "FAQ",
  },
  {
    label: "Time commitment",
    question: "How many hours per week does the bootcamp require?",
    tag: "FAQ",
  },
];
