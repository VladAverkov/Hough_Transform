The Hough Transform Project
==============================

The programm which can find lines in image


Installation
------------

To install the Hough Transform project,
download code via `hough_transform <https://github.com/YablochniyBoss/Hough_Transform>`_.


Usage
-----

Hough Transform's usage looks like:

First you need to put your image with lines into image directory.

After that you can use the code below as example (you can put this code into src/hough_transform_project/console.py:main).

.. code-block:: console

   >>> img_name: str = "img_name"
   >>> processor: ImageProcessor = ImageProcessor(img_name)
   >>> color_image = processor.process_image()
   >>> color_image.show()




.. toctree::
   :hidden:
   :maxdepth: 1

   license
