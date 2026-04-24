from __future__ import annotations

import csv
import shutil
from collections import defaultdict
from pathlib import Path

import paper_reorg


ROOT = Path("/Users/sidg/Downloads/Research Website Codex")
PAPERS_DIR = ROOT / "Papers"
METADATA_TSV = Path("/tmp/papers_metadata.tsv")


SUBCATEGORY_MAP = {
    "Propeller Aerodynamics and Distributed Propulsion": {
        "Boundary-Proximity Performance": {
            "findings": "These papers isolate how nearby ground and ceiling boundaries change propeller loading, power demand, and wake structure, especially as the rotor moves into forward-flight-like conditions rather than pure hover.",
            "value": "Their value is practical and predictive: they show exactly when isolated-propeller assumptions stop being reliable and when installation effects must be treated as part of the design problem.",
            "takeaways": "Boundary interactions are a first-order design variable for low-altitude, transition-flight, and constrained-volume propeller systems, not a small correction to baseline rotor performance.",
            "papers": [
                "PLhhwQ-cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf",
                "cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf",
                "cai-et-al-2020-propeller-partial-ground-effect.pdf",
                "cai-et-al-2021-propeller-partial-ground-and-ceiling-effect-prediction.pdf",
                "propeller-ground-and-ceiling-effect-parametric-data.pdf",
                "PropellerGroundandCeilingEffectinForwardFlight_Final_V4.pdf",
                "effect-of-partial-ground-and-partial-ceiling-on-propeller-performance.pdf",
                "cai-gunasekaran-2023-propeller-ground-effect-in-forward-flight.pdf",
            ],
        },
        "Tandem and Wing-Embedded Propulsion": {
            "findings": "This group shows how tandem spacing, vertical offset, wing embedding, and rotor-wing coupling reshape performance through wake interference and installation geometry, while also identifying cases where reduced-order superposition remains useful.",
            "value": "The value is architectural: these studies connect rotor placement and integration strategy to system-level efficiency and controllability rather than treating each propeller as an independent device.",
            "takeaways": "Distributed propulsion is fundamentally a coupling problem; rotor placement, overlap, and embedding choices can be as important as rotor design itself.",
            "papers": [
                "culpepper-et-al-2021-propeller-and-propeller-in-wing-thrust-vectoring.pdf",
                "cai-et-al-2023-vertically-offset-overlapping-propellers-in-tandem-configuration.pdf",
                "gogidze-et-al-2023-effect-of-propeller-incidence-angle-on-wing-embedded-propeller-configuration-in-forward-flight.pdf",
                "cai-et-al-2024-investigation-of-positively-staggered-vertically-offset-propellers-in-tandem.pdf",
                "cai-et-al-2024-on-the-linear-superposition-of-wing-and-propeller-performance-in-a-wing-embedded-propeller-system.pdf",
                "OntheLinearSuperpositionofWingandPropellerPerformanceinaWingEmbeddedPropellerSystem_Published.pdf",
                "cai-gunasekaran-2025-prediction-of-the-tandem-propeller-performance-using-linear-superposition-method.pdf",
                "foster-et-al-2025-flight-test-validation-of-tandem-propeller-performance-with-vertical-offset.pdf",
            ],
        },
        "Thrust Vectoring, Variable Pitch, and Unsteady Response": {
            "findings": "These papers treat propellers as controllable aerodynamic actuators, showing how tilt, inlet geometry, variable pitch, and unsteady inflow govern thrust-vectoring effectiveness and off-design response.",
            "value": "Their value is operational: they connect rotor aerodynamics directly to maneuvering authority, blown-wing behavior, and performance under gust-driven or edgewise-flight conditions.",
            "takeaways": "Propellers become far more useful in distributed-propulsion systems when their unsteady response and control authority are designed intentionally rather than inferred from steady isolated-rotor data.",
            "papers": [
                "barnhart-et-al-2021-blown-wing-aerodynamic-coefficient-predictions-using-traditional-machine-learning-and-data-science.pdf",
                "culpepper-et-al-2022-effect-of-forward-propeller-tilt-and-inlet-shape-in-propeller-in-wing-thrust-vectoring.pdf",
                "cai-et-al-2022-sinusoidal-gust-response-of-rc-propellers-at-different-incidence-angles.pdf",
                "SinusoidalGustResponseofRCPropellersinTandemConfigurationFinalV3.pdf",
                "wind-03-00015-v2.pdf",
                "parlett-et-al-2025-experimental-investigation-of-a-variable-pitch-propeller-at-various-incidence-angles-in-foward-flight.pdf",
                "parlett-et-al-2025v-experimental-investigation-of-a-variable-pitch-propeller-at-various-incidence-angles-in-foward-flight.pdf",
                "parlett-et-al-2026-experimental-investigation-of-a-variable-collective-pitch-propeller-in-near-edgewise-flight.pdf",
            ],
        },
    },
    "Morphing Wings and Lift Distribution": {
        "Morphing Camber and Actuated Control Surfaces": {
            "findings": "These papers show that reconfigurable wings can change camber, twist, and local loading without relying on a single fixed shape, often preserving or improving lift while reducing drag or delaying adverse separation.",
            "value": "The value is design flexibility: the structure itself becomes part of the flow-control strategy, enabling one wing to serve multiple aerodynamic objectives across the envelope.",
            "takeaways": "Morphing is most useful when the actuation changes the load path and wake deliberately, not when it only replaces a conventional surface with more complexity.",
            "papers": [
                "hung-et-al-2022-development-of-a-multi-purpose-flap-and-spoiler-mechanism-for-high-endurance-unmanned-aerial-vehicles.pdf",
                "gao-et-al-2024-experimental-investigation-of-a-novel-morphing-wing-design.pdf",
                "pabon-et-al-2024-experimental-investigation-of-a-novel-morphing-wing-design.pdf",
                "schreyer-et-al-2026-experimental-investigations-of-a-dual-mode-skin-actuated-camber-with-embedded-twist-(sacet).pdf",
            ],
        },
        "Distributed Lift and Multi-Wing Interactions": {
            "findings": "This set shows how nearby wings interact when lift is shared across multiple lifting surfaces, with interference, spacing, and proximity altering system performance in ways isolated-wing data cannot capture.",
            "value": "The value is system-level realism: these studies make it possible to reason about whether multi-wing and distributed-lift configurations are aerodynamically cooperative or self-defeating.",
            "takeaways": "Distributed lift is a flow-coupling problem as much as a layout problem, and wake-sharing must be designed deliberately if the concept is to deliver real efficiency gains.",
            "papers": [
                "jestus-et-al-2023-aerodynamic-characterization-of-wing-wing-interactions-for-distributed-lift-applications.pdf",
                "jestus-gunasekaran-2024-aerodynamic-interactions-among-three-identical-wings-in-close-proximity.pdf",
                "jestus-et-al-2024-proximity-effects-of-wings-on-system-performance-in-a-multi-wing-configuration.pdf",
            ],
        },
        "Spanloading and Unconventional Wing Loading": {
            "findings": "This paper treats spanwise lift distribution itself as the main design variable, showing how unconventional loading on an oblique wing changes aerodynamic behavior and downstream wake structure.",
            "value": "Its value is conceptual clarity: it provides a direct route to thinking about load redistribution, induced effects, and wake management as coupled outcomes of geometry rather than after-the-fact optimizations.",
            "takeaways": "Spanwise loading is a primary lever for controlling both performance and wake structure, not a secondary detail to be tuned late in the design process.",
            "papers": [
                "deslich-et-al-2020-effects-of-spanloading-and-slew-angle-on-an-oblique-flying-wing.pdf",
            ],
        },
    },
    "Understanding Spray Drift": {
        "Atomization Characterization and Spray Classification": {
            "findings": "These papers establish the initial droplet population through image-based atomization analysis, showing that shadowgraph data and learned classifiers can separate nozzle type and operating condition effectively.",
            "value": "Their value is methodological and applied: they show that useful spray characterization can be extracted from relatively low-cost imaging workflows rather than expensive direct droplet sizing alone.",
            "takeaways": "Spray drift management starts upstream with the nozzle and atomizer, because the initial spray structure sets the baseline that later flow can only preserve or distort.",
            "papers": [
                "6.2022-0188.pdf",
                "NAECONDeepLearningAlgorithmforAtomizationCharacterizationusingShadowgraphImages.pdf",
                "ivarson-et-al-2022-deep-learning-algorithm-for-atomization-characterization-using-shadowgraph-images.pdf",
            ],
        },
        "Propeller-Wake Spray Transport and Distortion": {
            "findings": "This group shows how an imposed propeller wake reshapes spray geometry downstream, making droplet distributions less predictable and often less uniform than atomizer-only behavior would suggest.",
            "value": "The value is immediately practical for agricultural application, because it shows that rotor-induced flow can dominate drift behavior and can also corrupt measurements if the wake is ignored.",
            "takeaways": "Spray performance cannot be evaluated in isolation when a propeller is present; the wake becomes part of the delivery system and must be treated as such.",
            "papers": [
                "grenwood-et-al-2025-characterization-of-agricultural-nozzle-spray-geometry-in-propeller-wake.pdf",
                "grenwood-et-al-2026-characterization-of-rotary-atomizer-spray-geometry-under-the-influence-of-a-propeller.pdf",
                "tierney-et-al-2023-measuring-agricultural-spray-droplet-distirbutions-in-propeller-wake-a-cautionary-tale.pdf",
            ],
        },
        "Droplet Breakup Under Extreme Forcing": {
            "findings": "This paper extends the category into fundamental multiphase breakup physics, using shock-induced forcing to isolate how droplets deform, transition, and fragment under extreme aerodynamic loading.",
            "value": "Its value is conceptual: it separates universal breakup mechanisms from geometry-specific delivery problems, which strengthens interpretation of more applied spray studies.",
            "takeaways": "Understanding drift and spray transport benefits from knowing the limiting breakup physics, not just the nozzle or vehicle configuration.",
            "papers": [
                "kastner-et-al-2026-morphological-transitions-in-droplet-breakup-under-shock-induced-flows.pdf",
            ],
        },
    },
    "Flow Diagnostics and Event-Based Sensing": {
        "Event-Camera Velocimetry and Algorithm Development": {
            "findings": "These papers move event-based flow measurement from proof-of-concept to a serious velocimetry tool by comparing algorithms, testing robustness, and showing that asynchronous sensors can recover particle motion in noisy, dense, or high-speed settings.",
            "value": "Their value is that they lower the barrier to high-temporal-resolution flow measurement and make event cameras usable where frame-based imaging struggles.",
            "takeaways": "The key challenge is no longer whether event cameras can see flow, but how to make the tracking and reconstruction reliable enough for routine aerodynamic use.",
            "papers": [
                "138800F.pdf",
                "alsattam-et-al-2024-toward-event-based-noise-robust-high-density-particle-velocimetry.pdf",
                "comparison-of-event-based-alogrithms-for-experimental-two-dimensional-two-component-velocimetry.pdf",
                "gunasekaran-et-al-2025-comparison-of-event-camera-processing-algorithms-for-experimental-2d2c-velocimetry.pdf",
                "khan-gunasekaran-2026-sensitivity-analysis-of-event-based-algorithms-for-velocimetry.pdf",
                "s00348-024-03877-y.pdf",
            ],
        },
        "Non-Contact Optical Diagnostics": {
            "findings": "This subcategory shows how non-contact diagnostics resolve flow fields where intrusive probes or ordinary imaging are inadequate, using Doppler lidar and back-imaged pressure-sensitive paint in challenging geometries.",
            "value": "The value is measurement reach: these techniques let researchers interrogate velocity or pressure signatures while preserving the flow they are trying to study.",
            "takeaways": "Alternative optical diagnostics are not just substitutes for PIV; they open access to boundary conditions and geometries that would otherwise be difficult to measure well.",
            "papers": [
                "barnhart-gunasekaran-2020-investigation-of-doppler-lidar-for-velocity-measurements-in-wind-tunnels.pdf",
                "kulig-et-al-2024-back-imaging-of-pressure-sensitive-paint-to-determine-close-proximity-ground-effects-of-propellers.pdf",
            ],
        },
        "Embedded Wake Sensing and Flow-Response Testbeds": {
            "findings": "These papers treat the sensor or testbed itself as part of the measurement system, using piezoelectric wake sensing and a cavity-flow platform to capture local flow phenomena and response dynamics.",
            "value": "Their value is that they connect sensing to actuation and experimentation in a way that supports future closed-loop systems rather than passive observation alone.",
            "takeaways": "Good flow diagnostics are increasingly embedded and interactive, because the sensing hardware and the test environment help determine how future control systems can be built.",
            "papers": [
                "aerospace-06-00033.pdf",
                "gunasekaran-et-al-2019-effect-of-flexible-inverted-pvdf-in-free-shear-layer-wake.pdf",
                "vincent-et-al-2024-development-of-an-experimental-testbed-to-study-cavity-flow-as-a-processing-element-for-flow.pdf",
            ],
        },
    },
    "Wing Aerodynamics and Wake Physics": {
        "Wake Structure and Efficiency Correlations": {
            "findings": "These papers make wake structure the primary explanatory variable for aerodynamic efficiency, showing that turbulence levels, vortex strength, and shear-layer organization often track performance changes more reliably than force coefficients alone.",
            "value": "Their value is interpretive: they turn improved or degraded aerodynamic performance into a measurable flow-physics question rather than a coefficient trend that lacks mechanism.",
            "takeaways": "Efficient wing design depends on reading the wake as a state of the airfoil or wing, not merely as a downstream consequence.",
            "papers": [
                "gunasekaran-altman-2017-better-insight-into-the-wingtip-vortex-free-shear-layer-interaction.pdf",
                "aerospace-05-00089.pdf",
                "goodman-et-al-2019-on-the-near-wake-turbulent-flow-properties-of-the-sd7003-airfoil.pdf",
                "energies-14-03641-v2.pdf",
                "gunasekaran-sharp-2021-airfoil-near-wake-turbulent-properties-at-maximum-aerodynamic-efficiency-condition.pdf",
                "loughnane-et-al-2021-effect-of-airfoil-preserved-undulations-on-free-shear-layer.pdf",
            ],
        },
        "Passive Surface Shaping and Boundary-Layer Control": {
            "findings": "These papers show how passive geometry changes redirect surface flow, weaken unwanted spanwise transport, and alter separation onset through different mechanisms such as tip-vortex feeding reduction, boundary-layer modification, and wake reshaping.",
            "value": "The value is design specificity: they show that passive control devices only work well when they target the actual transport pathway responsible for the unwanted wake behavior.",
            "takeaways": "Passive control is not a generic add-on; the geometry must be matched to the mechanism if aerodynamic gains are to be real and repeatable.",
            "papers": [
                "gunasekaran-curry-2018-effect-of-segmented-trailing-edge-extensions-in-aerodynamic-efficiency.pdf",
                "gunasekaran-gerham-2018-effect-of-chordwise-slots-on-aerodynamic-efficiency.pdf",
                "gunasekaran-thomas-2018-affecting-aerodynamic-efficiency-by-influencing-wing-surface-flow-direction.pdf",
                "preprints201807.0028.v1.pdf",
                "palmer-gunasekaran-2019-effect-of-curved-boundary-layer-fences-on-aerodynamic-efficiency.pdf",
                "loughnane-et-al-2020-effect-of-airfoil-preserved-undulations-on-wing-performance.pdf",
            ],
        },
        "Off-Design, Iced, and Actively Forced Wings": {
            "findings": "This subcategory captures wings pushed away from benign baseline behavior through icing, dynamic pitching, or blown jets, showing that off-design conditions change the flow topology rather than merely shifting the force coefficients.",
            "value": "Its value is operational realism: it extends wake-based aerodynamic reasoning into regimes where stall, separation, actuation, and contamination matter directly.",
            "takeaways": "Once geometry, actuation, or contamination changes the local flow regime, wake-aware analysis becomes essential because aerodynamic behavior is much less predictable from baseline trends.",
            "papers": [
                "insana-gunasekaran-2022-low-reynolds-number-experimental-aerodynamic-verification-of-scaled-and-lewice-simulated-ice.pdf",
                "pabon-gunasekaran-2026-experimental-investigation-of-dynamic-pitching-effects-on-a-delta-wing-with-blown-jet.pdf",
            ],
        },
    },
    "Wake Characteristics of Bell-Shaped Lift Distribution": {
        "Prandtl-D3 and D3C Wake Characterization": {
            "findings": "These papers provide direct experimental evidence that Prandtl-D3-family loading changes the wake structurally, weakening, displacing, or altering the persistence of the conventional wingtip vortex rather than simply scaling it with lift.",
            "value": "Their value is experimental legitimacy for an induced-drag-control idea that is often discussed conceptually but is much stronger when observed directly in the near wake.",
            "takeaways": "Prandtl-D3 and D3C are not only loading strategies; they are wake-shaping strategies with measurable near-field consequences.",
            "papers": [
                "pabon-et-al-2025-experimental-investigation-of-prandtl-d3-near-wake-signature.pdf",
                "cain-et-al-2026-cross-stream-piv-characterization-of-the-prandtl-d3c-wake.pdf",
            ],
        },
        "Bell-Shaped and Non-Elliptical Lift Evolution": {
            "findings": "These papers broaden the story from a named configuration to the underlying spanwise-loading principle, showing that changing lift distribution alters where circulation rolls up and how the near wake evolves toward the far wake.",
            "value": "The value is conceptual generality: they show that the relevant variable is not just planform or total lift, but how lift is distributed across the span.",
            "takeaways": "Wake control can be approached by shaping the lift profile first, with tip-vortex suppression and induced-drag management emerging as direct consequences of that choice.",
            "papers": [
                "schreyer-et-al-2025-variations-in-the-wake-structure-of-non-elliptical-lift-distributions-near-wingtip.pdf",
                "cain-gunasekaran-2026-wake-characteristics-of-a-bell-shaped-lift-distribution.pdf",
            ],
        },
    },
    "Gust Encounters and Closed-Loop Aerodynamic Control": {
        "Lift Regulation and Closed-Loop Gust Mitigation": {
            "findings": "This subcategory shows that lift can be regulated well beyond attached-flow limits if the controller is designed around disturbance physics, progressing from basic lift tracking to explicit gust-mitigation studies.",
            "value": "Its value is practical: the papers provide a usable blueprint for gust alleviation, stall-delay strategies, and feedback architectures that remain meaningful in strongly unsteady flow.",
            "takeaways": "Closed-loop performance depends on both the control law and the repeatability of the flow input; good control studies require both.",
            "papers": [
                "mongin-gunasekaran-2021-lift-regulation-using-closed-loop-feedback-and-control.pdf",
                "mongin-et-al-2022-high-amplitude-lift-tracking-using-closed-loop-feedback-and-control.pdf",
                "mongin-et-al-2023-high-amplitude-lift-tracking-using-closed-loop-feedback-and-control-a-flow-analysis.pdf",
                "killian-et-al-2023-periodic-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf",
                "porterfield-et-al-2024-discrete-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf",
                "porterfield-et-al-2025-closed-loop-control-of-a-wing-in-discrete-vortical-gust-encounter.pdf",
            ],
        },
        "Gust Generator Design and Disturbance Characterization": {
            "findings": "This paper treats the disturbance field itself as an experimental object by generating and characterizing discrete vortical gusts with a repeatable signature.",
            "value": "Its value is methodological: it gives later mitigation and control studies a reusable benchmark instead of an uncontrolled inflow event.",
            "takeaways": "Good gust research requires a known disturbance signature before mitigation results can be interpreted with confidence.",
            "papers": [
                "porterfield-et-al-2024-generation-and-characterization-of-discrete-vortical-gust.pdf",
            ],
        },
        "Powered-Wing and Airfoil Gust Response": {
            "findings": "These papers show how wings and airfoils respond when the disturbance is not yet being actively canceled, with response depending strongly on gust type, frequency, and operating state.",
            "value": "Their value is in defining the uncontrolled aerodynamic baseline that later control systems must outperform or exploit.",
            "takeaways": "Gust response is not just a load problem; it is a coupled flow-structure-performance problem, and quasi-steady assumptions break down as forcing becomes more dynamic.",
            "papers": [
                "duncan-et-al-2024-powered-wing-s-response-to-streamwise-gust-encounters.pdf",
                "duncan-et-al-2024-powered-wing-response-to-periodic-gust-encounters.pdf",
                "durgesh-et-al-2026-impact-of-gusts-on-performance-of-naca-0012-airfoil-at-low-re.pdf",
            ],
        },
    },
    "Experimental Platforms and Cross-Domain Fluid Systems": {
        "Experimental Facilities and Instrumentation": {
            "findings": "These papers treat the tunnel, jet, and measurement environment as part of the scientific result rather than background plumbing, showing that platform fidelity, frequency response, and manufacturability shape what aerodynamics can be trusted downstream.",
            "value": "Their value is foundational: once the facility is characterized, every later result gains a more credible experimental base.",
            "takeaways": "Building and validating the instrumented environment is itself a fluid-dynamics research contribution, not just setup work.",
            "papers": [
                "gazella-et-al-2020-design-and-analysis-of-an-additive-manufactured-supersonic-wind-tunnel.pdf",
                "cook-et-al-2020-frequency-response-of-a-shuttered-open-jet-wind-tunnel.pdf",
            ],
        },
        "Lensed Turbines": {
            "findings": "These papers transfer aerodynamic tools into wind-energy and turbomachinery settings, showing that wake interactions and proximity effects can be quantified with the same experimental mindset used for wings and propellers.",
            "value": "Their value is generalization: aircraft-flow methods remain useful in adjacent fluid systems when the goal is to understand how wakes bias power, mixing, and losses.",
            "takeaways": "Aerodynamic wake physics is portable across domains, and the same measurement logic can reveal performance mechanisms in very different geometries.",
            "papers": [
                "novotny-gunasekaran-2020-performance-and-proximity-investigations-on-small-scale-lensed-turbines.pdf",
                "donovan-et-al-2022-analysis-of-high-lift-low-pressure-turbine-endwall-vortices-using-modal-decomposition-methods.pdf",
                "peyton-gunasekaran-2022-investigation-into-wake-interactions-of-wind-lenses-at-close-proximities.pdf",
                "energies-15-04622.pdf",
            ],
        },
    },
    "Engineering Education and Entrepreneurial Learning": {
        "Teaching and Pedagogical Infrastructure": {
            "findings": "This work shows that understanding in aerodynamics improves when teaching is redesigned to connect equations, physical intuition, and real flow behavior more directly.",
            "value": "Its value is human infrastructure: stronger pedagogy helps develop researchers and engineers who can reason more clearly about fluid-dynamics problems.",
            "takeaways": "Education is part of the research ecosystem, especially in a field where insight depends on both mathematical analysis and physical intuition.",
            "papers": [
                "integrated-teaching-model-in-graduate-aerospace-classes-a-trial-with-compressible-flow-aerodynamics.pdf",
                "integrated-teaching-model-a-follow-up-with-fundamental-aerodynamics.pdf",
            ],
        },
    },
}


