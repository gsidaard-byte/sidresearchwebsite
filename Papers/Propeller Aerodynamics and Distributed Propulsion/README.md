# Propeller Aerodynamics and Distributed Propulsion

These papers track how propeller performance changes once the rotor is installed in a real configuration. The core issue is coupling: nearby ground, ceilings, wings, neighboring rotors, pitch changes, and flight attitude all reshape the inflow and wake, so isolated-rotor assumptions quickly become incomplete.

Across the folder, the papers move from boundary-proximity effects to tandem layouts, wing-embedded propulsion, and variable-pitch control. The common thread is that wake interaction is not a side effect. It is the mechanism that determines whether a configuration loses efficiency, gains authority, or becomes predictable enough for design use.

## Methods and Tools

The set combines wind-tunnel force and moment measurements, PIV, smoke visualization, flight testing, parametric data generation, and model validation with linear superposition and related prediction approaches. Several papers pair installed-performance data with wake observations so that changes in thrust, power, or authority can be tied back to a physical flow mechanism rather than only to coefficient trends.

## Why It Matters

This category matters because distributed propulsion succeeds or fails on installation effects. The papers here help define when a simplified propeller model is good enough and when geometry, spacing, and boundary conditions must be modeled explicitly.

That has direct value for low-altitude flight, transition regimes, thrust-vectoring concepts, blown-wing aircraft, and wing-embedded propulsion systems. The folder also gives a practical bridge between experimental aerodynamics and vehicle design, since the same interactions that reduce efficiency in one layout can be exploited for useful control in another.

## Subcategories

- **Boundary-Proximity Performance** (8 papers)
  Key takeaway: Ground and ceiling proximity are first-order design variables for installed propellers, especially in low-altitude and transition-flight conditions.
- **Tandem Propeller** (3 papers)
  Key takeaway: Tandem performance depends strongly on spacing, vertical offset, and overlap, so rotor pairing must be designed as a coupled system.
- **Wing-Embedded Propulsion** (4 papers)
  Key takeaway: Embedding rotors in or near wings changes the whole system, not just the propeller, and the wing-propeller interaction can dominate performance and thrust vectoring.
- **Variable Pitch Propeller** (2 papers)
  Key takeaway: Variable pitch turns propellers into active control surfaces for off-design flight, rather than fixed actuators with one operating point.
- **Autonomous Testing** (1 paper)
  Key takeaway: Flight-test validation is essential when tandem-propeller interactions are intended for real vehicles rather than only tunnel studies.

## Papers

### Boundary-Proximity Performance

- **Changes In Propeller Performance Due to Ground Proximity** (`cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf`)
  Foundational study showing that ground proximity changes propeller performance in a measurable and configuration-dependent way.
- **Changes In Propeller Performance Due to Ground Proximity** (`PLhhwQ-cai-et-al-2019-changes-in-propeller-performance-due-to-ground-proximity.pdf`)
  Alternate export of the same 2019 ground-effect study, retained here as a separate file in the folder.
- **Propeller Partial Ground Effect** (`cai-et-al-2020-propeller-partial-ground-effect.pdf`)
  Extends the ground-effect problem into partial-ground conditions, showing that boundary effects vary continuously rather than appearing as a binary on/off phenomenon.
- **Propeller Partial Ground and Ceiling Effect Prediction** (`cai-et-al-2021-propeller-partial-ground-and-ceiling-effect-prediction.pdf`)
  Moves from measurement to prediction, which is important for design workflows that need estimates before a test campaign exists.
- **Propeller Ground Effect in Forward Flight** (`cai-gunasekaran-2023-propeller-ground-effect-in-forward-flight.pdf`)
  Shows that ground proximity remains important in forward flight, where the inflow and wake are more complex than in hover.
- **Effect of Partial Ground and Partial Ceiling on Propeller Performance** (`effect-of-partial-ground-and-partial-ceiling-on-propeller-performance.pdf`)
  Treats both lower and upper boundaries, making the installation problem more realistic for constrained test spaces and vehicle clearance limits.
