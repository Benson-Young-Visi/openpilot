from types import SimpleNamespace

import pytest

from cereal import car
from openpilot.selfdrive.controls.lib.drive_helpers import VCruiseHelper

ButtonEvent = car.CarState.ButtonEvent
ButtonType = car.CarState.ButtonEvent.Type


@pytest.fixture
def frogpilot_toggles():
  return SimpleNamespace(
    conditional_experimental_mode=False,
    cruise_increase=1,
    cruise_increase_long=5,
    set_speed_limit=False,
    set_speed_offset=0,
  )


def adjust_speed(button_type, initial_speed, frogpilot_toggles, enabled=True):
  CP = car.CarParams(carName="volkswagen", openpilotLongitudinalControl=True, pcmCruise=False)
  helper = VCruiseHelper(CP)
  helper.v_cruise_kph = initial_speed

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=button_type, pressed=pressed)]
    helper.update_v_cruise(CS, enabled=enabled, is_metric=True, speed_limit_changed=False, frogpilot_toggles=frogpilot_toggles)

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


@pytest.mark.parametrize(("button_type", "initial_speed", "expected_speed"), (
  (ButtonType.accelCruise, 50, 60),
  (ButtonType.decelCruise, 60, 50),
))
def test_plus_minus_preselect_speed_while_disengaged(button_type, initial_speed, expected_speed, frogpilot_toggles):
  assert adjust_speed(button_type, initial_speed, frogpilot_toggles, enabled=False) == expected_speed


@pytest.mark.parametrize("button_type", (ButtonType.resumeCruise, ButtonType.setCruise))
def test_set_resume_keep_factory_behavior_while_disengaged(button_type, frogpilot_toggles):
  assert adjust_speed(button_type, 60, frogpilot_toggles, enabled=False) == 60


def test_disengaged_preselection_requires_stored_speed(frogpilot_toggles):
  CP = car.CarParams(carName="volkswagen", openpilotLongitudinalControl=True, pcmCruise=False)
  helper = VCruiseHelper(CP)

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=ButtonType.accelCruise, pressed=pressed)]
    helper.update_v_cruise(CS, enabled=False, is_metric=True, speed_limit_changed=False, frogpilot_toggles=frogpilot_toggles)

  assert not helper.v_cruise_initialized


def test_resume_reengages_at_preselected_speed(frogpilot_toggles):
  CP = car.CarParams(carName="volkswagen", openpilotLongitudinalControl=True, pcmCruise=False)
  helper = VCruiseHelper(CP)
  helper.v_cruise_kph = 60

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=ButtonType.accelCruise, pressed=pressed)]
    helper.update_v_cruise(CS, enabled=False, is_metric=True, speed_limit_changed=False, frogpilot_toggles=frogpilot_toggles)

  for pressed in (True, False):
    CS = car.CarState(vEgo=20, cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=ButtonType.resumeCruise, pressed=pressed)]
    helper.update_v_cruise(CS, enabled=False, is_metric=True, speed_limit_changed=False, frogpilot_toggles=frogpilot_toggles)

  helper.initialize_v_cruise(CS, experimental_mode=False, desired_speed_limit=0, frogpilot_toggles=frogpilot_toggles)
  assert helper.v_cruise_kph == 70
