from __future__ import annotations

import csv
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/Users/sidg/Downloads/Research Website Codex")
PAPERS_DIR = ROOT / "Papers"
METADATA_TSV = Path("/tmp/papers_metadata.tsv")


CATEGORY_ORDER = [
    "Propeller Aerodynamics and Distributed Propulsion",
    "Morphing Wings and Lift Distribution",
    "Understanding Spray Drift",
    "Flow Diagnostics and Event-Based Sensing",
    "Wing Aerodynamics and Wake Physics",
    "Wake Characteristics of Bell-Shaped Lift Distribution",
    "Gust Encounters and Closed-Loop Aerodynamic Control",
    "Experimental Platforms and Cross-Domain Fluid Systems",
    "Engineering Education and Entrepreneurial Learning",
]


CATEGORY_SUMMARIES = {
    "Propeller Aerodynamics and Distributed Propulsion": {
        "summary": (
            "This research examines how propeller performance changes once a rotor operates in a real "
            "aircraft configuration rather than in isolation. Ground and ceiling proximity, nearby "
            "wings and rotors, pitch changes, and flight attitude all reshape the inflow and wake, "
            "often in ways that strongly affect efficiency and controllability. Across these studies, "
            "wake interaction is treated not as a secondary effect, but as a central design variable "
            "in distributed propulsion systems."
        ),
        "methods": (
            "The work combines wind-tunnel force and moment measurements, smoke visualization, "
            "particle image velocimetry, pressure-sensitive paint, forward-flight testing, and "
            "full vehicle validation. It also includes reduced-order prediction methods, parametric "
            "correlations, and data-driven models aimed at connecting installed propeller behavior "
            "to practical aircraft design decisions."
        ),
        "importance": (
            "This theme matters because distributed propulsion systems rise or fall on installation "
            "effects rather than isolated-propeller performance alone. Once a rotor begins operating "
            "near a surface, another rotor, or an integrated lifting surface, the inflow changes in "
            "ways that can affect thrust, efficiency, controllability, and usable flight envelope. "
            "Understanding those interactions improves performance prediction, power budgeting, "
            "control authority, and the practical design of multirotors, blown wings, and "
            "propeller-in-wing aircraft."
        ),
    },
    "Morphing Wings and Lift Distribution": {
        "summary": (
            "This research explores how aerodynamic performance changes when lift is deliberately "
            "redistributed across a wing or across multiple lifting surfaces. The work spans morphing "
            "concepts, spanloading studies, and multi-wing configurations, with emphasis on how lift "
            "distribution shapes wake structure, induced drag, control authority, and overall system "
            "performance. Together, these papers show that changing where lift is produced can be just "
            "as important as changing how much lift is produced."
        ),
        "methods": (
            "The work combines force-balance testing, morphing-wing prototyping, comparative "
            "wind-tunnel studies, numerical aerodynamic analysis, and systematic interaction "
            "experiments across multi-wing configurations. These methods are used to connect "
            "geometry change and wing placement to spanwise loading, wake structure, induced drag, "
            "and control response."
        ),
        "importance": (
            "This theme matters because efficient aircraft are shaped not only by how much lift they "
            "produce, but by where and how that lift is distributed. Morphing surfaces, spanloading "
            "strategies, and multi-wing arrangements offer new ways to manage induced drag, "
            "stability, compactness, and low-speed performance. That is especially important for UAVs "
            "and unconventional aircraft concepts, where footprint, adaptability, and aerodynamic "
            "efficiency must often be balanced simultaneously."
        ),
    },
    "Understanding Spray Drift": {
        "summary": (
            "This research studies how sprays form, deform, and disperse in complex aerodynamic "
            "environments. The work connects droplet generation, propeller-wake interaction, and "
            "transport physics to build a clearer picture of how drift develops and how it can be "
            "measured. Taken together, these papers link fundamental multiphase flow behavior to "
            "practical questions in agricultural spray applications."
        ),
        "methods": (
            "The work uses shadowgraph imaging, spray patternation, controlled nozzle and atomizer "
            "experiments, propeller-wake transport studies, and data-driven interpretation using "
            "convolutional neural networks. Together, these methods connect droplet formation, spray "
            "geometry, breakup behavior, and transport physics under realistic application conditions."
        ),
        "importance": (
            "This theme matters because spray drift is fundamentally a multiphase fluid-dynamics "
            "problem with practical agricultural consequences. Better characterization of droplet "
            "size, plume shape, breakup, and transport improves application precision, helps reduce "
            "off-target deposition, and supports more efficient chemical use. The research also "
            "strengthens the measurement tools needed to evaluate how real aerodynamic environments "
            "reshape sprays after atomization."
        ),
    },
    "Flow Diagnostics and Event-Based Sensing": {
        "summary": (
            "This research focuses on new ways to measure and reconstruct complex flow fields, "
            "especially when the flow is highly unsteady or difficult to capture with conventional "
            "tools. The work spans event-based cameras, optical diagnostics, embedded sensing, and "
            "algorithm development aimed at improving temporal resolution, spatial fidelity, and "
            "measurement robustness. Together, these studies advance both the instrumentation and the "
            "analysis methods needed for modern experimental fluid mechanics."
        ),
        "methods": (
            "The work spans event cameras, Kalman-filter-based particle tracking, experimental 2D2C "
            "velocimetry, Doppler lidar, pressure-sensitive paint, piezoelectric wake sensors, and "
            "dedicated sensing testbeds. Just as important, it includes algorithm development, "
            "sensitivity analysis, and validation experiments that connect new instruments to "
            "interpretable flow measurements."
        ),
        "importance": (
            "This theme matters because progress in fluid dynamics depends on better measurements, "
            "not only better theories. These studies expand what can be measured, how quickly it can "
            "be measured, and how sensing can be embedded into future flow-aware and flow-control "
            "systems. That makes the work valuable both as instrumentation development and as a way "
            "to open difficult, highly unsteady flows to more reliable experimental analysis."
        ),
    },
    "Wing Aerodynamics and Wake Physics": {
        "summary": (
            "This research examines how wings generate, reshape, and shed vorticity under a wide range "
            "of passive and active modifications. Geometry changes, surface treatments, icing, "
            "blowing, and boundary-layer control are used to connect local flow physics to lift, "
            "drag, stall behavior, and aerodynamic efficiency. Across the category, wake structure is "
            "treated as a key window into aerodynamic performance rather than just a downstream consequence."
        ),
        "methods": (
            "The work uses particle image velocimetry, wake interrogation, force-based testing, flow "
            "visualization, icing verification experiments, and active-flow-control studies on wings "
            "and delta-wing configurations. These methods are used to connect local flow structure, "
            "separation, vorticity, and wake evolution to measurable changes in aerodynamic "
            "efficiency and controllability."
        ),
        "importance": (
            "This theme matters because aerodynamic performance is easier to improve when the flow "
            "mechanisms behind that performance are clearly understood. By treating the wake as a "
            "diagnostic window into lift, drag, separation, and vortex behavior, the research helps "
            "explain why efficiency changes, not just that it changes. That perspective is useful for "
            "designing passive devices, validating models, and guiding active-flow-control concepts."
        ),
    },
    "Wake Characteristics of Bell-Shaped Lift Distribution": {
        "summary": (
            "This research focuses on how spanwise lift distribution changes the structure of the wake, "
            "especially near the wingtip. The papers examine bell-shaped and other non-elliptical "
            "loading strategies and show how load shaping can redistribute circulation, weaken "
            "conventional tip vortices, and alter the evolution of the near wake. Together, they "
            "provide an experimental view of wake control as a pathway toward lower induced drag and "
            "more efficient lifting-surface design."
        ),
        "methods": (
            "The work combines cross-stream and streamwise particle image velocimetry, near-wake "
            "measurements, load-distribution-driven wing design, and comparisons across angle of "
            "attack and wing geometry. These methods are used to observe how bell-shaped and other "
            "non-elliptical loadings alter circulation placement, vortex formation, and near-wake "
            "structure."
        ),
        "importance": (
            "This theme matters because bell-shaped loading offers a physically different way to think "
            "about induced drag and wake control. Instead of treating the wingtip vortex as an "
            "inevitable outcome to be managed afterward, the work asks how lift distribution can "
            "reshape the wake from the outset. These studies make that idea experimentally legible and "
            "connect spanwise loading directly to vortex formation and aerodynamic efficiency."
        ),
    },
    "Gust Encounters and Closed-Loop Aerodynamic Control": {
        "summary": (
            "This research investigates how aerodynamic systems respond to unsteady inflow and how "
            "sensing and feedback can be used to shape that response. The work spans gust encounters "
            "on propellers, lift regulation, powered-wing response, and closed-loop mitigation "
            "strategies aimed at improving predictability in disturbed flow environments. Taken "
            "together, these studies connect unsteady aerodynamics with control, actuation, and "
            "system-level resilience."
        ),
        "methods": (
            "The work combines closed-loop control, PID and state-feedback methods, gust-generation "
            "experiments, powered-wing and propeller testing, time-resolved PIV, and supporting "
            "modeling tools such as unsteady panel methods and modal analysis. Together, these "
            "methods link unsteady flow structures to aerodynamic response and control action."
        ),
        "importance": (
            "This theme matters because unsteady environments are unavoidable in flight. Gusts, wake "
            "encounters, and rapidly changing inflow conditions affect both aerodynamic loads and the "
            "ability to control a vehicle. By linking flow structures, measured loads, and feedback "
            "control in the same research program, the work supports gust alleviation, agile "
            "maneuvering, and more resilient aerodynamic systems."
        ),
    },
    "Experimental Platforms and Cross-Domain Fluid Systems": {
        "summary": (
            "This research highlights the experimental platforms, teaching tools, and cross-domain "
            "applications that support and extend fluid-dynamics work. The papers span wind-tunnel "
            "development, additive-manufactured facilities, wind-energy studies, and pedagogical "
            "models for aerodynamics education. Together, they show that research capability is built "
            "not only through technical results, but also through the facilities, methods, and "
            "educational infrastructure that make those results possible."
        ),
        "methods": (
            "The work includes wind-tunnel design, additive manufacturing, hot-wire anemometry, PIV, "
            "modal decomposition, wake diagnostics, and cross-domain experimental studies in both "
            "aerodynamic and energy-related systems. These methods are used not only to study flows, "
            "but also to create and validate the facilities and platforms that make those studies possible."
        ),
        "importance": (
            "This theme matters because fluid-dynamics progress depends on good facilities, "
            "interpretable experiments, and the ability to transfer ideas across domains. Research "
            "capability is built not only through findings, but through the tunnels, instrumentation, "
            "platforms, and experimental methods that make reliable findings possible. These studies "
            "extend the reach of the work beyond a single aircraft-configuration problem and into the "
            "infrastructure of research itself."
        ),
    },
    "Engineering Education and Entrepreneurial Learning": {
        "summary": (
            "This research highlights the experimental platforms, teaching tools, and cross-domain "
            "applications that support and extend fluid-dynamics work. The papers span wind-tunnel "
            "development, additive-manufactured facilities, wind-energy studies, and pedagogical "
            "models for aerodynamics education. Together, they show that research capability is built "
            "not only through technical results, but also through the facilities, methods, and "
            "educational infrastructure that make those results possible."
        ),
        "methods": (
            "The work combines course design, experiential learning models, classroom-based "
            "assessment, context-rich instruction, reflective portfolios, and entrepreneurial-mindset "
            "development. These methods are used to connect analytical rigor, physical intuition, "
            "hands-on learning, and long-term ownership of engineering ideas."
        ),
        "importance": (
            "This theme matters because engineering progress depends not only on discoveries, but also "
            "on how effectively new engineers learn to reason, design, communicate, and create. "
            "Treating teaching as a scholarly activity makes educational infrastructure visible as "
            "part of the broader research mission, especially in areas such as aerodynamics, AI in "
            "education, and entrepreneurial-minded learning."
        ),
    },
}


