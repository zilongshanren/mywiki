---
title: GIF Writer
url: https://www.jonolick.com/home/gif-writer
author: Rxi
published: '2015-11-03'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

Basic Usage: // 4 component. RGBX format, where X is unused char *frame = new char[128*128*4]; jo_gif_t gif = jo_gif_start("foo.gif", 128, 128, 0, 32); jo_gif_frame(&gif, frame, 4, false); // frame 1 jo_gif_frame(&gif, frame, 4, false); // frame 2 jo_gif_frame(&gif, frame, 4, false); // frame 3, ... jo_gif_end(&gif); Where frame holds the RGBA pixels for a frame. You call start, then frame a bunch of times then end. Here is a more interesting example used to create the image above. :) Enjoy!
void hsv2rgb(float hsv[3], float rgb[3]) { if(hsv[1] <= 0.0) { // < is bogus, just shuts up warnings rgb[0] = rgb[1] = rgb[2] = hsv[2]; return; } float hh = hsv[0]; if(hh >= 360) { hh = 0; } hh /= 60; long i = (long)hh; float ff = hh - i; float p = hsv[2] * (1.f - hsv[1]); float q = hsv[2] * (1.f - (hsv[1] * ff)); float t = hsv[2] * (1.f - (hsv[1] * (1.f - ff))); switch(i) { case 0: rgb[0] = hsv[2]; rgb[1] = t; rgb[2] = p; break; case 1: rgb[0] = q; rgb[1] = hsv[2]; rgb[2] = p; break; case 2: rgb[0] = p; rgb[1] = hsv[2]; rgb[2] = t; break; case 3: rgb[0] = p; rgb[1] = q; rgb[2] = hsv[2]; break; case 4: rgb[0] = t; rgb[1] = p; rgb[2] = hsv[2]; break; case 5: rgb[0] = hsv[2]; rgb[1] = p; rgb[2] = q; break; } } int main(int argc, char **argv) { const int w = 256, h = 256; jo_gif_t gif = jo_gif_start("foo.gif", w,h,0,32); for(int frame = 0; frame < 360/4; ++frame) { unsigned char tmp[w*h*4]; double coordX = -0.74529; double coordY = 0.113075; double zoom = 1.5E-4*0.5; for(int y = 0; y < h; ++y) { for(int x = 0; x < w; ++x) { double x0 = (x/double(w) * 3.5 - 2.5) * zoom + coordX; double y0 = (y/double(h) * 3.0 - 1.5) * zoom + coordY; double xx = 0, yy = 0; int iter = 0; while(xx*xx + yy*yy < 2*2 && iter++ < 4096) { double xtmp = xx*xx - yy*yy + x0; yy = 2*xx*yy + y0; xx = xtmp; } int i = y*w*4+x*4; int iter2 = iter + 360 - frame*4; float hsv[3] = { float(iter2%360), 1, iter2 < 4096 ? 1.f : 0.f }; float rgb[3]; hsv2rgb(hsv, rgb); tmp[i+0] = (unsigned char)(rgb[0] * 255); tmp[i+1] = (unsigned char)(rgb[1] * 255); tmp[i+2] = (unsigned char)(rgb[2] * 255); tmp[i+3] = 255; } } jo_gif_frame(&gif, tmp, 4, false); } jo_gif_end(&gif); }
|
## Archives
## Categories |