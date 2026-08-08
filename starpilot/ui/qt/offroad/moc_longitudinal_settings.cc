/****************************************************************************
** Meta object code from reading C++ file 'longitudinal_settings.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.12.8)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "longitudinal_settings.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'longitudinal_settings.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.12.8. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_StarPilotLongitudinalPanel_t {
    QByteArrayData data[5];
    char stringdata0[76];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_StarPilotLongitudinalPanel_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_StarPilotLongitudinalPanel_t qt_meta_stringdata_StarPilotLongitudinalPanel = {
    {
QT_MOC_LITERAL(0, 0, 26), // "StarPilotLongitudinalPanel"
QT_MOC_LITERAL(1, 27, 12), // "openSubPanel"
QT_MOC_LITERAL(2, 40, 0), // ""
QT_MOC_LITERAL(3, 41, 15), // "openSubSubPanel"
QT_MOC_LITERAL(4, 57, 18) // "openSubSubSubPanel"

    },
    "StarPilotLongitudinalPanel\0openSubPanel\0"
    "\0openSubSubPanel\0openSubSubSubPanel"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_StarPilotLongitudinalPanel[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       3,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   29,    2, 0x06 /* Public */,
       3,    0,   30,    2, 0x06 /* Public */,
       4,    0,   31,    2, 0x06 /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void StarPilotLongitudinalPanel::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<StarPilotLongitudinalPanel *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->openSubPanel(); break;
        case 1: _t->openSubSubPanel(); break;
        case 2: _t->openSubSubSubPanel(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (StarPilotLongitudinalPanel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StarPilotLongitudinalPanel::openSubPanel)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (StarPilotLongitudinalPanel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StarPilotLongitudinalPanel::openSubSubPanel)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (StarPilotLongitudinalPanel::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StarPilotLongitudinalPanel::openSubSubSubPanel)) {
                *result = 2;
                return;
            }
        }
    }
    Q_UNUSED(_a);
}

QT_INIT_METAOBJECT const QMetaObject StarPilotLongitudinalPanel::staticMetaObject = { {
    &StarPilotListWidget::staticMetaObject,
    qt_meta_stringdata_StarPilotLongitudinalPanel.data,
    qt_meta_data_StarPilotLongitudinalPanel,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *StarPilotLongitudinalPanel::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *StarPilotLongitudinalPanel::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_StarPilotLongitudinalPanel.stringdata0))
        return static_cast<void*>(this);
    return StarPilotListWidget::qt_metacast(_clname);
}

int StarPilotLongitudinalPanel::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = StarPilotListWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 3)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 3;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 3)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 3;
    }
    return _id;
}

// SIGNAL 0
void StarPilotLongitudinalPanel::openSubPanel()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void StarPilotLongitudinalPanel::openSubSubPanel()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void StarPilotLongitudinalPanel::openSubSubSubPanel()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
