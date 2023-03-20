import qrcode
import barcode
from barcode.writer import ImageWriter


class Generator:
    """
    What is it for?
        This object generates a qr or barcode
    """

    def __init__(self, code_type: str, data: str, filename=None):

        self.code_type = code_type
        self.data = data
        self.filename = filename
        if self.code_type.lower() == "qrcode":
            self.img = self.qr_generator()
        else:
            self.img = self.barcode_generator()

    def __call__(self, *args, **kwargs):
        if self.filename:
            self.img.save(filename=self.filename)
        else:
            return self.img

    def barcode_generator(self):
        # Create a barcode object
        result = barcode.get_barcode_class(self.code_type)(
            self.data, writer=ImageWriter()
        )
        return result

    def qr_generator(self) -> object:
        # Create a QR code object
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=50,
            border=4,
        )

        # Add data to the QR code
        qr.add_data(self.data)

        # Make the QR code image
        qr.make(fit=True)

        # Create an image from the QR code data
        img = qr.make_image(back_color=(250, 250, 250), fill_color=(23, 46, 32))
        return img
