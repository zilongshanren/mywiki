---
title: 'GM Shaders: Noise 3'
url: https://mini.gmshaders.com/p/noise3
author: Xor
published: '2024-01-13'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

Hello people, Today we're going to go over some common noise functions. These are useful all kinds of effects, like smoke, water, fire, clouds, terrain and so much more. Tutorial Difficulty: Intermediate

Hi folks, Last week we went over 3 common noise algorithms. Today we will continue where we left off and show 3 more! Worley, Voronoi, and fractal noise. Tutorial Difficulty: Intermediate

It’d be a good idea to make sure you’re comfortable with those topics before reading this one. We’re going to be continuing where we left off, so some of that knowledge will be useful here. Today, we start with Simplex noise!

Simplex Noise

This algorithm was also created by Ken Perlin, building off of the concept of Perlin Noise, but being cheaper to compute in higher dimensions and producing fewer artifacts. Perlin Noise requires sampling gradients 4 times per pixel in 2D, 8 times in 3D, 16 times in 4D or generally 2^N samples per pixel. Simplex noise uses 3 samples in 2D, 4 in 3D, 5 in 4D or generally N+1 samples per pixel. It’s a little more complex than Perlin Noise, so you may not see any performances gains in 2D, but it may be with while in 3D or 4D. We’ll just look at the 2D case for now because it’s easier to understand.

Step 1: Skew

The first step is to squeeze our position coordinates (“p”) diagonally so that square cells become rhombuses. To do that, we can just add our diagonal vector which is p.x+p.y, multiplied by some factor “F”, to our coordinates:

vec2 skew = p+F*(p.x+p.y);

“F” controls the amount of skewing.

Square grid to rhombus grid

The goal here is to skew it so that each rhombus is composed of two equilateral triangles. With a triangle grid, we only have 3 corners in each cell instead of 4! The skew factor should be 0.366025403784 which is rather hard to derive, so we won’t cover here. Just know that it’s the perfect factor for breaking squares into triangles. Here’s the full code, along with another factor we’ll need later:

//Skewing and "unskewing" constants as decribed here:
//https://en.wikipedia.org/wiki/Simplex_noise
//N = dimensions, in this case: 2
//Skewing factor for triangular grid
#define F 0.366025403784 //(sqrt(N+1.0)-1.0)/N
//Reverse skewing factor for square grid
#define G 0.211324865405 //(1.0 - 1.0/sqrt(N+1.0))/N
//Skew sample position to Simplex grid
vec2 skew = p+F*(p.x+p.y);

Now let’s break these into cells.

Note: A Simplex is the generalized family of shapes like triangles in 2D, Tetrahedrons in 3D and so on in any dimension. This is why it’s called Simplex Noise.

Step 2: Cells

With Perlin Noise, we divide coordinates into square cells using floor(p). If we want a triangle grid, we have to split these cells in half along the cell’s diagonal:

//Break into cells
vec2 cell = floor(skew);
//Subcell coordinates, same as fract(skew)
vec2 sub = skew - cell;
//Pick end vertex depending on what cell half the sample position is in.
vec2 end = sub.x>sub.y ? vec2(1,0) : vec2(0,1);

“cell” is the cell coordinates, so the top-left cell is (0,0), the next cell to the right is (1,0) and so on. “sub” here are the coordinates within the cell, ranging from 0 to 1.

“end” is the nearest far end point, which depends on which half of the cell we’re currently in. Here’s what that looks like:

Dividing the square cells in half to make triangles, then skewing

As you can see, when skewing it, we have perfect triangles. Within each cell, the vertices are top-left, (0,0) and bottom-right for both (1,1) triangles and either top-right (1,0) or bottom-left (0,1) depending on which half we’re in.

Step 3: Points

For computing gradients later, we’ll need the relative position of the vertices from the current sample point, p. With a square grid, that is as simple as: p-cell-vert, with vert being (0,0), (1,0), (0,1) or (1,1). But for a skewed Simplex grid, it’s a little more complicated:

Don’t worry about that math of this too much, since it uses those fancy constants from earlier. All you need to know here is that this computes the relative position of the 3 nearest vertices on this grid. If you want to dig deeper, then see the Wikipedia page.

Step 4: Weights

To compute the weights for each sample point, we use the square of the distance to those points:

We want the weight of each sample to diminish as we get further from the sample point, so that when we’re at the other side of the triangle, the opposite point will have no weight. If it did, we’d have hard edges at the boundaries of the cells. Each cell has to start where the adjacent cell ended, and cannot extend beyond its boundaries without requiring more samples. Using the “F” skew factor, each point can start at 0.5 and diminish with our square distances. We can compute all three at once using a vec3:

//Compute gradient weights using distance to points
vec3 w = max(0.5 - vec3(d0, d1, d2), 0.0);
//Raise to 4th power
w *= w*w*w;

Raising the falloff to the fourth power here gives a nice smooth falloff and here’s what that looks like:

Sample weights color coded with the (0,0) vertices in red, end points in green and (1,1) vertices in blue.

Now that we have smoothly blending weights, we can blend the gradients.

Step 5: Gradients

We just need to sample the gradients, just like Perlin Noise, for each point and sum them up with our weight factors. By packing the gradients into a vec3, we can do the summing in one step with a dot product. Here’s what that looks like:

