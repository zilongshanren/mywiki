---
title: Oodle Lossless Image v1.4.7
url: https://www.jonolick.com/home/oodle-lossless-image-v147
published: '2019-12-04'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
Oodle Lossless Image (OLI) version 1.4.7 was just released. In this release there is lots of improvements - specifically with palettized and 1/2 component images. Also in 1.4.7 is a basic Unity engine integration! OLI now supports palettized images -- up to 2048 unique colors (though it could go as high as 64k, but I didn't see a benefit in my test set to go higher than 2048). Implementing this was pretty interesting in that the order of those colors in the palette matter quite a bit - and the reason is that if you get it right, then it works with the prediction filters. As in, if the palettized color indexes are linearly predictable then there is a good chance you will get significantly better compression than just a random ordering. In practice this means trying a bunch of different heuristics (since computing optimal brute force like is prohibitively expensive). So you sort by luma, or by different channels, or by distance from the last color for example (picking the most common color as the first one). I also implemented mZeng palette ordering technique which isn't commonly in PNG compressors. Believe it or not, while this theoretically should produce really good results in most cases, sometimes the simpler heuristics win by a lot so you can't just always use a single method to decide when going for minimum file sizes. Examples (some images I've seen used as examples on other sites): In all cases, the following arguments were used
pngcrush -brute <input> <output> cwebp -q 100 -lossless -exact -m 6 -mt <input> -o <output> flif -E100 -K <input> <output> Note that insane sometimes doing slightly worse than super-duper happens sometimes due to layered processes - just on average insane is going to be better. 1/2 Component images were just a matter of writing all the various SIMD routines to decode them. Other than that nothing special here except having fewer components means smaller files and faster decoding. I may in the future support more than 4 components if there is a demand for that, but for now its 1,2,3 or 4 components of 8 or 16-bits per component. There also were some general small encoding improvements. And soon coming up are some new color spaces which should further reduce file size. Specifically the new encoding flag called "--insane" which actually compresses stuff instead of using heuristics in most places to find whats the best thing to do. I use this for dev, but it might be useful for people looking to squeeze out a few more percent in file sizes. For more information on Oodle Lossless Image visit
|
## Archives
## Categories |