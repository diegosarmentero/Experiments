#include <QtGui/QGuiApplication>
#include "myclass.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    MyClass myclass;

    return app.exec();
}
