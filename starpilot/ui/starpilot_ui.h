#pragma once

#include "cereal/messaging/messaging.h"
#include "selfdrive/ui/qt/network/wifi_manager.h"

#include "starpilot/ui/qt/widgets/starpilot_controls.h"

struct StarPilotUIScene {
  bool always_on_lateral_active;
  bool downloading_update;
  bool enabled;
  bool starpilot_panel_active;
  bool online;
  bool parked;
  bool reverse;
  bool sidebars_open;
  bool standstill;
  bool switchback_mode_enabled;
  bool traffic_mode_enabled;
  bool wake_up_screen;

  int conditional_status;
  int driver_camera_timer;
  int started_timer;

  QJsonObject starpilot_toggles;
};

class StarPilotUIState : public QObject {
  Q_OBJECT

public:
  explicit StarPilotUIState(QObject *parent = nullptr);

  void update();

  std::unique_ptr<SubMaster> sm;

  StarPilotUIScene starpilot_scene;

  Params params;
  Params params_memory{"", true};

  WifiManager *wifi;

signals:
  void themeUpdated();
};

StarPilotUIState *starpilotUIState();
