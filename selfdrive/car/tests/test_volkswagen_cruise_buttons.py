from types import SimpleNamespace

import pytest

from cereal import car
from openpilot.selfdrive.car.cruise import VCruiseHelper, V_CRUISE_UNSET

ButtonEvent = car.CarState.ButtonEvent
ButtonType = car.CarState.ButtonEvent.Type


@pytest.fixture
def starpilot_toggles():
  return SimpleNamespace(
    cruise_increase=1,
    cruise_increase_long=5,
    reverse_cruise_increase=False,
    set_speed_limit=False,
  )


def make_helper(brand="volkswagen"):
  CP = car.CarParams(
    brand=brand,
    openpilotLongitudinalControl=True,
    pcmCruise=False,
  )
  return VCruiseHelper(CP)


def adjust_speed(button_type, initial_speed, toggles, enabled=True):
  helper = make_helper()
  helper.v_cruise_kph = initial_speed

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=button_type, pressed=pressed)]
    helper.update_v_cruise(CS, enabled, True, False, toggles)

  return helper.v_cruise_kph


@pytest.mark.parametrize(("button_type", "initial_speed", "expected_speed"), (
  (ButtonType.accelCruise, 50, 60),
  (ButtonType.decelCruise, 60, 50),
  (ButtonType.resumeCruise, 60, 61),
  (ButtonType.setCruise, 60, 59),
))
def test_factory_cruise_button_intervals(button_type, initial_speed, expected_speed, starpilot_toggles):
  assert adjust_speed(button_type, initial_speed, starpilot_toggles) == expected_speed


def test_factory_mapping_is_volkswagen_only(starpilot_toggles):
  helper = make_helper(brand="mock")
  helper.v_cruise_kph = 60

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=ButtonType.resumeCruise, pressed=pressed)]
    helper.update_v_cruise(CS, True, True, False, starpilot_toggles)

  assert helper.v_cruise_kph == 60


@pytest.mark.parametrize(("button_type", "initial_speed", "expected_speed"), (
  (ButtonType.accelCruise, 50, 60),
  (ButtonType.decelCruise, 60, 50),
))
def test_plus_minus_preselect_while_disengaged(button_type, initial_speed, expected_speed, starpilot_toggles):
  assert adjust_speed(button_type, initial_speed, starpilot_toggles, enabled=False) == expected_speed


@pytest.mark.parametrize("button_type", (ButtonType.resumeCruise, ButtonType.setCruise))
def test_set_resume_keep_factory_behavior_while_disengaged(button_type, starpilot_toggles):
  assert adjust_speed(button_type, 60, starpilot_toggles, enabled=False) == 60


def test_disengaged_preselection_requires_stored_speed(starpilot_toggles):
  helper = make_helper()

  for pressed in (True, False):
    CS = car.CarState(cruiseState={"available": True})
    CS.buttonEvents = [ButtonEvent(type=ButtonType.accelCruise, pressed=pressed)]
    helper.update_v_cruise(CS, False, True, False, starpilot_toggles)

  assert helper.v_cruise_kph == V_CRUISE_UNSET


def test_resume_reengages_at_preselected_speed(starpilot_toggles):
  helper = make_helper()
  helper.v_cruise_kph = 60

  for button_type in (ButtonType.accelCruise, ButtonType.resumeCruise):
    for pressed in (True, False):
      CS = car.CarState(vEgo=20, cruiseState={"available": True})
      CS.buttonEvents = [ButtonEvent(type=button_type, pressed=pressed)]
      helper.update_v_cruise(CS, False, True, False, starpilot_toggles)

  helper.initialize_v_cruise(CS, False, False, starpilot_toggles)
  assert helper.v_cruise_kph == 70
