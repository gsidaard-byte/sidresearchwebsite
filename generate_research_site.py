from __future__ import annotations

import html
import re
import shutil
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

import paper_reorg
from subcategory_site_copy import SUBCATEGORY_SITE_COPY


ROOT = Path("/Users/sidg/Downloads/Research Website Codex")
WEBSITE_DIR = ROOT / "website"
RESEARCH_DIR = WEBSITE_DIR / "research"
ASSETS_DIR = WEBSITE_DIR / "assets"
RESEARCH_INFOGRAPHICS_DIR = ASSETS_DIR / "research-infographics"
PROFILES_DIR = ROOT / "Students" / "Profiles"
PAPERS_DIR = ROOT / "Papers"
PAPER_EXTENSIONS = {".pdf", ".doc", ".docx", ".tex", ".bib", ".rtf"}


EXCLUDED_PROFILE_SLUGS = {"josh-deslich"}
PROFILE_SLUGS = {
    path.stem
    for path in (WEBSITE_DIR / "profiles").glob("*.html")
    if path.stem not in EXCLUDED_PROFILE_SLUGS
}
AUTHOR_ALIASES = {
    "abdul khan": "abdul-khan",
    "abdul r khan": "abdul-khan",
    "andrew killian": "andrew-killian",
    "andrew porterfield": "andrew-porterfield",
    "brock greenwood": "brock-greenwood",
    "brock a greenwood": "brock-greenwood",
    "charles b cain": "c-b-cain",
    "charles b. cain": "c-b-cain",
    "charles c b cain": "c-b-cain",
    "charles c.b. cain": "c-b-cain",
    "caiden guzman": "caiden-guzman",
    "daniel curry": "daniel-curry",
    "emma schutter": "emma-schutter",
    "eric insana": "eric-insana",
    "faith loughnane": "faith-loughnane",
    "george gogidze": "george-gogidze",
    "grace culpepper": "grace-culpepper",
    "grace selm": "grace-selm",
    "grace n selm": "grace-selm",
    "grace n. selm": "grace-selm",
    "grace schreyer": "grace-schreyer",
    "grant ross": "grant-ross",
    "ian tierney": "ian-tierney",
    "jielong cai": "jacky-cai",
    "jacky cai": "jacky-cai",
    "jessica c demoor": "jessica-demoor",
    "jessica demoor": "jessica-demoor",
    "joe ivarson": "joe-ivarson",
    "joseph ivarson": "joe-ivarson",
    "josh deslich": "josh-deslich",
    "joshua deslich": "josh-deslich",
    "julian pabon": "julian-pabon",
    "julian a pabon": "julian-pabon",
    "luke duncan": "luke-duncan",
    "lucas duncan": "luke-duncan",
    "madison peyton": "madison-peyton",
    "matt gazella": "matt-gazella",
    "matthew gazella": "matt-gazella",
    "michael mongin": "michael-mongin",
    "nathan thomas": "nathan-thomas",
    "neal novotny": "neal-novotny",
    "nevin jestus": "nevin-jestus",
    "asa palmer": "asa-palmer",
    "rachael supina": "rachael-supina",
    "rachel sharp": "rachel-sharp",
    "samuel barnhart": "samuel-barnhart",
    "sam barnhart": "samuel-barnhart",
    "samuel parlett": "samuel-parlett",
    "tim gerham": "tim-gerham",
    "timothy gerham": "tim-gerham",
    "steven goodman": "steven-goodman",
    "xinyu gao": "cindy",
}


