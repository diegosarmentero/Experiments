#ifndef GRABDRAGSCROLL_H
#define GRABDRAGSCROLL_H

#include <QtGui>
#include <QtCore>
#include <QtWebKit>
#include <QtGlobal>

class QObject;
class QTimerEvent;
class QEvent;
class QBasicTimer;
class QTimer;
class QWebView;
class QWebFrame;
class QString;
class QMouseEvent;
class QCursor;

struct ScrollData;

class GrabDragScroll : public QObject
{
    Q_OBJECT

public:
    explicit GrabDragScroll(QObject *parent = 0);
    void installWidget(QWebView* widget, bool withoutBars = true);

    bool eventFilter(QObject * obj, QEvent * event);
    void timerEvent(QTimerEvent * event);

private:
    QPoint scrollOffset(const QWebView* widget) const;
    void setScrollOffset(QWebView* widget, const QPoint& p);
    QPoint deaccelerate(const QPoint& speed, const int a=1, const int maxVal=64);

    QBasicTimer* timer;
    ScrollData* data;

};

#endif // GRABDRAGSCROLL_H
