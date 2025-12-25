# /// script
# dependencies = [
#   "requests",
#   "PyYAML",
# ]
# ///
from typing import Any
from pathlib import Path

import requests
import yaml


PUBLICATIONS_MD = Path(__file__).parent.parent / "src" / "pages" / "publications.mdx"
ZOTERO_API_URL = "https://api.zotero.org/groups/6251966/items"


def format_zotero_item(item):
    paper = item["data"]
    meta = item["meta"]
    try:
        return {
            "title": paper["title"],
            "doi": paper["DOI"],
            "authors": [
                f"{author['firstName']} {author['lastName']}"
                for author in paper.get("creators", [])
                if author["creatorType"] == "author"
            ],
            "journal": paper.get("journalAbbreviation")
            or paper.get("publicationTitle"),
            "volume": paper.get("volume") or "",
            "page": paper.get("pages") or paper.get("archiveID") or "",
            "year": int(meta["parsedDate"][:4]),
        }
    except KeyError as e:
        print(item)
        raise e from None


def all_items_from_zotero():
    all_items = []
    while items := requests.get(
        ZOTERO_API_URL,
        params={
            "sort": "dateModified",
            "itemType": "journalArticle || preprint",
            "start": len(all_items),
        },
    ).json():
        all_items.extend(items)
    return all_items


def sort_items(items: list[dict[str, Any]], dois: list[str]):
    dois = [doi.lower() for doi in dois]  # We need to do case insensitive match
    new_items = [item for item in items if item["data"]["DOI"].lower() not in dois]
    doi_to_item = {item["data"]["DOI"].lower(): item for item in items}
    return new_items + [doi_to_item[doi] for doi in dois if doi in doi_to_item]


def sync_with_zotero():
    lines = PUBLICATIONS_MD.read_text().split("\n")
    segment_line_no = lines.index("---", 1)
    frontmatter = yaml.safe_load("\n".join(lines[1:segment_line_no]))
    frontmatter["publications"] = [
        format_zotero_item(item)
        for item in sort_items(
            all_items_from_zotero(),
            [item["doi"] for item in frontmatter["publications"]],
        )
    ]
    yaml_string = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
    yaml_string = yaml_string.replace("\u2010", "-")
    lines[1:segment_line_no] = [yaml_string]
    PUBLICATIONS_MD.write_text("\n".join(lines))


if __name__ == "__main__":
    sync_with_zotero()
