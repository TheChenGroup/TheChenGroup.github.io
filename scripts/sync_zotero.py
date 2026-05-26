# /// script
# dependencies = [
#   "requests",
#   "PyYAML",
# ]
# ///
import os
from pathlib import Path
from typing import Any

import requests
import yaml


PUBLICATIONS_MD = Path(__file__).parent.parent / "src" / "pages" / "publications.mdx"
ZOTERO_API_URL = "https://api.zotero.org/groups/6251966/items"


def format_zotero_item(item):
    paper = item["data"]
    meta = item["meta"]
    try:
        result = {
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

    return {
        k: v.replace("\u2010", "-").replace("\u2011", "-") if isinstance(v, str) else v
        for k, v in result.items()
    }


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


def normalize_title(title: str) -> str:
    return " ".join(title.split()).casefold()


def summarize_changes(
    old_publications: list[dict[str, Any]], new_publications: list[dict[str, Any]]
):
    old_by_doi = {item["doi"].lower(): item for item in old_publications}
    new_by_doi = {item["doi"].lower(): item for item in new_publications}

    added_by_doi = [
        item for item in new_publications if item["doi"].lower() not in old_by_doi
    ]
    removed_by_doi = [
        item for item in old_publications if item["doi"].lower() not in new_by_doi
    ]
    removed_by_title = {}
    for item in removed_by_doi:
        removed_by_title.setdefault(normalize_title(item["title"]), []).append(item)

    added: list[dict[str, Any]] = []
    updated: list[dict[str, Any]] = []
    matched_removed_dois = set()

    for item in added_by_doi:
        matching_removed = removed_by_title.get(normalize_title(item["title"]), [])
        if matching_removed:
            old_item = matching_removed.pop(0)
            matched_removed_dois.add(old_item["doi"].lower())
            updated.append({"old": old_item, "new": item})
        else:
            added.append(item)

    removed = [
        item
        for item in removed_by_doi
        if item["doi"].lower() not in matched_removed_dois
    ]

    for item in new_publications:
        doi = item["doi"].lower()
        if doi in old_by_doi and item != old_by_doi[doi]:
            updated.append({"old": old_by_doi[doi], "new": item})

    return added, updated, removed


def format_subject(added: list[dict[str, Any]], updated: list[dict[str, Any]]) -> str:
    if len(added) == 1 and not updated:
        author = added[0]["authors"][0] if added[0]["authors"] else "unknown author"
        return f"add paper by {author} et al."
    if len(updated) == 1 and not added:
        author = (
            updated[0]["new"]["authors"][0]
            if updated[0]["new"]["authors"]
            else "unknown author"
        )
        return f"update paper by {author} et al."
    return "sync Zotero publications"


def format_publication(item: dict[str, Any]) -> str:
    return f"{item['title']} ({item['doi']})"


def format_change_body(
    added: list[dict[str, Any]],
    updated: list[dict[str, Any]],
    removed: list[dict[str, Any]],
) -> str:
    lines = ["Sync Zotero publications", ""]

    if added:
        lines.append("Added:")
        lines.extend(f"- {format_publication(item)}" for item in added)
        lines.append("")

    if updated:
        lines.append("Updated:")
        lines.extend(
            (
                f"- {change['old']['title']} ({change['old']['doi']})"
                f" -> {change['new']['title']} ({change['new']['doi']})"
            )
            for change in updated
        )
        lines.append("")

    if removed:
        lines.append("Removed:")
        lines.extend(f"- {format_publication(item)}" for item in removed)
        lines.append("")

    return "\n".join(lines).strip()


def write_github_output(name: str, value: str):
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return

    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"{name}<<EOF\n{value}\nEOF\n")


def sync_with_zotero():
    lines = PUBLICATIONS_MD.read_text().split("\n")
    segment_line_no = lines.index("---", 1)
    frontmatter = yaml.safe_load("\n".join(lines[1:segment_line_no]))
    old_publications = frontmatter["publications"]
    new_publications = [
        format_zotero_item(item)
        for item in sort_items(
            all_items_from_zotero(),
            [item["doi"] for item in old_publications],
        )
    ]
    frontmatter["publications"] = new_publications
    yaml_string = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
    lines[1:segment_line_no] = [yaml_string]
    PUBLICATIONS_MD.write_text("\n".join(lines))

    added, updated, removed = summarize_changes(old_publications, new_publications)
    subject = format_subject(added, updated)
    body = format_change_body(added, updated, removed)
    write_github_output("commit_message", subject)
    write_github_output("pr_title", subject)
    write_github_output("pr_body", body)


if __name__ == "__main__":
    sync_with_zotero()
