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
    label: "When does it start?",
    question: "When does Cohort 1 start?",
    tag: "FAQ",
  },
  {
    label: "2-Week Sprint",
    question: "What is the 2-Week AI Sprint and why is it the recommended starting point?",
    tag: "FAQ",
  },
  {
    label: "Class timings",
    question: "What are the live class timings on weekends?",
    tag: "FAQ",
  },
  {
    label: "Duration",
    question: "How long is the 2-Week Sprint compared to the 12-week bootcamp?",
    tag: "FAQ",
  },
];
