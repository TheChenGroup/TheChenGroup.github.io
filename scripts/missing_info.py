# /// script
# dependencies = [
#   "PyYAML",
# ]
# ///
from typing import Any
from pathlib import Path

import yaml


PUBLICATIONS_MD = Path(__file__).parent.parent / "src" / "pages" / "publications.mdx"


def paper_is_missing_info(paper):
    fields_to_check = ["title", "doi", "authors", "page", "year"]
    if "arxiv" not in paper.get("doi", "").lower():
        fields_to_check.extend(["journal", "volume"])
    return not all(paper.get(field) for field in fields_to_check)


def papers_missing_info():
    lines = PUBLICATIONS_MD.read_text().split("\n")
    segment_line_no = lines.index("---", 1)
    frontmatter = yaml.safe_load("\n".join(lines[1:segment_line_no]))
    papers = [
        item
        for item in frontmatter["publications"]
        if paper_is_missing_info(item)
    ]
    if not papers:
        print("All papers have complete information!")
    else:
        print("The following papers have missing information:\n")
        for paper in papers:
            print(f"- [ ] [{paper.get('title')}](https://doi.org/{paper.get('doi')})")


if __name__ == "__main__":
    papers_missing_info()
