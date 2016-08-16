import Image # Make and show images
import random # Pseudo random number library
import numpy
import math

featuresize = 10

def lerp(val,lower,upper):
	res = lower*(1-val) + upper*val
	return res

def lerp2d(x,y,ul,ur,ll,lr):
	x1 = lerp( x, ul, ur )
	x2 = lerp( x, ll, lr )
	return lerp( y, x1, x2 )

def perlin(x,y):
	
	xfrac = float(x)/featuresize
	yfrac = float(y)/featuresize

	# Find our closest feature node
	x0 = math.floor(x/featuresize)
	y0 = math.floor(y/featuresize)

	x1 = x0 + 1
	y1 = y0 + 1

	#val = int(lerp( xfrac - x0, table[x0,y0], table[x1,y0]))
	val = int( lerp2d( xfrac - x0, yfrac - y0, table[x0,y0], table[x1,y0], table[x0,y1], table[x1,y1] ) )
	return ( val, val, val );

# Generate a random map
table = numpy.empty( shape=(1000,1000) )

for i in range(1000):    # for every pixel:
    for j in range(1000):
        table[i,j] = random.randint( 0, 255 )

# Create a new image 255x255px and fill it with black pixels initially
img = Image.new( 'RGB', (255, 255), "black")

# Gets the pixelmap from the image
pixels = img.load()

# Fill in pixels with a pretty colour
for j in range(img.size[1]):
	for i in range(img.size[0]):    # for every pixel:
		pixels[i,j] = perlin( i, j )

img.show()


