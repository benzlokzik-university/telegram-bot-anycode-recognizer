from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image


class SignatureAdder:
    def __init__(self, start_image):
        if type(start_image) == str:
            self.image = Image.open(start_image)
        else:
            self.image = start_image

    def __call__(self, *args, **kwargs):
        self.merge(self.create_signature())

    def create_signature(
        self,
        signature="w/ ♡ by @benzlokzik",
        color=(5, 38, 17),
        font_path="ttf/Symbola.ttf",
        font_size=None,
        bg_color=(250, 250, 250),
    ) -> Image:
        """
        Returns PIL.Image object of the sign
        :type bg_color: tuple[int, int, int] || str
        :type signature: str
        :type color: tuple[float, float, float]
        :type font_path: str
        :type font_size: int || None
        """
        # Open the image file to find his size
        default_image: Image = self.image

        # Create an object with 1/8 height for sign
        image = Image.new(
            "RGB", (default_image.width, max(int(default_image.height / 8), 36))
        )

        # Create an ImageDraw object
        draw = ImageDraw.Draw(image)

        # Draw a rectangle over the entire image
        draw.rectangle((0, 0, image.width, image.height), fill=bg_color)

        # Set the font and font size
        font = ImageFont.truetype(font_path, font_size or int(image.height / 2))

        text_width: int
        text_height: int
        text_width, text_height = draw.textsize(signature, font=font)

        # Calculate the x and y coordinates of the text
        x: float = (image.width - text_width) / 2
        y: float = (image.height - text_height) / 2

        # Set the position of the text
        position: tuple[float, float] = (x, y)

        # Add the signature to the image
        draw.text(position, signature, font=font, fill=color)

        return image

    def merge(self, signature_image: Image, main_img_path=None) -> Image:
        """
        Merge two images together and saves to self.start_image
        :type main_img_path: NoneType || str
        :type signature_image: PIL.Image.Image
        """
        # Open the image file
        if main_img_path:
            image: Image = Image.open(main_img_path)
        else:
            image: Image = self.image

        # Create a new image that is the combined width of both images
        collage = Image.new("RGB", (image.width, image.height + signature_image.height))

        # Paste image onto the collage
        collage.paste(image, (0, 0))

        # Save the collage
        collage.paste(signature_image, (0, image.height))

        # Save the modified image
        # collage.save(f'{"".join(self.image_path.split(".")[:-1])}.png')
        return collage


if __name__ == "__main__":
    # calls the class
    SignatureAdder(input() or "testing/qr_g.png")()
