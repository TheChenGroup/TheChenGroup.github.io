import { Cite } from "@citation-js/core";
import "@citation-js/plugin-doi";
import yaml from "js-yaml";

import { argv } from "node:process";

function convert(paper) {
  const authors = paper.author
    .filter(({ family }) => !!family)
    .map(({ given, family }) => `${given} ${family}`);
  const year = paper.issued["date-parts"][0][0];
  if (paper?.publisher === "arXiv") {
    return {
      title: paper.title,
      doi: paper.DOI,
      authors,
      journal: "arXiv",
      volume: undefined,
      page: paper.number,
      year,
    };
  } else {
    return {
      title: paper.title,
      doi: paper.DOI,
      authors,
      journal: paper["container-title-short"] ?? paper["container-title"],
      volume: paper.volume,
      page: paper.page,
      year,
    };
  }
}
const doi = argv[2];
if (!doi) {
  console.error("Please provide a DOI as an argument.");
  process.exit(1);
}

const jsonObj = new Cite(doi).get().map(convert);

console.log(yaml.dump(jsonObj));
