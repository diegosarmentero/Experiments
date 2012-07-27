import sys
import math

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPainter

import mapping


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.data = mapping.get_robot_values()
        self.showMaximized()

    def paintEvent(self, event):
        super(Window, self).paintEvent(event)
        centerX = self.width() / 2
        centerY = self.height() / 2
        painter = QPainter(self)
        painter.setPen(QColor('black'))
        painter.setBrush(QBrush(QColor('black')))
        painter.drawLine(centerX, 0, centerX, self.height())
        painter.drawLine(0, centerY, self.width(), centerY)
        painter.setPen(QColor('blue'))
        painter.setBrush(QBrush(QColor('blue')))
        painter.drawEllipse(centerX - 5, centerY - 5, 10, 10)
#        for value in self.data:
#            points = self.get_point(value)
#            for x, y in points:
#                painter.drawEllipse(centerX + x, centerY + y, 1, 1)
#        points = self.get_point(self.data[0])
        for i in range(1000):
            x = (i - 500)
            y = math.sin(x) * 100
            x2 = (i - 499)
            y2 = math.sin(x2) * 100
            painter.drawLine(centerX + x * 5, centerY - y,
                centerX + x2 * 5, centerY - y2)
#            painter.drawEllipse(centerX + x, centerY - y, 1, 1)
#        for x, y in points:
#            painter.drawEllipse(centerX + x, centerY + y, 1, 1)

    def get_point(self, robot_data):
        x, y, rotation = robot_data.positions
        print rotation
        x = int(float(x) * 100)
        y = int(float(y) * 100)
        base_angle = float(rotation)
        rotation = self.fix_angle(base_angle)
        meassures = robot_data.meassures
        points = []
        i = 0
        for m in meassures:
            distance = int(float(m) * 100)
            if rotation > 90 and rotation < 270:
                posX = x + (distance * math.sin(
                    math.radians(180 - 90 - rotation)))
                posY = y + (distance * math.sin(math.radians(180 - rotation)))
            else:
                posX = x + (distance * math.sin(math.radians(90 - rotation)))
                posY = y + (distance * math.sin(math.radians(rotation)))
            points.append((posX, posY))
            i += 1
            rotation += 1

        return points

    def fix_angle(self, rotation):
        if 0 <= rotation <= 90:
            rotation = 90 - rotation
        elif 90 < rotation <= 180:
            rotation = 180 - rotation
        elif 180 < rotation <= 270:
            rotation = 270 - rotation
        else:
            rotation = 360 - rotation
        return rotation


app = QApplication(sys.argv)
w = Window()
w.show()

sys.exit(app.exec_())
