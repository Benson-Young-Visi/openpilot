from openpilot.selfdrive.controls.controlsd import cruise_lateral_active


def test_cruise_lateral_active():
  assert cruise_lateral_active(True, True)
  assert not cruise_lateral_active(True, False)
  assert not cruise_lateral_active(False, True)
  assert not cruise_lateral_active(False, False)
