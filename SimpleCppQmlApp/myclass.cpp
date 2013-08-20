#include "myclass.h"
#include <QUrl>
#include <QDebug>
#include <QQmlProperty>
#include <QMetaObject>
#include <QVariant>

MyClass::MyClass(QObject *parent) :
    QObject(parent)
{
    viewer.setSource(QUrl("qml/SimpleCppQmlApp/main.qml"));
    viewer.show();
    this->root = viewer.rootObject();
    viewer.rootContext()->setContextProperty("cppObject", this);
}

void MyClass::funcionCpp(QString string)
{
    qDebug() << "\n" << string;

    QQmlProperty::write(this->root, "opacidad", 0.5);

    QMetaObject::invokeMethod(this->root, "change_color",
                              Q_ARG(QVariant, "green"));
}
