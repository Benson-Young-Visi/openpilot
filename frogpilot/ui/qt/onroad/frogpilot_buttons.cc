#include "frogpilot/ui/qt/onroad/frogpilot_buttons.h"

namespace {
constexpr int profile_button_width = btn_size * 2 + UI_BORDER_SIZE;
}

DistanceButton::DistanceButton(QWidget *parent) : QPushButton(parent) {
  setFixedSize(profile_button_width, btn_size);

  QObject::connect(frogpilotUIState(), &FrogPilotUIState::themeUpdated, this, &DistanceButton::updateTheme);
  QObject::connect(this, &QPushButton::pressed, [this] {params_memory.putBool("OnroadDistanceButtonPressed", true);});
  QObject::connect(this, &QPushButton::released, [this] {params_memory.putBool("OnroadDistanceButtonPressed", false);});
}

void DistanceButton::showEvent(QShowEvent *event) {
  updateTheme();
}

void DistanceButton::updateTheme() {
  for (QMap<int, QPair<QPixmap, QSharedPointer<QMovie>>>::iterator it = icon_map.begin(); it != icon_map.end(); ++it) {
    QSharedPointer<QMovie> movie = it.value().second;
    if (!movie.isNull()) {
      QObject::disconnect(movie.data(), nullptr, this, nullptr);
      movie->stop();
    }
  }

  icon_map.clear();

  QPixmap traffic_img, aggressive_img, standard_img, relaxed_img;
  QSharedPointer<QMovie> traffic_gif, aggressive_gif, standard_gif, relaxed_gif;

  loadImage("../../frogpilot/assets/active_theme/distance_icons/traffic", traffic_img, traffic_gif, QSize(img_size, img_size), this);
  loadImage("../../frogpilot/assets/active_theme/distance_icons/aggressive", aggressive_img, aggressive_gif, QSize(img_size, img_size), this);
  loadImage("../../frogpilot/assets/active_theme/distance_icons/standard", standard_img, standard_gif, QSize(img_size, img_size), this);
  loadImage("../../frogpilot/assets/active_theme/distance_icons/relaxed", relaxed_img, relaxed_gif, QSize(img_size, img_size), this);

  icon_map.insert(0, qMakePair(traffic_img, traffic_gif));
  icon_map.insert(1, qMakePair(aggressive_img, aggressive_gif));
  icon_map.insert(2, qMakePair(standard_img, standard_gif));
  icon_map.insert(3, qMakePair(relaxed_img, relaxed_gif));
}

void DistanceButton::updateState(cereal::LongitudinalPersonality personality_state, bool traffic_mode_enabled) {
  const int new_personality = static_cast<int>(personality_state) + 1;
  const bool state_changed = traffic_mode_active != traffic_mode_enabled || personality != new_personality;

  if (!state_changed) {
    return;
  }

  personality = new_personality;
  traffic_mode_active = traffic_mode_enabled;

  update();
}

QColor DistanceButton::profileColor() const {
  if (traffic_mode_active) {
    return QColor(0xff, 0x5f, 0x57);
  }

  switch (personality) {
    case 1: return QColor(0xff, 0x9f, 0x43);
    case 2: return QColor(0x80, 0xd8, 0xa6);
    case 3: return QColor(0x62, 0xae, 0xef);
    default: return QColor(0xb0, 0xb0, 0xb0);
  }
}

QString DistanceButton::profileName() const {
  if (traffic_mode_active) {
    return QStringLiteral("TRAFFIC");
  }

  switch (personality) {
    case 1: return QStringLiteral("AGGRESSIVE");
    case 2: return QStringLiteral("STANDARD");
    case 3: return QStringLiteral("RELAXED");
    default: return QStringLiteral("—");
  }
}

void DistanceButton::paintEvent(QPaintEvent *event) {
  QPainter p(this);
  p.setRenderHint(QPainter::Antialiasing);

  QPair<QPixmap, QSharedPointer<QMovie>> icon = icon_map.value(traffic_mode_active ? 0 : personality);
  const QPixmap img = icon.first;
  QMovie *gif = icon.second.data();
  const QPixmap active_img = gif ? gif->currentPixmap() : img;
  const QColor color = profileColor();
  const qreal opacity = isDown() ? 0.65 : 1.0;

  p.setOpacity(opacity);
  p.setPen(QPen(color, 5));
  p.setBrush(QColor(0, 0, 0, 166));
  p.drawRoundedRect(rect().adjusted(3, 3, -3, -3), btn_size / 2, btn_size / 2);

  const QRect icon_rect(UI_BORDER_SIZE, (height() - img_size) / 2, img_size, img_size);
  p.drawPixmap(icon_rect.topLeft(), active_img);

  const int text_left = icon_rect.right() + UI_BORDER_SIZE / 2;
  const QRect text_rect(text_left, 0, width() - text_left - UI_BORDER_SIZE, height());

  p.setPen(QColor(255, 255, 255, 210));
  p.setFont(InterFont(19, QFont::DemiBold));
  p.drawText(text_rect.adjusted(0, 40, 0, 0), Qt::AlignTop | Qt::AlignHCenter, QStringLiteral("DRIVING PROFILE"));

  p.setPen(color);
  p.setFont(InterFont(30, QFont::Bold));
  p.drawText(text_rect.adjusted(0, 84, 0, 0), Qt::AlignTop | Qt::AlignHCenter, profileName());
}
