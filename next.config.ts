import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'export',
  // disable image optimization for export
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
