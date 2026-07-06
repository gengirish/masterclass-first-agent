import type { NextConfig } from "next";

const embedFrameAncestors =
  "frame-ancestors 'self' https://upskill.intelliforge.tech https://*.intelliforge.tech http://localhost:* http://127.0.0.1:*";

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: "/embed",
        headers: [
          {
            key: "Content-Security-Policy",
            value: embedFrameAncestors,
          },
        ],
      },
      {
        source: "/embed/:path*",
        headers: [
          {
            key: "Content-Security-Policy",
            value: embedFrameAncestors,
          },
        ],
      },
    ];
  },
};

export default nextConfig;
