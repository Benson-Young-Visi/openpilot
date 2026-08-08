from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from opendbc.car.gm.values import GMFlags


LOW_SPEED_MANEUVER_DESCRIPTIONS = (
  "come to stop",
  "start from stop",
  "creep: alternate between +1m/s^2 and -1m/s^2",
)


@dataclass(frozen=True)
class LongitudinalManeuverSupport:
  openpilotLongitudinalControl: bool
  fullStopAndGo: bool
  autoResumeFromStop: bool
  requiresResumeAssist: bool
  expectedToReachZero: bool
  minEnableSpeed: float
  stopAccel: float
  caveats: tuple[str, ...]
  skippedManeuvers: tuple[str, ...]

  def to_dict(self) -> dict[str, Any]:
    return asdict(self)


def get_longitudinal_maneuver_support(CP: Any) -> LongitudinalManeuverSupport:
  openpilot_longitudinal = bool(getattr(CP, "openpilotLongitudinalControl", False))
  auto_resume_supported = bool(getattr(CP, "autoResumeSng", False))

  brand = str(getattr(CP, "brand", "") or getattr(CP, "carName", "") or "").lower()
  fingerprint = str(getattr(CP, "carFingerprint", "") or "")
  flags = int(getattr(CP, "flags", 0) or 0)
  has_pedal = bool(getattr(CP, "enableGasInterceptorDEPRECATED", False))

  min_enable_speed = float(getattr(CP, "minEnableSpeed", 0.0) or 0.0)
  stop_accel = float(getattr(CP, "stopAccel", 0.0) or 0.0)

  is_gm = brand == "gm"
  is_volt = fingerprint.startswith("CHEVROLET_VOLT")
  has_sascm = is_gm and bool(flags & GMFlags.SASCM.value)

  # CarParams does not expose a dedicated "won't fully brake to zero" flag.
  # For most platforms, low-speed engagement support is the best proxy.
  full_stop_and_go = min_enable_speed <= 0.0

  # GM Volt without pedal can often engage below 0 mph but still creep instead of
  # reliably achieving a true stop in these canned maneuvers, especially on SASCM paths.
  if is_volt and not has_pedal:
    full_stop_and_go = False

  auto_resume_from_stop = full_stop_and_go and auto_resume_supported
  expected_to_reach_zero = full_stop_and_go
  requires_resume_assist = expected_to_reach_zero and not auto_resume_from_stop

  caveats: list[str] = []
  if not openpilot_longitudinal:
    caveats.append("openpilot longitudinal is disabled, so the maneuver suite cannot drive longitudinal tests on this platform.")

  if is_volt and not has_pedal:
    caveats.append("Volt without pedal is not expected to reach a true standstill in the maneuver suite. Stop, start, and creep maneuvers will be skipped.")
  elif not expected_to_reach_zero:
    caveats.append("This car is not expected to reach a true standstill in the suite. Stop, start, and creep maneuvers will be skipped.")
  elif requires_resume_assist:
    caveats.append("This car can reach a stop, but restart-from-stop needs resume assistance. Zero-speed maneuvers will allow cruise standstill instead of treating it as setup failure.")
  elif has_sascm and full_stop_and_go:
    caveats.append("SASCM is present on this GM platform. If a real standstill is reached, restart behavior can still depend on resume handling.")

  skipped_maneuvers = LOW_SPEED_MANEUVER_DESCRIPTIONS if not expected_to_reach_zero else ()

  return LongitudinalManeuverSupport(
    openpilotLongitudinalControl=openpilot_longitudinal,
    fullStopAndGo=full_stop_and_go,
    autoResumeFromStop=auto_resume_from_stop,
    requiresResumeAssist=requires_resume_assist,
    expectedToReachZero=expected_to_reach_zero,
    minEnableSpeed=min_enable_speed,
    stopAccel=stop_accel,
    caveats=tuple(caveats),
    skippedManeuvers=tuple(skipped_maneuvers),
  )


def get_maneuver_skip_reason(description: str, support: LongitudinalManeuverSupport) -> str | None:
  if not support.openpilotLongitudinalControl:
    return "openpilot longitudinal is disabled"

  if description in LOW_SPEED_MANEUVER_DESCRIPTIONS and not support.expectedToReachZero:
    return "vehicle is not expected to reach a true standstill"

  return None