- **Propeller Ground and Ceiling Effect Parametric Data** (`propeller-ground-and-ceiling-effect-parametric-data.pdf`)
  Provides supporting parametric data for installed-performance modeling and for checking prediction models against a broader design space.
- **VFS Forum 75** (`PropellerGroundandCeilingEffectinForwardFlight_Final_V4.pdf`)
  Conference-style forward-flight boundary study that reinforces the same installation lesson with a complementary presentation format.

### Tandem Propeller

- **Vertically Offset Overlapping Propellers in Tandem Configuration** (`cai-et-al-2023-vertically-offset-overlapping-propellers-in-tandem-configuration.pdf`)
  Establishes how vertical offset changes the interaction between overlapping rotors and why tandem layouts cannot be treated as independent propellers.
- **Investigation of Positively Staggered Vertically Offset Propellers in Tandem** (`cai-et-al-2024-investigation-of-positively-staggered-vertically-offset-propellers-in-tandem.pdf`)
  Refines the tandem problem by examining stagger and offset together, which is directly relevant to compact distributed-propulsion layouts.
- **Prediction of the Tandem Propeller Performance Using Linear Superposition Method** (`cai-gunasekaran-2025-prediction-of-the-tandem-propeller-performance-using-linear-superposition-method.pdf`)
  Tests whether linear superposition can predict tandem performance well enough for design use, rather than relying only on full experimental characterization.

### Wing-Embedded Propulsion

- **On the Linear Superposition of Wing and Propeller Performance in a Wing Embedded Propeller System** (`cai-et-al-2024-on-the-linear-superposition-of-wing-and-propeller-performance-in-a-wing-embedded-propeller-system.pdf`)
  Probes whether wing and propeller effects can be combined simply or whether embedding creates stronger nonlinear coupling.
- **Propeller and Propeller-in-Wing Thrust Vectoring** (`culpepper-et-al-2021-propeller-and-propeller-in-wing-thrust-vectoring.pdf`)
  Shows how embedding or partial embedding changes thrust-vectoring behavior relative to a standalone propeller.
- **Effect of Forward Propeller Tilt and Inlet Shape in Propeller-in-Wing Thrust Vectoring** (`culpepper-et-al-2022-effect-of-forward-propeller-tilt-and-inlet-shape-in-propeller-in-wing-thrust-vectoring.pdf`)
  Highlights geometry choices that matter for thrust vectoring, especially the forward tilt and inlet shaping that alter the local flow path.
- **Effect of Propeller Incidence Angle on Wing Embedded Propeller Configuration in Forward Flight** (`gogidze-et-al-2023-effect-of-propeller-incidence-angle-on-wing-embedded-propeller-configuration-in-forward-flight.pdf`)
  Extends the wing-embedded problem into forward flight, where incidence angle becomes a key driver of performance and wake structure.

### Variable Pitch Propeller

- **Experimental Investigation of a Variable Pitch Propeller at Various Incidence Angles in Foward Flight.** (`parlett-et-al-2025-experimental-investigation-of-a-variable-pitch-propeller-at-various-incidence-angles-in-foward-flight.pdf`)
  Examines how pitch scheduling changes propeller behavior as incidence varies, which is central to control authority in off-design flight.
- **Experimental Investigation of a Variable Pitch Propeller at Various Incidence Angles in Foward Flight.** (`parlett-et-al-2025v-experimental-investigation-of-a-variable-pitch-propeller-at-various-incidence-angles-in-foward-flight.pdf`)
  Alternate exported copy of the same variable-pitch study, preserved as a separate file in the folder.

### Autonomous Testing

- **Flight Test Validation of Tandem Propeller Performance With Vertical Offset** (`foster-et-al-2025-flight-test-validation-of-tandem-propeller-performance-with-vertical-offset.pdf`)
  Validates tandem-propeller behavior in flight, which is the main step from laboratory interaction studies to vehicle-relevant performance evidence.
