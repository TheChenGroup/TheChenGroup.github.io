export default {
  "*.{md,mdx}": (stagedFiles) => [`remark ${stagedFiles.join(" ")} -o`],
  "*.{mjs,ts,json,astro}": "prettier -w",
  "*.{css,astro}": "stylelint",
};
