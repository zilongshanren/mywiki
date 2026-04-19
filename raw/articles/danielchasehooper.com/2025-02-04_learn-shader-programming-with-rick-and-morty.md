---
title: Learn Shader Programming with Rick and Morty
url: https://danielchasehooper.com/posts/code-animated-rick/
published: '2025-02-04'
source_blog: Daniel Hooper
source_site: https://danielchasehooper.com/
category: graphics
fetched: '2026-04-19'
---

February 4, 2025

This animation of Rick was made with 240 lines of code. No libraries, no images. I’m going to show you how to use GPU shaders and signed distance fields to make animations like it for videos, video games, or just for fun! I even built a live coding editor into the page so you can see the examples running and tinker with them.

```
vec2 rotateAt(vec2 p, float angle, vec2 origin) {
float s = sin(angle), c = cos(angle);
return (p-origin)*mat2( c, -s, s, c ) + origin;
}
float map(float value, float inMin, float inMax, float outMin, float outMax) {
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) {
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) {
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) {
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) {
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) {
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) {
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) {
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
#define H(i,j) fract(sin(dot(ceil(P+vec2(i,j)), resolution.xy )) * 4e3)
float N( vec2 P) {
float s,i,w = .5;
for (; i < 3. ; i++, w *= .4, P *= 1.9 ) {
vec2 F = fract( P *= mat2(.866,-.5,.5,.866) );
F *= F*(3.-F-F);
s += w* mix( mix(H(0,0) , H(1,0), F.x),
mix(H(0,1) , H(1,1), F.x),
F.y );
}
return s;
}
vec3 portal(vec2 pixel, float time) {
float l = length( pixel ),
a = atan(pixel.y, pixel.x) / 6.28 + .5,
k = 10.;
a = fract(a + l*.3 - time*.01 );
vec2 U = vec2( l+time*.3, a );
return vec3[]( vec3(.18, .53, .09),
vec3(.56, .89, .16),
vec3(.35, .84, .11),
vec3(.92, .98, .85)
) [ int( 4.* pow( mix( N(U*k), N(U*k-vec2(0,k)), U.y) * 1.5, 2.5))];
}
vec3 color_for_pixel(vec2 pixel, float time) {
{
// rotate the whole drawing
pixel = rotateAt(pixel, sin(time*2.)*.1, vec2(0,-.6));
pixel.y += .1;
// Blink eyes
if (mod(time+1., 3.) < .09) {
// closed eyes
float d = round_rect(pixel+vec2(.07,-.16), vec2(.24,0), vec4(0));
if (d < .008) return vec3(0);
}
else {
// move pupils randomly
vec2 pupil_warp = pixel + vec2(.095,-.18);
pupil_warp.x -= noise(vec2(round(time)*7.+.5, 0.5))*.1;
pupil_warp.y -= noise(vec2(round(time)*9.+.5, 0.5))*.1;
pupil_warp.x = abs(pupil_warp.x) - .16;
float d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
}
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// `map()` is used to change the thickness of
// the tongue along the x axis
vec2 tongue = rotateAt(pixel, sin(time*2.-1.5)*.15+.1, vec2(0,-.5));
float tongue_thickness = map(tongue.x, -.16, .01, .02, .045);
d = bezier(tongue,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
// NEW animate the middle up and down
vec2(-.05, 0.5 + cos(time)*.1),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
// Hair
float twist = sin(time*2.-length(pixel)*2.1)*.12;
vec2 hair = rotateAt(pixel, twist, vec2(0.,.1));
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(d, -0.012);
}
}
return portal(pixel, time);
}
```


This is the editor I used to create Pixel Rick. It updates after every code edit — try changing `green = 0.9`

to `green = 0.1`

.

```
vec3 color_for_pixel(vec2 pixel, float time) {
// fract returns fractional part. fract(1.3) == 0.3
float red = fract(pixel.y);
float green = 0.9;
float blue = fract(pixel.x);
return vec3(red, green, blue);
}
```


The code is written in OpenGL Shading Language (GLSL), and the `color_for_pixel`

function runs on your GPU for every pixel in the preview. Amazingly this is all you need to make animations — a function that answers “What color should this pixel be at this time?”.

Optional Challenge: What happens if you set `green = time`

? What could you do to make it keep going? (`time`

counts seconds since last edit)

