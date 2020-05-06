from PIL import Image, ImageDraw
import sys, os, datetime, argparse

export_fformat = '.jpg' # Output-Format
export_fformats = {'.jpg': 'JPEG', '.png': 'PNG'}

ext = '_rgb-matrix' #filename extension for the output file

pixel_width = 2 #width of each pixel - so three units (rgb) of this value must go into one block
pixel_height = 5 #height of the pixels (value must go into one block)

block = 7 #block width - 1 block contains one red, one greed and one blue pixel - black space inclusive

valid_formats = ['.bmp', '.jpeg', '.jpg', '.png', '.tiff', '.tif', '.webp']


# argparse
parser = argparse.ArgumentParser(description='Render a display RGB matrix from a source image.')
parser.add_argument('file', type=str, metavar='', help='Filename of Source-Image')
parser.add_argument('-f', '--format', type=str, metavar='', help='Export File-Format (.jpg or .png)')
parser.add_argument('-w', '--width', type=int, metavar='', help='Width of each individual Pixel (R-G-B).')
parser.add_argument('-H', '--height', type=int, metavar='', help='Height of each individual Pixel (R-G-B).')
parser.add_argument('-b', '--block', type=int, metavar='', help='Block-Size defines the overall size of the repeated Pixel-Pattern')
args = parser.parse_args()

source = args.file #Source image filename
new_fn = ''

#error correction for bad input values
if isinstance(args.width, int) and isinstance(args.height, int) and isinstance(args.block, int):
	pixel_width = args.width
	pixel_height = args.height
	block = args.block

	if args.width < args.height:
		if (pixel_width*3 > block):
			pixel_width = int(block/3)
		if (pixel_height > block):
			pixel_height = block
	elif args.height < args.width:
		if (pixel_height*3 > block):
			pixel_height = int(block/3)
		if (pixel_width > block):
			pixel_width = block
	else:
		pixel_width = int(block/3)
		pixel_height = block

# Test if given output file format is supported
if isinstance(args.format, str):
	if args.format in export_fformats:
		export_fformat = args.format
	else:
		print("Unsupported Fileformat.")

def main(source):

	img = Image.open(source)

	#Convert to RGB if necessary
	if img.mode == 'CMYK':
		img = img.convert('RGB')

	#new image size
	x_orig, y_orig = img.size

	x_new = x_orig*block
	y_new = y_orig*block

	#Create new Image
	i1 = Image.new('RGB', (x_new,y_new))
	d1 = ImageDraw.Draw(i1)

	process(img, d1, x_orig, y_orig)

	i1.save(new_fn + export_fformat, export_fformats[export_fformat])

def process(img, d1, x_orig, y_orig):

	x_count = 0
	y_count = 0
	
	if pixel_width < pixel_height:

		#horizontal pixel alignment
		for a in range(0, y_orig):
			for b in range(0, x_orig):
				color = img.getpixel((b,a))			
				
				#R
				d1.line([(x_count, y_count), (x_count, y_count+(pixel_height-1))],(color[0],0,0), width=pixel_width)
				
				#G
				d1.line([(x_count+pixel_width, y_count), (x_count+pixel_width, y_count+(pixel_height-1))], (0,color[1],0), width=pixel_width)
				
				#B
				d1.line([(x_count+(2*pixel_width),y_count), (x_count+(2*pixel_width),(y_count+pixel_height-1))], (0,0,color[2]), width=pixel_width)
				
				x_count+=block
	
			x_count = 0
			y_count+=block
			
			
	else:
		#vertical pixel alignment
		for a in range(0, y_orig):
			for b in range(0, x_orig):
				color = img.getpixel((b,a))			
				
				#R
				
				d1.line([(x_count, y_count), (x_count+(pixel_width-1), y_count)], (color[0],0,0), width=pixel_height)
				
				#G
				d1.line([(x_count, y_count+pixel_height), (x_count+(pixel_width-1), y_count+pixel_height)], (0,color[1],0), width=pixel_height)
				
				#B
				d1.line([(x_count, y_count+(2*pixel_height)), (x_count+(pixel_width-1), y_count+(2*pixel_height))], (0,0,color[2]), width=pixel_height)
				
				x_count+=block
	
			x_count = 0
			y_count+=block
			

if __name__ == "__main__":

	#Check if source file exists
	if os.path.isfile(source):
		fn, fext = os.path.splitext(source)
		
		t = datetime.datetime.now()
		new_fn = fn + ext + '_' + t.strftime("%d-%m-%Y_%H-%M-%S")

		#Check if source file format is supported
		if (fext in valid_formats) or (str.lower(fext) in valid_formats):
			
			print(f'Found image {source}')
			print('Starting process...')
			main(source)
			print(f'Result saved as {new_fn}{export_fformat}')
			
		else:
			print(f'{fext} file is not supported. \nSupported formats are: {valid_formats}')

	else:
		print(f'Couldn\'t find the image {source}')
