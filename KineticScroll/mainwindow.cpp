#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QWidget(parent)
{
    v_box = new QVBoxLayout(this);

    this->web = new QWebView(this);
    this->web->load(QUrl("http://diegosarmentero.com.ar"));

    this->grab = new GrabDragScroll(this);
    this->grab->installWidget(this->web, true);
    this->progress = new QProgressBar(this);
    this->v_box->addWidget(this->web);
    this->v_box->addWidget(this->progress);

    this->connect(this->web, SIGNAL(loadProgress(int)), this->progress, SLOT(setValue(int)));
    this->connect(this->web, SIGNAL(loadFinished(bool)), this->progress, SLOT(hide()));
    this->connect(this->web, SIGNAL(loadStarted()), this->progress, SLOT(show()));
}
