from pyzbar import pyzbar
from PIL import Image


class Decoder:
    def __init__(self, image):
        if type(image) == str:
            self.image = Image.open(image)
        else:
            self.image = Image.open(image)

    def __len__(self):
        return len(self.decode())

    def __call__(self, *args, **kwargs):
        return self.decode()

    def decode(self):
        # decodes all barcodes from an image
        decoded_objects = pyzbar.decode(self.image)
        return decoded_objects
