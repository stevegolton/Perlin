import Image # Make and show images
import random # Pseudo random number library
import numpy
import math

# guide showing types of interpolation http://paulbourke.net/miscellaneous/interpolation/

# should be power of 2
featuresize = 64

# val should be in the range 0.0 - 1.0
def lerp( lower, upper, val ):
	return lower*(1-val) + upper*val

def cosinterp( y1, y2, mu ):
	mu2 = (1-math.cos(mu*math.pi))/2;
	return(y1*(1-mu2)+y2*mu2)

def dotGridGradient(ix, iy, x, y):
	# Compute the distance vector
	dx = x - float(ix);
	dy = y - float(iy);
 
	# Compute the dot-product
	return dx*gradient[iy,ix,0] + dy*gradient[iy,ix,1]

def perlin(x,y):
	
	# Find our closest feature node
	x0 = math.floor(x)
	y0 = math.floor(y)

	if ( x <= 0.0 ):
		x0 -= 1
	if ( y <= 0.0 ):
		y0 -= 1

	x1 = x0 + 1
	y1 = y0 + 1

	# Interpolation weights
	sx = x - x0
	sy = y - y0

	n0 = dotGridGradient(x0, y0, x, y);
	n1 = dotGridGradient(x1, y0, x, y);
	ix0 = cosinterp(n0, n1, sx);

	n0 = dotGridGradient(x0, y1, x, y);
	n1 = dotGridGradient(x1, y1, x, y);
	ix1 = cosinterp(n0, n1, sx);

	value = cosinterp(ix0, ix1, sy)
	
	return value

# Generate a random map
gradient = numpy.empty( shape=(500,500,2) )

for i in range(500):    # for every node:
    for j in range(500):
		x = random.uniform(-1.0, 1.0)
		y = random.uniform(-1.0, 1.0)
		m = math.sqrt(x*x + y*y)
		gradient[i,j,0] = x / m
		gradient[i,j,1] = y / m

# Create a new image 255x255px and fill it with black pixels initially
img = Image.new( 'RGB', (200, 200), "black")

# Gets the pixelmap from the image
pixels = img.load()

# Fill in pixels with a pretty colour
for j in range(img.size[1]):
	for i in range(img.size[0]):    # for every pixel:
		val = 0.0
		a = 1.0
		k = featuresize
		
		while (k >= 1):
			val += perlin( float(i)/k, float(j)/k ) * a
			k /= 2
			a /= 2

		pval = int( 128 * ( val + 1.0 ) )

		pixels[i,j] = ( pval, pval, pval )

img.show()

