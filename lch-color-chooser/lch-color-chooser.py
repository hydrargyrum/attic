#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL
# inspired by https://css.land/lch/

from math import ceil

# import colorspacious  # lib seems buggy
from colormath.color_objects import LCHabColor, sRGBColor
from colormath.color_conversions import convert_color
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


Slot = pyqtSlot


def clamp(mini, v, maxi):
	return min(maxi, max(mini, v))


class ColorSlider(QAbstractSlider):
	lightness = 0
	chroma = 0
	hue = 0
	forceGamut = False

	margin = 10

	def __init__(self):
		super().__init__()
		self.setLayout(QHBoxLayout())
		self.setMaximum(self.maximum())
		self.setMinimumSize(self.maximum(), 5)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

	@Slot(int)
	def setChroma(self, value):
		self.chroma = value
		self.repaint()

	@Slot(int)
	def setLightness(self, value):
		self.lightness = value
		self.repaint()

	@Slot(int)
	def setHue(self, value):
		self.hue = value
		self.repaint()

	@Slot(bool)
	def setForceGamut(self, value):
		self.forceGamut = value
		self.repaint()

	def buildColor(self, step):
		orig = self.buildLCH(step)

		def is_in_gamut(rgb):
			return all(0 <= elem <= 1 for elem in rgb.get_value_tuple())

		def convert_until_gamut(l, c, h):
			lch_obj = LCHabColor(l, c, h)
			rgb = convert_color(lch_obj, sRGBColor)
			if is_in_gamut(rgb):
				return rgb

			c_lo = 0
			c_hi = c
			c /= 2
			while (c_hi - c_lo) > .0001:
				lch_obj = LCHabColor(l, c, h)
				rgb = convert_color(lch_obj, sRGBColor)
				if is_in_gamut(rgb):
					c_lo = c
				else:
					c_hi = c

				c = (c_lo + c_hi) / 2

			return rgb

		if self.forceGamut:
			rgb = convert_until_gamut(orig.lch_l, orig.lch_c, orig.lch_h)
		else:
			rgb = convert_color(orig, sRGBColor)

		rgb255 = rgb.get_upscaled_value_tuple()
		return QColor(*rgb255)

		(r, g, b), = colorspacious.cspace_convert(
			[(self.lightness, self.chroma, step)],
			"CIELCh", "sRGB255"
		)
		print(step, r, g, b)
		return QColor(int(r), int(g), int(b))

	def getCurrentColor(self):
		return self.buildColor(self.value())

	def paintEvent(self, ev):
		pnt = QPainter(self)

		# gradient
		step_width = (self.width() - self.margin * 2) / self.maximum()
		start = self.margin
		colors = [self.buildColor(step) for step in range(self.maximum())]

		for color in colors:
			pnt.fillRect(
				int(start), 4, ceil(step_width), self.height() - 8,
				color
			)
			start += step_width

		# user handle
		avail_width = self.width() - self.margin * 2
		pos = self.value() * avail_width // self.maximum() + self.margin

		pnt.setPen(QColor("black"))
		pnt.drawRoundedRect(
			pos - self.margin // 2,
			2,
			self.margin,
			self.height() - 4,
			2,
			2,
		)
		pnt.setPen(QColor("white"))
		pnt.drawRoundedRect(
			1 + pos - self.margin // 2,
			2,
			self.margin - 2,
			self.height() - 4,
			2,
			2,
		)

	def mousePressEvent(self, ev):
		vw = self.width() - self.margin * 2
		vpos = clamp(0, ev.x() - self.margin, vw)
		lpos = int(vpos * self.maximum() / vw)

		self.setSliderDown(True)
		self.setSliderPosition(lpos)

	def mouseMoveEvent(self, ev):
		vw = self.width() - self.margin * 2
		vpos = clamp(0, ev.x() - self.margin, vw)
		lpos = int(vpos * self.maximum() / vw)

		self.setSliderDown(True)
		self.setSliderPosition(lpos)

	def mouseReleaseEvent(self, ev):
		vw = self.width() - self.margin * 2
		vpos = clamp(0, ev.x() - self.margin, vw)
		lpos = int(vpos * self.maximum() / vw)

		self.setSliderPosition(lpos)
		self.setSliderDown(False)

	def maximum(self):
		raise NotImplementedError()

	def buildLCH(self, step):
		raise NotImplementedError()


class LightnessSlider(ColorSlider):
	def maximum(self):
		return 100

	def buildLCH(self, step):
		return LCHabColor(step, self.chroma, self.hue)


class ChromaSlider(ColorSlider):
	def maximum(self):
		return 130

	def buildLCH(self, step):
		return LCHabColor(self.lightness, step, self.hue)


class HueSlider(ColorSlider):
	def maximum(self):
		return 360

	def buildLCH(self, step):
		return LCHabColor(self.lightness, self.chroma, step)


class SliderGroup:
	def __init__(self):
		self.hslider = HueSlider()
		self.cslider = ChromaSlider()
		self.lslider = LightnessSlider()

		self.cslider.valueChanged.connect(self.hslider.setChroma)
		self.cslider.valueChanged.connect(self.lslider.setChroma)

		self.hslider.valueChanged.connect(self.lslider.setHue)
		self.hslider.valueChanged.connect(self.cslider.setHue)

		self.lslider.valueChanged.connect(self.hslider.setLightness)
		self.lslider.valueChanged.connect(self.cslider.setLightness)


class Window(QColorDialog):
	def __init__(self):
		super().__init__()

		self.sliders = SliderGroup()
		w = QWidget()
		w.setLayout(QFormLayout())

		def buildWidget(slider):
			edit = QSpinBox()
			edit.setMaximum(slider.maximum())
			slider.valueChanged.connect(edit.setValue)
			edit.valueChanged.connect(slider.setValue)

			forceGamut.toggled.connect(slider.setForceGamut)

			widget = QWidget()
			widget.setLayout(QHBoxLayout())
			widget.layout().addWidget(slider)
			widget.layout().addWidget(edit)

			return widget

		forceGamut = QCheckBox("If needed, mangle LCH color to fit into sRGB space (warning: slow)")
		w.layout().addRow(forceGamut)
		w.layout().addRow("&Lightness", buildWidget(self.sliders.lslider))
		w.layout().addRow("&Chroma", buildWidget(self.sliders.cslider))
		w.layout().addRow("&Hue", buildWidget(self.sliders.hslider))

		self.layout().insertWidget(0, w)

		self.sliders.lslider.valueChanged.connect(self.updateRGB)
		self.sliders.cslider.valueChanged.connect(self.updateRGB)
		self.sliders.hslider.valueChanged.connect(self.updateRGB)

		self.sliders.lslider.setValue(50)
		self.sliders.cslider.setValue(50)
		self.sliders.hslider.setValue(20)

	@Slot()
	def updateRGB(self):
		self.setCurrentColor(self.sliders.hslider.getCurrentColor())


if __name__ == "__main__":
	app = QApplication([])
	win = Window()
	win.show()
	app.exec()
