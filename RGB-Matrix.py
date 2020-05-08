from PIL import Image, ImageDraw, ImageChops
import sys, os, datetime, argparse


# Standard values
export_fformat = '.jpg' # Output-Format
export_fformats = {'.jpg': 'JPEG', '.png': 'PNG'}

ext = '_rgb-matrix' # filename extension for the output file

pixel_width = 2 # width of each pixel - so three units (rgb) of this value must go into one block
pixel_height = 5 # height of the pixels (value must go into one block)
block = 7 # block width - 1 block contains one red, one greed and one blue pixel - black space inclusive

black = 0 # shift black to simulate display backlight

valid_formats = ['.bmp', '.jpeg', '.jpg', '.png', '.tiff', '.tif', '.webp']

output_path = ''
fn = ''
fext = ''
new_fn = ''


# argparse
parser = argparse.ArgumentParser(description='Render a display RGB matrix from a source image.')
parser.add_argument('file', type=str, metavar='', help='Filename of a single Source-Image, or a directory for batch processing.')
parser.add_argument('-f', '--format', type=str, metavar='', help='Export File-Format (.jpg or .png)')
parser.add_argument('-w', '--width', type=int, metavar='', help='Width of each individual Pixel (R-G-B).')
parser.add_argument('-H', '--height', type=int, metavar='', help='Height of each individual Pixel (R-G-B).')
parser.add_argument('-b', '--block', type=int, metavar='', help='Block-Size defines the overall size of the repeated Pixel-Pattern')
parser.add_argument('-B', '--black', type=int, metavar='', help='Shift brightness of black pixels to simulate backlight shining - otherwise no pixels are visible in black areas. Value between 0-100 (0 = black 100 = white)')
args = parser.parse_args()

source = args.file # Source image filename


# error correction for bad input values
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

if isinstance(args.black, int):
	if args.black in range(0, 101):
		black = args.black
	else:
		print("Value for -B --black must be between 0 and 100.")
		exit()


# Test if desired output file format is supported
if isinstance(args.format, str):
	if args.format in export_fformats:
		export_fformat = args.format
	else:
		print("Unsupported Fileformat.")
		exit()


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

	if black != 0:
		img = chop(img, img.size)

	process(img, d1, x_orig, y_orig)
	
	#t = datetime.datetime.now()
	#new_fn = fn + ext + '_' + t.strftime("%d-%m-%Y_%H-%M-%S")
	new_fn = fn + ext
	print(f'Image saved as {new_fn}{export_fformat}')

	i1.save(output_path + new_fn + export_fformat, export_fformats[export_fformat])


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


# superimpose source image with grey image
def chop(image, size):

	bg_color = int((255 / 100) * black)

	#Create new Image
	image_new = Image.new('RGB', size, (bg_color, bg_color, bg_color))
	result = ImageChops.screen(image, image_new)
	return result
			

if __name__ == "__main__":

	# Check if source image exists
	if os.path.isfile(source):
		fn, fext = os.path.splitext(source)

		# Check if source file format is supported
		if (fext in valid_formats) or (str.lower(fext) in valid_formats):
			
			print(f'Found image {source}')
			print('Starting process...')
			main(source)
			
		else:
			print(f'{fext} file is not supported. \nSupported formats are: {valid_formats}')
	
	# Folder as source
	elif os.path.isdir(source) or os.path.isdir('./' + source):
		counter = 1
		fn_list = []
		fext_list = []
		for file in os.listdir(source):
			fn, fext = os.path.splitext(file)
			
			# Check if source file format is supported
			if (fext in valid_formats) or (str.lower(fext) in valid_formats):
				fn_list.append(fn)
				fext_list.append(fext)
		
		if len(fn_list)>=1:
			status = True
			yes = ['yes', 'y', '']
			no = ['no', 'n']
			
			# Ask to start batch process
			while status:
				choice = input(f'{len(fn_list)} images fount - start process now? (y/n)').lower()
				
				if choice in yes:
					print('Batch process started...')
					
					for file in range(0, len(fn_list)):
						fn = fn_list[file]
						fext = fext_list[file]
						output_path = source + '/'
						main(output_path+fn+fext)
					
					print('Batch process finished!')
						
					status = False
					
				elif choice in no:
					print('exiting')
					status = False
					
				else:
					print('Please answer with yes/no (y/n).')
					
		else:
			print(f'No supported images found. \nSupported formats are: {valid_formats}')

	else:
		print(f'File not found: {source}')
