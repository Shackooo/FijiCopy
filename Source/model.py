from PyQt6.QtGui import QPixmap

class Model:
	def __init__(self):
		self.window_title = "FijiClone"
		self.window_size = (800, 600) # width, height
		self.image = None # QPixmap

	def load_image(self, path):
		"""
		@brief Load an image from file into the model
		@param path - The file path to the image
		@return Opened image
		"""
		#print("Supported formats:", [str(fmt.data(), 'utf-8') for fmt in QImageReader.supportedImageFormats()])

		pixmap = QPixmap(path)
		self.image = pixmap
		return self.image
	