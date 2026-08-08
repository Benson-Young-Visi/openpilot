from types import SimpleNamespace

import pytest

from cereal import car
from openpilot.selfdrive.controls.lib.drive_helpers import VCruiseHelper

ButtonEvent = car.CarState.ButtonEvent
ButtonType = car.CarState.ButtonEvent.Type


@pytest.fixture
def frogpilot_toggles():
  return SimpleNamespace(cruise_increase=1, cruise_increase_long=5, set_speed_offset=0)


def adjust_speed(button_type, initial_speed, frogpilot_toggles):
  CP = car.CarParams(carName="volkswagen", openpilotLongitudinalControl=True, pcmCruise=False)
  helper = VCruiseHelper(CP)
  helper.v_cruise_kph = initial_speed

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=button_type, pressed=pressed)]
    helper.update_v_cruise(CS, enabled=True, is_metric=True, speed_limit_changed=False, frogpilot_toggles=frogpilot_toggles)

  return helper.v_cruise_kph


@pytest.mark.parametrize(("button_type", "initial_speed", "expected_speed"), (
  (ButtonType.accelCruise, 50, 60),
  (ButtonType.decelCruise, 60, 50),
  (ButtonType.resumeCruise, 60, 61),
  (ButtonType.setCruise, 60, 59),
))
def test_factory_cruise_button_intervals(button_type, initial_speed, expected_speed, frogpilot_toggles):
  assert adjust_speed(button_type, initial_speed, frogpilot_toggles) == expected_speed


def test_factory_cruise_button_mapping_is_volkswagen_only(frogpilot_toggles):
  CP = car.CarParams(carName="mock", openpilotLongitudinalControl=True, pcmCruise=False)
  helper = VCruiseHelper(CP)
  helper.v_cruise_kph = 60

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=ButtonType.resumeCruise, pressed=pressed)]
    helper.update_v_cruise(CS, enabled=True, is_metric=True, speed_limit_changed=False, frogpilot_toggles=frogpilot_toggles)

  assert helper.v_cruise_kph == 60
