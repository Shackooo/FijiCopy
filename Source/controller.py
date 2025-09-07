from PyQt6.QtWidgets import QFileDialog, QLabel
from PyQt6.QtGui import QPixmap
from model import Model
from view import View

class Controller:

	def __init__(self):
		self.model = Model()
		self.view = View()
		self.view.apply_model(self.model)

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
				self.view.display_image(pixmap)