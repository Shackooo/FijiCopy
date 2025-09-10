from PyQt6.QtWidgets import QFileDialog, QLabel
from PyQt6.QtGui import QPixmap
from model import Model
from view import View

class Controller:

	def __init__(self):
		self.model = Model()
		self.view = View()
		self.view.apply_model(self.model)

		# Store references to image windows
		self.image_windows = []

		# Connecting the "Open..." action
		self.view.open_action.triggered.connect(self.open_file)

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
				# Create a new window for the image
				new_window = View()
				new_window.apply_model(self.model)
				new_window.display_image(pixmap)
				new_window.show()
				# Keep a reference so it doesn't get garbage collected
				self.image_windows.append(new_window)