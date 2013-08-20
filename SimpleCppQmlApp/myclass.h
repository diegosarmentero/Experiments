#ifndef MYCLASS_H
#define MYCLASS_H

#include <QWidget>
#include <QtQuick/QQuickView>
#include <QQuickItem>
#include <QQmlContext>

class MyClass : public QObject
{
    Q_OBJECT
public:
    explicit MyClass(QObject *parent = 0);

    Q_INVOKABLE void funcionCpp(QString string);
    
signals:
    void myCppSignal();
    
public slots:

private:
    QQuickView viewer;
    QQuickItem* root;
    
};

#endif // MYCLASS_H
