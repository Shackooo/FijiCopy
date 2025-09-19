from PyQt6.QtWidgets import QFileDialog, QLabel
from PyQt6.QtGui import QPixmap
from model import Model
from view import View
import numpy as np

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View()
		self.view.apply_model(self.model)
		self.view.resize(640, 200)  # Set initial main window size

		# Reference to the single image window
		self.image_window = None

		# Connecting the actions
		self.view.open_action.triggered.connect(self.open_file)
		self.view.cut_action.triggered.connect(self.cut_active_image)
		self.view.copy_action.triggered.connect(self.copy_active_image)
		self.view.paste_action.triggered.connect(self.paste_active_image)
		self.view.save_action.triggered.connect(self.save_active_image)
		self.view.gaussian_action.triggered.connect(self.gaussian_filter)
		# Connect min/max sliders to update_histogram
		self.view.min_slider.valueChanged.connect(self.update_histogram)
		self.view.max_slider.valueChanged.connect(self.update_histogram)
		self.view.brightness_slider.valueChanged.connect(self.update_histogram)
		self.view.contrast_slider.valueChanged.connect(self.update_histogram)

	def show(self):
		self.view.show()

	def open_file(self):
		file_path, _ = QFileDialog.getOpenFileName(
			self.view,
			"Open Image",
			"",
			"Image Files (*.png *.bmp)" #.jpg unsupported :(
		)

		if file_path:
			pixmap = self.model.load_image(file_path)
			if pixmap:
				# Close previous image window if open
				if self.image_window:
					self.image_window.close()
				# Create a new window for the image (no menu bar)
				self.image_window = View(show_menu=False)
				self.image_window.apply_model(self.model)
				self.image_window.display_image(pixmap)
				self.image_window.show()

	def cut_active_image(self):
		if self.image_window:
			self.image_window.cut_selection()

	def copy_active_image(self):
		if self.image_window:
			self.image_window.copy_selection()

	def paste_active_image(self):
		if self.image_window:
			self.image_window.paste_selection()

	def save_active_image(self):
		if self.image_window:
			self.image_window.save_image()

	def gaussian_filter(self):
		if self.image_window:
			self.image_window.apply_gaussian_filter()

	def update_histogram(self):
		"""
		Applies pixel-wise brightness (beta), contrast (alpha), min, and max adjustments to the image and updates display.
		"""
		min_val = self.view.min_slider.value()
		max_val = self.view.max_slider.value()
		beta = self.view.brightness_slider.value()  # brightness
		alpha = self.view.contrast_slider.value() / 128.0  # contrast, 128=neutral

		if self.model.image is None:
			return
		image_array = self.view.qimage_to_numpy(self.model.image.toImage())
		new_image = np.empty_like(image_array)
		new_image = np.clip(alpha * image_array + beta, min_val, max_val)
		if max_val == min_val:
			scaled = np.zeros_like(new_image, dtype=np.uint8)
		else:
			scaled = ((new_image - min_val) / (max_val - min_val) * 255).astype(np.uint8)
		adjusted_pixmap = self.view.numpy_to_qpixmap(scaled)
		self.model.adjusted_image = adjusted_pixmap
		if self.image_window:
			self.image_window.display_image(adjusted_pixmap)