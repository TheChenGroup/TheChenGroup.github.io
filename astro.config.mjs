// @ts-check
import { defineConfig } from "astro/config";

import rehypeExternalLinks from "rehype-external-links";
import Icons from "unplugin-icons/vite";
import mdx from "@astrojs/mdx";
import remarkSmartypants from "remark-smartypants";

// https://astro.build/config
export default defineConfig({
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [
      // dashes limilar to LaTeX
      // @ts-ignore
      [remarkSmartypants, { dashes: "oldschool" }],
    ],
    rehypePlugins: [[rehypeExternalLinks, { target: "_blank" }]],
  },
  vite: {
    plugins: [
      Icons({
        compiler: "astro",
      }),
    ],
  },
});