PAPER_MAP = {
    "Papers/2017/integrated-teaching-model-in-graduate-aerospace-classes-a-trial-with-compressible-flow-aerodynamics.pdf": {
        "category": "Engineering Education and Entrepreneurial Learning",
        "themes": "graduate aerodynamics pedagogy, context-rich learning design",
        "rationale": "Pedagogy paper on teaching compressible-flow aerodynamics rather than a primary flow-physics study.",
        "notes": "",
    },
    "Papers/2017/gunasekaran-altman-2017-better-insight-into-the-wingtip-vortex-free-shear-layer-interaction.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "wingtip vortex, free shear layer, aerodynamic efficiency",
        "rationale": "Directly studies wake interactions that explain wing aerodynamic efficiency.",
        "notes": "",
    },
    "Papers/2018/gunasekaran-curry-2018-effect-of-segmented-trailing-edge-extensions-in-aerodynamic-efficiency.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "segmented trailing edge, drag reduction, wake structure",
        "rationale": "Passive wing modification tied to aerodynamic efficiency and wake behavior.",
        "notes": "",
    },
    "Papers/2018/integrated-teaching-model-a-follow-up-with-fundamental-aerodynamics.pdf": {
        "category": "Engineering Education and Entrepreneurial Learning",
        "themes": "fundamental aerodynamics education, experiential learning",
        "rationale": "Education-focused paper documenting an aerodynamics teaching model.",
        "notes": "",
    },
    "Papers/2018/preprints201807.0028.v1.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "surface contours, wingtip vortex, PIV wake analysis",
        "rationale": "Examines how wing-surface contours alter vortex formation and wake signatures.",
        "notes": "",
    },
    "Papers/2018/gunasekaran-gerham-2018-effect-of-chordwise-slots-on-aerodynamic-efficiency.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "chordwise slots, lift-drag behavior, passive flow control",
        "rationale": "Wing-surface geometry study focused on aerodynamic performance mechanisms.",
        "notes": "",
    },
    "Papers/2018/aerospace-05-00089.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "wake properties, segmented trailing edge extensions, turbulence",
        "rationale": "Wake-focused journal version on segmented trailing-edge extensions.",
        "notes": "",
    },
    "Papers/2018/gunasekaran-thomas-2018-affecting-aerodynamic-efficiency-by-influencing-wing-surface-flow-direction.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "surface-flow direction, aerodynamic efficiency, wing modification",
        "rationale": "Targets wing efficiency by manipulating near-surface flow and resulting wake behavior.",
        "notes": "",
    },
    "Papers/2019/cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "propeller ground effect, proximity, performance variation",
        "rationale": "Core propeller-installation study on how ground proximity changes performance.",
        "notes": "",
    },
    "Papers/2019/gunasekaran-et-al-2019-effect-of-flexible-inverted-pvdf-in-free-shear-layer-wake.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "piezoelectric wake sensing, energy harvesting, free shear layer",
        "rationale": "Primary contribution is sensing the wake with a piezo-embedded inverted flag.",
        "notes": "Secondary relevance: Wing Aerodynamics and Wake Physics.",
    },
    "Papers/2019/palmer-gunasekaran-2019-effect-of-curved-boundary-layer-fences-on-aerodynamic-efficiency.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "boundary layer fences, stall behavior, aerodynamic efficiency",
        "rationale": "Wing-focused passive-flow-control study tied to efficiency and separation behavior.",
        "notes": "",
    },
    "Papers/2019/goodman-et-al-2019-on-the-near-wake-turbulent-flow-properties-of-the-sd7003-airfoil.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "SD7003 airfoil, near wake turbulence, efficiency condition",
        "rationale": "Uses wake turbulence to interrogate efficient airfoil operating conditions.",
        "notes": "",
    },
    "Papers/2019/aerospace-06-00033.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "inverted flag sensor, wake sensing, piezoelectric response",
        "rationale": "Sensor-centric journal paper on extracting wake information from a piezo-embedded flag.",
        "notes": "Secondary relevance: Wing Aerodynamics and Wake Physics.",
    },
    "Papers/2019/PLhhwQ-cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "propeller ground effect, duplicate record, proximity performance",
        "rationale": "Same propeller-ground-effect topic as the cleaner 2019 copy.",
        "notes": "Likely duplicate/alternate export of the same paper.",
    },
    "Papers/2020/novotny-gunasekaran-2020-performance-and-proximity-investigations-on-small-scale-lensed-turbines.pdf": {
        "category": "Experimental Platforms and Cross-Domain Fluid Systems",
        "themes": "lensed turbines, rotor proximity, wind-energy aerodynamics",
        "rationale": "Cross-domain rotor-flow study focused on wind-energy lens effects rather than aircraft propulsion.",
        "notes": "",
    },
    "Papers/2020/deslich-et-al-2020-effects-of-spanloading-and-slew-angle-on-an-oblique-flying-wing.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "spanloading, oblique wing, lift distribution, slew angle",
        "rationale": "Centered on spanwise loading and unconventional wing-load distribution.",
        "notes": "",
    },
    "Papers/2020/gazella-et-al-2020-design-and-analysis-of-an-additive-manufactured-supersonic-wind-tunnel.pdf": {
        "category": "Experimental Platforms and Cross-Domain Fluid Systems",
        "themes": "supersonic wind tunnel, additive manufacturing, facility design",
        "rationale": "Primary contribution is a fluid-dynamics experimental platform.",
        "notes": "",
    },
    "Papers/2020/barnhart-gunasekaran-2020-investigation-of-doppler-lidar-for-velocity-measurements-in-wind-tunnels.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "doppler lidar, wind tunnel velocimetry, measurement methods",
        "rationale": "Diagnostics paper evaluating lidar as a flow-measurement tool.",
        "notes": "",
    },
    "Papers/2020/cook-et-al-2020-frequency-response-of-a-shuttered-open-jet-wind-tunnel.pdf": {
        "category": "Experimental Platforms and Cross-Domain Fluid Systems",
        "themes": "open-jet tunnel, shuttering system, gust-generation infrastructure",
        "rationale": "Primarily characterizes the experimental platform used to create unsteady flow inputs.",
        "notes": "Secondary relevance: Gust Encounters and Closed-Loop Aerodynamic Control.",
    },
    "Papers/2020/loughnane-et-al-2020-effect-of-airfoil-preserved-undulations-on-wing-performance.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "airfoil-preserved undulations, wing performance, tubercle-inspired geometry",
        "rationale": "Wing-performance study using passive geometric undulations to alter aerodynamic behavior.",
        "notes": "",
    },
    "Papers/2020/cai-et-al-2020-propeller-partial-ground-effect.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "partial ground effect, propeller installation, close-proximity rotor flow",
        "rationale": "Foundational propeller proximity study relevant to installed distributed propulsion.",
        "notes": "",
    },
    "Papers/2021/mongin-gunasekaran-2021-lift-regulation-using-closed-loop-feedback-and-control.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "closed-loop lift control, feedback, dynamic stall regime",
        "rationale": "Primary focus is active aerodynamic regulation via feedback control.",
        "notes": "",
    },
    "Papers/2021/culpepper-et-al-2021-propeller-and-propeller-in-wing-thrust-vectoring.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "thrust vectoring, propeller-in-wing, distributed propulsion integration",
        "rationale": "Directly studies propeller and propeller-in-wing thrust-vectoring performance.",
        "notes": "",
    },
    "Papers/2021/NAECONDeepLearningAlgorithmforAtomizationCharacterizationusingShadowgraphImages.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "atomization classification, shadowgraph imaging, spray diagnostics",
        "rationale": "Spray-focused paper using image-based learning to infer atomization state.",
        "notes": "Likely earlier conference version of the 2022 AIAA paper.",
    },
    "Papers/2021/loughnane-et-al-2021-effect-of-airfoil-preserved-undulations-on-free-shear-layer.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "free shear layer, preserved undulations, wake turbulence",
        "rationale": "Looks past forces to quantify how undulated wings reshape the wake.",
        "notes": "",
    },
    "Papers/2021/energies-14-03641-v2.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "far wake, aerodynamic efficiency, wake-based performance inference",
        "rationale": "Wake-centered study relating downstream flow signatures to aerodynamic efficiency.",
        "notes": "",
    },
    "Papers/2021/cai-et-al-2021-propeller-partial-ground-and-ceiling-effect-prediction.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "ground and ceiling effect, propeller prediction, installed rotor flow",
        "rationale": "Prediction-oriented propeller installation study for nearby boundaries.",
        "notes": "",
    },
    "Papers/2021/gunasekaran-sharp-2021-airfoil-near-wake-turbulent-properties-at-maximum-aerodynamic-efficiency-condition.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "near wake turbulence, maximum efficiency, airfoil flow physics",
        "rationale": "Examines wake conditions associated with peak aerodynamic efficiency.",
        "notes": "",
    },
    "Papers/2021/barnhart-et-al-2021-blown-wing-aerodynamic-coefficient-predictions-using-traditional-machine-learning-and-data-science.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "blown wing, aerodynamic prediction, machine learning, propulsion-airframe coupling",
        "rationale": "Coupled blown-wing prediction study aligned with distributed-propulsion design.",
        "notes": "Secondary relevance: Flow Diagnostics and Event-Based Sensing.",
    },
    "Papers/2021/propeller-ground-and-ceiling-effect-parametric-data.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "parametric dataset, ground effect, ceiling effect, propellers",
        "rationale": "Propeller proximity dataset supporting prediction and installed-performance studies.",
        "notes": "",
    },
    "Papers/2022/culpepper-et-al-2022-effect-of-forward-propeller-tilt-and-inlet-shape-in-propeller-in-wing-thrust-vectoring.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "forward tilt, inlet shape, propeller-in-wing thrust vectoring",
        "rationale": "Installed propeller study on geometry changes that alter thrust-vectoring behavior.",
        "notes": "",
    },
    "Papers/2022/ivarson-et-al-2022-deep-learning-algorithm-for-atomization-characterization-using-shadowgraph-images.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "deep learning, atomization characterization, shadowgraph spray images",
        "rationale": "Spray-atomization classification study using image-based inference.",
        "notes": "",
    },
    "Papers/2022/donovan-et-al-2022-analysis-of-high-lift-low-pressure-turbine-endwall-vortices-using-modal-decomposition-methods.pdf": {
        "category": "Experimental Platforms and Cross-Domain Fluid Systems",
        "themes": "turbine endwall vortices, modal decomposition, turbomachinery flow",
        "rationale": "Cross-domain vortex-analysis paper centered on turbine flow structures.",
        "notes": "",
    },
    "Papers/2022/insana-gunasekaran-2022-low-reynolds-number-experimental-aerodynamic-verification-of-scaled-and-lewice-simulated-ice.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "icing effects, low Reynolds number, aerodynamic verification",
        "rationale": "Wing/aerofoil performance study under iced geometries rather than a platform or sensing paper.",
        "notes": "",
    },
    "Papers/2022/cai-et-al-2022-sinusoidal-gust-response-of-rc-propellers-at-different-incidence-angles.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "unsteady propeller response, sinusoidal gusts, incidence angle",
        "rationale": "Propeller-response study whose primary object is propeller performance in unsteady inflow.",
        "notes": "Secondary relevance: Gust Encounters and Closed-Loop Aerodynamic Control.",
    },
    "Papers/2022/peyton-gunasekaran-2022-investigation-into-wake-interactions-of-wind-lenses-at-close-proximities.pdf": {
        "category": "Experimental Platforms and Cross-Domain Fluid Systems",
        "themes": "wind lenses, wake interactions, close-proximity rotor systems",
        "rationale": "Cross-domain wind-energy application focused on wake interactions between lens profiles.",
        "notes": "",
    },
    "Papers/2022/mongin-et-al-2022-high-amplitude-lift-tracking-using-closed-loop-feedback-and-control.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "lift tracking, closed-loop control, post-stall regulation",
        "rationale": "Feedback-control paper focused on commanding lift beyond attached flow.",
        "notes": "",
    },
    "Papers/2022/6.2022-0188.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "atomization characterization, shadowgraph images, spray-learning duplicate",
        "rationale": "Same atomization-classification study as the explicitly named 2022 file.",
        "notes": "Likely duplicate/alternate export of the same paper.",
    },
    "Papers/2022/PropellerGroundandCeilingEffectinForwardFlight_Final_V4.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "forward-flight propeller proximity, ground effect, ceiling effect",
        "rationale": "Propeller-installation study extending boundary-proximity effects into forward flight.",
        "notes": "",
    },
    "Papers/2022/energies-15-04622.pdf": {
        "category": "Experimental Platforms and Cross-Domain Fluid Systems",
        "themes": "wind lenses, wake interactions, wind-energy performance bias",
        "rationale": "Journal paper on wind-lens interaction physics in a wind-energy setting.",
        "notes": "",
    },
    "Papers/2022/hung-et-al-2022-development-of-a-multi-purpose-flap-and-spoiler-mechanism-for-high-endurance-unmanned-aerial-vehicles.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "flap-spoiler mechanism, UAV high endurance, adaptive lifting surfaces",
        "rationale": "Wing-mechanism paper that changes lift and drag behavior through movable geometry.",
        "notes": "",
    },
    "Papers/2023/cai-et-al-2023-vertically-offset-overlapping-propellers-in-tandem-configuration.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "tandem propellers, vertical offset, wake interference",
        "rationale": "Direct tandem-propeller interaction study for distributed-propulsion layouts.",
        "notes": "",
    },
    "Papers/2023/mongin-et-al-2023-high-amplitude-lift-tracking-using-closed-loop-feedback-and-control-a-flow-analysis.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "lift tracking, closed-loop control, flow analysis",
        "rationale": "Follow-on control paper interpreting the flow structures behind lift regulation.",
        "notes": "",
    },
    "Papers/2023/SinusoidalGustResponseofRCPropellersinTandemConfigurationFinalV3.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "tandem propellers, sinusoidal gusts, unsteady installed performance",
        "rationale": "Propeller-centric study of tandem response under unsteady inflow.",
        "notes": "Secondary relevance: Gust Encounters and Closed-Loop Aerodynamic Control.",
    },
    "Papers/2023/jestus-et-al-2023-aerodynamic-characterization-of-wing-wing-interactions-for-distributed-lift-applications.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "wing-wing interactions, distributed lift, multi-wing aerodynamics",
        "rationale": "Directly tied to distributed-lift load-sharing and multi-wing aerodynamic interaction.",
        "notes": "",
    },
    "Papers/2023/effect-of-partial-ground-and-partial-ceiling-on-propeller-performance.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "partial ground effect, partial ceiling effect, propeller performance",
        "rationale": "Boundary-proximity propeller study with immediate installation relevance.",
        "notes": "",
    },
    "Papers/2023/wind-03-00015-v2.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "streamwise gusts, RC propellers, forward flight response",
        "rationale": "Unsteady-inflow study whose main target remains propeller performance prediction.",
        "notes": "Secondary relevance: Gust Encounters and Closed-Loop Aerodynamic Control.",
    },
    "Papers/2023/killian-et-al-2023-periodic-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "periodic vortical gusts, mitigation, closed-loop control",
        "rationale": "Core gust-mitigation and feedback-control study.",
        "notes": "",
    },
    "Papers/2023/cai-gunasekaran-2023-propeller-ground-effect-in-forward-flight.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "forward flight, propeller ground effect, installed rotor aerodynamics",
        "rationale": "Propeller-in-forward-flight ground-effect paper with direct design relevance.",
        "notes": "",
    },
    "Papers/2023/duncan-et-al-2024-powered-wing-response-to-periodic-gust-encounters.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "powered wing, periodic gusts, unsteady response",
        "rationale": "Powered-wing gust-response paper centered on unsteady loads and performance.",
        "notes": "",
    },
    "Papers/2023/porterfield-et-al-2024-generation-and-characterization-of-discrete-vortical-gust.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "discrete vortical gusts, generation method, characterization",
        "rationale": "Builds the gust-generation and characterization foundation for later control studies.",
        "notes": "",
    },
    "Papers/2023/gogidze-et-al-2023-effect-of-propeller-incidence-angle-on-wing-embedded-propeller-configuration-in-forward-flight.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "wing-embedded propeller, incidence angle, forward flight",
        "rationale": "Installed wing-embedded propeller study central to distributed-propulsion integration.",
        "notes": "",
    },
    "Papers/2023/tierney-et-al-2023-measuring-agricultural-spray-droplet-distirbutions-in-propeller-wake-a-cautionary-tale.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "agricultural spray, droplet distribution, propeller wake",
        "rationale": "Directly addresses droplet behavior and measurement challenges in propeller-induced flow.",
        "notes": "",
    },
    "Papers/2023/jestus-gunasekaran-2024-aerodynamic-interactions-among-three-identical-wings-in-close-proximity.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "three-wing interactions, close proximity, distributed lift",
        "rationale": "Multi-wing interaction study concerned with spanwise load sharing and interference.",
        "notes": "",
    },
    "Papers/2023/gao-et-al-2024-experimental-investigation-of-a-novel-morphing-wing-design.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "morphing wing, skin-actuated camber, experimental design",
        "rationale": "Morphing-wing study focused on camber-changing lifting-surface design.",
        "notes": "Likely alternate/earlier version of the 2024 morphing-wing paper.",
    },
    "Papers/2024/jestus-et-al-2024-proximity-effects-of-wings-on-system-performance-in-a-multi-wing-configuration.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "multi-wing configuration, proximity effects, system performance",
        "rationale": "Distributed-lift paper on how neighboring wings reshape system-level performance.",
        "notes": "",
    },
    "Papers/2024/kulig-et-al-2024-back-imaging-of-pressure-sensitive-paint-to-determine-close-proximity-ground-effects-of-propellers.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "pressure-sensitive paint, back-imaging, propeller ground effect",
        "rationale": "Primary novelty is the diagnostic method used to resolve propeller ground-effect flow.",
        "notes": "Secondary relevance: Propeller Aerodynamics and Distributed Propulsion.",
    },
    "Papers/2024/s00348-024-03877-y.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "event-based PIV, Kalman filtering, particle event velocimetry",
        "rationale": "Method paper advancing event-camera velocimetry.",
        "notes": "",
    },
    "Papers/2024/pabon-et-al-2024-experimental-investigation-of-a-novel-morphing-wing-design.pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "morphing wing, skin-actuated camber, experimental and numerical study",
        "rationale": "Core morphing-wing paper linking geometry change to aerodynamic performance.",
        "notes": "",
    },
    "Papers/2024/cai-et-al-2024-investigation-of-positively-staggered-vertically-offset-propellers-in-tandem.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "positively staggered propellers, tandem interaction, vertical offset",
        "rationale": "Distributed-propulsion configuration study on tandem rotor placement.",
        "notes": "",
    },
    "Papers/2024/alsattam-et-al-2024-toward-event-based-noise-robust-high-density-particle-velocimetry.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "event-based velocimetry, noise robustness, dense particle fields",
        "rationale": "Directly advances event-based flow-diagnostic algorithms for challenging measurements.",
        "notes": "",
    },
    "Papers/2024/duncan-et-al-2024-powered-wing-s-response-to-streamwise-gust-encounters.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "powered wing, streamwise gusts, unsteady aerodynamic response",
        "rationale": "Gust-response study focused on the aerodynamics of a powered wing.",
        "notes": "",
    },
    "Papers/2024/vincent-et-al-2024-development-of-an-experimental-testbed-to-study-cavity-flow-as-a-processing-element-for-flow.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "cavity flow, sensing testbed, flow disturbances, processing element",
        "rationale": "Builds a sensing-and-response experimental platform for local flow phenomena.",
        "notes": "Secondary relevance: Gust Encounters and Closed-Loop Aerodynamic Control.",
    },
    "Papers/2024/porterfield-et-al-2024-discrete-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "discrete vortical gust, mitigation, closed-loop response",
        "rationale": "Direct gust-encounter and mitigation study using feedback control.",
        "notes": "",
    },
    "Papers/2024/cai-et-al-2024-on-the-linear-superposition-of-wing-and-propeller-performance-in-a-wing-embedded-propeller-system.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "wing-embedded propeller, linear superposition, installed performance",
        "rationale": "Installed wing-propeller interaction study for distributed-propulsion modeling.",
        "notes": "",
    },
    "Papers/2024/OntheLinearSuperpositionofWingandPropellerPerformanceinaWingEmbeddedPropellerSystem_Published.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "wing-embedded propeller, linear superposition, published duplicate",
        "rationale": "Published copy of the wing-embedded propeller superposition study.",
        "notes": "Likely duplicate/alternate export of the same paper.",
    },
    "Papers/2025/schreyer-et-al-2025-variations-in-the-wake-structure-of-non-elliptical-lift-distributions-near-wingtip.pdf": {
        "category": "Wake Characteristics of Bell-Shaped Lift Distribution",
        "themes": "non-elliptical loading, wingtip wake, bell-shaped trends",
        "rationale": "Explicitly investigates wake structure induced by non-elliptical lift distributions.",
        "notes": "",
    },
    "Papers/2025/porterfield-et-al-2025-closed-loop-control-of-a-wing-in-discrete-vortical-gust-encounter.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "discrete gust, wing control, closed-loop mitigation",
        "rationale": "Control-focused continuation of the discrete-vortical-gust research thread.",
        "notes": "",
    },
    "Papers/2025/cai-gunasekaran-2025-prediction-of-the-tandem-propeller-performance-using-linear-superposition-method.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "tandem propellers, linear superposition, performance prediction",
        "rationale": "Modeling paper for tandem-propeller performance in distributed layouts.",
        "notes": "",
    },
    "Papers/2025/grenwood-et-al-2025-characterization-of-agricultural-nozzle-spray-geometry-in-propeller-wake.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "agricultural nozzle, spray geometry, propeller wake distortion",
        "rationale": "Spray-propeller interaction study directly tied to drift-relevant geometry changes.",
        "notes": "",
    },
    "Papers/2025/foster-et-al-2025-flight-test-validation-of-tandem-propeller-performance-with-vertical-offset.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "flight validation, tandem propellers, vertical offset performance",
        "rationale": "Validates distributed-propulsion interaction findings in flight rather than only in the tunnel.",
        "notes": "",
    },
    "Papers/2025/parlett-et-al-2025-experimental-investigation-of-a-variable-pitch-propeller-at-various-incidence-angles-in-foward-flight.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "variable-pitch propeller, incidence, forward flight performance",
        "rationale": "Propeller-aerodynamics paper on variable-pitch behavior under installed forward-flight conditions.",
        "notes": "",
    },
    "Papers/2025/parlett-et-al-2025v-experimental-investigation-of-a-variable-pitch-propeller-at-various-incidence-angles-in-foward-flight.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "variable-pitch propeller, incidence, alternate file version",
        "rationale": "Same variable-pitch forward-flight study in an alternate exported file.",
        "notes": "Likely duplicate/alternate export of the same paper.",
    },
    "Papers/2025/pabon-et-al-2025-experimental-investigation-of-prandtl-d3-near-wake-signature.pdf": {
        "category": "Wake Characteristics of Bell-Shaped Lift Distribution",
        "themes": "Prandtl-D3, near wake, tip-vortex suppression",
        "rationale": "Directly probes the near-wake signature of a Prandtl-D3 configuration.",
        "notes": "",
    },
    "Papers/2025/gunasekaran-et-al-2025-comparison-of-event-camera-processing-algorithms-for-experimental-2d2c-velocimetry.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "event-camera processing, 2D2C velocimetry, algorithm comparison",
        "rationale": "Method-comparison paper advancing event-camera flow diagnostics.",
        "notes": "",
    },
    "Papers/2026/khan-gunasekaran-2026-sensitivity-analysis-of-event-based-algorithms-for-velocimetry.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "event-based velocimetry, algorithm sensitivity, parameter robustness",
        "rationale": "Algorithm-sensitivity study for event-based flow measurement.",
        "notes": "",
    },
    "Papers/2026/cain-et-al-2026-cross-stream-piv-characterization-of-the-prandtl-d3c-wake.pdf": {
        "category": "Wake Characteristics of Bell-Shaped Lift Distribution",
        "themes": "Prandtl-D3C wake, cross-stream PIV, bell-shaped loading",
        "rationale": "Measures the wake topology tied to Prandtl-D3C lift distribution.",
        "notes": "",
    },
    "Papers/2026/pabon-gunasekaran-2026-experimental-investigation-of-dynamic-pitching-effects-on-a-delta-wing-with-blown-jet.pdf": {
        "category": "Wing Aerodynamics and Wake Physics",
        "themes": "delta wing, blown jet, dynamic pitching, active flow control",
        "rationale": "Primary contribution is wing-flow physics under dynamic pitching with blowing.",
        "notes": "Secondary relevance: Gust Encounters and Closed-Loop Aerodynamic Control.",
    },
    "Papers/2026/schreyer-et-al-2026-experimental-investigations-of-a-dual-mode-skin-actuated-camber-with-embedded-twist-(sacet).pdf": {
        "category": "Morphing Wings and Lift Distribution",
        "themes": "morphing wing, embedded twist, bell-shaped loading target",
        "rationale": "Morphing-wing mechanism paper designed to realize targeted lift distributions.",
        "notes": "Secondary relevance: Wake Characteristics of Bell-Shaped Lift Distribution.",
    },
    "Papers/2026/durgesh-et-al-2026-impact-of-gusts-on-performance-of-naca-0012-airfoil-at-low-re.pdf": {
        "category": "Gust Encounters and Closed-Loop Aerodynamic Control",
        "themes": "gust loads, NACA 0012, low Reynolds number response",
        "rationale": "Airfoil study centered on performance changes caused by gust encounters.",
        "notes": "",
    },
    "Papers/2026/parlett-et-al-2026-experimental-investigation-of-a-variable-collective-pitch-propeller-in-near-edgewise-flight.pdf": {
        "category": "Propeller Aerodynamics and Distributed Propulsion",
        "themes": "collective-pitch propeller, edgewise flight, variable incidence performance",
        "rationale": "Installed propeller-aerodynamics paper on collective-pitch behavior in near-edgewise flight.",
        "notes": "",
    },
    "Papers/2026/cain-gunasekaran-2026-wake-characteristics-of-a-bell-shaped-lift-distribution.pdf": {
        "category": "Wake Characteristics of Bell-Shaped Lift Distribution",
        "themes": "bell-shaped lift distribution, wake structure, cross-stream PIV",
        "rationale": "Flagship paper for the bell-shaped-lift wake category.",
        "notes": "",
    },
    "Papers/2026/grenwood-et-al-2026-characterization-of-rotary-atomizer-spray-geometry-under-the-influence-of-a-propeller.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "rotary atomizer, spray geometry, propeller influence",
        "rationale": "Spray-geometry paper studying how propeller-induced flow alters atomized output.",
        "notes": "",
    },
    "Papers/2026/138800F.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "event-based PIV, manufacturing flow, optical diagnostics",
        "rationale": "Abstract indicates an event-based velocimetry application for manufacturing flow fields.",
        "notes": "Opaque filename; classified from extracted abstract text.",
    },
    "Papers/2026/comparison-of-event-based-alogrithms-for-experimental-two-dimensional-two-component-velocimetry.pdf": {
        "category": "Flow Diagnostics and Event-Based Sensing",
        "themes": "event-based algorithms, experimental velocimetry, journal version",
        "rationale": "Journal version of the event-based velocimetry algorithm comparison work.",
        "notes": "Likely expanded journal version of the 2025 conference paper.",
    },
    "Papers/2026/kastner-et-al-2026-morphological-transitions-in-droplet-breakup-under-shock-induced-flows.pdf": {
        "category": "Understanding Spray Drift",
        "themes": "droplet breakup, shock-induced flow, breakup morphology",
        "rationale": "Broader droplet-physics study that still centers on breakup morphology relevant to spray behavior.",
        "notes": "",
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
            metadata[rel] = {"title": title.strip(), "snippet": snippet.strip()}
    return metadata


def list_papers() -> list[str]:
    return sorted(str(path.relative_to(ROOT)).replace("\\", "/") for path in PAPERS_DIR.rglob("*") if path.is_file() and path.suffix.lower() in {".pdf", ".doc", ".docx", ".tex", ".rtf"})


def extract_methods(snippet: str) -> str:
    text = snippet.lower()
    methods = []
    key_methods = [
        ("particle image velocimetry", "PIV"),
        ("tr-piv", "TR-PIV"),
        ("event-based", "event-based sensing"),
        ("event camera", "event cameras"),
        ("kalman", "Kalman-filter tracking"),
        ("shadowgraph", "shadowgraph imaging"),
        ("convolution neural network", "CNN-based classification"),
        ("machine learning", "machine-learning prediction"),
        ("flightstream", "FlightStream simulations"),
        ("wind tunnel", "wind-tunnel testing"),
        ("water tunnel", "water-tunnel testing"),
        ("smoke", "smoke visualization"),
        ("pressure-sensitive paint", "pressure-sensitive paint"),
        ("lidar", "Doppler lidar"),
        ("hotwire", "hot-wire anemometry"),
        ("flight test", "flight testing"),
        ("modal decomposition", "modal decomposition"),
        ("patternator", "spray patternator measurements"),
        ("shock", "shock-tube experiments"),
        ("closed-loop", "closed-loop control"),
        ("state-feedback", "state-feedback control"),
        ("pid", "PID control"),
    ]
    for needle, label in key_methods:
        if needle in text and label not in methods:
            methods.append(label)
    return ", ".join(methods[:3])


def contribution_sentence(title: str, snippet: str, rationale: str, notes: str) -> str:
    sentence = rationale.strip()
    if sentence and sentence[-1] not in ".!?":
        sentence += "."
    methods = extract_methods(snippet)
    if methods:
        sentence += f" Methods/tools: {methods}."
    return sentence


def ensure_collision_safe_path(dest_dir: Path, filename: str, rel_path: str, title: str) -> Path:
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    year_match = re.search(r"(19|20)\d{2}", rel_path)
    if year_match:
        year_candidate = dest_dir / f"{stem} ({year_match.group(0)}){suffix}"
        if not year_candidate.exists():
            return year_candidate
    short_title = re.sub(r"[^A-Za-z0-9]+", " ", title).strip().split()
    short = " ".join(short_title[:4]) if short_title else "Alt"
    short_candidate = dest_dir / f"{stem} ({short}){suffix}"
    if not short_candidate.exists():
        return short_candidate
    i = 2
    while True:
        numbered = dest_dir / f"{stem} ({i}){suffix}"
        if not numbered.exists():
            return numbered
        i += 1


def dry_run() -> str:
    files = list_papers()
    missing = [f for f in files if f not in PAPER_MAP]
    extra = [f for f in PAPER_MAP if f not in files]
    if missing or extra:
        raise SystemExit(f"Mapping mismatch. Missing={missing} Extra={extra}")

    lines = ["Dry-Run Plan", ""]
    for category in CATEGORY_ORDER:
        lines.append(f"{category}")
        for rel in [f for f in files if PAPER_MAP[f]["category"] == category]:
            item = PAPER_MAP[rel]
            note = f" | Notes: {item['notes']}" if item["notes"] else ""
            lines.append(f"- {Path(rel).name} -> {category}: {item['rationale']}{note}")
        lines.append("")

    collisions = defaultdict(list)
    for rel in files:
        collisions[(PAPER_MAP[rel]["category"], Path(rel).name)].append(rel)
    collision_lines = []
    for (category, name), rels in sorted(collisions.items()):
        if len(rels) > 1:
            collision_lines.append(f"- {category}: {name} from {len(rels)} sources")
    if collision_lines:
        lines.append("Potential filename collisions")
        lines.extend(collision_lines)
    else:
        lines.append("Potential filename collisions")
        lines.append("- None detected from current basenames; duplicate-like papers remain distinct because filenames differ.")
    return "\n".join(lines)


def write_readmes(metadata: dict[str, dict[str, str]], moved: dict[str, Path]) -> None:
    by_category = defaultdict(list)
    for rel, item in PAPER_MAP.items():
        by_category[item["category"]].append(rel)

    for category in CATEGORY_ORDER:
        info = CATEGORY_SUMMARIES[category]
        lines = [f"# {category}", "", info["summary"], "", "## Methods and Tools", "", info["methods"], "", "## Why It Matters", "", info["importance"], "", "## Papers", ""]
        for rel in sorted(by_category[category], key=lambda p: Path(p).name.lower()):
            meta = metadata.get(rel, {})
            title = meta.get("title") or Path(rel).stem
            if title.lower().startswith("abstract "):
                title = Path(rel).stem
            item = PAPER_MAP[rel]
            contribution = contribution_sentence(title, meta.get("snippet", ""), item["rationale"], item["notes"])
            lines.append(f"- **{title}** ({Path(rel).name})")
            lines.append(f"  {contribution}")
        (PAPERS_DIR / category / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_catalog() -> None:
    lines = [
        "# Papers Catalog",
        "",
        "| Filename | Category | Key themes (5-10 words) | 1-sentence rationale |",
        "| --- | --- | --- | --- |",
    ]
    for rel in sorted(PAPER_MAP, key=lambda p: (PAPER_MAP[p]["category"], Path(p).name.lower())):
        item = PAPER_MAP[rel]
        lines.append(
            f"| {Path(rel).name} | {item['category']} | {item['themes']} | {item['rationale']} |"
        )
    (PAPERS_DIR / "00_Catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply() -> None:
    metadata = load_metadata()
    files = list_papers()
    missing = [f for f in files if f not in PAPER_MAP]
    extra = [f for f in PAPER_MAP if f not in files]
    if missing or extra:
        raise SystemExit(f"Mapping mismatch. Missing={missing} Extra={extra}")

    for category in CATEGORY_ORDER:
        (PAPERS_DIR / category).mkdir(exist_ok=True)

    moved: dict[str, Path] = {}
    for rel in files:
        src = ROOT / rel
        item = PAPER_MAP[rel]
        title = metadata.get(rel, {}).get("title", Path(rel).stem)
        dest_dir = PAPERS_DIR / item["category"]
        dest = ensure_collision_safe_path(dest_dir, src.name, rel, title)
        if src.resolve() != dest.resolve():
            shutil.move(str(src), str(dest))
        moved[rel] = dest

    write_readmes(metadata, moved)
    write_catalog()

    for path in sorted(PAPERS_DIR.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()) and path.name not in CATEGORY_ORDER:
            path.rmdir()

    counts = Counter(item["category"] for item in PAPER_MAP.values())
    print("Applied reorganization.")
    for category in CATEGORY_ORDER:
        print(f"{category}: {counts[category]}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or sys.argv[1] not in {"dry-run", "apply"}:
        raise SystemExit("Usage: paper_reorg.py [dry-run|apply]")
    if sys.argv[1] == "dry-run":
        print(dry_run())
    else:
        apply()
