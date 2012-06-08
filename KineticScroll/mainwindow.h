#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QtGui>
#include <QtCore>
#include <QtWebKit>
#include "grabdragscroll.h"

class QWidget;
class QVBoxLayout;
class QWebView;
class QVBoxLayout;
class QProgressBar;
class GrabDragScroll;

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);

private:
    QWebView* web;
    QVBoxLayout* v_box;
    QProgressBar* progress;
    GrabDragScroll* grab;
};

#endif // MAINWINDOW_H
