from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QAction, QPainter, QPen, QPixmap, QImage
from PyQt6.QtCore import Qt, QPoint, QRect


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set alignment and scaling behavior for image display
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScaledContents(False)
        self.setMinimumSize(1, 1)
        # Variables for selection rectangle
        self.selecting = False
        self.selection_start = None
        self.selection_end = None

    def mousePressEvent(self, event):
        # Start selection when left mouse button is pressed on image
        if self.pixmap() and event.button() == Qt.MouseButton.LeftButton:
            self.selecting = True
            self.selection_start = event.position().toPoint()
            self.selection_end = self.selection_start
            self.update()

    def mouseMoveEvent(self, event):
        # Update selection rectangle as mouse moves
        if self.selecting:
            self.selection_end = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        # Finish selection when left mouse button is released
        if self.selecting and event.button() == Qt.MouseButton.LeftButton:
            self.selection_end = event.position().toPoint()
            self.selecting = False
            self.update()

    def paintEvent(self, event):
        # Draw the selection rectangle on top of the image
        super().paintEvent(event)
        if self.selection_start and self.selection_end:
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.yellow, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.selection_start, self.selection_end)
            painter.drawRect(rect)


class View(QMainWindow):
    def apply_gaussian_filter(self, sigma=5):
        """Apply a Gaussian filter to the current image and update display."""
        import numpy as np
        from scipy.ndimage import gaussian_filter
        print("gaussian start")
        if not hasattr(self, 'model') or self.model.image is None:
            return
        # Apply Gaussian filter to each channel
        img = self.model.image
        if img.ndim == 2:
            filtered = gaussian_filter(img, sigma=sigma)
        else:
            filtered = np.zeros_like(img)
            for i in range(img.shape[2]):
                filtered[..., i] = gaussian_filter(img[..., i], sigma=sigma)
        print("gaussian end")
        self.model.image = filtered.astype(img.dtype)
        self.display_image(self.model.image)

    def __init__(self, show_menu=True):
        super().__init__()
        # Create menu bar for main window
        if show_menu:
            self.create_menu()
        # Set up image display area
        self.image_label = ImageLabel(self)
        self.setCentralWidget(self.image_label)
        self.setMinimumSize(100, 50)  # Allow window to be very small
        self.show_menu = show_menu

    def apply_model(self, model):
        self.model = model  # Ensure model is set for image processing
        # Set window title and initial size from model
        self.setWindowTitle(model.window_title)
        w, h = model.window_size
        self.resize(w, h)

    def create_menu(self):
        # Create File and Edit menus with actions
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")

        open_action = QAction("Open...", self)
        file_menu.addAction(open_action)
        self.open_action = open_action

        save_action = QAction("Save", self)
        file_menu.addAction(save_action)
        self.save_action = save_action

        cut_action = QAction("Cut", self)
        edit_menu.addAction(cut_action)
        self.cut_action = cut_action
        self.cut_action.triggered.connect(self.cut_selection)

        copy_action = QAction("Copy", self)
        edit_menu.addAction(copy_action)
        self.copy_action = copy_action

        paste_action = QAction("Paste", self)
        edit_menu.addAction(paste_action)
        self.paste_action = paste_action

        gaussian_action = QAction("Apply Gaussian Filter", self)
        edit_menu.addAction(gaussian_action)
        self.gaussian_action = gaussian_action
        self.gaussian_action.triggered.connect(lambda: self.apply_gaussian_filter())

    def display_image(self, np_image):
        # Convert NumPy array to QPixmap and display
        if np_image is None:
            return
        h, w = np_image.shape[:2]
        if np_image.ndim == 2:
            # Grayscale
            qimage = QImage(np_image.data, w, h, w, QImage.Format.Format_Grayscale8)
        else:
            # RGB or RGBA
            if np_image.shape[2] == 3:
                fmt = QImage.Format.Format_RGB888
            else:
                fmt = QImage.Format.Format_RGBA8888
            qimage = QImage(np_image.data, w, h, w * np_image.shape[2], fmt)
        pixmap = QPixmap.fromImage(qimage)
        # Scale down if needed
        desktop = self.screen().geometry()
        max_width = int(desktop.width() * 0.9)
        max_height = int(desktop.height() * 0.9)
        if pixmap.width() > max_width or pixmap.height() > max_height:
            scaled_pixmap = pixmap.scaled(
                max_width, max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.resize(scaled_pixmap.width(), scaled_pixmap.height())
        else:
            self.image_label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())

    def copy_selection(self):
        # Copy selected area to buffer for paste/cut
        pixmap = self.image_label.pixmap()
        if not pixmap or not self.image_label.selection_start or not self.image_label.selection_end:
            return
        rect = QRect(self.image_label.selection_start, self.image_label.selection_end).normalized()
        image = pixmap.toImage()
        self.copied_image = image.copy(rect)

    def cut_selection(self):
        # Copy selected area, then fill it with black
        pixmap = self.image_label.pixmap()
        if not pixmap or not self.image_label.selection_start or not self.image_label.selection_end:
            return
        rect = QRect(self.image_label.selection_start, self.image_label.selection_end).normalized()
        image = pixmap.toImage()
        # Copy selected area to buffer
        self.copied_image = image.copy(rect)
        # Fill selected area with black
        for x in range(rect.left(), rect.right()):
            for y in range(rect.top(), rect.bottom()):
                if 0 <= x < image.width() and 0 <= y < image.height():
                    image.setPixel(x, y, 0xFF000000)  # ARGB black
        new_pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(new_pixmap)
        self.image_label.selection_start = None
        self.image_label.selection_end = None
        self.image_label.update()

    def paste_selection(self):
        pixmap = self.image_label.pixmap()
        if not pixmap or not hasattr(self, 'copied_image') or self.copied_image is None:
            return
        if not self.image_label.selection_start or not self.image_label.selection_end:
            return
        rect = QRect(self.image_label.selection_start, self.image_label.selection_end).normalized()
        image = pixmap.toImage()
        # Paste copied image at top-left of selection
        paste_x = rect.left()
        paste_y = rect.top()
        for x in range(self.copied_image.width()):
            for y in range(self.copied_image.height()):
                if 0 <= paste_x + x < image.width() and 0 <= paste_y + y < image.height():
                    image.setPixel(paste_x + x, paste_y + y, self.copied_image.pixel(x, y))
        new_pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(new_pixmap)
        self.image_label.selection_start = None
        self.image_label.selection_end = None
        self.image_label.update()

    def save_image(self):
        # Save current image to disk using file dialog
        pixmap = self.image_label.pixmap()
        if not pixmap:
            return
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;BMP Files (*.bmp)")
        if file_path:
            pixmap.save(file_path)