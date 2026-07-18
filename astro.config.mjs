// @ts-check
import { defineConfig, fontProviders } from "astro/config";
import { unified } from "@astrojs/markdown-remark";

import rehypeExternalLinks from "rehype-external-links";
import Icons from "unplugin-icons/vite";
import mdx from "@astrojs/mdx";
import remarkSmartypants from "remark-smartypants";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

// https://astro.build/config
export default defineConfig({
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: "Inter",
      cssVariable: "--font-inter",
      weights: [400, 600, 700],
      styles: ["normal"],
      subsets: ["latin"],
    },
    {
      provider: fontProviders.fontsource(),
      name: "Inter",
      cssVariable: "--font-inter",
      weights: [400],
      styles: ["italic"],
      subsets: ["latin"],
    },
  ],
  integrations: [mdx()],
  security: {
    csp: true,
  },
  markdown: {
    processor: unified({
      syntaxHighlight: false,
      remarkPlugins: [
        // dashes limilar to LaTeX
        // @ts-ignore
        [remarkSmartypants, { dashes: "oldschool" }],
        remarkMath,
      ],
      rehypePlugins: [[rehypeExternalLinks, { target: "_blank" }], rehypeKatex],
    }),
  },
  vite: {
    plugins: [
      Icons({
        compiler: "astro",
      }),
    ],
  },
});