//Compute gradients for each point
vec3 g;
g.x = dot(noise2(cell )*2.0-1.0, p0);
g.y = dot(noise2(cell+end)*2.0-1.0, p1);
g.z = dot(noise2(cell+1.0)*2.0-1.0, p2);
//Sum gradients with their weights
return 0.5+dot(g,w)*32.0;
//32 here is the noise contrast factor
//The weights are at most 1/16th, but 32 was an arbitrary pick

noise2 can be a simple white noise or hash function that returns a vec2 in the 0 to 1 range. We have to map it to the -1 to +1 range so that our gradients can be oriented in any direction. Finally, we add 0.5 so that we bring the total back to 0 to 1 range and multiply it by some contrast factor. I find that 32 looks good. In the end, you should get something like this:

Nice Simplex Noise!

I’ve also made a ShaderToy demo here! The best part about Simplex noise is that it generalizes well in higher dimensions. If you want to attempt 3D, I recommend checking out this guide.

Functions vs Textures

Simplex Noise is a great solution for improving performance in higher dimensions, however it might not be worth it in 2D, so what other options do we have for optimization? Sometimes it’s better to just bake your noise onto a texture and read from that, rather than doing all the calculations in your fragment shader every time. Let’s look at the positives and negatives of both options:

Functions

+Virtually unlimited range, without repeating +Full dynamic, allowing for real-time animations or inputs +Lower video memory usage +High precision and smooth +Extends to any dimensions -Can be costly, especially with fractal noise -Inconsistent on across devices and hardware -Has visual artifacts occasionally

So overall functions are more versatile in dynamic usage, but generally more costly and inconsistent. How about textures?

Textures

+Can bake any complex noise function +Relatively cheap for advanced noise algorithms +Consistent on all devices +Fewer visual artifacts +Can be hand edited -Harder to animate efficiently -Uses more video memory and texture samples -Limited range and usually has to be tillable -Texture interpolation is blocky

Textures are generally faster and give you more direct control, but you have to work around the limits of the texture size. If you do decide to go the texture route, you’ll probably need a way to generate tillable noise, so let’s go over that now!

Noise Tiling

The general idea is that you want to stick with a square grid, because we’re working with square textures. That means no Simplex Noise and no octave rotation if you’re doing fractal noise. Keep everything neat and square, Then when you’re sampling the hash/noise for each cell corner, modulo it first. That’s basically all there is to it.

Here’s my basic value noise function from the first tutorial, with modulo tiling:

//Tillable value noise
//s - tile size (e.g. a value of 8 means it tiles every 8 units)
float value_noise(vec2 p, vec2 s)
{
//Cell (whole number) coordinates
vec2 cell = floor(p);
//Sub-cell (fractional) coordinates
vec2 sub = p - cell;
//Cubic interpolation (use sub for linear interpolation)
vec2 cube = sub*sub*(3.-2.*sub);
//Offset vector
const vec2 off = vec2(0,1);
//Sample cell corners and interpolate between them.
return mix( mix(hash1(mod(cell+off.xx,s)), hash1(mod(cell+off.yx,s)), cube.x),
mix(hash1(mod(cell+off.xy,s)), hash1(mod(cell+off.yy,s)), cube.x), cube.y);
}

So for example, if you want 512x512 texture, you might do:

To modify our fractal noise function, instead of rotating octaves, we can just swap the x and y axes and add some position offset:

//Generate fractal value noise from multiple octaves
//s - tile size (e.g. a value of 8 means it tiles every 8 units)
//oct - The number of octave passes
//per - Octave persistence value (should be between 0 and 1)
float fractal_noise(vec2 p,vec2 s, int oct, float per)
{
float noise_sum = 0.0; //Noise total
float weight_sum = 0.0; //Weight total
float weight = 1.0; //Octave weight
for(int i = 0; i < oct; i++) //Iterate through octaves
{
//Add noise octave to total
noise_sum += value_noise(p,s) * weight;
//Add octave weight to total
weight_sum += weight;
//Reduce octave amplitude with persistence value
weight *= per;
//Rotate, scale and translate for next octave
p = p.yx*2.0+9.0;
s *= 2.0;
}
//Compute weighted average
return noise_sum / weight_sum;
}

gpu_set_texrepeat(true) is your friend here! Here’s a ShaderToy demo for both of these examples. This same method works for Perlin, Worley and Voronoi noise, but I leave those for you to work out if you want. The neat part about tillable noise, is you can compute it once and save it to a texture, so you don’t have to recalculate it for every pixel every frame!

Conclusion

Wow, we covered a lot today! Simplex noise is ideal for higher dimension noise like in 3D or 4D because it uses less hash/noise samples. The process of converting to Simplex coordinates is a rather interesting topic in its own right because it can have many applications in different places. In essence, Simplex noise is like Perlin Noise that has been skewed so that each point has fewer neighboring cells to sample from, and that’s what makes it so powerful. Sometimes, your noise functions are just too costly and in those cases it might be a good idea to look into baking your noise onto textures so it doesn’t need to be recomputed all the time. Another reason you might prefer textures to functions is that they are consistent across all devices, but that call must be made on a case by case basis. Finally, we looked at making noise functions tillable. It’s really easy to make value, Perlin, Worley or Voronoi noise tillable. Anything that works with square cells, should be tillable, as long as you keep it orientated and scaled correctly. I think that just about covers it!

Subscribe for more, maybe?

Extras

Gabor Noise is another interesting algorithm which is good for making wavy patterns. I don’t plan on covering that in my series, so this is the best place to read about it.