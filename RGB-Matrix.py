from PIL import Image, ImageDraw, ImageChops
import sys, os, datetime, argparse


ext = '_rgb-matrix' # filename extension for the output file

pixel_width = 1 # width of each pixel - so three units (rgb) of this value must go into one block
pixel_height = 3 # height of the pixels (value must go into one block)
block = 4 # block width - 1 block contains one red, one greed and one blue pixel - black space inclusive

black = 0 # shift black to simulate display backlight

valid_formats = ['.bmp', '.jpeg', '.jpg', '.png', '.tiff', '.tif', '.webp']

counter = 1

fn_list = []
fext_list = []

output_path = ''
fn = ''
fext = ''
new_fn = ''


# argparse
parser = argparse.ArgumentParser(description='Render a display RGB matrix from a source image.')
parser.add_argument('file', type=str, metavar='', help='Filename of a single Source-Image, or a directory for batch processing.')
parser.add_argument('-w', '--width', type=int, metavar='', help='Width of each individual Pixel (R-G-B).')
parser.add_argument('-H', '--height', type=int, metavar='', help='Height of each individual Pixel (R-G-B).')
parser.add_argument('-b', '--block', type=int, metavar='', help='Block-Size defines the overall size of the repeated Pixel-Pattern')
parser.add_argument('-B', '--black', type=int, metavar='', help='Shift brightness of black pixels to simulate backlight shining; 0 = black 100 = white')
parser.add_argument('-rw', '--resizeWidth', type=int, metavar='', help='Resize width of source image. (For processing only)')
parser.add_argument('-rh', '--resizeHeight', type=int, metavar='', help='Resize height of source image. (For processing only)')
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


def main(source):
	resized = False
	img = Image.open(source)

	#Convert to RGB if necessary
	if img.mode == 'CMYK':
		img = img.convert('RGB')
	
	# Resize
	# Check if values for resizing are set
	if isinstance(args.resizeWidth, int) or isinstance(args.resizeHeight, int):
		
		x_orig, y_orig = img.size
		
		# If both values are set
		if isinstance(args.resizeWidth, int) and isinstance(args.resizeHeight, int):
			if args.resizeWidth > 0 and args.resizeHeight > 0:
				resize_size = (args.resizeWidth, args.resizeHeight)
				img = img.resize(resize_size)
				resized = True
			else:
				print('Please enter a valid value >0')
		# If only width is set
		elif isinstance(args.resizeWidth, int):
			if args.resizeWidth > 0:
				factor = x_orig / args.resizeWidth
				newH = int(y_orig / (x_orig / args.resizeWidth))
				resize_size = (args.resizeWidth, newH)
				img = img.resize(resize_size)
				resized = True
			else:
				print('Please enter a valid value >0')
		# If only height is set
		else:
			if args.resizeHeight > 0:
				factor = y_orig / args.resizeHeight
				newW = int(x_orig / (y_orig / args.resizeHeight))
				resize_size = (newW, args.resizeHeight)
				img = img.resize(resize_size)
				resized = True
			else:
				print('Please enter a valid value >0')
			

	x_orig, y_orig = img.size

	x_new = x_orig*block
	y_new = y_orig*block

	#Create new Image
	i1 = Image.new('RGB', (x_new,y_new))
	d1 = ImageDraw.Draw(i1)

	# Shift black color values if desired
	if black != 0:
		img = chop(img, img.size)

	# Start main process
	process(img, d1, x_orig, y_orig)
	
	
	# Save Image
	#t = datetime.datetime.now()
	#new_fn = fn + ext + '_' + t.strftime("%d-%m-%Y_%H-%M-%S")
	new_fn = fn + ext
	print(f'Image {counter}/{len(fn_list)}')
	if not resized:
		print(f'RGB-Matrix saved as {new_fn}.png')
	else:
		print(f'Resized to {resize_size[0]}x{resize_size[1]}px\nRGB-Matrix saved as {new_fn}.png')
	print(40*'_'+'\n')

	i1.save(output_path + new_fn + '.png', 'PNG')
	
	resized = False


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
		fn_list.append(fn)

		# Check if source file format is supported
		if (fext in valid_formats) or (str.lower(fext) in valid_formats):
			
			print(f'Found image {source}')
			print('Starting process...')
			print(40*'_'+'\n')
			main(source)
			
		else:
			print(f'{fext} file is not supported. \nSupported formats are: {valid_formats}')
	
	# Folder as source
	elif os.path.isdir(source) or os.path.isdir('./' + source):
		
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
					print(40*'_'+'\n')
					
					for file in range(0, len(fn_list)):
						fn = fn_list[file]
						fext = fext_list[file]
						output_path = source + '/'
						main(output_path+fn+fext)
						counter+=1
					
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
