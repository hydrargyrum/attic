#!/usr/bin/env python3

# A GUI for encoding/decoding QR codes.
# It can load a picture from a file and decode data from it.
# It can also take a screenshot if the QR code is on screen but not in a file.
# Pictures can be cropped if there are multiple codes on the picture.
# It can encode text to a QR code image and save to a file.

# took 4 evenings in 2010/12
# SPDX-License-Identifier: WTFPL
# decoding is possible if 'zbar' module is installed, and 'qrencode' for encoding

from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, Qt, QRect, QSize, QUrl
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel, QDialog, QMainWindow, QApplication, QMessageBox, QTextEdit, QVBoxLayout, QFileDialog, QScrollArea, QDialogButtonBox, QLineEdit, QRubberBand, QFormLayout, qApp

import sys
import time
import tempfile

if sys.version_info.major > 2:
	unicode = str

def tryImport(modulename):
	try:
		__import__(modulename)
		return True
	except ImportError:
		return False

USE_ZBAR = tryImport('zbar')
USE_QRENCODE = tryImport('qrencode')


def decodeImage(qpix):
	'''Decode one bar code from a QPixmap'''
	# TODO rename function
	temp = tempfile.NamedTemporaryFile(suffix='.png')
	qpix.save(temp.name)

	import PIL.Image
	pilimage = PIL.Image.open(temp.name)
	pilimage = pilimage.convert('L')
	rawbytes = pilimage.tobytes()

	import zbar
	zimage = zbar.Image(qpix.width(), qpix.height(), 'Y800', rawbytes)
	scanner = zbar.ImageScanner()
	scanner.scan(zimage)
	results = list(scanner.results)

	if not results:
		return None
	return results[0].data


def encodeText(text, zoom=5):
	'''Encodes text into a QPixmap with 5 pixels wide squares'''
	import qrencode
	_, rows, pilimage = qrencode.encode(text)
	temp = tempfile.NamedTemporaryFile(suffix='.png')
	pilimage.save(temp.name)
	return QPixmap(temp.name).scaled(rows * zoom, rows * zoom)


class ImageCropperDropper(QLabel):
	'''A QLabel that displays a rectangle when drawing a rectangle with the mouse'''

	cropped = Signal(QPixmap)
	fileDropped = Signal(QUrl)

	def __init__(self, mainwin):
		QLabel.__init__(self)

		self.setAcceptDrops(True)

		self.marker = QRubberBand(QRubberBand.Rectangle, self)
		self.markOrigin = self.markEnd = None

		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.addAction(mainwin.cropAction)
		self.addAction(mainwin.saveAction)

	def setPixmap(self, pix):
		QLabel.setPixmap(self, pix)
		self.resize(pix.size())

		self.marker.hide()
		self.markOrigin = self.markEnd = None

	@Slot()
	def doCrop(self):
		'''Crop the pixmap using the user-drawn rectangle, emits cropped(QPixmap) signal'''
		if not self.markEnd:
			QMessageBox.warning(self, 'Error', 'Select a region to crop first')
			return
		cropzone = self._makeRect(self.markOrigin, self.markEnd)
		croppedpix = self.pixmap().copy(cropzone)

		self.setPixmap(croppedpix)
		self.cropped.emit(croppedpix)

	def _makeRect(self, p1, p2):
		'''Make a QRect based on QPoints p1 and p2.
		The 2 points must be 2 corners but don't need to be upper-left&lower-right'''
		x1, x2 = min(p1.x(), p2.x()), max(p1.x(), p2.x())
		y1, y2 = min(p1.y(), p2.y()), max(p1.y(), p2.y())
		return QRect().adjusted(x1, y1, x2, y2)

	def mouseMoveEvent(self, ev):
		if ev.buttons() != Qt.LeftButton:
			return QLabel.mouseMoveEvent(self, ev)
		self.markEnd = ev.pos()
		diffpoint = self.markEnd - self.markOrigin
		#~ self.marker.resize(diffpoint.x(), diffpoint.y())
		self.marker.setGeometry(self._makeRect(self.markOrigin, self.markEnd))
		#~ ev.accept()

	def mousePressEvent(self, ev):
		if ev.button() != Qt.LeftButton:
			return QLabel.mousePressEvent(self, ev)
		self.markOrigin = ev.pos()
		self.marker.move(ev.pos())
		self.marker.resize(QSize())
		self.marker.show()
		#~ ev.accept()

	def dragEnterEvent(self, ev):
		if ev.mimeData().hasUrls():
			ev.setDropAction(Qt.CopyAction)
			ev.accept()

	def dropEvent(self, ev):
		if ev.mimeData().hasUrls():
			ev.setDropAction(Qt.CopyAction)
			ev.accept()
			self.fileDropped.emit(ev.mimeData().urls()[0])


#~ class EncodingJobData(dict):
	#~ pass

class EncoderDialog(QDialog):
	'''A dialog asking user for data to encode. Data is placed in 'value' attribute as a dict'''
	def __init__(self, *args):
		QDialog.__init__(self, *args)
		self.setWindowTitle('Text to encode')
		self.value = {}

		self.text = QLineEdit()

		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttons.accepted.connect(self.validateAndAccept)
		self.buttons.rejected.connect(self.reject)

		self.lay = QFormLayout()
		self.setLayout(self.lay)
		self.lay.addRow('Data', self.text)
		self.lay.addRow(self.buttons)

	@Slot()
	def validateAndAccept(self):
		if self.text.text():
			self.value = {'text': unicode(self.text.text())}
			self.accept()


