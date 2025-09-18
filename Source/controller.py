from PyQt6.QtWidgets import QFileDialog, QLabel
from PyQt6.QtGui import QPixmap
from model import Model
from view import View

class Controller:

	def __init__(self):
		self.model = Model()
		self.view = View()
		self.view.apply_model(self.model)

		# Reference to the single image window
		self.image_window = None

		# Connecting the "Open..." action
		self.view.open_action.triggered.connect(self.open_file)
		self.view.cut_action.triggered.connect(self.cut_active_image)
		self.view.copy_action.triggered.connect(self.copy_active_image)
		self.view.paste_action.triggered.connect(self.paste_active_image)
		self.view.save_action.triggered.connect(self.save_active_image)
		# Remove connection for Gaussian Filter action

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
			if pixmap is not None:
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