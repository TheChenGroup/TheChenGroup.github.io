# /// script
# dependencies = [
#   "arxiv",
#   "requests",
#   "PyYAML",
# ]
# ///
import argparse
import sys
from pathlib import Path
from urllib3.util import Retry

import arxiv
import requests
import yaml
from requests.adapters import HTTPAdapter


def fetch_arxiv(doi: str) -> dict:
    arxiv_id = doi.lower().split("arxiv.")[-1]
    client = arxiv.Client()
    paper = next(client.results(arxiv.Search(id_list=[arxiv_id])))
    return {
        "title": paper.title,
        "doi": doi,
        "authors": [author.name for author in paper.authors],
        "journal": "arXiv",
        "volume": None,
        "page": arxiv_id,
        "year": paper.published.year,
    }


def fetch_crossref(doi: str) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)

    response = session.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    if data.get("status") != "ok":
        print(data.get("message"), file=sys.stderr)
        sys.exit(1)

    paper = data["message"]

    return {
        "title": paper["title"][0],
        "doi": paper.get("DOI"),
        "authors": [
            f"{author['given']} {author['family']}"
            for author in paper.get("author", [])
            if author.get("family")
        ],
        "journal": paper.get("short-container-title", paper.get("container-title"))[0],
        "volume": paper.get("volume"),
        "page": paper.get("page", paper.get("article-number")),
        "year": paper["issued"]["date-parts"][0][0],
    }


def fetch_doi(doi: str) -> dict:
    if "arxiv" in doi.lower():
        return fetch_arxiv(doi)
    else:
        return fetch_crossref(doi)


def doi2yaml(dois: list[str]) -> list[str]:
    result = []
    for doi in dois:
        yaml_string = yaml.dump(
            [fetch_doi(doi)], sort_keys=False, allow_unicode=True
        ).strip()
        print(yaml_string)
        result.append(yaml_string)
    return result


def insert_yaml(yaml_strings: list[str]) -> None:
    publications_md = (
        Path(__file__).parent.parent / "src" / "pages" / "publications.mdx"
    )
    lines = publications_md.read_text().split("\n")
    idx = lines.index("publications:")
    publications_md.write_text(
        "\n".join(lines[: idx + 1] + yaml_strings + lines[idx + 1 :])
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch and convert Crossref metadata to YAML."
    )
    parser.add_argument(
        "doi", help="The DOI of the paper to fetch metadata for.", nargs="+"
    )
    parser.add_argument(
        "--insert", "-i", help="Insert the YAML to publications.md", action="store_true"
    )
    args = parser.parse_args()
    yaml_strings = doi2yaml(args.doi)
    if args.insert:
        insert_yaml(yaml_strings)
