#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# not very useful per se: show a window covering everything except a "hole"
# following the mouse cursor.

# blur with _KDE_NET_WM_BLUR_BEHIND_REGION?
# see https://github.com/Peticali/PythonBlurBehind/blob/main/blurWindow/blurWindow.py

from PyQt6.QtWidgets import QApplication, QFrame
from PyQt6.QtGui import QCursor, QRegion
from PyQt6.QtCore import Qt, QRect


class Peep(QFrame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.lastCursor = None
		self.cursorTimer = self.startTimer(20)
		self.setStyleSheet("background-color: black")

		self.holeRegion = QRegion(QRect(0, 0, 200, 200), QRegion.RegionType.Ellipse)
		self.holeCenter = self.holeRegion.boundingRect().center()

	def timerEvent(self, ev):
		if ev.timerId() != self.cursorTimer:
			return

		cur = QCursor.pos()
		if cur == self.lastCursor:
			return

		self.lastCursor = cur

		region = QRegion(self.geometry())
		hole = self.holeRegion.translated(self.mapFromGlobal(cur) - self.holeCenter)
		region -= hole
		self.setMask(region)


if __name__ == "__main__":
	app = QApplication([])

	wid = Peep()
	wid.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
	wid.showMaximized()

	app.exec()
