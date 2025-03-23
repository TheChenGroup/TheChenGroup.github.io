// @ts-check
import { defineConfig } from "astro/config";

import rehypeExternalLinks from "rehype-external-links";
import Icons from "unplugin-icons/vite";
import mdx from "@astrojs/mdx";
import remarkSmartypants from "remark-smartypants";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

// https://astro.build/config
export default defineConfig({
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [
      // dashes limilar to LaTeX
      // @ts-ignore
      [remarkSmartypants, { dashes: "oldschool" }],
      remarkMath,
    ],
    rehypePlugins: [[rehypeExternalLinks, { target: "_blank" }], rehypeKatex],
  },
  vite: {
    plugins: [
      Icons({
        compiler: "astro",
      }),
    ],
  },
});