class DecoderDialog(QDialog):
	'''A dialog to display decoded data'''
	def __init__(self, text, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('Decoded text')

		self.textDisplay = QTextEdit(text)
		self.textDisplay.setReadOnly(True)

		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok)
		self.buttons.accepted.connect(self.accept)

		self.setLayout(QVBoxLayout())
		self.layout().addWidget(self.textDisplay)
		self.layout().addWidget(self.buttons)


class Window(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self.resize(250, 250)
		self.setWindowTitle('QRShot - decoder/encoder')
		self.fullpix = None # uncropped picture

		menu = self.menuBar().addMenu('File') # some of the qactions are reused by ImageCropperDropper
		self.loadAction = menu.addAction('Load image...')
		self.saveAction = menu.addAction('Save image...')
		menu.addAction('Quit').triggered.connect(QApplication.instance().quit)

		menu = self.menuBar().addMenu('Data')
		self.decodeAction = menu.addAction('Decode image')
		self.encodeAction = menu.addAction('Encode text...')

		menu = self.menuBar().addMenu('Screenshot')
		self.shootAction = menu.addAction('Take screenshot')
		self.cropAction = menu.addAction('Crop')

		self.scroller = QScrollArea()
		self.scroller.setWidgetResizable(True)
		self.scroller.setAlignment(Qt.AlignCenter)
		self.setCentralWidget(self.scroller)

		self.cropper = ImageCropperDropper(self)
		self.cropper.setAlignment(Qt.AlignCenter)
		self.scroller.setWidget(self.cropper)

		self.status = self.statusBar()

		self.shootAction.triggered.connect(self.shootScreen)
		self.cropAction.triggered.connect(self.cropper.doCrop)
		self.saveAction.triggered.connect(self.saveImage)
		self.loadAction.triggered.connect(self.loadImage)
		self.decodeAction.triggered.connect(self.decodeImage)
		self.encodeAction.triggered.connect(self.displayEncodeDialog)
		self.cropper.fileDropped.connect(self.loadImageDropped)

		if not USE_ZBAR:
			self.decodeAction.setEnabled(False)
		if not USE_QRENCODE:
			self.encodeAction.setEnabled(False)

	@Slot()
	def shootScreen(self):
		#~ g = QRect(self.geometry())
		self.hide()
		time.sleep(1)
		pix = qApp.primaryScreen().grabWindow(QApplication.desktop().winId())
		#~ pix = QPixmap.grabWindow(QApplication.desktop().winId())
		self.show()
		#~ self.setGeometry(g)
		self.setPixmap(pix)
		self.status.showMessage('Use the crop tool and then decode the image')

	@Slot()
	def saveImage(self):
		img = self.cropper.pixmap()
		if not img:
			return
		fileout, _ = QFileDialog.getSaveFileName(self, 'Save image', '', 'Images (*.png *.jpg *.gif *.bmp)')
		if not fileout:
			return
		if not img.save(fileout):
			QMessageBox.critical(self, 'Error', 'An error occured while saving image')

	@Slot()
	def loadImage(self):
		filein, _ = QFileDialog.getOpenFileName(self, 'Open image', '', 'Images (*.png *.jpg *.gif *.bmp)')
		if not filein:
			return False
		pix = QPixmap(filein)
		if pix.isNull():
			QMessageBox.critical(self, 'Error', 'An error occured while loading image')
			return False
		self.setPixmap(pix)
		return pix

	@Slot(QUrl)
	def loadImageDropped(self, urlin):
		pix = QPixmap(urlin.toLocalFile())
		if pix.isNull():
			QMessageBox.critical(self, 'Error', 'An error occured while loading image')
			return False
		self.setPixmap(pix)
		return pix

	@Slot()
	def decodeImage(self):
		pix = self.cropper.pixmap()
		if not pix or pix.isNull():
			pix = self.loadImage()
			if not pix or pix.isNull():
				return
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		text = decodeImage(pix)
		QApplication.restoreOverrideCursor()
		if not text:
			QMessageBox.warning(self, 'Failure', 'No bar code detected in image')
			return
		DecoderDialog(text, self).show()

	@Slot()
	def displayEncodeDialog(self):
		if not hasattr(self, 'encodeDialog'):
			self.encodeDialog = EncoderDialog(self)
		ok = (self.encodeDialog.exec_() == QDialog.Accepted)
		if not ok:
			return
		text = self.encodeDialog.value['text']
		if len(text) > 1000:
			if QMessageBox.question(self, 'Warning', 'The text entered is quite large, this could make the app crash. Continue anyway?', QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
				return
		pix = encodeText(text)

		self.cropper.setStyleSheet('*{background: white;}')
		self.setPixmap(pix)

	def setPixmap(self, pix):
		self.fullpix = pix
		self.cropper.setPixmap(pix)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Window()
	w.show()
	sys.exit(app.exec_())
