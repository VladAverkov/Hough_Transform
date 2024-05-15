"""Class for processing images."""

from __future__ import annotations

from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps


class ImageProcessor:
    """A class to process images and find lines.

    Example usage:
    >>> img_name = input("input image name: ")
    >>> processor = ImageProcessor(img_name)
    >>> color_image = processor.process_image()
    >>> color_image.show()
    """

    def __init__(self, img_name: str) -> None:
        """Initialize ImageProcessor.

        Args:
            img_name (str): The name of the image file.
        """
        self.max_img_size: int = 200  # Max image size
        self.red_color: Tuple[int, int, int] = (255, 0, 0)  # Color for drawing borders
        self.img_name: str = img_name

    def resize_to_const(self, img: Image.Image) -> Image.Image:
        """Resize the image to a constant size if needed.

        Args:
            img (PIL.Image.Image): The input image.

        Returns:
            PIL.Image.Image: The resized image.
        """
        m = max(img.size)
        if m <= self.max_img_size:
            return img
        comp_ratio = int(m / self.max_img_size) + 1
        new_size = (img.size[0] // comp_ratio, img.size[1] // comp_ratio)
        return img.resize(new_size)

    def calc_sums(self, img: np.ndarray, xmin: int, xmax: int, H: int) -> np.ndarray:
        """Calculate sums of pixel values along line.

        Calculates res[x, y] for img from xmin to xmax.

        Args:
            img (np.ndarray): The image as a NumPy array.
            xmin (int): Minimum x-coordinate.
            xmax (int): Maximum x-coordinate.
            H (int): Height.

        Returns:
            np.ndarray: Resulting sums array.
        """
        res = np.zeros([H, H])
        if xmax - xmin == 1:
            for x in range(H):
                res[:, x] = 1 - img[:, xmin] / 255
        else:
            mid = (xmin + xmax) // 2
            ans1 = self.calc_sums(img, xmin, mid, H)
            ans2 = self.calc_sums(img, mid, xmax, H)
            for x in range(H):
                for y in range(H):
                    res[x, y] = ans1[x, (x + y) // 2] + ans2[(x + y) // 2, y]
        return res

    def process_image(self) -> Image.Image:
        """Process the image and find lines.

        Returns:
            PIL.Image.Image: The processed image.
        """
        color_image = Image.open(self.img_name)
        color_image = self.resize_to_const(color_image)
        gray_image = color_image.convert("L")

        edges = gray_image.filter(ImageFilter.FIND_EDGES())
        wb_image = ImageOps.invert(edges)

        W, H = wb_image.size

        for x in range(W):
            wb_image.putpixel((x, 0), 255)
            wb_image.putpixel((x, H - 1), 255)
        for y in range(H):
            wb_image.putpixel((0, y), 255)
            wb_image.putpixel((W - 1, y), 255)

        for theta in (0, 15, 30, 45, 60, 75, 90):
            transparent_image = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            rot_tr_img = transparent_image.rotate(theta, fillcolor=(0, 0, 0, 0))
            draw = ImageDraw.Draw(rot_tr_img)

            rotated_image = wb_image.rotate(theta, fillcolor="white")
            rotated_array = np.array(rotated_image)

            result = self.calc_sums(rotated_array, 0, W, H)

            for i in range(2, H - 2):
                for j in range(2, H - 2):
                    if result[i][j] >= max(
                        np.max(result[i - 2 : i + 2, :]),
                        np.max(result[:, j - 2 : j + 2]),
                        100,
                    ):
                        draw.line([(0, i), (W - 1, j)], fill="red", width=2)

            transparent_image = rot_tr_img.rotate(-theta, fillcolor=(0, 0, 0, 0))
            color_image.paste(transparent_image, (0, 0), transparent_image)

        return color_image
