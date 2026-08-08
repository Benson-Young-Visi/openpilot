#include "tools/cabana/streams/socketcanstream.h"

#if defined(__linux__)
#include <cstring>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <unistd.h>
#endif

#include <QDebug>
#if defined(__linux__)
#include <QDir>
#include <QFile>
#endif
#include <QFormLayout>
#include <QHBoxLayout>
#include <QMessageBox>
#include <QPushButton>
#include <QThread>

SocketCanStream::SocketCanStream(QObject *parent, SocketCanStreamConfig config_) : config(config_), LiveStream(parent) {
  if (!available()) {
#if defined(__linux__)
    throw std::runtime_error("SocketCAN not available");
#else
    throw std::runtime_error("SocketCAN plugin not available");
#endif
  }

  qDebug() << "Connecting to SocketCAN device" << config.device;
  if (!connect()) {
    throw std::runtime_error("Failed to connect to SocketCAN device");
  }
}

SocketCanStream::~SocketCanStream() {
  stop();
#if defined(__linux__)
  if (sock_fd >= 0) {
    ::close(sock_fd);
    sock_fd = -1;
  }
#endif
}

bool SocketCanStream::available() {
#if defined(__linux__)
  int fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);
  if (fd < 0) return false;
  ::close(fd);
  return true;
#else
  return QCanBus::instance()->plugins().contains("socketcan");
#endif
}

bool SocketCanStream::connect() {
#if defined(__linux__)
  sock_fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);
  if (sock_fd < 0) {
    qDebug() << "Failed to create CAN socket";
    return false;
  }

  int fd_enable = 1;
  setsockopt(sock_fd, SOL_CAN_RAW, CAN_RAW_FD_FRAMES, &fd_enable, sizeof(fd_enable));

  struct ifreq ifr = {};
  strncpy(ifr.ifr_name, config.device.toStdString().c_str(), IFNAMSIZ - 1);
  if (ioctl(sock_fd, SIOCGIFINDEX, &ifr) < 0) {
    qDebug() << "Failed to get interface index for" << config.device;
    ::close(sock_fd);
    sock_fd = -1;
    return false;
  }

  struct sockaddr_can addr = {};
  addr.can_family = AF_CAN;
  addr.can_ifindex = ifr.ifr_ifindex;
  if (bind(sock_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    qDebug() << "Failed to bind CAN socket";
    ::close(sock_fd);
    sock_fd = -1;
    return false;
  }

  struct timeval tv = {.tv_sec = 0, .tv_usec = 100000};
  setsockopt(sock_fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

  return true;
#else
  // Connecting might generate warnings about missing socketcan/libsocketcan helpers.
  // Cabana only needs the basic SocketCAN plugin path.
  QString error_string;
  device.reset(QCanBus::instance()->createDevice("socketcan", config.device, &error_string));
  if (!device) {
    qDebug() << "Failed to create SocketCAN device" << error_string;
    return false;
  }

  device->setConfigurationParameter(QCanBusDevice::CanFdKey, true);
  if (!device->connectDevice()) {
    qDebug() << "Failed to connect to device";
    return false;
  }

  return true;
#endif
}

void SocketCanStream::streamThread() {
#if defined(__linux__)
  struct canfd_frame frame;
  while (!QThread::currentThread()->isInterruptionRequested()) {
    ssize_t nbytes = read(sock_fd, &frame, sizeof(frame));
    if (nbytes <= 0) continue;

    uint8_t len = (nbytes == CAN_MTU) ? frame.len : frame.len;
    MessageBuilder msg;
    auto evt = msg.initEvent();
    auto canData = evt.initCan(1);
    canData[0].setAddress(frame.can_id & CAN_EFF_MASK);
    canData[0].setSrc(0);
    canData[0].setDat(kj::arrayPtr(frame.data, len));

    handleEvent(capnp::messageToFlatArray(msg));
  }
#else
  while (!QThread::currentThread()->isInterruptionRequested()) {
    QThread::msleep(1);

    auto frames = device->readAllFrames();
    if (frames.empty()) continue;

    MessageBuilder msg;
    auto evt = msg.initEvent();
    auto can_data = evt.initCan(frames.size());

    for (uint i = 0; i < frames.size(); ++i) {
      if (!frames[i].isValid()) continue;

      can_data[i].setAddress(frames[i].frameId());
      can_data[i].setSrc(0);

      auto payload = frames[i].payload();
      can_data[i].setDat(kj::arrayPtr(reinterpret_cast<uint8_t *>(payload.data()), payload.size()));
    }

    handleEvent(capnp::messageToFlatArray(msg));
  }
#endif
}

OpenSocketCanWidget::OpenSocketCanWidget(QWidget *parent) : AbstractOpenStreamWidget(parent) {
  QVBoxLayout *main_layout = new QVBoxLayout(this);
  main_layout->addStretch(1);

  QFormLayout *form_layout = new QFormLayout();

  QHBoxLayout *device_layout = new QHBoxLayout();
  device_edit = new QComboBox();
  device_edit->setFixedWidth(300);
  device_layout->addWidget(device_edit);

  QPushButton *refresh = new QPushButton(tr("Refresh"));
  refresh->setFixedWidth(100);
  device_layout->addWidget(refresh);
  form_layout->addRow(tr("Device"), device_layout);
  main_layout->addLayout(form_layout);

  main_layout->addStretch(1);

  QObject::connect(refresh, &QPushButton::clicked, this, &OpenSocketCanWidget::refreshDevices);
  QObject::connect(device_edit, &QComboBox::currentTextChanged, this, [this] { config.device = device_edit->currentText(); });

  refreshDevices();
}

void OpenSocketCanWidget::refreshDevices() {
  device_edit->clear();
#if defined(__linux__)
  QDir net_dir("/sys/class/net");
  for (const auto &iface : net_dir.entryList(QDir::Dirs | QDir::NoDotAndDotDot)) {
    QFile type_file(net_dir.filePath(iface) + "/type");
    if (type_file.open(QIODevice::ReadOnly)) {
      int type = type_file.readAll().trimmed().toInt();
      if (type == 280) {
        device_edit->addItem(iface);
      }
    }
  }
#else
  for (const auto &device_info : QCanBus::instance()->availableDevices(QStringLiteral("socketcan"))) {
    device_edit->addItem(device_info.name());
  }
#endif
}

AbstractStream *OpenSocketCanWidget::open() {
  try {
    return new SocketCanStream(qApp, config);
  } catch (std::exception &e) {
    QMessageBox::warning(nullptr, tr("Warning"), tr("Failed to connect to SocketCAN device: '%1'").arg(e.what()));
    return nullptr;
  }
}
