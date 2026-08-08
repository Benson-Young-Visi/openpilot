import threading
import time

from openpilot.common.params import Params
from openpilot.system.athena import athenad


class TestAthenadMain:
  def setup_method(self):
    self.default_params = {
      "DongleId": "0000000000000000",
      "AthenadUploadQueue": [],
    }

    self.params = Params()
    for k, v in self.default_params.items():
      self.params.put(k, v)

  def test_main_waits_for_dongle_id(self, mocker):
    self.params.remove("DongleId")

    mock_create_connection = mocker.patch("openpilot.system.athena.athenad.create_connection")
    exit_event = threading.Event()
    thread = threading.Thread(target=athenad.main, args=(exit_event,))
    thread.start()

    try:
      time.sleep(0.2)
      mock_create_connection.assert_not_called()
      assert thread.is_alive()
    finally:
      exit_event.set()
      thread.join(5)

    assert not thread.is_alive()
