# 2018 Volkswagen Tiguan comma 3X build

This branch is based on StarPilot's FrogPilot-derived staging code and is intended for a supported 2018 Volkswagen Tiguan Mk2 on a comma 3X.

## Driving model

- **Regret Driven Framework (RDF), v15** is the bundled default driving model.
- The branch uses StarPilot's combined model runtime and packaged RDF artifact; it does not relabel an older split-policy model.
- Other StarPilot models remain available through the normal model selector as fallbacks.

## Branch behavior

- All audible alerts are muted, including engagement, refusal, prompts, driver-monitoring warnings, immediate warnings, controls-timeout sounds, and StarPilot event sounds. Visual alerts and normal driver-monitoring enforcement remain active.
- Lateral actuation is coupled to the vehicle cruise state. Always On Lateral is forced off by this branch.
- **Driving Confidence Ball** and **Steering Torque Limit Bar** are independent on/off options under **StarPilot Settings → Visuals → Driving Screen Widgets**. Both default on.
- The onroad driving-personality control shows the live Traffic, Aggressive, Standard, or Relaxed profile as a labeled badge.
- With openpilot longitudinal control engaged, the Tiguan's factory cruise buttons adjust the comma set speed as follows:
  - **+ / −:** 10 display-unit steps.
  - **RES / SET:** +1 / −1 display-unit steps.
  - **Cruise mode/main:** disengages comma control while engaged.
- While disengaged but the factory cruise master remains available, **+ / −** preselect a new stored comma speed. **SET** and **RES** retain their factory engage/resume behavior, and RES uses the preselected speed instead of braking toward a stale setpoint.

The torque bar visualizes normalized steering utilization. It does not raise or otherwise modify the vehicle or panda safety torque limits.

## Before driving

Verify the UI and every button behavior while parked. Perform the first road test in a low-risk environment with hands on the wheel and immediate readiness to take over. Treat this as experimental driver-assistance software, not autonomous driving. This build has no audio fallback if a visual alert is missed.
