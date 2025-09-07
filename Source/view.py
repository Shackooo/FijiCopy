from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class View(QMainWindow):

	def __init__(self):
		super().__init__()
		self.create_menu()

		self.image_label = QLabel(self)
		self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.setCentralWidget(self.image_label)

	def apply_model(self, model):
		self.setWindowTitle(model.window_title)
		w, h = model.window_size
		self.resize(w,h)

	def create_menu(self):
		menu_bar = self.menuBar()
		file_menu = menu_bar.addMenu("File")
		edit_menu = menu_bar.addMenu("Edit")

		open_action = QAction("Open...", self)
		file_menu.addAction(open_action)

		self.open_action = open_action

	def display_image(self, qt_pixmap):
		self.image_label.setPixmap(qt_pixmap)