PAPER_DETAIL_OVERRIDES = {
    "B2_s00348-024-03877-y.pdf": {
        "title": "Causal Kalman Filtering for Particle Tracking Velocimetry Using an Event Camera",
        "summary": "Develops a causal Kalman-filtering approach for event-camera particle tracking, aimed at more reliable real-time velocimetry in unsteady flows.",
        "citations": [
            "Khan, Abdul R., Michael P. Mongin, Andrew Killian, Keigo Hirakawa, and Sidaard Gunasekaran. \"Causal Kalman Filtering for Particle Tracking Velocimetry Using an Event Camera.\" Experiments in Fluids (2024)."
        ],
        "students": [("Abdul Khan", "abdul-khan"), ("Andrew Killian", "andrew-killian"), ("Michael Mongin", "michael-mongin")],
    },
    "B1_gunasekaran-et-al-2019-effect-of-flexible-inverted-pvdf-in-free-shear-layer-wake.pdf": {
        "title": "Effect of Flexible Inverted PVDF in Free Shear Layer Wake",
        "summary": "Introduces a flexible piezoelectric flag as a wake-sensing approach for unsteady free-shear-layer measurements.",
        "citations": [
            "15. Gunasekaran, Sidaard, Grant V. Ross, and Daniel Curry. \"Effect of Flexible Inverted PVDF in Free Shear Layer Wake.\" In AIAA Scitech 2019 Forum, p. 1338. 2019. https://doi.org/10.2514/6.2019-1338"
        ],
        "doi": "https://doi.org/10.2514/6.2019-1338",
        "students": [("Grant Ross", "grant-ross"), ("Daniel Curry", "daniel-curry")],
    },
    "A3_integrated-teaching-model-a-follow-up-with-fundamental-aerodynamics.pdf": {
        "title": "Integrated Teaching Model: A Follow Up with Fundamental Aerodynamics",
        "summary": "Examines a teaching model built around fundamental aerodynamics to strengthen conceptual understanding and applied reasoning.",
        "citations": [
            "14. Gunasekaran, Sidaard. \"Integrated Teaching Model: A Follow Up with Fundamental Aerodynamics.\" ASEE Annual Conference and Exposition. 2018. https://peer.asee.org/30677"
        ],
        "students": [],
    },
    "A3_integrated-teaching-model-in-graduate-aerospace-classes-a-trial-with-compressible-flow-aerodynamics.pdf": {
        "title": "Integrated Teaching Model in Graduate Aerospace Classes: A Trial With Compressible Flow Aerodynamics",
        "summary": "Adapts the integrated teaching model to graduate compressible-flow instruction, emphasizing analytical depth alongside application.",
        "citations": [
            "Integrated Teaching Model in Graduate Aerospace Classes: A Trial With Compressible Flow Aerodynamics. 2017."
        ],
        "students": [],
    },
    "C1_killian-et-al-2023-periodic-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf": {
        "title": "Periodic Vortical Gust Encounter and Mitigation Using Closed Loop Control",
        "summary": "Studies how a wing responds to periodic vortical gusts and demonstrates closed-loop mitigation of the resulting unsteady loads.",
        "citations": [
            "44. Killian, Andrew, Sidaard Gunasekaran, Michael P. Mongin, and Albert Medina. \"Periodic Vortical Gust Encounter and Mitigation Using Closed Loop Control.\" In AIAA SCITECH 2023 Forum, p. 2477. 2023. https://doi.org/10.2514/6.2023-2477"
        ],
        "doi": "https://doi.org/10.2514/6.2023-2477",
        "students": [("Andrew Killian", "andrew-killian"), ("Michael Mongin", "michael-mongin")],
    },
    "B2_138800F.pdf": {
        "title": "Event-Based Velocimetry in Additive-Manufacturing Flowfields",
        "summary": "Explores an event-based velocimetry application in an additive-manufacturing flow environment, extending high-speed sensing beyond conventional aerodynamic test cases.",
        "citations": [
            "Event-Based Velocimetry in Additive-Manufacturing Flowfields. 2026."
        ],
        "students": [],
    },
    "A2_PropellerGroundandCeilingEffectinForwardFlight_Final_V4.pdf": {
        "title": "Propeller Ground and Ceiling Effect in Forward Flight",
        "summary": "Extends propeller boundary-proximity studies into forward flight, connecting nearby surfaces to changes in installed performance and wake behavior.",
        "citations": [
            "Propeller Ground and Ceiling Effect in Forward Flight. 2022."
        ],
        "students": [],
    },
    "E1_PropellerGroundandCeilingEffectinForwardFlight_Final_V4.pdf": {
        "title": "Propeller Ground and Ceiling Effect in Forward Flight",
        "summary": "Extends propeller boundary-proximity studies into forward flight, connecting nearby surfaces to changes in installed performance and wake behavior.",
        "citations": [
            "Propeller Ground and Ceiling Effect in Forward Flight. 2022."
        ],
        "students": [],
    },
    "PropellerGroundandCeilingEffectinForwardFlight_Final_V4.pdf": {
        "title": "Propeller Ground and Ceiling Effect in Forward Flight",
        "summary": "Extends propeller boundary-proximity studies into forward flight, connecting nearby surfaces to changes in installed performance and wake behavior.",
        "citations": [
            "Propeller Ground and Ceiling Effect in Forward Flight. 2022."
        ],
        "students": [],
    },
    "E1_PLhhwQ-cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf": {
        "title": "Changes In Propeller Performance Due to Ground Proximity",
        "summary": "Examines how nearby ground surfaces reshape propeller inflow, wake behavior, and installed aerodynamic performance.",
        "citations": [
            "Cai, Jielong, Sidaard Gunasekaran, Anwar Ahmed, and Michael V. Ol. \"Changes In Propeller Performance Due to Ground Proximity.\" In AIAA Scitech 2019 Forum, p. 1097. 2019. https://doi.org/10.2514/6.2019-1097"
        ],
        "students": [("Jacky Cai", "jacky-cai")],
        "doi": "https://doi.org/10.2514/6.2019-1097",
    },
}


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


STUDENT_PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
STUDENT_PHOTOS_BY_SLUG = {
    slugify(path.stem): path.name
    for path in sorted((ROOT / "Students").iterdir())
    if path.is_file() and path.suffix.lower() in STUDENT_PHOTO_EXTENSIONS
}


def normalize_title(text: str) -> str:
    text = text.lower()
    text = text.replace("&", "and")
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def unique_preserving_order(items: list[str]) -> list[str]:
    seen = set()
    ordered = []
    for item in items:
        key = re.sub(r"\s+", " ", strip_citation_numbers(item)).strip()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(item)
    return ordered


def strip_citation_numbers(text: str) -> str:
    text = re.sub(r"^\s*\d{1,3}\.\s+", "", text)
    text = re.sub(r"(?:(?<=\.\s)|(?<=\)\s))\d{1,3}\.\s+(?=[A-Z][A-Za-z'().-]+(?:\s+[A-Z][A-Za-z'().-]+)*,)", "", text)
    return text


def sanitize_public_copy(text: str) -> str:
    text = text.replace("The current folder now spans ", "The theme now spans ")
    text = text.replace("The papers now present in the folder ", "The papers in this subcategory ")
    text = text.replace("generated from the paper archive itself", "prepared for this research overview")
    text = text.replace("current folder", "theme")
    text = text.replace("Across the folder, ", "Across this body of work, ")
    text = text.replace("The folder also gives ", "The body of work also gives ")
    text = text.replace("This folder contains ", "This subcategory contains ")
    text = text.replace("The folder shows ", "These papers show ")
    text = text.replace("The folder identifies ", "These papers identify ")
    text = text.replace("gives the folder a useful modeling backbone", "provides a useful modeling backbone")
    text = text.replace("The duplicated 2019 export and the conference-style forward-flight paper reinforce the same lesson from multiple outputs, while the parametric data paper provides a useful modeling backbone.", "Multiple papers reinforce the same lesson across hover and forward-flight conditions, while the parametric data paper provides a useful modeling backbone.")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_lookup_stem(text: str) -> str:
    stem = Path(text).stem.lower()
    stem = re.sub(r"^[a-z]\d+[_-]+", "", stem)
    stem = re.sub(r"^[a-z]{1,3}\d+[_-]+", "", stem)
    stem = stem.replace("_", "-")
    return normalize_title(stem)


