#pragma once

#include "starpilot/ui/qt/offroad/starpilot_settings.h"

class StarPilotNavigationPanel : public StarPilotListWidget {
  Q_OBJECT

public:
  explicit StarPilotNavigationPanel(StarPilotSettingsWindow *parent, bool forceOpen = false);

signals:
  void closeSubPanel();
  void openSubPanel();

protected:
  void hideEvent(QHideEvent *event);
  void showEvent(QShowEvent *event) override;

private:
  void mousePressEvent(QMouseEvent *event);
  void updateButtons();
  void updateState(const UIState &s, const StarPilotUIState &fs);
  void updateStep();

  bool forceOpenDescriptions;
  bool mapboxPublicKeySet;
  bool mapboxSecretKeySet;
  bool updatingLimits;

  StarPilotButtonsControl *publicMapboxKeyControl;
  StarPilotButtonsControl *secretMapboxKeyControl;
  ButtonControl *setupButton;

  StarPilotButtonControl *updateSpeedLimitsToggle;

  StarPilotSettingsWindow *parent;

  LabelControl *ipLabel;

  Params params;
  Params params_memory{"", true};

  QLabel *imageLabel;

  QNetworkAccessManager *networkManager;

  QStackedLayout *primelessLayout;
};
