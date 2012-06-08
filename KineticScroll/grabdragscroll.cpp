#include "grabdragscroll.h"

struct ScrollData
{
    enum STATE { STEADY, PRESSED, MANUAL_SCROLL, AUTO_SCROLL, STOP };
    int state;
    QWebView *widget;
    QPoint pressPos;
    QPoint offset;
    QPoint dragPos;
    QPoint speed;
};

GrabDragScroll::GrabDragScroll(QObject *parent) :
    QObject(parent)
{
    this->data = new ScrollData;
    this->data->state = ScrollData::STEADY;
    this->data->pressPos = QPoint(0, 0);
    this->data->offset = QPoint(0, 0);
    this->data->dragPos = QPoint(0, 0);
    this->data->speed = QPoint(0, 0);

    this->timer = new QBasicTimer;
}

void GrabDragScroll::installWidget(QWebView* widget, bool withoutBars)
{
    if(withoutBars){
        QWebFrame* frame = widget->page()->mainFrame();
        frame->setScrollBarPolicy(Qt::Vertical, Qt::ScrollBarAlwaysOff);
        frame->setScrollBarPolicy(Qt::Horizontal, Qt::ScrollBarAlwaysOff);
    }
    widget->installEventFilter(this);
    data->widget = widget;
}

bool GrabDragScroll::eventFilter(QObject *obj, QEvent *event)
{
    if(!(obj->isWidgetType())){
        return false;
    }

    QEvent::Type eventType = event->type();
    if(eventType != QEvent::MouseButtonPress &&
       eventType != QEvent::MouseButtonRelease &&
       eventType != QEvent::MouseMove){
        return false;
    }

    QMouseEvent* mouseEvent = dynamic_cast<QMouseEvent*>(event);
    if(this->data->pressPos.x() == mouseEvent->pos().x() &&
       this->data->pressPos.y() == mouseEvent->pos().y()){
        this->data->state = ScrollData::STEADY;
        return false;
    }
    bool consumed = false;

    if(this->data->state == ScrollData::STEADY && eventType == QEvent::MouseButtonPress && mouseEvent->buttons() == Qt::LeftButton){
            consumed = false;
            data->state = ScrollData::PRESSED;
            data->pressPos = QPoint(mouseEvent->pos());
            data->offset = this->scrollOffset(data->widget);

    }else if(data->state == ScrollData::PRESSED){
        if(eventType == QEvent::MouseButtonRelease){
            consumed = true;
            data->state = ScrollData::STEADY;
            QMouseEvent* event1 = new QMouseEvent(QEvent::MouseButtonPress,
                                                  data->pressPos, Qt::LeftButton,
                                                  Qt::LeftButton, Qt::NoModifier);
            QMouseEvent* event2 = new QMouseEvent(*event1);

        }else if(eventType == QEvent::MouseMove){
            consumed = true;
            data->state = ScrollData::MANUAL_SCROLL;
            data->dragPos = QCursor::pos();
            if(!this->timer->isActive()){
                this->timer->start(20, this);
            }
        }

    }else if(data->state == ScrollData::MANUAL_SCROLL){
        if(eventType == QEvent::MouseMove){
            consumed = true;
            const QPoint pos = mouseEvent->pos();
            const QPoint delta = pos - data->pressPos;
            this->setScrollOffset(this->data->widget, this->data->offset - delta);

        }else if(eventType == QEvent::MouseButtonRelease){
            consumed = true;
            data->state = ScrollData::AUTO_SCROLL;
        }

    }else if(data->state == ScrollData::AUTO_SCROLL){
        if(eventType == QEvent::MouseButtonPress){
            consumed = true;
            data->offset = this->scrollOffset(data->widget);
            data->state = ScrollData::STOP;
            data->speed = QPoint(0, 0);
        }else if(eventType == QEvent::MouseButtonRelease){
            consumed = true;
            data->state = ScrollData::STEADY;
            data->speed = QPoint(0, 0);
        }

    }else if(data->state == ScrollData::STOP){
        if(eventType == QEvent::MouseButtonRelease){
            consumed = true;
            data->state = ScrollData::STEADY;
        }else if(eventType == QEvent::MouseMove){
            consumed = false;
            data->state = ScrollData::MANUAL_SCROLL;
            const QPoint pos = mouseEvent->pos();
            this->setScrollOffset(this->data->widget, this->data->offset);
        }
    }

    return consumed;
}

void GrabDragScroll::timerEvent(QTimerEvent *event)
{
    if(data->state == ScrollData::MANUAL_SCROLL){
        QPoint cursorPos = QCursor::pos();
        data->speed = cursorPos - data->dragPos;
        data->dragPos = cursorPos;
    }else if(data->state == ScrollData::AUTO_SCROLL){
        data->speed = this->deaccelerate(this->data->speed);
        QPoint p = this->scrollOffset(data->widget);
        this->setScrollOffset(this->data->widget, p - data->speed);
        if(data->speed == QPoint(0, 0)){
            data->state = ScrollData::STEADY;
        }
    }

    QObject::timerEvent(event);
}

QPoint GrabDragScroll::scrollOffset(const QWebView* view) const {
    int x, y = 0;
    QWebFrame* frame = view->page()->mainFrame();
    x = frame->evaluateJavaScript("window.scrollX").toInt();
    y = frame->evaluateJavaScript("window.scrollY").toInt();

    return QPoint(x, y);
}

void GrabDragScroll::setScrollOffset(QWebView* view, const QPoint& p)
{
    QWebFrame* frame = view->page()->mainFrame();
    frame->evaluateJavaScript(QString("window.scrollTo(%1,%2);").arg(p.x()).arg(p.y()));
}

QPoint GrabDragScroll::deaccelerate(const QPoint &speed, const int a, const int maxVal)
{
    int x = qBound<int>(-maxVal, speed.x(), maxVal);
    int y = qBound<int>(-maxVal, speed.y(), maxVal);
    if(x > 0){
        x = qMax<int>(0, x - a);
    }else if(x < 0){
        x = qMin<int>(0, x + a);
    }
    if(y > 0){
        y = qMax(0, y - a);
    }else if(y < 0){
        y = qMin(0, y + a);
    }

    return QPoint(x, y);
}
