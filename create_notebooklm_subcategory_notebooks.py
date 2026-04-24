#!/usr/bin/env python3
import json
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/Users/sidg/Downloads/Research Website Codex/Papers")
NLM = "nlm"


def run_nlm(args):
    cmd = " ".join([shlex.quote(NLM)] + [shlex.quote(a) for a in args])
    result = subprocess.run(
        ["zsh", "-lic", cmd],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_notebooks():
    output = run_nlm(["notebook", "list"])
    data = json.loads(output)
    return {item.get("title", ""): item["id"] for item in data if item.get("id")}


def create_notebook(title):
    output = run_nlm(["notebook", "create", title])
    try:
        data = json.loads(output)
        return data["id"]
    except Exception:
        # Fallback for non-JSON create output.
        notebooks = get_notebooks()
        if title in notebooks:
            return notebooks[title]
        raise RuntimeError(f"Could not determine notebook id for {title!r}: {output}")


def list_source_titles(notebook_id):
    output = run_nlm(["source", "list", notebook_id, "--json"])
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return set()
    titles = set()
    for item in data:
        title = item.get("title") or item.get("name")
        if title:
            titles.add(title)
    return titles


def add_pdf(notebook_id, pdf_path):
    run_nlm(["source", "add", notebook_id, "--file", str(pdf_path), "--title", pdf_path.name])


def main():
    notebooks = get_notebooks()
    summary = []

    for category_dir in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        for subcategory_dir in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            pdfs = sorted(p for p in subcategory_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf")
            if not pdfs:
                continue

            title = f"{category_dir.name} — {subcategory_dir.name}"
            notebook_id = notebooks.get(title)
            created = False
            if not notebook_id:
                notebook_id = create_notebook(title)
                notebooks[title] = notebook_id
                created = True

            existing_titles = list_source_titles(notebook_id)
            uploaded = 0
            skipped = 0
            failed = []
            for pdf in pdfs:
                if pdf.name in existing_titles:
                    skipped += 1
                    continue
                try:
                    add_pdf(notebook_id, pdf)
                    uploaded += 1
                except subprocess.CalledProcessError as exc:
                    failed.append(
                        {
                            "file": pdf.name,
                            "error": (exc.stderr or exc.stdout or "").strip(),
                        }
                    )

            summary.append(
                {
                    "title": title,
                    "notebook_id": notebook_id,
                    "created": created,
                    "pdf_count": len(pdfs),
                    "uploaded": uploaded,
                    "skipped_existing": skipped,
                    "failed": failed,
                }
            )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
