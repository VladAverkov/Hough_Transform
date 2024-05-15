"""Invoke the Hough Transform function."""

from __init__ import __version__
import click

# from hough_transform_project.ImageProcessor import ImageProcessor


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Run the Hough Transform Project.

    This function prompts the user to input an image name, processes the image using
    the ImageProcessor class, and returns the processed image.
    """
    # img_name: str = "images/horizontal_lines.png"
    # processor: ImageProcessor = ImageProcessor(img_name)
    # color_image = processor.process_image()
    print("testing...")
