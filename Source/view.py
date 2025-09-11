from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QAction, QPainter, QPen
from PyQt6.QtCore import Qt, QPoint, QRect


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScaledContents(False)
        self.setMinimumSize(1, 1)
        self.selecting = False
        self.selection_start = None
        self.selection_end = None

    def mousePressEvent(self, event):
        if self.pixmap() and event.button() == Qt.MouseButton.LeftButton:
            self.selecting = True
            self.selection_start = event.position().toPoint()
            self.selection_end = self.selection_start
            self.update()

    def mouseMoveEvent(self, event):
        if self.selecting:
            self.selection_end = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.selecting and event.button() == Qt.MouseButton.LeftButton:
            self.selection_end = event.position().toPoint()
            self.selecting = False
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.selection_start and self.selection_end:
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.yellow, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.selection_start, self.selection_end)
            painter.drawRect(rect)


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menu()

        self.image_label = ImageLabel(self)
        self.setCentralWidget(self.image_label)
        self.setMinimumSize(100, 50)  # Allow window to be very small

    def apply_model(self, model):
        self.setWindowTitle(model.window_title)
        w, h = model.window_size
        self.resize(w, h)

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")

        open_action = QAction("Open...", self)
        file_menu.addAction(open_action)

        self.open_action = open_action

    def display_image(self, qt_pixmap):
        # Get desktop size
        desktop = self.screen().geometry()
        max_width = desktop.width() * 0.9
        max_height = desktop.height() * 0.9

        img_width = qt_pixmap.width()
        img_height = qt_pixmap.height()

        # If image is larger than desktop, scale it down
        if img_width > max_width or img_height > max_height:
            scale_w = min(img_width, max_width)
            scale_h = min(img_height, max_height)
            scaled_pixmap = qt_pixmap.scaled(
                max_width, max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setPixmap(qt_pixmap)