def ordered_categories() -> list[str]:
    present = [path.name for path in PAPERS_DIR.iterdir() if path.is_dir()]
    ordered = [category for category in paper_reorg.CATEGORY_ORDER if category in present]
    ordered.extend(sorted(category for category in present if category not in ordered))
    return ordered


def paper_files_in(directory: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() in PAPER_EXTENSIONS
        ],
        key=lambda path: path.name.lower(),
    )


INFOGRAPHIC_MEDIA_EXTENSIONS = {".png", ".mp4", ".webm", ".mov"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}


def infographic_files_in(directory: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() in INFOGRAPHIC_MEDIA_EXTENSIONS
        ],
        key=lambda path: path.name.lower(),
    )


def build_taxonomy() -> dict[str, dict[str, object]]:
    taxonomy: dict[str, dict[str, object]] = {}
    for category in ordered_categories():
        category_dir = PAPERS_DIR / category
        subcategories = {}
        for subdir in sorted([path for path in category_dir.iterdir() if path.is_dir()], key=lambda path: path.name.lower()):
            papers = [path.name for path in paper_files_in(subdir)]
            subcategories[subdir.name] = papers
        taxonomy[category] = {"subcategories": subcategories}
    return taxonomy


def infographic_title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").strip()


def build_infographic_registry(taxonomy: dict[str, dict[str, object]]) -> dict[tuple[str, str], list[dict[str, str]]]:
    registry: dict[tuple[str, str], list[dict[str, str]]] = {}
    if RESEARCH_INFOGRAPHICS_DIR.exists():
        shutil.rmtree(RESEARCH_INFOGRAPHICS_DIR)
    RESEARCH_INFOGRAPHICS_DIR.mkdir(parents=True, exist_ok=True)

    for category in ordered_categories():
        cat_slug = slugify(category)
        for subcategory in taxonomy[category]["subcategories"]:
            sub_slug = slugify(subcategory)
            source_dir = PAPERS_DIR / category / subcategory
            asset_dir = RESEARCH_INFOGRAPHICS_DIR / cat_slug / sub_slug
            items = []
            for image_path in infographic_files_in(source_dir):
                asset_dir.mkdir(parents=True, exist_ok=True)
                dest_path = asset_dir / image_path.name
                shutil.copy2(image_path, dest_path)
                items.append(
                    {
                        "title": infographic_title_from_path(image_path),
                        "filename": image_path.name,
                        "kind": "video" if image_path.suffix.lower() in VIDEO_EXTENSIONS else "image",
                        "src": f"../../assets/research-infographics/{quote(cat_slug)}/{quote(sub_slug)}/{quote(image_path.name)}",
                    }
                )
            registry[(category, subcategory)] = items
    return registry


def parse_category_summary(category: str) -> dict[str, str]:
    info = paper_reorg.CATEGORY_SUMMARIES[category]
    return {
        "title": category,
        "summary": sanitize_public_copy(info["summary"]),
        "methods": sanitize_public_copy(info["methods"]),
        "why": sanitize_public_copy(info["importance"]),
    }


def parse_subcategory_summary(category: str, subcategory: str) -> dict[str, str]:
    override = SUBCATEGORY_SITE_COPY.get((category, subcategory))
    if override:
        return {
            "Important Findings": override["Overview"],
            "Value": override["Why It Matters"],
            "Key Takeaways": override["Research Focus"],
            "Overview": override["Overview"],
            "Why It Matters Expanded": override["Why It Matters"],
            "Research Focus Expanded": override["Research Focus"],
            "Blurb": subcategory_card_blurb({"Important Findings": override["Overview"], "Key Takeaways": override["Research Focus"]}),
        }
    path = ROOT / "Papers" / category / subcategory / "README.md"
    text = path.read_text(encoding="utf-8")
    sections = {"Important Findings": "", "Value": "", "Key Takeaways": ""}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:]
            continue
        if current in sections:
            sections[current] += line + "\n"
    cleaned = {k: polish_research_copy(v.strip()) for k, v in sections.items()}
    overview_parts = [cleaned["Important Findings"], cleaned["Value"]]
    overview = "\n\n".join(part for part in overview_parts if part)
    why_it_matters = cleaned["Value"]
    if cleaned["Key Takeaways"]:
        why_it_matters = "\n\n".join(part for part in [cleaned["Value"], cleaned["Key Takeaways"]] if part)
    research_focus = "\n\n".join(part for part in [cleaned["Important Findings"], cleaned["Key Takeaways"]] if part)
    return {
        **cleaned,
        "Overview": overview,
        "Why It Matters Expanded": why_it_matters,
        "Research Focus Expanded": research_focus,
        "Blurb": subcategory_card_blurb(cleaned),
    }


