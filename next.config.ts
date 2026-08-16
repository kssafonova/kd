import type { NextConfig } from "next";

const isGitHubPages = process.env.GITHUB_ACTIONS === "true";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  basePath: isGitHubPages ? "/kd" : "",
  assetPrefix: isGitHubPages ? "/kd/" : undefined,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
