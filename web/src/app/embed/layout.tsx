import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "IntelliForge Bootcamp Assistant",
  description: "Ask questions about the IntelliForge AI Bootcamp.",
  robots: { index: false, follow: false },
};

export default function EmbedLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="embed-page fixed inset-0 overflow-hidden bg-background">
      {children}
    </div>
  );
}
