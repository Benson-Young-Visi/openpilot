#pragma once

#include "starpilot/ui/qt/offroad/starpilot_settings.h"

class StarPilotWheelPanel : public StarPilotListWidget {
  Q_OBJECT

public:
  explicit StarPilotWheelPanel(StarPilotSettingsWindow *parent, bool forceOpen = false);

protected:
  void showEvent(QShowEvent *event) override;

private:
  void updateToggles();

  bool forceOpenDescriptions;

  std::map<QString, AbstractControl*> toggles;

  StarPilotSettingsWindow *parent;

  Params params;
};