def polish_research_copy(text: str) -> str:
    text = sanitize_public_copy(text).strip()
    replacements = [
        (r"\bThese papers isolate how\b", "This research examines how"),
        (r"\bThese papers isolate\b", "This research examines"),
        (r"\bThese papers show\b", "The work shows"),
        (r"\bThese papers move\b", "This research moves"),
        (r"\bThese papers treat\b", "This research treats"),
        (r"\bThese papers provide\b", "This research provides"),
        (r"\bThese papers broaden\b", "This research broadens"),
        (r"\bThese papers trace\b", "This research traces"),
        (r"\bThese papers study\b", "This research studies"),
        (r"\bThese papers examine\b", "This research examines"),
        (r"\bThese papers capture\b", "This research examines"),
        (r"\bThese papers identify\b", "The work identifies"),
        (r"\bThese studies define\b", "The work defines"),
        (r"\bThe papers\b", "The work"),
        (r"\bthe papers\b", "the work"),
        (r"^These papers\b", "This research"),
        (r"^These studies\b", "This research"),
        (r"^This paper\b", "This work"),
        (r"^This set\b", "This research"),
        (r"^This subcategory\b", "This line of research"),
        (r"^Its value is in closing the loop between aerodynamic theory and vehicle behavior\.", "This work matters because it closes the loop between aerodynamic theory and vehicle behavior."),
        (r"^Its value is in design guidance for distributed propulsion\.", "This work matters because it offers design guidance for distributed propulsion."),
        (r"^Its value is in defining the uncontrolled aerodynamic baseline that later control systems must outperform or exploit\.", "This work matters because it defines the uncontrolled aerodynamic baseline that later control systems must outperform or exploit."),
        (r"^The value is in design guidance for distributed propulsion\.", "This work matters because it offers design guidance for distributed propulsion."),
        (r"^Their value is in defining the uncontrolled aerodynamic baseline that later control systems must outperform or exploit\.", "This work matters because it defines the uncontrolled aerodynamic baseline that later control systems must outperform or exploit."),
        (r"^This work matters because in design guidance for distributed propulsion\.", "This work matters because it offers design guidance for distributed propulsion."),
        (r"^This work matters because in defining the uncontrolled aerodynamic baseline that later control systems must outperform or exploit\.", "This work matters because it defines the uncontrolled aerodynamic baseline that later control systems must outperform or exploit."),
        (r"^The value is operational:\s*", "This work matters operationally because "),
        (r"^Their value is operational\.\s*", "This work matters operationally because "),
        (r"^This work matters because operational\.\s*", "This work matters operationally because "),
        (r"^Their value is direct design guidance for blown-wing and propeller-in-wing concepts\.", "This work matters because it offers direct design guidance for blown-wing and propeller-in-wing concepts."),
        (r"^The value is direct design guidance for blown-wing and propeller-in-wing concepts\.", "This work matters because it offers direct design guidance for blown-wing and propeller-in-wing concepts."),
        (r"^This work matters because direct design guidance for blown-wing and propeller-in-wing concepts\.", "This work matters because it offers direct design guidance for blown-wing and propeller-in-wing concepts."),
        (r"^Their value is methodological and applied:\s*", "This work matters both methodologically and practically: "),
        (r"^The value is immediately practical for agricultural application,\s*", "This work matters because it directly informs agricultural spray application, "),
        (r"^Their value is that they connect sensing to actuation and experimentation in a way that supports future closed-loop systems rather than passive observation alone\.", "This work matters because it connects sensing, experimentation, and future closed-loop control rather than treating measurement as passive observation alone."),
        (r"^Their value is that they lower the barrier\b", "This work matters because it lowers the barrier"),
        (r"^Their value is measurement reach:\s*", "This work matters because it extends what can be measured: "),
        (r"^Its value is foundational:\s*", "This work matters because it provides a stronger experimental foundation: "),
        (r"^Its value is generalization:\s*", "This work matters because it shows how aerodynamic methods can transfer across fluid systems: "),
        (r"^Their value is practical and predictive:\s*", "This work matters in practical and predictive terms: "),
        (r"^Their value is practical and predictive\.\s*", "This work matters in practical and predictive terms. "),
        (r"^Their value is architectural:\s*", "This work matters at the system-design level: "),
        (r"^The value is architectural:\s*", "This work matters at the system-design level: "),
        (r"^The value is design flexibility:\s*", "This work matters because it expands aerodynamic design flexibility: "),
        (r"^The value is system-level realism:\s*", "This work matters because it brings system-level realism to the problem: "),
        (r"^Its value is conceptual clarity:\s*", "This work matters because it clarifies the governing aerodynamic idea: "),
        (r"^Its value is practical:\s*", "This work matters in practice because "),
        (r"^Its value is methodological:\s*", "This work matters methodologically because "),
        (r"^Its value is operational realism:\s*", "This work matters because it extends aerodynamic understanding into operational conditions: "),
        (r"^Their value is interpretive:\s*", "This work matters because it turns performance changes into an interpretable flow-physics question: "),
        (r"^The value is design specificity:\s*", "This work matters because it links aerodynamic gains to specific flow mechanisms: "),
        (r"^The value is conceptual generality:\s*", "This work matters because it clarifies a broader aerodynamic principle: "),
        (r"^Their value is experimental legitimacy for an induced-drag-control idea that is often discussed conceptually but is much stronger when observed directly in the near wake\.", "This work matters because it brings direct experimental evidence to an induced-drag-control idea that is often discussed more conceptually than observed."),
        (r"^Its value is human infrastructure:\s*", "This work matters because strong pedagogy is part of the infrastructure that sustains research and engineering practice: "),
        (r"^Their value is that\s*", "This work matters because "),
        (r"^Their value is\s*", "This work matters because "),
        (r"^The value is that\s*", "This work matters because "),
        (r"^The value is\s*", "This work matters because "),
        (r"^Its value is that\s*", "This work matters because "),
        (r"^Its value is\s*", "This work matters because "),
        (r"\bThe work connect\b", "The work connects"),
        (r"\bThe work help\b", "The work helps"),
        (r"\bthe work provide\b", "the work provides"),
        (r"\bthe work connect\b", "the work connects"),
        (r"\bthey show\b", "it shows"),
        (r"\bthey turn\b", "it turns"),
        (r"\bthey lower the barrier\b", "it lowers the barrier"),
        (r"\band make event cameras usable\b", "and makes event cameras usable"),
        (r"^This work matters in practice because the work provides\b", "This work matters in practice because it provides"),
        (r"^This work matters operationally because The work\b", "This work matters operationally because the work"),
        (r"^This work matters because measurement reach:\s*", "This work matters because it extends measurement reach: "),
        (r"^This work matters because foundational:\s*", "This work matters because it provides a stronger experimental foundation: "),
        (r"^This work matters because generalization:\s*", "This work matters because it shows how aerodynamic methods can transfer across fluid systems: "),
        (r"^This work matters because human infrastructure:\s*", "This work matters because pedagogy is part of the human infrastructure that sustains research and engineering practice: "),
        (r"^This work matters because it offers design guidance for distributed propulsion\.\s*The work identifies\b", "This work matters because it offers design guidance for distributed propulsion. The work identifies"),
        (r"^This work matters operationally because\s*", "This work matters operationally because "),
        (r"^This work matters because it offers direct design guidance for blown-wing and propeller-in-wing concepts\.\s*The work helps\b", "This work matters because it offers direct design guidance for blown-wing and propeller-in-wing concepts. The work helps"),
        (r"^This work matters because it defines the uncontrolled aerodynamic baseline that later control systems must outperform or exploit\.", "This work matters because it defines the uncontrolled aerodynamic baseline that later control systems must outperform or exploit."),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text.strip()


def subcategory_card_blurb(summary: dict[str, str]) -> str:
    findings = summary.get("Important Findings", "")
    takeaways = summary.get("Key Takeaways", "")
    first_sentence = re.split(r"(?<=[.!?])\s+", findings, maxsplit=1)[0].strip()
    if first_sentence and len(first_sentence) <= 260:
        return first_sentence
    return takeaways or findings


def profile_display_name(slug: str) -> str:
    text = (PROFILES_DIR / f"{slug}.md").read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else slug.replace("-", " ").title()


def build_student_publication_index() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    paper_index: dict[str, dict[str, object]] = defaultdict(lambda: {"citations": [], "students": set(), "title": None})
    doi_index: dict[str, dict[str, object]] = defaultdict(lambda: {"citations": [], "students": set(), "title": None})
    for path in PROFILES_DIR.glob("*.md"):
        slug = path.stem
        if slug in EXCLUDED_PROFILE_SLUGS:
            continue
        display = profile_display_name(slug)
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        current_title = None
        for line in lines:
            if line.startswith("### "):
                current_title = re.sub(r"^\d+\.\s*", "", line[4:].strip()).rstrip(".")
            elif line.startswith("- Citation:") and current_title:
                citation = line.split(":", 1)[1].strip()
                key = normalize_title(current_title)
                paper_index[key]["title"] = current_title
                if citation not in paper_index[key]["citations"]:
                    paper_index[key]["citations"].append(strip_citation_numbers(citation))
                paper_index[key]["students"].add((display, slug))
                doi_match = re.search(r"https://doi\.org/([A-Za-z0-9./\-]+)", citation)
                if doi_match:
                    doi = doi_match.group(1)
                    doi_index[doi]["title"] = current_title
                    if citation not in doi_index[doi]["citations"]:
                        doi_index[doi]["citations"].append(strip_citation_numbers(citation))
                    doi_index[doi]["students"].add((display, slug))
    return paper_index, doi_index


def prettify_filename_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^[A-Za-z]\d+[_-]+", "", stem)
    stem = re.sub(r"^[A-Za-z]{1,3}\d+[_-]+", "", stem)
    stem = re.sub(r"^[A-Za-z]+-et-al-\d{4}-", "", stem)
    stem = re.sub(r"^[A-Za-z]+-[A-Za-z]+-\d{4}-", "", stem)
    stem = re.sub(r"^\d+\.\d+-", "", stem)
    stem = stem.replace("_", " ")
    stem = stem.replace("-", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem.title() if stem else Path(filename).stem


def extract_paper_details(taxonomy: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    metadata = paper_reorg.load_metadata()
    student_index, doi_index = build_student_publication_index()
    paper_map_by_name: dict[str, list[str]] = defaultdict(list)
    paper_map_by_lookup: dict[str, list[str]] = defaultdict(list)
    for rel in paper_reorg.PAPER_MAP:
        paper_map_by_name[Path(rel).name].append(rel)
        paper_map_by_lookup[normalize_lookup_stem(Path(rel).name)].append(rel)
    details = {}
    doi_pat = re.compile(r"10\.\d{4,9}/[^\s|)]+")
    current_filenames = []
    for category_info in taxonomy.values():
        for papers in category_info["subcategories"].values():
            current_filenames.extend(papers)
    for filename in sorted(set(current_filenames), key=str.lower):
        rels = paper_map_by_name.get(filename, [])
        if not rels:
            rels = paper_map_by_lookup.get(normalize_lookup_stem(filename), [])
        rel = rels[0] if rels else None
        item = paper_reorg.PAPER_MAP.get(rel, {"rationale": "", "notes": ""}) if rel else {"rationale": "", "notes": ""}
        meta = metadata.get(rel, {}) if rel else {}
        title = meta.get("title") or prettify_filename_title(filename)
        if (
            title.lower().startswith("abstract ")
            or "downloaded by" in title.lower()
            or title.startswith("AIAA ")
            or title.startswith("VFS Forum")
            or len(title) > 220
        ):
            title = prettify_filename_title(filename)
        snippet = meta.get("snippet", "")
        key = normalize_title(title)
        doi_match = doi_pat.search(snippet)
        doi = doi_match.group(0).rstrip(".,)") if doi_match else None
        if doi and doi in doi_index:
            canonical = doi_index[doi]
            title = canonical["title"] or title
            key = normalize_title(title)
            citations = list(canonical.get("citations", []))
            students = set(canonical.get("students", set()))
        else:
            title_match = student_index.get(key, {})
            title = title_match.get("title") or title
            citations = list(title_match.get("citations", []))
            students = set(title_match.get("students", set()))
        if not citations:
            year_match = re.search(r"(19|20)\d{2}", rel or "")
            if not year_match:
                year_match = re.search(r"(19|20)\d{2}", filename)
            year = year_match.group(0) if year_match else "n.d."
            citation = f"{title}. {year}."
            if doi:
                citation += f" https://doi.org/{doi}"
            citations = [citation]
        citations = unique_preserving_order(citations)
        normalized_snippet = normalize_title(f"{snippet} {title} {filename}")
        for alias, slug in AUTHOR_ALIASES.items():
            if slug in PROFILE_SLUGS and alias in normalized_snippet:
                students.add((profile_display_name(slug), slug))
        summary = paper_reorg.contribution_sentence(title, snippet, item.get("rationale", ""), item.get("notes", ""))
        if not summary.strip():
            summary = f"This paper contributes to the {title.lower()} line of work represented in this research area."
        details[filename] = {
            "title": title,
            "summary": sanitize_public_copy(summary),
            "citations": citations,
            "doi": f"https://doi.org/{doi}" if doi else None,
            "students": sorted(students),
        }
        if filename in PAPER_DETAIL_OVERRIDES:
            details[filename].update(PAPER_DETAIL_OVERRIDES[filename])
            details[filename]["citations"] = unique_preserving_order(details[filename].get("citations", []))
    return details


def nav(prefix: str, active: str = "research") -> str:
    links = [
        ("Home", f"{prefix}index.html", "home"),
        ("Research Projects", f"{prefix}research.html", "research"),
        ("Students", f"{prefix}students.html", "students"),
        ("Alumni", f"{prefix}alumni.html", "alumni"),
        ("Publications", f"{prefix}publications.html", "publications"),
        ("Teaching", f"{prefix}teaching.html", "teaching"),
        ("Facilities", f"{prefix}facilities.html", "facilities"),
        ("News", f"{prefix}news.html", "news"),
        ("Community", f"{prefix}community.html", "community"),
    ]
    rendered_parts = []
    for label, href, key in links:
        cls = ' class="active"' if key == active else ""
        rendered_parts.append(f'<a{cls} href="{href}">{label}</a>')
    rendered = "".join(rendered_parts)
    return (
        f'<header class="site-header"><div class="shell"><a class="brand" href="{prefix}index.html">'
        '<span class="brand-mark">Welcome to Our Community </span><span class="brand-name">Dr. Sidaard Gunasekaran, Ph.D., University of Dayton</span></a>'
        f'<nav class="nav">{rendered}</nav></div></header>'
    )


def footer(prefix: str) -> str:
    return (
        f'<footer class="footer"><div class="shell"><div>Research themes, publications, and contributors across the group.</div>'
        f'<div class="footer-links"><a href="{prefix}research.html">Research Projects</a><a href="{prefix}publications.html">Publications</a></div></div></footer>'
    )


def paragraph_html(text: str) -> str:
    return "".join(f"<p>{escape(part)}</p>" for part in text.split("\n\n") if part.strip())


def render_students(students: list[tuple[str, str]], prefix: str) -> str:
    if not students:
        return '<p class="meta-note">Student contributors are listed where available.</p>'
    chips = []
    for name, slug in students:
        if slug in PROFILE_SLUGS:
            chips.append(f'<a class="chip-link" href="{prefix}profiles/{slug}.html">{escape(name)}</a>')
        else:
            chips.append(f'<span class="chip-link chip-static">{escape(name)}</span>')
    return f'<div class="chip-row">{"".join(chips)}</div>'


def aggregate_students(filenames: list[str], paper_details: dict[str, dict[str, object]]) -> list[tuple[str, str]]:
    students = set()
    for filename in filenames:
        students.update(paper_details[filename]["students"])
    return sorted(students, key=lambda item: item[0].split()[-1].lower())


def unique_publication_filenames(filenames: list[str], paper_details: dict[str, dict[str, object]]) -> list[str]:
    seen = set()
    ordered = []
    for filename in filenames:
        data = paper_details[filename]
        key = (
            normalize_title(data["title"]),
            tuple(unique_preserving_order(data.get("citations", []))),
        )
        if key in seen:
            continue
        seen.add(key)
        ordered.append(filename)
    return ordered


def student_photo_src(slug: str, prefix: str) -> str | None:
    filename = STUDENT_PHOTOS_BY_SLUG.get(slug)
    if not filename:
        return None
    return f"{prefix}../Students/{quote(filename)}"


def render_contributor_card(name: str, slug: str, prefix: str) -> str:
    profile_href = f"{prefix}profiles/{slug}.html" if slug in PROFILE_SLUGS else ""
    photo_src = student_photo_src(slug, prefix)
    photo = (
        f'<img src="{photo_src}" alt="{escape(name)}" loading="lazy" />'
        if photo_src
        else f'<div class="student-photo-placeholder">{escape(name[:1])}</div>'
    )
    profile_link = (
        f'<div class="student-links"><a href="{profile_href}">View profile</a></div>'
        if profile_href
        else ""
    )
    return (
        '<article class="student-card research-contributor-card">'
        f'<div class="student-photo">{photo}</div>'
        '<div class="student-copy">'
        '<div class="student-role">Contributor</div>'
        f"<h3>{escape(name)}</h3>"
        f"{profile_link}"
        "</div>"
        "</article>"
    )


def render_contributor_section(students: list[tuple[str, str]], prefix: str) -> str:
    if students:
        content = (
            '<div class="student-grid research-contributor-grid">'
            + "".join(render_contributor_card(name, slug, prefix) for name, slug in students)
            + "</div>"
        )
    else:
        content = '<article class="card"><p class="meta-note">Student contributors will appear here as publication and profile information becomes available.</p></article>'
    return f"""
      <section>
        <div class="shell">
          <div class="section-header">
            <div><div class="section-kicker">Contributors</div><h2>Students who contributed to this work</h2></div>
            <p class="section-copy">Students connected to the publications and projects represented on this page.</p>
          </div>
          {content}
        </div>
      </section>
"""


def render_citations(citations: list[str]) -> str:
    items = []
    for citation in citations:
        citation_html = escape(strip_citation_numbers(citation))
        citation_html = re.sub(r"(https://doi\.org/[A-Za-z0-9./\-]+)", r'<a href="\1">\1</a>', citation_html)
        items.append(f"<li>{citation_html}</li>")
    return '<ul class="citation-list">' + "".join(items) + "</ul>"


def render_paper_card(filename: str, paper_details: dict[str, dict[str, object]], prefix: str) -> str:
    data = paper_details[filename]
    return (
        '<article class="pub-card research-paper-card">'
        f"<h3>{escape(data['title'])}</h3>"
        '<div class="paper-meta"><strong>Students</strong></div>'
        f"{render_students(data['students'], prefix)}"
        '<div class="paper-meta"><strong>Citation</strong></div>'
        f"{render_citations(data['citations'])}"
        + (f'<div class="pub-links"><a href="{data["doi"]}">DOI</a></div>' if data["doi"] else "")
        + "</article>"
    )


def render_infographic_section(infographics: list[dict[str, str]]) -> str:
    if not infographics:
        return ""

    def render_infographic_media(infographic: dict[str, str]) -> str:
        if infographic.get("kind") == "video":
            return (
                f'<video src="{infographic["src"]}" controls preload="metadata">'
                f'<a href="{infographic["src"]}">Open {escape(infographic["title"])} video</a>'
                "</video>"
            )
        return (
            f'<a href="{infographic["src"]}" target="_blank" rel="noopener noreferrer">'
            f'<img src="{infographic["src"]}" alt="{escape(infographic["title"])} infographic" loading="lazy" />'
            "</a>"
        )

    if len(infographics) == 1:
        infographic = infographics[0]
        media = (
            '<div class="infographic-frame infographic-single">'
            f'{render_infographic_media(infographic)}'
            f'<p class="infographic-caption">{escape(infographic["title"])}</p>'
            "</div>"
        )
    else:
        cards = []
        for infographic in infographics:
            cards.append(
                '<figure class="infographic-frame">'
                f'{render_infographic_media(infographic)}'
                f'<figcaption class="infographic-caption">{escape(infographic["title"])}</figcaption>'
                "</figure>"
            )
        media = f'<div class="infographic-grid">{"".join(cards)}</div>'

    return f"""
      <section>
        <div class="shell">
          <div class="section-header">
            <div><div class="section-kicker">Infographic</div><h2>Research infographic</h2></div>
            <p class="section-copy">NotebookLM-generated infographic and video assets for this research subcategory. Click any image to open the full-size file, or play videos directly on the page.</p>
          </div>
          <div class="infographic-section">
            {media}
          </div>
        </div>
      </section>
"""


def category_page(category: str, taxonomy: dict[str, dict[str, object]], paper_details: dict[str, dict[str, object]]) -> str:
    info = parse_category_summary(category)
    cat_slug = slugify(category)
    subcards = []
    subcategories = taxonomy[category]["subcategories"]
    for subcategory, papers in subcategories.items():
        sub_slug = slugify(subcategory)
        subinfo = parse_subcategory_summary(category, subcategory)
        subcards.append(
            '<article class="card research-subcard">'
            f"<h3><a href=\"{cat_slug}/{sub_slug}.html\">{escape(subcategory)}</a></h3>"
            f"{paragraph_html(subinfo['Overview'])}"
            f"<div class=\"meta-row\"><span>{len(papers)} papers</span></div>"
            f'<a class="button secondary inner-link" href="{cat_slug}/{sub_slug}.html">Open Subcategory</a>'
            "</article>"
        )
    all_papers = []
    category_filenames = []
    for subcategory in subcategories:
        for filename in subcategories[subcategory]:
            category_filenames.append(filename)
    unique_category_filenames = unique_publication_filenames(category_filenames, paper_details)
    for filename in unique_category_filenames:
        all_papers.append(render_paper_card(filename, paper_details, "../"))
    contributor_section = render_contributor_section(aggregate_students(unique_category_filenames, paper_details), "../")
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape(category)} | Research Projects</title>
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body class="research-page">
    {nav("../")}
    <div class="page-hero">
      <div class="shell page-hero-grid">
        <div>
          <div class="section-kicker">Research Category</div>
          <h1>{escape(info["title"])}</h1>
          {paragraph_html(info["summary"])}
        </div>
        <aside class="panel">
          <h3>Methods and Tools</h3>
          <p>{escape(info["methods"])}</p>
          <h3>Why It Matters</h3>
          {paragraph_html(info["why"])}
        </aside>
      </div>
    </div>
    <main>
      <section>
        <div class="shell">
          <div class="section-header">
            <div><div class="section-kicker">Research Directions</div><h2>Focused lines of work within this area</h2></div>
            <p class="section-copy">Each subcategory offers a more focused view of the questions, methods, and applications that shape this broader research area.</p>
          </div>
          <div class="grid-2">
            {"".join(subcards)}
          </div>
        </div>
      </section>
      {contributor_section}
      <section>
        <div class="shell">
          <div class="section-header">
            <div><div class="section-kicker">Publications</div><h2>Research publications in this area</h2></div>
            <p class="section-copy">Publication entries include citation details and student contributors where available.</p>
          </div>
          <div class="pub-list">
            {"".join(all_papers)}
          </div>
        </div>
      </section>
    </main>
    {footer("../")}
  </body>
</html>
"""


def subcategory_page(
    category: str,
    subcategory: str,
    taxonomy: dict[str, dict[str, object]],
    paper_details: dict[str, dict[str, object]],
    infographic_registry: dict[tuple[str, str], list[dict[str, str]]],
) -> str:
    cat_slug = slugify(category)
    summary = parse_subcategory_summary(category, subcategory)
    filenames = unique_publication_filenames(taxonomy[category]["subcategories"][subcategory], paper_details)
    papers = "".join(render_paper_card(filename, paper_details, "../../") for filename in filenames)
    infographic_section = render_infographic_section(infographic_registry.get((category, subcategory), []))
    contributor_section = render_contributor_section(aggregate_students(filenames, paper_details), "../../")
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape(subcategory)} | {escape(category)}</title>
    <link rel="stylesheet" href="../../styles.css" />
  </head>
  <body class="research-page">
    {nav("../../")}
    <div class="page-hero">
      <div class="shell page-hero-grid">
        <div>
          <div class="section-kicker">Research Subcategory</div>
          <h1>{escape(subcategory)}</h1>
          <p class="breadcrumb-trail"><a href="../{cat_slug}.html">{escape(category)}</a> / {escape(subcategory)}</p>
          {paragraph_html(summary["Overview"])}
        </div>
        <aside class="panel">
          <h3>Why It Matters</h3>
          {paragraph_html(summary["Why It Matters Expanded"])}
          <h3>Research Focus</h3>
          {paragraph_html(summary["Research Focus Expanded"])}
        </aside>
      </div>
    </div>
    <main>
      {infographic_section}
      {contributor_section}
      <section>
        <div class="shell">
          <div class="section-header">
            <div><div class="section-kicker">Publications</div><h2>Research publications in this area</h2></div>
            <p class="section-copy">Publication entries include citation details and student contributors where available.</p>
          </div>
          <div class="pub-list">
            {papers}
          </div>
        </div>
      </section>
    </main>
    {footer("../../")}
  </body>
</html>
"""


def update_research_index() -> None:
    taxonomy = build_taxonomy()
    category_cards = []
    for category in ordered_categories():
        cat_slug = slugify(category)
        cat_summary = parse_category_summary(category)
        subcategories = taxonomy[category]["subcategories"]
        sublinks = "".join(
            f'<li><a href="research/{cat_slug}/{slugify(sub)}.html">{escape(sub)}</a></li>'
            for sub in subcategories
        )
        category_cards.append(
            '<article class="card research-index-card">'
            f'<h3><a href="research/{cat_slug}.html">{escape(category)}</a></h3>'
            f"<p>{escape(cat_summary['summary'].splitlines()[0])}</p>"
            f'<div class="meta-row"><span>{sum(len(v) for v in subcategories.values())} papers</span>'
            f'<span>{len(subcategories)} subcategories</span></div>'
            f'<ul class="plain-list compact-links">{sublinks}</ul>'
            f'<a class="button secondary inner-link" href="research/{cat_slug}.html">Open Category Page</a>'
            "</article>"
        )
    path = WEBSITE_DIR / "research.html"
    html_text = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Research Projects | Sidaard Gunasekaran Research Group</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body class="research-page">
    {nav("")}
    <div class="page-hero">
      <div class="shell page-hero-grid">
        <div>
          <div class="section-kicker">Research Projects</div>
          <h1>Where Propulsion, Aerodynamics, and Sensing Meet</h1>
          <p>Explore a connected body of research spanning propulsion, aerodynamics, wake physics, diagnostics, and student-led discovery.</p>
        </div>
        <aside class="panel">
          <h3>Inside the Research</h3>
          <ul class="plain-list">
            <li>Major themes across propulsion, aerodynamics, and sensing</li>
            <li>Focused projects connecting experiments, computation, and diagnostics</li>
            <li>Publications, student contributions, and research outcomes</li>
            <li>Video Summaries of Research</li>
          </ul>
        </aside>
      </div>
    </div>
    <main>
      <section>
        <div class="shell">
          <div class="section-header">
            <div><div class="section-kicker">Research Taxonomy</div><h2>Research Themes and Focus Areas</h2></div>
            <p class="section-copy">Explore the major research areas and the focused project themes within each one.</p>
          </div>
          <div class="grid-2">
            {"".join(category_cards)}
          </div>
        </div>
      </section>
    </main>
    {footer("")}
  </body>
</html>
"""
    path.write_text(html_text, encoding="utf-8")


def update_styles() -> None:
    path = WEBSITE_DIR / "styles.css"
    text = path.read_text(encoding="utf-8")
    marker = "@media (max-width: 860px) {"
    insert = """
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.research-index-card,
.research-subcard,
.research-paper-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.inner-link {
  margin-top: auto;
  align-self: flex-start;
}

.compact-links {
  display: grid;
  gap: 8px;
  margin: 0;
  padding-left: 18px;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip-link {
  display: inline-block;
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--seafoam-200);
  color: var(--navy-900);
  font-size: 0.92rem;
}

.chip-static {
  text-decoration: none;
}

.citation-list {
  margin: 0;
  padding-left: 18px;
  color: var(--ink-700);
  line-height: 1.7;
}

.paper-meta,
.meta-note,
.breadcrumb-trail {
  color: var(--ink-700);
}

.breadcrumb-trail a {
  text-decoration: underline;
  text-underline-offset: 3px;
}

.research-summary-grid .card,
.research-paper-card {
  padding: 24px;
}

.infographic-section {
  display: grid;
  gap: 24px;
}

.infographic-single {
  max-width: 980px;
  margin: 0 auto;
}

.infographic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}

.infographic-frame {
  margin: 0;
  padding: 18px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.infographic-frame a {
  display: block;
}

.infographic-frame img {
  width: 100%;
  height: auto;
  border-radius: 12px;
}

.infographic-caption {
  margin: 14px 4px 0;
  color: var(--ink-700);
  font-size: 0.95rem;
}

"""
    if ".grid-3 {" not in text:
        text = text.replace(marker, insert + marker)
    if "@media (max-width: 860px) {" in text and ".grid-3" in text:
        text = text.replace(
            "@media (max-width: 860px) {\n",
            "@media (max-width: 860px) {\n  .grid-3 {\n    grid-template-columns: 1fr;\n  }\n",
            1,
        )
    path.write_text(text, encoding="utf-8")


def write_pages() -> None:
    taxonomy = build_taxonomy()
    if RESEARCH_DIR.exists():
        shutil.rmtree(RESEARCH_DIR)
    RESEARCH_DIR.mkdir(exist_ok=True)
    paper_details = extract_paper_details(taxonomy)
    infographic_registry = build_infographic_registry(taxonomy)
    for category in ordered_categories():
        cat_slug = slugify(category)
        (RESEARCH_DIR / cat_slug).mkdir(exist_ok=True)
        (RESEARCH_DIR / f"{cat_slug}.html").write_text(category_page(category, taxonomy, paper_details), encoding="utf-8")
        for subcategory in taxonomy[category]["subcategories"]:
            sub_slug = slugify(subcategory)
            (RESEARCH_DIR / cat_slug / f"{sub_slug}.html").write_text(
                subcategory_page(category, subcategory, taxonomy, paper_details, infographic_registry),
                encoding="utf-8",
            )
    update_research_index()
    update_styles()


if __name__ == "__main__":
    write_pages()
