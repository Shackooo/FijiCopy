from PyQt6.QtGui import QPixmap

class Model:
	def __init__(self):
		self.window_title = "FijiClone"
		self.window_size = (640, 108) # width, height
		self.image = None # QPixmap

	def load_image(self, path):
		"""
		Load an image from file into the model as a NumPy array
		"""
		import imageio.v3 as iio
		img_array = iio.imread(path)
		self.image = img_array
		return self.image
	