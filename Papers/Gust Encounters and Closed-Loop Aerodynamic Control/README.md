# Gust Encounters and Closed-Loop Aerodynamic Control

These papers trace a focused line of inquiry into how unsteady inflow changes aerodynamic loads and how feedback can be used to shape that response. The current folder now spans propeller gust response, lift regulation, gust mitigation, and powered-wing response studies, so the theme is not just disturbance rejection but the broader problem of making aerodynamic systems predictable in unsteady air. The result is a coherent body of work on unsteady aerodynamics that is as much about sensing and actuation as it is about the flow itself.

## Methods and Tools

Closed-loop control, PID and state-feedback control, water-tunnel experiments, powered-wing testing, propeller response measurements, and TR-PIV/PIV diagnostics.

## Why It Matters

Unsteady environments are unavoidable in flight, especially for small aircraft, agile vehicles, and wings operating near stall or in disturbed atmospheres. This theme matters because it closes the loop between the disturbance, the measured flow response, and the control action needed to recover performance. That connection supports gust alleviation, better load management, and more resilient aerodynamic systems.

The collection is also notable for building its own experimental and analytical infrastructure. Several papers establish the gust generator, quantify its structure, and then reuse that disturbance field to test control laws under repeatable conditions. That progression strengthens the credibility of the results and makes the studies useful as a reference point for future work on adaptive flight control, disturbance rejection, and unsteady aerodynamic modeling. The propeller papers extend that logic to rotating propulsors, showing that unsteady inflow is not only a wing problem but a propulsion-system problem as well.

## Subcategories

- **Gust Encounters on Propellers** (3 papers)
  Key takeaway: Propeller response to gusts depends on incidence, tandem arrangement, and disturbance periodicity, so propulsion studies need their own unsteady-flow baselines.
- **Lift Regulation and Closed-Loop Gust Mitigation** (6 papers)
  Key takeaway: Closed-loop performance depends on both the control law and the repeatability of the flow input; good control studies require both.
- **Powered-Wing and Airfoil Gust Response** (2 papers)
  Key takeaway: Gust response is not just a load problem; it is a coupled flow-structure-performance problem, and quasi-steady assumptions break down as forcing becomes more dynamic.

## Papers

- **Sinusoidal Gust Response of RC Propellers in Tandem Configuration** (C3_SinusoidalGustResponseofRCPropellersinTandemConfigurationFinalV3.pdf)
  Establishes how tandem propellers respond to periodic gust forcing and how mutual interference alters the load response.
- **Sinusoidal Gust Response of RC Propellers at Different Incidence Angles** (C3_cai-et-al-2022-sinusoidal-gust-response-of-rc-propellers-at-different-incidence-angles.pdf)
  Shows how inflow angle changes the gust sensitivity of propellers and therefore the design envelope for rotating propulsion in unsteady air.
- **Wind (Aerospace Science and Technology, 2023)** (C3_wind-03-00015-v2.pdf)
  Provides the third propeller-focused study in the folder and extends the unsteady-propulsion baseline used by the other two papers.
- **Periodic Vortical Gust Encounter and Mitigation Using Closed Loop Control** (killian-et-al-2023-periodic-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf)
  Core gust-mitigation and feedback-control study that turns a disturbance into a controllable input.
- **High Amplitude Lift Tracking Using Closed-Loop Feedback and Control** (mongin-et-al-2022-high-amplitude-lift-tracking-using-closed-loop-feedback-and-control.pdf)
  Feedback-control paper focused on commanding lift beyond attached-flow limits.
- **High Amplitude Lift Tracking Using Closed-Loop Feedback and Control; A Flow Analysis** (mongin-et-al-2023-high-amplitude-lift-tracking-using-closed-loop-feedback-and-control-a-flow-analysis.pdf)
  Follow-on control paper interpreting the flow structures behind lift regulation.
- **Lift Regulation Using Closed-Loop Feedback and Control** (mongin-gunasekaran-2021-lift-regulation-using-closed-loop-feedback-and-control.pdf)
  Primary focus is active aerodynamic regulation via feedback control.
- **Discrete Vortical Gust Encounter and Mitigation Using Closed Loop Control** (porterfield-et-al-2024-discrete-vortical-gust-encounter-and-mitigation-using-closed-loop-control.pdf)
  Direct gust-encounter and mitigation study using feedback control.
- **Generation and Characterization of Discrete Vortical Gust** (porterfield-et-al-2024-generation-and-characterization-of-discrete-vortical-gust.pdf)
  Builds the gust-generation and characterization foundation for later control studies.
- **Closed-Loop Control of a Wing in Discrete Vortical Gust Encounter** (porterfield-et-al-2025-closed-loop-control-of-a-wing-in-discrete-vortical-gust-encounter.pdf)
  Control-focused continuation of the discrete-vortical-gust research thread.
- **Powered Wing Response to Periodic Gust Encounters** (duncan-et-al-2024-powered-wing-response-to-periodic-gust-encounters.pdf)
  Powered-wing gust-response paper centered on unsteady loads and performance.
- **Powered Wing's Response to Streamwise Gust Encounters** (duncan-et-al-2024-powered-wing-s-response-to-streamwise-gust-encounters.pdf)
  Gust-response study focused on the aerodynamics of a powered wing.
