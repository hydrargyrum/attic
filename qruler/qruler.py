#!/usr/bin/env python3
# 2013-01-26
# license: WTFPL [http://www.wtfpl.net/]
# A Qt app that just displays a ruler to measure pixel lengths

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget

import sys


class RulerWidget(QWidget):
	def __init__(self, *args):
		super(RulerWidget, self).__init__(*args)
		self.orientation = Qt.Horizontal

	def setOrientation(self, orientation):
		self.orientation = orientation
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		
		if self.orientation == Qt.Horizontal:
			ticksLineEnd = self.size().height()
			ticksLast = self.size().width()
		else:
			ticksLineEnd = self.size().width()
			ticksLast = self.size().height()
			
		for tick in range(0, ticksLast, 5):
			if tick % 50 == 0:
				self._drawTick(painter, tick, ticksLineEnd - 20, ticksLineEnd)
				self._drawTickLabel(painter, tick, ticksLineEnd - 20)
			elif tick % 10 == 0:
				self._drawTick(painter, tick, ticksLineEnd - 10, ticksLineEnd)
			else:
				self._drawTick(painter, tick, ticksLineEnd - 5, ticksLineEnd)

	def _drawTick(self, painter, tick, tickStart, tickEnd):
		if self.orientation == Qt.Horizontal:
			painter.drawLine(tick, tickStart, tick, tickEnd)
		else:
			painter.drawLine(tickStart, tick, tickEnd, tick)

	def _drawTickLabel(self, painter, tick, tickStart):
		if self.orientation == Qt.Horizontal:
			textFlags = Qt.TextDontClip | Qt.AlignBottom | Qt.AlignHCenter
			rect = QRect(tick - 10, tickStart - 10, 20, 10)
			painter.drawText(rect, textFlags, str(tick))
		else:
			textFlags = Qt.TextDontClip | Qt.AlignRight | Qt.AlignVCenter
			rect = QRect(tickStart - 20, tick - 5, 20, 10)
			painter.drawText(rect, textFlags, str(tick))

	def sizeHint(self):
		if self.orientation == Qt.Horizontal:
			return QSize(300, 50)
		else:
			return QSize(50, 300)


class RulerWindow(RulerWidget):
	def __init__(self, *args):
		super(RulerWindow, self).__init__(*args)
		self.setToolTip('Double-click to toggle horizontal/vertical.\n'
		                'Press arrows to move window by 1 pixel.')

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Left:
			self.move(self.x() - 1, self.y())
		elif event.key() == Qt.Key_Right:
			self.move(self.x() + 1, self.y())
		elif event.key() == Qt.Key_Up:
			self.move(self.x(), self.y() - 1)
		elif event.key() == Qt.Key_Down:
			self.move(self.x(), self.y() + 1)
		else:
			super(RulerWindow, self).keyPressEvent(event)

	def mouseDoubleClickEvent(self, event):
		if self.orientation == Qt.Horizontal:
			self.setOrientation(Qt.Vertical)
		else:
			self.setOrientation(Qt.Horizontal)
		self.resize(self.height(), self.width()) # transpose size


def main():
	app = QApplication(sys.argv)
	win = RulerWindow()
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
