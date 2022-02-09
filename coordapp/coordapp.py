#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, QPoint, QBasicTimer, Qt
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QAction, qApp, QMainWindow, QApplication, QPushButton, QMessageBox

import sys


class CoordWidget(QLineEdit):
	def __init__(self, *args):
		super(CoordWidget, self).__init__(*args)
		self.setReadOnly(True)

	@Slot(QPoint)
	def showCoords(self, point):
		self.setText('%4d : %4d' % (point.x(), point.y()))


class MouseFollower(QWidget):
	def __init__(self, *args):
		super(MouseFollower, self).__init__(*args)

		self.following = False
		self.grabbing = False
		self.cursorTimer = QBasicTimer()

	def isGrabbing(self):
		return self.grabbing

	def isFollowing(self):
		return self.following

	mouseMoved = Signal(QPoint)
	clickWhileGrabbed = Signal()

	@Slot()
	def toggleGrab(self):
		refollow = self.following
		
		if refollow:
			self.endFollow()
		self.grabbing = not self.grabbing
		
		if refollow:
			self.startFollow()

	def toggleFollow(self):
		if self.following:
			self.endFollow()
		else:
			self.startFollow()

	@Slot()
	def startFollow(self):
		if not self.grabbing:
			self.cursorTimer.start(100, self)
		else:
			self.setMouseTracking(True)
			self.grabMouse()
		self.following = True

	@Slot()
	def endFollow(self):
		if not self.grabbing:
			self.cursorTimer.stop()
		else:
			self.releaseMouse()
		self.following = False

	def timerEvent(self, ev):
		if ev.timerId() == self.cursorTimer.timerId():
			self.mouseMoved.emit(QCursor.pos())
		else:
			super(MouseFollower, self).timerEvent(ev)

	def mouseMoveEvent(self, ev):
		self.mouseMoved.emit(QCursor.pos())
		return super(MouseFollower, self).mouseMoveEvent(ev)

	def mousePressEvent(self, ev):
		if self.grabbing:
			self.clickWhileGrabbed.emit()
		return super(MouseFollower, self).mousePressEvent(ev)


class CoordApp(QMainWindow):
	def __init__(self, parent=None):
		super(CoordApp, self).__init__(parent)

		self.setWindowTitle('Mouse coordinates')

		container = QWidget()
		layout = QHBoxLayout()
		container.setLayout(layout)
		self.setCentralWidget(container)

		self.label = CoordWidget()
		self.label.selectionChanged.connect(self._showSelectionInfo)
		layout.addWidget(self.label)

		help = QPushButton('&?')
		help.clicked.connect(self.showHelp)
		layout.addWidget(help)

		self.follower = MouseFollower()
		self.follower.mouseMoved.connect(self.label.showCoords)
		# disable grabbing here to avoid confusion
		self.follower.clickWhileGrabbed.connect(self.follower.toggleGrab)
		self.follower.clickWhileGrabbed.connect(self._showGrabInfo)
		layout.addWidget(self.follower)

		self.statusBar() # creates it

		self.resize(layout.sizeHint())

		## shortcuts
		self.copyAction = QAction(self)
		self.copyAction.setShortcut(QKeySequence(QKeySequence.Copy))
		self.copyAction.triggered.connect(self.copyToClibpoard)
		self.addAction(self.copyAction)

		self.toggleGrabAction = QAction(self)
		self.toggleGrabAction.setShortcut(QKeySequence(Qt.Key_G))
		self.toggleGrabAction.triggered.connect(self.follower.toggleGrab)
		self.toggleGrabAction.triggered.connect(self._showGrabInfo)
		self.addAction(self.toggleGrabAction)

		self.toggleFollowAction = QAction(self)
		self.toggleFollowAction.setShortcut(QKeySequence(Qt.Key_Space))
		self.toggleFollowAction.triggered.connect(self.follower.toggleFollow)
		self.addAction(self.toggleFollowAction)

		self.toggleAlwaysOnTopAction = QAction(self)
		self.toggleAlwaysOnTopAction.setShortcut(QKeySequence(Qt.Key_A))
		self.toggleAlwaysOnTopAction.triggered.connect(self.toggleAlwaysOnTop)
		self.addAction(self.toggleAlwaysOnTopAction)

	@Slot()
	def _showGrabInfo(self):
		if self.follower.isGrabbing():
			self.statusBar().showMessage('Press G again or click to release grab.')
		else:
			self.statusBar().clearMessage()

	@Slot()
	def _showSelectionInfo(self):
		self.statusBar().showMessage('Press Ctrl-C anytime to copy, no need to select this text!', 5000)

	def showEvent(self, ev):
		self.follower.startFollow()
		return QMainWindow.showEvent(self, ev)

	def hideEvent(self, ev):
		self.follower.endFollow()
		return QMainWindow.hideEvent(self, ev)

	def toggleAlwaysOnTop(self):
		self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
		self.show() # setWindowFlags hides...

	@Slot()
	def displayInfo(self):
		pos = QCursor.pos()
		self.label.showCoords(pos)

	@Slot()
	def copyToClibpoard(self):
		text = self.label.text().replace(' ', '')
		qApp.clipboard().setText(text)
		self.statusBar().showMessage('%s copied to clipboard' % text, 2000)

	def showHelp(self):
		QMessageBox.information(self, 'Help',
		                        'Press [Ctrl-C] (or your copy shortcut) to copy coordinates to clipboard.\n'
		                        'Press [Space] to toggle mouse-follow.\n'
		                        'Press [A] to toggle always-on-top.\n'
		                        'Press [G] to toggle mouse-grabbing mode (faster, but prevents you to click when enabled).')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = CoordApp()
	gui.show()
	sys.exit(app.exec_())
