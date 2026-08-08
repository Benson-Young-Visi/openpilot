from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def update(self, CC, CS, now_nanos, starpilot_toggles):
    return CC.actuators.as_builder(), []
