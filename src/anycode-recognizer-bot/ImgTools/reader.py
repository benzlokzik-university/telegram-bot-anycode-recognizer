from pyzbar import pyzbar
from PIL import Image


class Decoder:
    def __init__(self, image):
        if isinstance(image, Image.Image):
            self.image = image
        else:
            self.image = Image.open(image)
        self.decoded = self.decode()

    def __len__(self):
        return len(self.decoded)

    def __call__(self, *args, **kwargs):
        return self.decoded

    def decode(self):
        # decodes all barcodes from an image
        decoded_objects = pyzbar.decode(self.image)
        return decoded_objects
