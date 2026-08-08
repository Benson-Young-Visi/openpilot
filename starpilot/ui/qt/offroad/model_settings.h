#pragma once

#include <set>

#include "starpilot/ui/qt/offroad/starpilot_settings.h"

class StarPilotModelPanel : public StarPilotListWidget {
  Q_OBJECT

public:
  explicit StarPilotModelPanel(StarPilotSettingsWindow *parent);

signals:
  void openSubPanel();

protected:
  void showEvent(QShowEvent *event) override;

private:
  void updateModelLabels(StarPilotListWidget *labelsList);
  void updateState(const UIState &s, const StarPilotUIState &fs);
  void updateToggles();
  bool isModelInstalled(const QString &key) const;
  QMap<QString, QString> getDeletableModelDisplayNames();

  bool allModelsDownloaded;
  bool allModelsDownloading;
  bool cancellingDownload;
  bool finalizingDownload;
  bool forceOpenDescriptions;
  bool modelDownloading;
  bool noModelsDownloaded;
  bool started;
  bool tinygradUpdate;
  bool updatingTinygrad;

  int tuningLevel;

  std::map<QString, AbstractControl*> toggles;

  ButtonControl *selectModelButton;

  StarPilotButtonsControl *deleteModelButton;
  StarPilotButtonsControl *downloadModelButton;
  StarPilotButtonsControl *updateTinygradButton;

  StarPilotSettingsWindow *parent;

  Params params;
  Params params_memory{"", true};

  QDir modelDir{"/data/models/"};

  QJsonObject starpilotToggleLevels;

  QMap<QString, QString> modelFileToNameMap;
  QMap<QString, QString> modelFileToNameMapProcessed;
  QMap<QString, QString> modelReleasedDates;
  QMap<QString, QString> modelSeriesMap;

  QString currentModel;


  QStringList availableModelNames;
  QStringList availableModelSeries;
};
