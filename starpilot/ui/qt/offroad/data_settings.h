#pragma once

#include "starpilot/ui/qt/offroad/starpilot_settings.h"

class StarPilotDataPanel : public StarPilotListWidget {
  Q_OBJECT

public:
  explicit StarPilotDataPanel(StarPilotSettingsWindow *parent, bool forceOpen = false);

signals:
  void openSubPanel();

private:
  void updateStatsLabels(StarPilotListWidget *labelsList);

  bool forceOpenDescriptions;
  bool isMetric;

  StarPilotSettingsWindow *parent;

  Params params;
};
