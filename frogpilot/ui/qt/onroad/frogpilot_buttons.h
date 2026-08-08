#pragma once

#include <QMovie>

#include "selfdrive/ui/qt/onroad/buttons.h"

class DistanceButton : public QPushButton {
  Q_OBJECT

public:
  explicit DistanceButton(QWidget *parent = 0);

  void updateState(cereal::LongitudinalPersonality personality_state, bool traffic_mode_enabled);

private:
  void paintEvent(QPaintEvent *event) override;
  void showEvent(QShowEvent *event) override;
  void updateTheme();

  QColor profileColor() const;
  QString profileName() const;

  bool traffic_mode_active = false;

  int personality = 2;

  Params params_memory{"/dev/shm/params"};

  QMap<int, QPair<QPixmap, QSharedPointer<QMovie>>> icon_map;
};