def load_metadata() -> dict[str, dict[str, str]]:
    metadata: dict[str, dict[str, str]] = {}
    if not METADATA_TSV.exists():
        return metadata
    with METADATA_TSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter="\t")
        for row in reader:
            rel, title, snippet = (row + ["", ""])[:3]
            metadata[Path(rel).name] = {"title": title.strip(), "snippet": snippet.strip()}
    return metadata


def slug(name: str) -> str:
    return name.replace("/", "-")


def contribution_for_file(filename: str, metadata: dict[str, dict[str, str]]) -> str:
    rel = next(k for k in paper_reorg.PAPER_MAP if Path(k).name == filename)
    item = paper_reorg.PAPER_MAP[rel]
    meta = metadata.get(filename, {})
    title = meta.get("title") or Path(filename).stem
    return paper_reorg.contribution_sentence(title, meta.get("snippet", ""), item["rationale"], item["notes"])


def write_subcategory_readme(category: str, subcategory: str, info: dict, metadata: dict[str, dict[str, str]]) -> None:
    subdir = PAPERS_DIR / category / subcategory
    lines = [
        f"# {subcategory}",
        "",
        f"Parent category: **{category}**",
        "",
        "## Important Findings",
        "",
        info["findings"],
        "",
        "## Value",
        "",
        info["value"],
        "",
        "## Key Takeaways",
        "",
        info["takeaways"],
        "",
        "## Papers",
        "",
    ]
    for filename in sorted(info["papers"], key=str.lower):
        title = metadata.get(filename, {}).get("title") or Path(filename).stem
        if title.lower().startswith("abstract "):
            title = Path(filename).stem
        lines.append(f"- **{title}** ({filename})")
        lines.append(f"  {contribution_for_file(filename, metadata)}")
    (subdir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_category_readme(category: str) -> None:
    path = PAPERS_DIR / category / "README.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines = []
    skipping = False
    inserted = False
    for line in lines:
        if line == "## Subcategories":
            skipping = True
            continue
        if skipping and line == "## Papers":
            skipping = False
        if skipping:
            continue
        if line == "## Papers" and not inserted:
            new_lines.extend([
                "## Subcategories",
                "",
            ])
            for subcategory, info in SUBCATEGORY_MAP[category].items():
                count = len(info["papers"])
                new_lines.append(f"- **{subcategory}** ({count} papers)")
                new_lines.append(f"  Key takeaway: {info['takeaways']}")
            new_lines.extend(["", "## Papers"])
            inserted = True
            continue
        new_lines.append(line)
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def apply() -> None:
    metadata = load_metadata()
    expected = set()
    for category, subcats in SUBCATEGORY_MAP.items():
        for subcategory, info in subcats.items():
            subdir = PAPERS_DIR / category / subcategory
            subdir.mkdir(exist_ok=True)
            for filename in info["papers"]:
                expected.add(filename)
                src = PAPERS_DIR / category / filename
                dest = subdir / filename
                if src.exists():
                    shutil.move(str(src), str(dest))
                elif not dest.exists():
                    raise FileNotFoundError(f"Missing paper for move: {src}")
            write_subcategory_readme(category, subcategory, info, metadata)
        update_category_readme(category)

    existing = {p.name for p in PAPERS_DIR.rglob("*.pdf")}
    if expected != existing:
        missing = sorted(expected - existing)
        extra = sorted(existing - expected)
        raise SystemExit(f"Mismatch after move. Missing={missing} Extra={extra}")

    print("Applied subcategory reorganization.")
    for category, subcats in SUBCATEGORY_MAP.items():
        print(f"{category}: {len(subcats)} subcategories")


if __name__ == "__main__":
    apply()
