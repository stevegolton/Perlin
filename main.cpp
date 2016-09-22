#include <stdio.h>
#include <CImg.h>
#include <stdint.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#define WIDTH			1024
#define HEIGHT			1024
#define FEATURESIZE		256		// Should be a power of 2
#define PI (3.141592653589793)

static float aaafGradient[WIDTH+1][HEIGHT+1][2];

float cosinterpf( float y1, float y2, float mu )
{
	float mu2 = (1-cosf(mu*PI))/2;
	return(y1*(1-mu2)+y2*mu2);
}

float dotGridGradient( int ix, int iy, float x, float y)
{
	float dx, dy;

	// Compute the distance vector
	dx = x - (float)ix;
	dy = y - (float)iy;

	// Compute the dot-product
	return dx*aaafGradient[iy][ix][0] + dy*aaafGradient[iy][ix][1];
}

float perlin(float x, float y)
{
	int x0, y0, x1, y1;
	float sx, sy;
	float n0, n1, ix0, ix1, value;

	// Find our closest feature node
	x0 = floor(x);
	y0 = floor(y);

	/*
	if ( x <= 0.0 )
		x0 -= 1;
	if ( y <= 0.0 )
		y0 -= 1;
		*/

	x1 = x0 + 1;
	y1 = y0 + 1;

	// Interpolation weights
	sx = x - x0;
	sy = y - y0;

	n0 = dotGridGradient(x0, y0, x, y);
	n1 = dotGridGradient(x1, y0, x, y);
	ix0 = cosinterpf(n0, n1, sx);

	n0 = dotGridGradient(x0, y1, x, y);
	n1 = dotGridGradient(x1, y1, x, y);
	ix1 = cosinterpf(n0, n1, sx);

	value = cosinterpf(ix0, ix1, sy);

	return value;
}

int main( void )
{
	uint8_t *pui8Start;
	int iX, iY;
	float fX, fY, fM;
	float fVal;
	float fAmp;
	int k;

	// Seed the random number generator
	//srand( time( NULL ) );
	srand( 0 );

	for (iX = 0; iX < HEIGHT+1; iX++)
	{
		for (iY = 0; iY < WIDTH+1; iY++)
		{
			fX = (float)rand()/(float)RAND_MAX;
			fX -= 0.5f;

			fY = (float)rand()/(float)RAND_MAX;
			fY -= 0.5f;

			fM = sqrtf( fX*fX + fY*fY );

			aaafGradient[iX][iY][0] = fX / fM;
			aaafGradient[iX][iY][1] = fY / fM;
		}
	}

	// Create a new cimg object
	cimg_library::CImg<unsigned char> cimgImage( WIDTH, HEIGHT, 1, 1, 0);

	// Populate the pixels
	pui8Start = cimgImage.data();

	for (iX = 0; iX < HEIGHT; iX++)
	{
		for (iY = 0; iY < WIDTH; iY++)
		{
			fVal = 0.0f;
			fAmp = 1.0f;
			k = FEATURESIZE;

			while (k >= 1)
			{
				fVal += perlin( (float)iX/k, (float)iY/k ) * fAmp;
				k /= 2;
				fAmp /= 2;
			}

			*pui8Start = 128 * ( fVal + 1.0 );
			pui8Start++;
		}
	}

	cimgImage.save("/tmp/perlin.png");

	// Display thie image
	cimg_library::CImgDisplay disp_raw(cimgImage, "Perlin Noise");

	while (!disp_raw.is_closed())
	{
		// All the interactive code is inside the event loop
		cimg_library::CImgDisplay::wait(disp_raw);
	}

	return 0;
}
