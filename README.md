<img src="Example_01.jpg">
<h3># RGB-Matrix</h3><p>Render a display RGB matrix from a source image.</p>
<br><h3>Dependency:</h3>
<p>Pillow - <a href="https://pillow.readthedocs.io/en/stable/">https://pillow.readthedocs.io/en/stable/</a></p>
<br><h3>Usage:</h3>
<pre>RGB-Matrix.py [-h] [-f] [-w] [-H] [-b] [-B]</pre>
<pre>positional arguments:
Filename of a single source-image, or directory for batch processing.
<br>
optional arguments:
-f , --format   Export File-Format (.jpg or .png)
-w , --width    Width of each Individual Pixel (R-G-B).
-H , --height   Height of each individual Pixel (R-G-B).
-b , --block    Block-Size defines the overall size of the repeated Pixel-Pattern.
-B , --black    Shift brightness of black pixels to simulate backlight shining - otherwise no pixels are visible in black areas. Value between 0-100 (0 = black 100 = white)</pre>
<br>
<img src="info.png" width="30%">
<br>
<p>If you execute the script without optional arguments, these settings are used:</p>
<pre>-w 2 -H 5 -b 7 -B 0 -f .jpg</pre>
<p>Supported file formats for source image:<br>.bmp, .jpeg, .jpg, .png, .tiff, .tif, .webp</p><br>
<br><h3>Tips:</h3>
<ul><li>Two output formats are supported (.jpg & .png). Choosing png as output file format results in a pretty clean matrix, while the compression for .jpg results in a more realistic, organic look.</li><li>A pretty low resolution is recommended for the source image. The effect is more visible that way.</li></ul>