To draw Rick, we’ll start with drawing a circle and build up to other shapes. Let’s use GLSL’s built in[1](https://danielchasehooper.com#fn:1)`length()`

function to visualize how far each pixel is from the origin at the center of the screen. By returning that distance as the pixel’s color, we get 0 (black) near the center, and fade to 1 (white) further away:

```
vec3 color_for_pixel(vec2 pixel, float time) {
return vec3(length(pixel));
}
```


GLSL Tip: `vec3(x)`

is the same as `vec3(x, x, x)`

. We’ll use this trick a lot.

To draw a circle, we compare the distance to a radius:

```
vec3 color_for_pixel(vec2 pixel, float time) {
float radius = 0.6;
return vec3(length(pixel) > radius);
}
```


GLSL Tip: `vec3`

turns the boolean result of `>`

into `1`

or `0`

.

What would that circle look like if you replaced `length()`

with your own function that calculates [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry)?

We can extract that into a reusable `circle()`

function:

```
float circle(vec2 pixel, float radius) {
return length(pixel) - radius;
}
vec3 color_for_pixel(vec2 pixel, float time) {
if (circle(pixel - vec2(.3, -.3), .4) < 0.0) {
return vec3(0.2,.7,.5);
}
if (circle(pixel - vec2(-.4,0), .8) < 0.0) {
return vec3(.7,.5, .3);
}
return vec3(.2);
}
```


The circles are positioned by shifting the pixel passed to `circle()`

. The line order of that code is important - it determines which circle appears in front of the other.

Notice that `circle()`

returns the *distance* to the perimeter instead of just a `bool`

to indicate inside/outside. This is known as a “signed distance field” (SDF) function. The word “signed” here means that the distances for locations inside the shape are negative, and positive outside. We’ll use the distance to achieve some cool effects in a bit.

There are [many SDF functions](https://iquilezles.org/articles/distfunctions2d/) besides `circle()`

. Here are a few we’ll be using:

```
// Click {...} to see the code
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
// from https://www.shadertoy.com/view/MlKcDD
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float star(vec2 p, float r, float points, float ratio) { // fold
// from https://www.shadertoy.com/view/3tSGDy
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en));
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
// from https://www.shadertoy.com/view/4llXD7
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
vec3 color_for_pixel(vec2 pixel, float time) {
if (bezier(pixel,
vec2(-.7,-.35),
vec2(-1.5,-.4),
vec2(-1.2,.35)) < 0.1)
return vec3(.9,.3,.3);
if (round_rect(pixel, vec2(.3, .4), vec4(.1)) < 0.0)
return vec3(.3, .9, .3);
if (star(pixel - vec2(1.,0.), .45, 5., .3) < 0.0)
return vec3(.2, .4, .9);
return vec3(1.0);
}
```


With those shapes in hand, let’s get started on Rick.

I wish I could tell you I had the ability to look at a cartoon and then effortlessly replicate it in code. Unfortunately, I don’t. I spent *a lot* of time painstakingly trying numbers to recreate Rick’s face from the season 1 poster.

I did find one trick that sped up the trial and error process: I flashed my reference image of Rick on top of the preview so I could compare my drawing to the original while I was changing the code. The editor below has that enabled so you can experience what my week has been like.

Change the size and corner radii parameters to make the rectangle match Rick’s head shape.

```
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
vec3 color_for_pixel(vec2 pixel, float time) {
float dist = round_rect(
pixel,
// Change these:
vec2(.3, .5), // size
vec4(.1, .01, .05, .1) // corner radii
);
if (dist < 0.)
return vec3(.838, 0.8, 0.76);
return vec3(1);
}
```


In case it isn’t obvious by now, the techniques in this article won’t be replacing your favorite vector drawing tool. This is the only time we’ll do the flashing exercise; just know that all the seemingly random numbers in the rest of this article were discovered via this process. I found the color values using an image editor’s eyedropper tool.

Ok, so here are the values I came up with for Rick’s head. I also added a second `round_rect()`

for his ear:

```
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
vec3 color_for_pixel(vec2 pixel, float time) {
vec3 skin_color = vec3(0.838, 0.799, 0.760);
// head
float dist = round_rect(
pixel,
vec2(.36, 0.6385),
vec4(.34, .415, .363, .315)
);
if (dist < 0.) return skin_color;
// ear
dist = round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13));
if (dist < 0.) return skin_color;
return vec3(1);
}
```


Let’s add the outline. This is where drawing with signed distance functions comes in handy. We can return black for pixels with a distance between -0.01 and 0.0.

```
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
vec3 color_for_pixel(vec2 pixel, float time) {
vec3 skin_color = vec3(0.838, 0.799, 0.760);
// head
float dist = round_rect(
pixel,
vec2(.36, 0.6385),
vec4(.34, .415, .363, .315)
);
if (dist < -0.01) return skin_color;
if (dist < 0.0) return vec3(0); // outline
// ear
dist = round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13));
if (dist < -0.01) return skin_color;
if (dist < 0.0) return vec3(0); // outline
return vec3(1); // background
}
```


That line between the ear and the head shouldn’t be there (according to my reference image of Rick). I don’t want to outline each shape individually, I want to outline the *union* of the shapes. Union is easy with SDFs - use `min()`

to combine two distances:

```
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
vec3 color_for_pixel(vec2 pixel, float time) {
float dist = min( // <- combine the shapes
// head
round_rect(
pixel,
vec2(.36, 0.6385),
vec4(.34, .415, .363, .315)),
// ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (dist < -0.01) return vec3(0.838, 0.799, 0.760);
if (dist < 0.0) return vec3(0);
return vec3(1);
}
```


There are [other ways](https://iquilezles.org/articles/distfunctions/#:~:text=Primitive%20combinations) to combine two signed distance fields. Try swapping out `min()`

for the smooth union function to smoothly blend the ear with the head.

Let’s draw an eye:

```
float circle(vec2 pixel, float radius) { // fold
return length(pixel) - radius;
}
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en));
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
// pupil
vec2 pupil_pos = pixel - vec2(.16-.13,.24);
// subtract 0.007 to outset & round the corners of star
if (star(pupil_pos, 0.019, 6., .9) - 0.007 < 0.0) {
return vec3(.1);
}
// eyeball
vec2 eyeball_pos = pixel;
eyeball_pos.y *= .93; // stretch vertically
eyeball_pos -= vec2(0.07, .16);
float dist = circle(eyeball_pos, .16);
if (dist < 0.0) return vec3(dist < -0.013);
// head
{ // fold
dist = min(
// head
round_rect(
pixel,
vec2(.36, 0.6385),
vec4(.34, .415, .363, .315)),
// ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (dist < -0.01) return vec3(0.838, 0.799, 0.760);
if (dist < 0.0) return vec3(0); // outline
}
return vec3(1.);
}
```


Two interesting things here:

`eyeball_pos.y *= .93`

stretches the eyeball a ```
float star(vec2 p, float r, float points, float ratio) { // fold
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en));
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float d = star(pixel, 0.4, 6., .5);
// show blue inside shape, orange outside
vec3 color = (d < 0.0) ? vec3(0.5, .8, 1.) : vec3(0.98,.6,.13);
color *= sin(d*150.)*.1+.8; // show distance field lines
color *= 1.0 - exp(-20.0*abs(d)); // darken near perimeter
float offset = (sin(time)+1.)*.25; // animate outline offset
if (abs(d-offset) < 0.01) return vec3(1.0); // draw white outline
return color;
}
```


For the second eye, we could duplicate the first eye’s code, but instead let’s mirror it horizontally with `pixel.x = abs(pixel.x)`

. To rationalize this, consider that if the point `(1, 0)`

is inside the circle, then it’s mirror `(-1, 0)`

will *also* be inside the circle after `pixel.x = abs(pixel.x)`

, so both points will get colored.

```
float circle(vec2 pixel, float radius) { // fold
return length(pixel) - radius;
}
vec3 color_for_pixel(vec2 pixel, float time) {
pixel.x -= .3; // controls position
pixel.x = abs(pixel.x); // mirror
pixel.x -= .7; // controls spacing
return vec3(circle(pixel, .5) > 0.0);
}
```


The way that order of operations works still hurts my head, but it helps to play with the code to get a feel for what’s going on.

Mirror the circles on both the x *and* the y axis

Here is the mirroring technique applied to Rick’s eyes:

```
float circle(vec2 pixel, float radius) { // fold
return length(pixel) - radius;
}
float round_rect(vec2 p, vec2 size, vec4 radii) { // fold
radii.xy = (p.x>0.0)?radii.xy : radii.zw;
radii.x = (p.y>0.0)?radii.x : radii.y;
vec2 q = abs(p)-size+radii.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - radii.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en));
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
// pupils
vec2 pupil_pos = pixel;
pupil_pos += vec2(.13, -.24); // position pupils on eyeballs
pupil_pos.x = abs(pupil_pos.x); // mirror pupils
pupil_pos.x -= .16; // pupil spacing
if (star(pupil_pos, 0.019, 6., .9) < 0.007) {
return vec3(.1);
}
// eyeballs
// position/mirror/scale one liner
vec2 eye_pos = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
float dist = circle(eye_pos, .16);
if (dist < 0.0) return vec3(dist < -0.013);
// head
{ // fold
dist = min(
// head
round_rect(
pixel,
vec2(.36, 0.6385),
vec4(.34, .415, .363, .315)),
// ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, .12),
vec4(.13, .1, .13, .13))
);
if (dist < -0.01) return vec3(0.838, 0.799, 0.760);
if (dist < 0.0) return vec3(0); // outline
}
return vec3(1);
}
```


Let’s skip ahead. The mouth, nose, and eyebrow are all created with `bezier()`

. The hair is an 11-point `star()`

that I stretched vertically.

```
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float circle(vec2 p, float r) { // fold
return length(p) - r;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float d;
// eyes
{ // fold
// pupils
vec2 pupil_warp = pixel;
pupil_warp.x = abs(pupil_warp.x +.13);
pupil_warp -= vec2(.16,.24);
d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) {
return vec3(step(0.013, -d));
}
}
// nose
d = min( // combine the curves
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// mouth
d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .12) {
// The `*step(d, .11)` creates the outline.
// it's the same as `*vec3(d < .11)`
// aka, it multiplies the color by zero for
// pixels near the perimeter
return vec3(.42, .147, .152)*step(d, .11);
}
// eyebrow
d = bezier(pixel,
vec2(-.34, .38),
vec2(-.05, .68),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
// head
{ // fold
float dist = min(
// head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (dist < -.01) return vec3(.838, .799, .76);
if (dist < 0.) return vec3(0); // outline
}
// hair
d = star((pixel-vec2(.08,.15))*vec2(1.3,1.), 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(0.012, -d);
}
return vec3(1.);
}
```


That’s as far as basic shape positioning, scaling, and outlining can get us.

The remaining steps will elevate our crude sketch of Rick into a drawing that looks exactly like him. We’ll learn a few more techniques to make this possible. First up: let’s fix his rigid looking hair. There isn’t a “wavy hair” signed distance function, but we can make the star shape more wavy using a technique called [domain warping](https://iquilezles.org/articles/warp/).

Domain warping randomly offsets pixel locations. That random offset is “seeded” by the pixel’s location, so the offset is consistent over time for any given location. You can use that warped location for whatever shapes you want warped. Here’s an 11-point star with and without warping:

```
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
// these functions are used by the `warp()` function
// to generate pseudo random numbers. The details aren't
// super important. I looked these functions up:
// https://www.shadertoy.com/view/XdXGW8
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) {
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
vec3 color_for_pixel(vec2 pixel, float time) {
vec2 warped_pixel = warp(pixel, 4., .07);
float d = min(
star(warped_pixel + vec2(.8,0), 0.7, 11., .28),
star(pixel - vec2(.8,0), 0.7, 11., .28)
);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929);
}
return vec3(1);
}
```


Visualize the warp offsets by drawing the x offset to the red channel and the y offset to the green channel

Fun fact: the Lord of the Rings movies [used domain warping](https://www.youtube.com/watch?v=6Koa50421Pg&t=1056s) to create the visual effect seen when Frodo is wearing the Ring. Their warp offsets came from tracking fire movement.

Animate the warp effect above to achieve the Lord of the Rings effect.

Rick needs teeth, a lot them. But we’ll start by drawing one. A parabola is the best tooth shape I could find:

```
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float d = parabola(pixel, 38.);
if (d < 0.) return vec3(0.902, 0.890, 0.729)*step(d, -.01);
return vec3(1);
}
```


Yes that is a tooth. Stick with me.

Is there a way to draw multiple teeth without duplicating a bunch of code, or using a `for`

loop? Yes! Similar to how we used `abs()`

to mirror shapes, we can use `mod()`

to repeat shapes. `mod(a,b)`

calculates the remainder of `a`

divided by `b`

. Look below at what `mod(pixel.x, 0.5)`

does. Every time `pixel.x`

increases above a multiple of `.5`

, `mod()`

starts back at zero (black) again.

```
vec3 color_for_pixel(vec2 pixel, float time) {
return vec3(mod(pixel.x, 0.5));
}
```


Here is `mod()`

applied to the single tooth

```
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float width = .065;
pixel.x = mod(pixel.x, width)-width*.5; // NEW: repeat horizontally
float d = parabola(pixel, 38.);
if (d < 0.) return vec3(0.902, 0.890, 0.729)*step(d, -.01);
return vec3(1);
}
```


Repeat the teeth [in a circle](https://iquilezles.org/articles/sdfrepetition/#:~:text=Rotational%20and%20Rectangular%20Repetition) instead of in a line to create a [sandworm mouth](https://duckduckgo.com/?q=sandworm&iax=images&ia=images)

and we can mirror that to get the bottom teeth

```
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float width = .065;
pixel.y = abs(pixel.y)-.06; // NEW: mirror vertically
pixel.x = mod(pixel.x, width)-width*.5; // repeat horizontally
float d = parabola(pixel, 38.);
if (d < 0.) return vec3(0.902, 0.890, 0.729)*step(d, -.01);
return vec3(1);
}
```


Then to make it a smile, we offset the y position of the tooth based on `pixel.x`

.

```
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float width = .065;
pixel.y -= pow(pixel.x, 2.); // NEW: curve into a smile
pixel.y = abs(pixel.y)-.06; // mirror vertically
pixel.x = mod(pixel.x, width)-width*.5; // repeat horizontally
float d = parabola(pixel, 38.);
if (d < 0.) return vec3(0.902, 0.890, 0.729)*step(d, -.01);
return vec3(1);
}
```


Kind of creepy. Reducing the infinite teeth down to 12 will make it a little less creepy — done by only drawing teeth when `pixel.x`

is within the desired range

```
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float width = .065;
vec2 teeth = pixel;
teeth.y -= pow(pixel.x, 2.);
teeth.y = abs(teeth.y)-.06;
teeth.x = mod(teeth.x, width)-width*.5;
float d = parabola(teeth, 38.);
if (d < 0.
// Limit where the teeth are drawn
&& pixel.x < width*3.
&& pixel.x > -width*3.
) {
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
}
return vec3(1);
}
```


Here’s Rick with wavy hair and new set of teeth. I also added the tongue. Notice that the tongue and teeth only draw inside the mouth thanks to placing their code inside the `if`

that checks the mouth distance.

```
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
float d;
// Mouth
d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// only draw the teeth and tongue inside hte mouth shape
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// Make the right side of the tongue thicker
float tongue_thickness = map(pixel.x, -.16, .01, .02, .045);
d = bezier(pixel,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
if (d < .12) // mouth outline
return vec3(0);
// Eyebrow, Eyes, Nose & Head
{ // fold
// Pupils
vec2 pupil_warp = pixel;
pupil_warp.x = abs(pupil_warp.x +.13);
pupil_warp -= vec2(.16,.24);
d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) {
return vec3(step(0.013, -d));
}
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
vec2(-.05, .68),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
}
// Hair
vec2 hair = pixel;
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(0.012, -d);
}
return vec3(1.);
}
```


The final bits needed are the curves below the eyes and around the mouth. Those lines are just like our normal shape outlines, except they’re offset away from the perimeter of the shape. This can be done by subtracting a little from distance when drawing the outline. In other words this:`if (abs(distance_to_shape) < thickness) return vec3(0);`


becomes this:`if (abs(distance_to_shape - outset) < thickness) return vec3(0);`


The blue line below illustrates that technique.

Since Rick’s under-eye lines should only be visible…under the eye, we’ll need to limit where they are drawn. That can be done using whatever logic you can think of, as shown by the green line:

```
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
vec3 color_for_pixel(vec2 pixel, float time) {
float dist = round_rect(pixel, vec2(.5), vec4(.1));
float thickness = .02;
// outline
if (abs(dist) < thickness)
return vec3(0);
// outset outline
if (abs(dist-.2) < thickness)
return vec3(.1,.1,1);
// limited outline
if (abs(dist-.4) < thickness && pixel.y < -.4)
return vec3(.1,.9,.1);
// fill
if (dist < 0.) return vec3(1);
return vec3(.92);
}
```


Here are those techniques applied to Rick:

```
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) { // fold
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// Make the right side of the tongue thicker
float tongue_thickness = map(pixel.x, -.16, .01, .02, .045);
d = bezier(pixel,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Pupils
{ // fold
vec2 pupil_warp = pixel;
pupil_warp.x = abs(pupil_warp.x +.13);
pupil_warp -= vec2(.16,.24);
d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
// Nose, Eyebrow, Head, Hair
{ // fold
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
vec2(-.05, .68),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
// Hair
vec2 hair = pixel;
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(0.012, -d);
}
}
return vec3(1);
}
```


Draw another character from Rick and Morty, or whatever your favorite cartoon is.

Use [raymarching](https://www.youtube.com/results?search_query=raymarching) with 3D signed distance fields to draw a 3D version of Rick. Let me know if you do this, I want to see.

With our drawing complete, there are several animation techniques we can use to introduce movement. First up:

The easiest way to add animation is to slap a `sin(time)`

into the code somewhere. The `sin`

is important because it wraps the ever-increasing `time`

value into the range of -1 to 1, which makes nice looping animations. You will often change that range with a scale and offset like so: `sin(time)*.5 + .5`

. The head angle, tongue angle, and eyebrow height are animated in this way. I added a `rotateAt`

function to do the rotation math.

```
vec2 rotateAt(vec2 p, float angle, vec2 origin) {
float s = sin(angle), c = cos(angle);
return (p-origin)*mat2( c, -s, s, c ) + origin;
}
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
// NEW: rotate the whole drawing
pixel = rotateAt(pixel, sin(time*2.)*.1, vec2(0,-.6));
pixel.y += .1;
// Mouth, eyes, nose
{ // fold
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
vec2 tongue = rotateAt(pixel, sin(time*2.-1.5)*.15+.1, vec2(0,-.5));
float tongue_thickness = map(tongue.x, -.16, .01, .02, .045);
d = bezier(tongue,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Pupils
vec2 pupil_warp = pixel;
pupil_warp.x = abs(pupil_warp.x +.13);
pupil_warp -= vec2(.16,.24);
d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
}
// Eyebrow
float d = bezier(pixel,
vec2(-.34, .38),
// NEW: animate the middle up and down
vec2(-.05, 0.5 + cos(time)*.1),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
// Head and hair
{ // fold
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
// Hair
vec2 hair = pixel;
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(0.012, -d);
}
}
return vec3(1.);
}
```


Animate Rick’s head as if he is walking left and right. Flip the face direction when he is moving to the right (this is easier than it sounds!).

Animating a property with `sin()`

just moves stuff around, but you can also draw something totally different based on time. We’ll do that to make Rick blink.

```
vec2 rotateAt(vec2 p, float angle, vec2 origin) { // fold
float s = sin(angle), c = cos(angle);
return (p-origin)*mat2( c, -s, s, c ) + origin;
}
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
{ // fold
// rotate the whole drawing
pixel = rotateAt(pixel, sin(time*2.)*.1, vec2(0,-.6));
pixel.y += .1;
}
// blink for .09 seconds, every 2 seconds
if (mod(time, 2.) < .09) { // closed eyes
float d = round_rect(pixel+vec2(.07,-.16), vec2(.24,0), vec4(0));
if (d < .008) return vec3(0);
}
else // open eyes
{ // fold
// Pupils
vec2 pupil_warp = pixel;
pupil_warp.x = abs(pupil_warp.x +.13);
pupil_warp -= vec2(.16,.24);
float d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
}
// Rest of face
{ // fold
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// `map()` is used to change the thickness of
// the tongue along the x axis
vec2 tongue = rotateAt(pixel, sin(time*2.-1.5)*.15+.1, vec2(0,-.5));
float tongue_thickness = map(tongue.x, -.16, .01, .02, .045);
d = bezier(tongue,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
// NEW animate the middle up and down
vec2(-.05, 0.5 + cos(time)*.1),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
// Hair
vec2 hair = pixel;
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(0.012, -d);
}
}
return vec3(1);
}
```


Use this technique to animate Rick’s mouth so it looks like he is talking.

If `sin`

is too smooth for you, try using noise! I used `noise()`

to make the eyes randomly look around. Since I don’t want the eyes to be continuously moving, I rounded the time value before passing it to `noise()`

.

```
vec2 rotateAt(vec2 p, float angle, vec2 origin) { // fold
float s = sin(angle), c = cos(angle);
return (p-origin)*mat2( c, -s, s, c ) + origin;
}
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
{ // fold
// rotate the whole drawing
pixel = rotateAt(pixel, sin(time*2.)*.1, vec2(0,-.6));
pixel.y += .1;
}
// Blink eyes
if (mod(time, 2.) < .09) { // fold
// closed eyes
float d = round_rect(pixel+vec2(.07,-.16), vec2(.24,0), vec4(0));
if (d < .008) return vec3(0);
}
else {
// move pupils randomly
vec2 pupil_warp = pixel + vec2(.095,-.18);
pupil_warp.x -= noise(vec2(round(time)*7.+.5, 0.5))*.1;
pupil_warp.y -= noise(vec2(round(time)*9.+.5, 0.5))*.1;
pupil_warp.x = abs(pupil_warp.x) - .16;
float d = star(pupil_warp, 0.019, 6., .9);
{// fold
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
}
}
// Rest of face
{ // fold
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// `map()` is used to change the thickness of
// the tongue along the x axis
vec2 tongue = rotateAt(pixel, sin(time*2.-1.5)*.15+.1, vec2(0,-.5));
float tongue_thickness = map(tongue.x, -.16, .01, .02, .045);
d = bezier(tongue,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
// NEW animate the middle up and down
vec2(-.05, 0.5 + cos(time)*.1),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
// Hair
vec2 hair = pixel;
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(0.012, -d);
}
}
return vec3(1);
}
```


Make the pupil movement [more realistic](https://www.youtube.com/watch?v=Fmg9ZOHESgQ) instead of jumping between positions

Our final animation technique is “time domain warping” to make the hair bend as the head tilts. It’s like domain warping, except instead of offsetting *space* we offset *time*. Basically we delay time more the closer to the hair tip a pixel is. Because that delay isn’t constant along the length of the hair, the hair will bend instead of rotate rigidly.

```
vec2 rotateAt(vec2 p, float angle, vec2 origin) { // fold
float s = sin(angle), c = cos(angle);
return (p-origin)*mat2( c, -s, s, c ) + origin;
}
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
vec3 color_for_pixel(vec2 pixel, float time) {
{ // fold
// rotate the whole drawing
pixel = rotateAt(pixel, sin(time*2.)*.1, vec2(0,-.6));
pixel.y += .1;
// Blink eyes
if (mod(time, 2.) < .09) {
// closed eyes
float d = round_rect(pixel+vec2(.07,-.16), vec2(.24,0), vec4(0));
if (d < .008) return vec3(0);
}
else {
// move pupils randomly
vec2 pupil_warp = pixel + vec2(.095,-.18);
pupil_warp.x -= noise(vec2(round(time)*7.+.5, 0.5))*.1;
pupil_warp.y -= noise(vec2(round(time)*9.+.5, 0.5))*.1;
pupil_warp.x = abs(pupil_warp.x) - .16;
float d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
}
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// `map()` is used to change the thickness of
// the tongue along the x axis
vec2 tongue = rotateAt(pixel, sin(time*2.-1.5)*.15+.1, vec2(0,-.5));
float tongue_thickness = map(tongue.x, -.16, .01, .02, .045);
d = bezier(tongue,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
// NEW animate the middle up and down
vec2(-.05, 0.5 + cos(time)*.1),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
}
// Hair
float twist = sin(time*2.-length(pixel)*2.1)*.12;
vec2 hair = rotateAt(pixel, twist, vec2(0.,.1));
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
float d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(d, -0.012);
}
return vec3(1);
}
```


Apply this trick to to other parts of Rick’s face for a rubbery and ricklaxed look.

After we add a portal effect 2 our animation is complete.

```
vec2 rotateAt(vec2 p, float angle, vec2 origin) { // fold
float s = sin(angle), c = cos(angle);
return (p-origin)*mat2( c, -s, s, c ) + origin;
}
float map(float value, float inMin, float inMax, float outMin, float outMax) { // fold
value = clamp(value, inMin, inMax);
return outMin + (outMax - outMin) * (value - inMin) / (inMax - inMin);
}
vec2 grad(ivec2 z) { // fold
int n = z.x+z.y*11111;
n = (n<<13)^n;
n = (n*(n*n*15731+789221)+1376312589)>>16;
n &= 7;
vec2 gr = vec2(n&1,n>>1)*2.0-1.0;
return ( n>=6 ) ? vec2(0.0,gr.x) :
( n>=4 ) ? vec2(gr.x,0.0) :
gr;
}
float noise(vec2 p) { // fold
ivec2 i = ivec2(floor(p));
vec2 f = fract(p);
vec2 u = f*f*(3.0-2.0*f);
return mix( mix( dot( grad( i+ivec2(0,0) ), f-vec2(0.0,0.0) ),
dot( grad( i+ivec2(1,0) ), f-vec2(1.0,0.0) ), u.x),
mix( dot( grad( i+ivec2(0,1) ), f-vec2(0.0,1.0) ),
dot( grad( i+ivec2(1,1) ), f-vec2(1.0,1.0) ), u.x), u.y);
}
vec2 warp(vec2 p, float scale, float strength) { // fold
float offsetX = noise(p * scale + vec2(0.0, 100.0));
float offsetY = noise(p * scale + vec2(100.0, 0.0));
return p + vec2(offsetX, offsetY) * strength;
}
float bezier(vec2 p, vec2 v0, vec2 v1, vec2 v2) { // fold
vec2 i = v0 - v2;
vec2 j = v2 - v1;
vec2 k = v1 - v0;
vec2 w = j-k;
v0-= p; v1-= p; v2-= p;
float x = v0.x*v2.y-v0.y*v2.x;
float y = v1.x*v0.y-v1.y*v0.x;
float z = v2.x*v1.y-v2.y*v1.x;
vec2 s = 2.0*(y*j+z*k)-x*i;
float r = (y*z-x*x*0.25)/dot(s,s);
float t = clamp( (0.5*x+y+r*dot(s,w))/(x+y+z),0.0,1.0);
vec2 d = v0+t*(k+k+t*w);
vec2 outQ = d + p;
return length(d);
}
float parabola(vec2 pos, float k) { // fold
// from https://www.shadertoy.com/view/ws3GD7
pos.x = abs(pos.x);
float ik = 1.0/k;
float p = ik*(pos.y - 0.5*ik)/3.0;
float q = 0.25*ik*ik*pos.x;
float h = q*q - p*p*p;
float r = sqrt(abs(h));
float x = (h>0.0) ?
pow(q+r,1.0/3.0) - pow(abs(q-r),1.0/3.0)*sign(r-q) :
2.0*cos(atan(r,q)/3.0)*sqrt(p);
return length(pos-vec2(x,k*x*x)) * sign(pos.x-x);
}
float round_rect(vec2 p, vec2 b, vec4 r) { // fold
r.xy = (p.x>0.0)?r.xy : r.zw;
r.x = (p.y>0.0)?r.x : r.y;
vec2 q = abs(p)-b+r.x;
return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}
float star(vec2 p, float r, float points, float ratio) { // fold
// next 4 lines can be precomputed for a given shape
float an = 3.141593/points;
float en = 3.141593/(ratio*(points-2.) + 2.);
vec2 acs = vec2(cos(an),sin(an));
vec2 ecs = vec2(cos(en),sin(en)); // ecs=vec2(0,1) for regular polygon
float bn = mod(atan(p.x,p.y),2.0*an) - an;
p = length(p)*vec2(cos(bn),abs(sin(bn)));
p -= r*acs;
p += ecs*clamp( -dot(p,ecs), 0.0, r*acs.y/ecs.y);
return length(p)*sign(p.x);
}
#define H(i,j) fract(sin(dot(ceil(P+vec2(i,j)), resolution.xy )) * 4e3)
float N( vec2 P) { // fold
float s,i,w = .5;
for (; i < 3. ; i++, w *= .4, P *= 1.9 ) {
vec2 F = fract( P *= mat2(.866,-.5,.5,.866) );
F *= F*(3.-F-F);
s += w* mix( mix(H(0,0) , H(1,0), F.x),
mix(H(0,1) , H(1,1), F.x),
F.y );
}
return s;
}
vec3 portal(vec2 pixel, float time) { // fold
// from https://www.shadertoy.com/view/l3f3zM
float l = length( pixel ),
a = atan(pixel.y, pixel.x) / 6.28 + .5,
k = 10.;
a = fract(a + l*.3 - time*.01 );
vec2 U = vec2( l+time*.3, a );
return vec3[]( vec3(.18, .53, .09),
vec3(.56, .89, .16),
vec3(.35, .84, .11),
vec3(.92, .98, .85)
) [ int( 4.* pow( mix( N(U*k), N(U*k-vec2(0,k)), U.y) * 1.5, 2.5))];
}
vec3 color_for_pixel(vec2 pixel, float time) {
{ // fold
// rotate the whole drawing
pixel = rotateAt(pixel, sin(time*2.)*.1, vec2(0,-.6));
pixel.y += .1;
// Blink eyes
if (mod(time, 2.) < .09) {
// closed eyes
float d = round_rect(pixel+vec2(.07,-.16), vec2(.24,0), vec4(0));
if (d < .008) return vec3(0);
}
else {
// move pupils randomly
vec2 pupil_warp = pixel + vec2(.095,-.18);
pupil_warp.x -= noise(vec2(round(time)*7.+.5, 0.5))*.1;
pupil_warp.y -= noise(vec2(round(time)*9.+.5, 0.5))*.1;
pupil_warp.x = abs(pupil_warp.x) - .16;
float d = star(pupil_warp, 0.019, 6., .9);
if (d < 0.007) {
return vec3(.1);
}
// Eyeballs
vec2 eye = vec2(abs(pixel.x+.1)-.17, pixel.y*.93 - .16);
d = length(eye) - .16;
if (d < 0.) return vec3(step(.013, -d));
// under eye lines
bool should_show = pixel.y < 0.25 &&
(abs(pixel.x+.29) < .05 ||
abs(pixel.x-.12) < .085);
if (abs(d - .04) < .0055 && should_show) return vec3(0);
}
// Mouth
float d = bezier(pixel,
vec2(-.26, -.28),
vec2(-.05,-.42),
vec2(.115, -.25));
if (d < .11) {
// Teeth
float width = .065;
vec2 teeth = pixel;
teeth.x = mod(teeth.x, width)-width*.5;
teeth.y -= pow(pixel.x+.09, 2.) * 1.5 - .34;
teeth.y = abs(teeth.y)-.06;
d = parabola(teeth, 38.);
if (d < 0. && abs(pixel.x+.06) < .194)
return vec3(0.902, 0.890, 0.729)*step(d, -.01);
// Tongue
// `map()` is used to change the thickness of
// the tongue along the x axis
vec2 tongue = rotateAt(pixel, sin(time*2.-1.5)*.15+.1, vec2(0,-.5));
float tongue_thickness = map(tongue.x, -.16, .01, .02, .045);
d = bezier(tongue,
vec2(-.16, -.35),
vec2(.001,-.33),
vec2(.01, -.5)) - tongue_thickness;
if (d < 0.0)
return vec3(0.816, 0.302, 0.275)*step(d, -0.01);
// mouth fill color
return vec3(.42, .147, .152);
}
// lip outlines
if (d < .12 || (abs(d-.16) < .005
&& (pixel.x*-6.4 > -pixel.y+1.6
|| pixel.x*1.7 > -pixel.y+.1
|| pixel.y < -0.49)))
return vec3(0);
// lips
if (d < .16) return vec3(.838, .799, 0.76);
// Nose
d = min(
bezier(pixel,
vec2(-.15, -.13),
vec2(-.21,-.14),
vec2(-.14, .08)),
bezier(pixel,
vec2(-.085, -.01),
vec2(-.12, -.13),
vec2(-.15,-.13)));
if (d < 0.0055) return vec3(0);
// Eyebrow
d = bezier(pixel,
vec2(-.34, .38),
// NEW animate the middle up and down
vec2(-.05, 0.5 + cos(time)*.1),
vec2(.205, .36)) - 0.035;
if (d < 0.0)
return vec3(.71, .839, .922)*step(d, -.013);
d = min(
// Head
round_rect(
pixel,
vec2(.36, .6385),
vec4(.34, .415, .363, .315)),
// Ear
round_rect(
pixel + vec2(-.32, .15),
vec2(.15, 0.12),
vec4(.13,.1,.13,.13))
);
if (d < 0.) return vec3(.838, .799, .76)*step(d, -.01);
// Hair
float twist = sin(time*2.-length(pixel)*2.1)*.12;
vec2 hair = rotateAt(pixel, twist, vec2(0.,.1));
hair -= vec2(.08,.15);
hair.x *= 1.3;
hair = warp(hair, 4.0, 0.07);
d = star(hair, 0.95, 11., .28);
if (d < 0.) {
return vec3(0.682, 0.839, 0.929)*step(d, -0.012);
}
}
return portal(pixel, time);
}
```


I prioritized readability over performance for this code - see how much faster you can make it run.

That’s everything I know about making 2D animations using shaders. I hope it’s useful. Maybe next time we’ll talk about 3D, or some totally different topic! If you’d like to be notified about my next article, please join my newsletter.

Join my newsletter lol

When you’re done with an animation you’ll probably want to turn it into a video. The editor we’ve been using on this page can not yet do that, but I’m working on it. Join my newsletter to be notified when I add video export!

In the meantime, you can use a script with [glslviewer](https://github.com/patriciogonzalezvivo/glslViewer) and [ffmpeg](https://www.ffmpeg.org). Below is my macOS workflow, on Windows and Linux you’ll have to figure out what your platform’s equivalent is.

```
brew install glslviewer ffmpeg # brew is macos only
```


Write your `shader.frag`

file

And then put this in a bash file and run to export your video

```
#!/bin/bash
set -e
set -o pipefail
if [ -z "$1" ]; then
echo "Usage: $0 <shader_file>"
exit 1
fi
ORIGINAL_DIR=$(pwd)
TMP_DIR=$(mktemp -d)
if [ ! -d "$TMP_DIR" ]; then
echo "Failed to create temporary directory."
exit 1
fi
cd "$TMP_DIR"
glslViewer "$ORIGINAL_DIR/$1" -w 1920 -h 1080 --headless -e sequence,0,7,60 -e q
ffmpeg -framerate 60 -y -i %05d.png -c:v libx264 -pix_fmt yuv420p animation.mp4
mv animation.mp4 "$ORIGINAL_DIR/"
cd "$ORIGINAL_DIR"
rm -rf "$TMP_DIR"
```


And if you want to live code locally, use this:

```
glslViewer shader.frag -w 575 -h 324 --noncurses -x 0 -y 0
```


You may have noticed that the edges of shapes in the examples on this page are smooth. I did a bit of work behind the scenes make that happen. I use a technique called super sampling where I call `color_for_pixel()`

for 9 locations within each screen pixel and then display the average. The left side of this example shows what it looks like with super sampling disabled. You may need to zoom in on the page to see the difference.

```
#version 300 es
// The above line switches the editor to "pro" mode
// and removes automatic super sampling
precision highp float;
uniform float time;
uniform vec2 resolution;
out vec4 outColor;
vec3 color_for_pixel(vec2 p, float time) {
return vec3(length(mod(p+time*.05, .5) - .25) > 0.2);
}
void main() {
float zone = gl_FragCoord.x - resolution.x*.5;
if (abs(zone) < 1.5) {
// vertical line
outColor = vec4(1, 0, 0, 1);
} else if (zone < 0.) {
// left side: no super sampling
vec2 st = (2.0*(gl_FragCoord.xy)-resolution)/resolution.y;
outColor = vec4(color_for_pixel(st, time), 1);
} else {
// right side: super sampling
int sample_count = 3;
vec3 sum = vec3(0);
for( int m=0; m<sample_count; m++ ) {
for( int n=0; n<sample_count; n++ ) {
vec2 o = (vec2(m,n) + 0.5) / float(sample_count);
vec2 st = (2.0*(gl_FragCoord.xy+o)-resolution)/resolution.y;
sum += color_for_pixel(st, time);
}
}
outColor = vec4(sum / float(sample_count*sample_count), 1);
}
}
```


Eight months ago I published a video titled “* I Made a 3D Modeler, in C, in a Week*”. The video has several animations, like this one that illustrates the the marching cubes algorithm:

```
#define INTERP 1.0
#define GRID_RESOLUTION 0
#define TRIANGULATE_4
#define TRIANGULATE_3
#define TRIANGULATE_2
#define TRIANGULATE_1
#define SHOW_INNER_DOTS 1
#define SHOW_OUTER_DOTS 1
#define ANTIALIAS_LEVEL 3
vec3 fill_color = vec3(0.4);
vec3 wireframe_color = vec3(.1);
float wireframe_thickness = .003;
vec2 repeated( vec2 p, float s ) {
vec2 r = p - s*floor(p/s);
return r;
}
float Circle(vec2 p, vec2 origin, float radius) {
return length(p - origin) - radius;
}
float sdTriangle( in vec2 p, in vec2 p0, in vec2 p1, in vec2 p2 )
{
vec2 e0 = p1 - p0;
vec2 e1 = p2 - p1;
vec2 e2 = p0 - p2;
vec2 v0 = p - p0;
vec2 v1 = p - p1;
vec2 v2 = p - p2;
vec2 pq0 = v0 - e0*clamp( dot(v0,e0)/dot(e0,e0), 0.0, 1.0 );
vec2 pq1 = v1 - e1*clamp( dot(v1,e1)/dot(e1,e1), 0.0, 1.0 );
vec2 pq2 = v2 - e2*clamp( dot(v2,e2)/dot(e2,e2), 0.0, 1.0 );
float s = e0.x*e2.y - e0.y*e2.x;
vec2 d = min( min( vec2( dot( pq0, pq0 ), s*(v0.x*e0.y-v0.y*e0.x) ),
vec2( dot( pq1, pq1 ), s*(v1.x*e1.y-v1.y*e1.x) )),
vec2( dot( pq2, pq2 ), s*(v2.x*e2.y-v2.y*e2.x) ));
return -sqrt(d.x)*sign(d.y);
}
float sdf(vec2 p) {
float d = Circle(p, vec2(0,-.2), 0.7);
d = min(d, Circle(vec2(abs(p.x),p.y), vec2(.73,.45), 0.4));
return d;
}
float triangle_wave(float x, float amplitude, float period) {
return (amplitude/period) * (period - abs(mod(x, (2.*period)) - period) );
}
vec2 interpVert(vec2 p1, vec2 p2, float w1, float w2) {
return p1 + (-w1 / (w2-w1)) * (p2-p1);
}
vec3 color_for_pixel(vec2 st, float time) {
vec3 color;
if (sdf(st) > 0.) {
color = vec3(.2);
} else {
color = vec3(1.);
}
float grid_resolution = sin(time/1.2)/4. + 0.4;
// find 4 nearest points
vec2 p1 = floor((st) / grid_resolution) * grid_resolution;
vec2 p2 = p1 + vec2(0, grid_resolution);
vec2 p3 = p1 + vec2(grid_resolution, 0);
vec2 p4 = p1 + vec2(grid_resolution, grid_resolution);
vec2 nearest = vec2(round(st.x/grid_resolution)*grid_resolution,
round(st.y/grid_resolution)*grid_resolution);
vec2 j = abs(nearest - st);
// sample sdf
float v1 = sdf(p1);
float v2 = sdf(p2);
float v3 = sdf(p3);
float v4 = sdf(p4);
// count number inside
float count = step(0.,-v1) + step(0.,-v2) +step(0.,-v3) +step(0.,-v4);
vec2 p12 = (p1 + p2) / 2.;
vec2 p13 = (p1 + p3) / 2.;
vec2 p24 = (p4 + p2) / 2.;
vec2 p34 = (p4 + p3) / 2.;
p12 = mix(p12, interpVert(p1, p2, v1, v2), min(1.,time*INTERP));
p13 = mix(p13, interpVert(p1, p3, v1, v3), min(1.,time*INTERP));
p24 = mix(p24, interpVert(p2, p4, v2, v4), min(1.,time*INTERP));
p34 = mix(p34, interpVert(p4, p3, v4, v3), min(1.,time*INTERP));
float d = 10.;
vec3 special_fill = fill_color;
if (count == 4.) {
#ifdef TRIANGULATE_4
special_fill = vec3(0.178, 0.321, 0.400);
d = min(sdTriangle(st, p1,p2,p3), sdTriangle(st, p4,p2,p3));
#endif
} else if (count == 3.) {
#ifdef TRIANGULATE_3
special_fill = vec3(0.431, 0.532, 0.595);
if (v1 > 0.) {
d = min(sdTriangle(st, p4,p2,p12), min(sdTriangle(st, p4,p3,p13), sdTriangle(st, p4,p13,p12)));
} else if (v2 > 0.) {
d = min(sdTriangle(st, p1,p3,p12), min(sdTriangle(st, p12,p3,p24), sdTriangle(st, p4,p3,p24)));
} else if (v3 > 0.) {
d = min(sdTriangle(st, p1,p2,p13), min(sdTriangle(st, p2,p13,p34), sdTriangle(st, p2,p4,p34)));
} else {
d = min(sdTriangle(st, p1,p2,p24), min(sdTriangle(st, p1,p24,p34), sdTriangle(st, p1,p3,p34)));
}
#endif
} else if (count == 2.) {
#ifdef TRIANGULATE_2
special_fill = vec3(0.622, 0.692, 0.738);
if ((v1 < 0.) == (v2 < 0.) || (v1 < 0.) == (v3 < 0.)) {
if (v1 < 0. && v2 < 0.) {
d = min(sdTriangle(st, p1,p2,p24), sdTriangle(st, p1,p24,p13));
} else if (v3 < 0. && v4 < 0.) {
d = min(sdTriangle(st, p3,p4,p24), sdTriangle(st, p3,p24,p13));
} else if (v3 < 0. && v1 < 0.) {
d = min(sdTriangle(st, p3,p1,p12), sdTriangle(st, p3,p12,p34));
} else if (v2 < 0. && v4 < 0.){
d = min(sdTriangle(st, p4,p2,p12), sdTriangle(st, p4,p12,p34));
}
} else {
// unhandled
}
#endif
} else if (count == 1.) {
#ifdef TRIANGULATE_1
special_fill = vec3(0.825, 0.815, 0.794);
if (v1 < 0.) {
d = sdTriangle(st, p1,p12,p13);
} else if (v2 < 0.) {
d = sdTriangle(st, p2,p12,p24);
} else if (v3 < 0.) {
d = sdTriangle(st, p3,p13,p34);
} else {
d = sdTriangle(st, p4,p24,p34);
}
#endif
}
if (abs(d) < wireframe_thickness) {
color = wireframe_color;
} else if (d < 0.) {
color = special_fill;
}
if (Circle(repeated(st+.05, grid_resolution), vec2(.05,.05), 0.007) < 0.) {
if (sdf(nearest) < 0.) {
#if SHOW_INNER_DOTS
color = vec3(0.404, 0.827, 0.478);
#endif
} else {
#if SHOW_OUTER_DOTS
color = vec3(0.875, 0.376, 0.243);
#endif
}
}
return color;
}
```


I needed this animation for the video to make sense, but couldn’t get past how painful and time consuming it’d be to make in a typical animation program. It seemed like the only way to accurately and quickly make it was with code. So I started coding, and the animation above is what I ended up with. I’m pretty happy with it. Some people asked me how I made the animations, so I wrote this article to answer that question.