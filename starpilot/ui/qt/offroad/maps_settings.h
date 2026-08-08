#pragma once

#include "starpilot/ui/qt/offroad/starpilot_settings.h"
#include "starpilot/ui/qt/widgets/navigation_functions.h"

class StarPilotMapsPanel : public StarPilotListWidget {
  Q_OBJECT

public:
  explicit StarPilotMapsPanel(StarPilotSettingsWindow *parent, bool forceOpen = false);

signals:
  void openSubPanel();

protected:
  void showEvent(QShowEvent *event) override;

private:
  void cancelDownload();
  void startDownload();
  void updateDownloadLabels(int downloadedFiles, int totalFiles);
  void updateState(const UIState &s, const StarPilotUIState &fs);

  bool cancellingDownload;
  bool forceOpenDescriptions;
  bool hasMapsSelected;

  ButtonControl *downloadMapsButton;
  ButtonControl *removeMapsButton;

  ButtonParamControl *preferredSchedule;

  StarPilotButtonsControl *selectMaps;

  StarPilotSettingsWindow *parent;

  LabelControl *downloadETA;
  LabelControl *downloadStatus;
  LabelControl *downloadTimeElapsed;
  LabelControl *lastMapsDownload;
  LabelControl *mapsSize;

  Params params;
  Params params_memory{"", true};

  QDateTime startTime;

  QDir mapsFolderPath{"/data/media/0/osm/offline"};

  QElapsedTimer elapsedTime;
};
