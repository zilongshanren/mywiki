---
title: 'Rendepth: Red/Cyan Anaglyph Filter Optimized for Stereoscopic 3D on LCD Monitors'
url: https://cybereality.com/rendepth-red-cyan-anaglyph-filter-optimized-for-stereoscopic-3d-on-lcd-monitors/
author: Cybereality
published: '2023-04-06'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/775d2c2d6d107db9.jpg)

Recently I got interested in exploring red/cyan anaglyph 3D again. Most people write off anaglyph, but it’s still the cheapest and most compatible solution for stereoscopic 3D, even today. Glasses can get had for a few dollars, and literally any display device works (even printed on paper). In my research I found some newer methods that have been more optimized for LCD monitors, rather than CRT when the original developments were done. While the quality is clearly not to the level of shutter glasses, or dual display like with virtual reality, it still offers an experience of 3 dimensions at an affordable cost without complex and expensive additional hardware.

I took some reference photos using the new [KanDao QooCam EGO](https://prd.kandaovr.com/product/qoocam-ego/), which is a consumer 3D camera that released recently. Though this is not professional quality, it does help to view the process with real life captured images, rather than computer generated ones I used to develop the algorithm. Note these were taken on a somewhat cloudy day and are not necessarily the best quality the camera can achieve, but good enough to test the filter. These images are best viewed with quality plastic red/cyan anaglyph 3D glasses. ProView and ProAna provide the least ghosting with some color reproduction loss. AnaChrome provides a much closer to native color reproduction, at the cost of additional ghosting.

As you can see, the image quality is not on the level of shutter glasses (as expected) but gets closer to a “real” 3D experience than was possible on anaglyph previously for LCD monitors. The difference seems subtle in images, but it much more apparent in animation and with different scenes, like with video or gaming. I will first explain the algorithm, and then you can watch the video at the end, which demonstrates the quality best.

The method I am using is based on the [Least-Squares Projection Method](https://www.site.uottawa.ca/~edubois/anaglyph/LeastSquaresHowToPhotoshop.pdf) created by Eric Dubois. Since then this has been widely used and mostly considered the optimal method for red/cyan in terms of ghosting and the comfort of the image. However, that research was done for CRT monitors, and LCD screens have slightly different calibrations. My method is based the revised LSM from Sanders and McAllister in the paper [Producing Anaglyphs from Synthetic Images](https://research.csc.ncsu.edu/stereographics/ei03.pdf). This method is very similar to Dubois, and derived from his formula, but works better on LCD screens. Most notably, the color reproduction is closer to native, particular with displaying the red channel. The ghosting is also quite low compared to older anaglyph methods, like pure anaglyph. The matrix multiplications to process the images are shown below (using GLSL shader code, but can easily be ported to other graphics processing APIs).

`vec3 optimized_color = clamp(color_left * left_filter, vec3(0.0), vec3(1.0)) + clamp(color_right * right_filter, vec3(0.0), vec3(1.0));`


Where the filter matrices from the paper are shown as below.

```
const mat3 left_filter = mat3(
vec3(0.4561, 0.500484, 0.176381),
vec3(-0.400822, -0.0378246, -0.0157589),
vec3(-0.0152161, -0.0205971, -0.00546856));
const mat3 right_filter = mat3(
vec3(-0.0434706, -0.0879388, -0.00155529),
vec3(0.378476, 0.73364, -0.0184503),
vec3(-0.0721527, -0.112961, 1.2264));
```


While this was a decent improvement by itself, I kept researching. There have been some new processing methods for anaglyph, within the last 5 or 10 years, however some of these algorithms were complex and iterative, while I needed a simple linear transformation for real time applications. There was a new paper from 2010, also from McAllister et al, called [Methods for computing color anaglyphs](https://ui.adsabs.harvard.edu/abs/2010SPIE.7524E..0SM/abstract). The research here outlines some methods for processing stereo images in anaglyph that appear have not been commercially used. I did not use their method, due to the many non-linear transformations and I did not feel it would be suitable for real time. My main application is for gaming, and producing stereo 3D without drastically lowing performance is a hard requirement. However, if you are interested in offline processing, this research may be valuable. That said, I did take one important thing from the paper which was the gamma correction. This was inspired by Peter Wimmer’s “Optimized Anaglyph” and works by doing separate gamma operations on each color channel. This has the effect of boosting the red channel in a manner that improves color reproduction with very little cost. I utilized this in my shader.

```
const vec3 gamma_map = vec3(1.6, 0.8, 1.0);
vec3 correctColor(vec3 original) {
vec3 corrected;
corrected.r = pow(original.r, 1.0 / gamma_map.r);
corrected.g = pow(original.g, 1.0 / gamma_map.g);
corrected.b = pow(original.b, 1.0 / gamma_map.b);
return corrected;
}
vec3 color_final = correctColor(optimized_color);
```


I did attempt other values for the gamma map, but I was unable to tweak it for further improvements. There are also other filter matrices, like in the paper [A Uniform Metric for Anaglyph Calculation](https://research.csc.ncsu.edu/stereographics/ei06.pdf) from Zhang, but I found the Sanders filter to be superior. Overall I am satisfied with the quality and the performance in a GLSL shader is extremely fast, so suitable from real-time. I decided to release the code I produced with this hybrid method in order that people can test it with their own applications, as I feel it gives a new life to red/cyan anaglyph 3D.

This is also a component of a larger project I’m working on that will allow 2D to 3D conversion in real time for gaming applications. I am still in the early stages of this project, and only have one game working so far, but I am making good progress. You can watch the demonstration video below from a commercial game, Forsaken Remastered, running through the Steam client with my software. This is still a work in development, but should provide an idea of what this technology looks like with video and gaming applications.

The stereo 3D aspects of this work will be released under the brand Rendepth, however it will not be limited to anaglyph, as I plan to support “real” stereo solutions that are just now coming to the market again. This is just the beginning, thanks so much for all your support.