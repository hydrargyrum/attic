#!/usr/bin/env python3
# 2013-01-26
# license: WTFPL [http://www.wtfpl.net/]
# A Qt app that just displays a ruler to measure pixel lengths

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot as Slot
from PyQt5.QtGui import QPainter, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QAction

import sys


class RulerWidget(QWidget):
	def __init__(self, *args):
		super(RulerWidget, self).__init__(*args)
		self.orientation = Qt.Horizontal
		self.firstEdge = False
		self.inv = False

	def setOrientation(self, orientation):
		self.orientation = orientation
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)

		tick = 0
		while True:
			if tick % 50 == 0:
				if not self._drawTick(painter, tick, 20):
					break
				self._drawTickLabel(painter, tick, 20)
			elif tick % 10 == 0:
				if not self._drawTick(painter, tick, 10):
					break
			else:
				if not self._drawTick(painter, tick, 5):
					break

			tick += 5

	def _drawTick(self, painter, tick, length):
		if self.firstEdge:
			tickStart = 0
			tickEnd = length

		if self.orientation == Qt.Horizontal:
			if self.inv:
				tick = self.size().width() - tick - 1

			if not (0 <= tick < self.size().width()):
				return False

			if not self.firstEdge:
				tickStart = self.size().height()
				tickEnd = tickStart - length

			painter.drawLine(tick, tickStart, tick, tickEnd)
		else:
			if self.inv:
				tick = self.size().height() - tick - 1

			if not (0 <= tick < self.size().height()):
				return False

			if not self.firstEdge:
				tickStart = self.size().width()
				tickEnd = tickStart - length

			painter.drawLine(tickStart, tick, tickEnd, tick)

		return True

	def _drawTickLabel(self, painter, tick, pos):
		label = str(tick)

		if self.orientation == Qt.Horizontal:
			if self.inv:
				tick = self.size().width() - tick - 1

			if self.firstEdge:
				tickStart = pos + 10
			else:
				tickStart = self.size().height() - pos - 10

			textFlags = Qt.TextDontClip | Qt.AlignBottom | Qt.AlignHCenter
			rect = QRect(tick - 10, tickStart, 20, 10)
			painter.drawText(rect, textFlags, label)
		else:
			if self.inv:
				tick = self.size().height() - tick - 1

			if self.firstEdge:
				tickStart = pos + 20
			else:
				tickStart = self.size().width() - pos - 20

			textFlags = Qt.TextDontClip | Qt.AlignRight | Qt.AlignVCenter
			rect = QRect(tickStart, tick - 5, 20, 10)
			painter.drawText(rect, textFlags, label)

	def sizeHint(self):
		if self.orientation == Qt.Horizontal:
			return QSize(300, 50)
		else:
			return QSize(50, 300)


class RulerWindow(RulerWidget):
	def __init__(self, *args):
		super(RulerWindow, self).__init__(*args)
		self.setToolTip(
			'Double-click (or press V) to toggle horizontal/vertical.\n'
			'Press arrows to move window by 1 pixel.\n'
			'Press B to toggle borderless.\n'
			'Press R to toggle reverse direction of the ruler.'
		)
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		self.vertAction = QAction('&Vertical', self)
		self.vertAction.setShortcut(QKeySequence('v'))
		self.vertAction.setCheckable(True)
		self.vertAction.triggered.connect(self.toggleVertical)
		self.addAction(self.vertAction)

		self.borderAction = QAction('&Borderless', self)
		self.borderAction.setShortcut(QKeySequence('b'))
		self.borderAction.setCheckable(True)
		self.borderAction.triggered.connect(self.toggleBorderless)
		self.addAction(self.borderAction)

		self.edgeAction = QAction('First edge', self)
		self.edgeAction.setCheckable(True)
		self.edgeAction.triggered.connect(self.toggleEdge)
		self.addAction(self.edgeAction)

		self.invAction = QAction('&Reverse direction', self)
		self.invAction.setShortcut(QKeySequence('r'))
		self.invAction.setCheckable(True)
		self.invAction.triggered.connect(self.toggleInv)
		self.addAction(self.invAction)

		self.setContextMenuPolicy(Qt.ActionsContextMenu)

	def keyPressEvent(self, event):
		xy = None
		if event.key() == Qt.Key_Left:
			xy = -1, 0
		elif event.key() == Qt.Key_Right:
			xy = 1, 0
		elif event.key() == Qt.Key_Up:
			xy = 0, -1
		elif event.key() == Qt.Key_Down:
			xy = 0, 1

		if xy is None:
			super(RulerWindow, self).keyPressEvent(event)
		else:
			if event.modifiers() & Qt.ShiftModifier:
				self.resize(self.width() + xy[0], self.height() + xy[1])
			else:
				self.move(self.x() + xy[0], self.y() + xy[1])

	def mouseDoubleClickEvent(self, event):
		self.toggleVertical()

	@Slot()
	def toggleVertical(self):
		if self.orientation == Qt.Horizontal:
			self.setOrientation(Qt.Vertical)
			self.vertAction.setChecked(True)
		else:
			self.setOrientation(Qt.Horizontal)
			self.vertAction.setChecked(False)
		self.resize(self.height(), self.width()) # transpose size

	@Slot()
	def toggleBorderless(self):
		size = self.size()

		self.hide()  # seems the flag can't be set when window is visible
		self.setWindowFlags(self.windowFlags() ^ Qt.FramelessWindowHint)
		self.borderAction.setChecked(self.windowFlags() & Qt.FramelessWindowHint)
		self.show()

		self.resize(size)

	@Slot()
	def toggleEdge(self):
		self.firstEdge = not self.firstEdge
		self.update()

	@Slot()
	def toggleInv(self):
		self.inv = not self.inv
		self.update()


def main():
	app = QApplication(sys.argv)
	win = RulerWindow()
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
