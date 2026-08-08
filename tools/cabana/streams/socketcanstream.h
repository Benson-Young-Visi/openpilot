#pragma once

#include <memory>

#include <QComboBox>
#if !defined(__linux__)
#include <QtSerialBus/QCanBus>
#include <QtSerialBus/QCanBusDevice>
#include <QtSerialBus/QCanBusDeviceInfo>
#endif

#include "tools/cabana/streams/livestream.h"

struct SocketCanStreamConfig {
  QString device = "";
};

class SocketCanStream : public LiveStream {
  Q_OBJECT
public:
  SocketCanStream(QObject *parent, SocketCanStreamConfig config_ = {});
  ~SocketCanStream();
  static bool available();

  inline QString routeName() const override {
    return QString("Live Streaming From Socket CAN %1").arg(config.device);
  }

protected:
  void streamThread() override;
  bool connect();

  SocketCanStreamConfig config = {};
#if defined(__linux__)
  int sock_fd = -1;
#else
  std::unique_ptr<QCanBusDevice> device;
#endif
};

class OpenSocketCanWidget : public AbstractOpenStreamWidget {
  Q_OBJECT

public:
  OpenSocketCanWidget(QWidget *parent = nullptr);
  AbstractStream *open() override;

private:
  void refreshDevices();

  QComboBox *device_edit;
  SocketCanStreamConfig config = {};
};
