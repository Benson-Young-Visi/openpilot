from cereal import log
from cereal import messaging
from cereal.messaging import SubMaster, PubMaster
from openpilot.selfdrive.ui.soundd import SELFDRIVE_STATE_TIMEOUT, check_selfdrive_timeout_alert, suppress_audible_alert

import time

AudibleAlert = log.SelfdriveState.AudibleAlert


class TestSoundd:
  def test_suppress_all_audible_alerts(self):
    assert suppress_audible_alert(AudibleAlert.engage) == AudibleAlert.none
    assert suppress_audible_alert(AudibleAlert.disengage) == AudibleAlert.none
    assert suppress_audible_alert(AudibleAlert.prompt) == AudibleAlert.none
    assert suppress_audible_alert(AudibleAlert.warningImmediate) == AudibleAlert.none

  def test_check_selfdrive_timeout_alert(self):
    sm = SubMaster(['selfdriveState'])
    pm = PubMaster(['selfdriveState'])

    for _ in range(100):
      cs = messaging.new_message('selfdriveState')
      cs.selfdriveState.enabled = True

      pm.send("selfdriveState", cs)

      time.sleep(0.01)

      sm.update(0)

      assert not check_selfdrive_timeout_alert(sm)

    for _ in range(SELFDRIVE_STATE_TIMEOUT * 110):
      sm.update(0)
      time.sleep(0.01)

    assert check_selfdrive_timeout_alert(sm)

  # TODO: add test with micd for checking that soundd actually outputs sounds
