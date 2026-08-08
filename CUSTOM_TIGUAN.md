# 2018 Volkswagen Tiguan comma 3X customizations

This branch is based on FrogPilot and is intended for a supported 2018 Volkswagen Tiguan Mk2 on a comma 3X.

## Branch behavior

- Routine engage and disengage chimes are muted. Refusal, prompt, distracted-driver, soft-warning, immediate-warning, and controls-timeout sounds remain enabled.
- Lateral actuation is allowed only when openpilot controls are active **and** the vehicle reports cruise control active. FrogPilot's Always On Lateral safety alternative is not enabled in this branch.
- **Driving Confidence Ball** can be switched on or off under **FrogPilot Settings → Visuals → Driving Screen Widgets**.
- **Steering Torque Limit Bar** can be switched on or off in the same menu.
- **Driving Personality Button** can be switched on under **FrogPilot Settings → Visuals → Driving Screen Widgets**. It shows the live **Aggressive**, **Standard**, **Relaxed**, or **Traffic** profile as both an icon and a clearly labeled, color-coded badge; the badge updates as soon as the profile changes.
- With openpilot longitudinal control engaged, the Tiguan's factory cruise buttons adjust the comma set speed as follows:
  - **+ / −:** 10 km/h steps.
  - **RES / SET:** +1 / −1 km/h steps.
  - **Cruise main:** disengages openpilot while it is engaged.
- While openpilot is disengaged but the factory cruise master remains on, **+ / −** preselect the stored comma speed in 10 km/h steps. **RES** then re-engages at that updated speed, avoiding an initial command toward the stale set speed; **RES / SET** retain their normal factory engagement behavior while disengaged.

The torque bar is a visualization of normalized steering utilization. It does not raise or otherwise modify the vehicle or panda safety torque limits.

## Before driving

Build and install the branch through the normal FrogPilot custom-fork workflow. Verify the UI and engagement behavior while parked, then perform the first road test in a low-risk environment with hands on the wheel and immediate readiness to take over.
