---
title: hdrpng.js - HDR images for the web.
url: https://enkimute.github.io/hdrpng.js/
author: Enki's blog
published: '2017-04-03'
source_blog: Enki's blog – Math, Graphics, Programming.
source_site: https://enkimute.github.io/
category: graphics
fetched: '2026-04-19'
---

GIT

![view on github](../../assets/cb9f317b98c6b74a.png)

# hdrpng.js - HDR images for the web.

A small (7122 bytes) script to add support for radiance HDR, RGBE.PNG and RGB9_E5.PNG images to your browser.

# HDRPNG

HDRPNG adds HDR Image support to your browser. It allows you to load industry standard Radiance .HDR files and PNG files containing RGBE or RGB9_E5 information.

- Loading Radiance .HDR files. (rgbe format)
- Loading/Saving 32bit RGBE.PNG files.
- Loading/Saving 32bit RGB9_E5.PNG files.
- Converting RGBE, RGB9_E5 or float to LDR (with exposure and gamma tonemap)
- Converting from and to RGBE, RGB9_E5 and float.
- Interfaces like normal images. (can be added to document, used as texture, on canvas, ..)

## Download

7122 bytes - [https://enkimute.github.io/res/hdrpng.min.js](https://enkimute.github.io/res/hdrpng.min.js)

## Demo

## Using hdrpng.js

Include the hdrpng.js script in your document.

```
<SCRIPT SRC="hdrpng.min.js"></SCRIPT>
```


Create a HDR Image and add it to the page.

```
var myHDR = new HDRImage();
myHDR.src = 'memorial.hdr';
document.body.appendChild(myHDR);
```


## Setting exposure and gamma.

The exposure of your image is controlled by simply setting the exposure value. Values are in stops, 1 means no change, 2 is 1 stop up, 3 is two stops up etc .. (0 is one stop down, ..)

```
myHDR.exposure = 2.0; // 1 stop up.
myHDR.exposure = -2.0; // 3 stops down
```


The gamma propertie can be used to control the display gamma (default value is 2.2).

```
myHDR.gamma = 2.2; // default gamma.
myHDR.gamma = 1.0; // display curve linear.
```


## Using HDR Images as textures.

HDRImage Objects can be used as textures in webGL in a couple of ways :

- as LDR images with the given exposure and gamma.
- as full floating point images (96 bits per pixel)
- as RGBE images to be decoded in the shader (32 bits per pixel)
- as RGB9_E5 images supported by hardware (webGL2 only !)

```
var myHDR = new HDRImage();
myHDR.src = 'memorial.hdr.png';
myHDR.onload = function() {
// upload as LDR with current exposure/gamma
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, myHDR);
// upload as full linear float
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, w, h, 0, gl.RGB, gl.FLOAT, myHDR.dataFloat);
// upload in 32bit RGBE
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, myHDR.dataRGBE);
// or in webGL2
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB9_E5, w, h, 0, gl.RGB, gl.FLOAT, new Float32Array(myHDR.dataRAW.buffer));
}
```


when uploading in the 32bit RGBE format, a single line of shader code will unpack your textures to the full range.

```
vec4 rgbe = texture2D(myHDR, texture_coords);
rgbe.rgb *= pow(2.0,rgbe.a*255.0-128.0); // unpack RGBE to HDR RGB
```


## Saving .RGBE.PNG images

hdrpng.js can be used to convert Radiance .HDR files to the internal .RGBE.PNG format.

```
// save RGBE.PNG (default format)
myHDR.toHDRBlob(function(blob){..});
// save RGB9_E5.PNG
myHDR.toHDRBlob(function(blob){..},"image/rgb9_e5");
```


full example :

```
var myHDR = new HDRImage();
myHDR.src = 'memorial.hdr';
myHDR.onload = function() {
myHDR.toHDRBlob(function(blob){
var a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'memorial.RGBE.PNG';
a.innerHTML = 'click to save';
document.body.appendChild(a); // or a.click()
}
}
```


## Using .RGBE.PNG files without hdrpng.js

Once you saved your .HDR files as .RGBE.PNG, you can use them in your webGL projects without hdrpng.js. They can be loaded like any other PNG file with transparency, and a single extra line in your shader will unpack them ..

Load as normal png with transparency.

```
var i = new Image(); // -> not HDRImage !!
i.src = 'texture.RGBE.PNG';
...
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, i);
```


and in the shader

```
vec4 rgbe = texture2D(myHDR, texture_coords);
rgbe.rgb *= pow(2.0,rgbe.a*255.0-128.0);
```


## Supported formats :

- .HDR (Radiance .HDR files)
- .RGBE.PNG (RGBE embedded in PNG)
- .RGB9_E5.PNG (RGB9_E5 embedded in PNG)

### why .HDR ?

- RGBE 32 bit, RLE compressed.
- Industry standard HDR format.
- loading/decompressing in javascript.
- rendering in software or shader.

HDR (Radiance) files are HDR images that are stored using an internal 32 bit format called RGBE. Pixels are stored with an 8 bit mantissa per color channel and a shared 8 bit exponent. Radiance HDR files can be RLE compressed.

### why .RGBE.PNG ?

- RGBE 32 bit, PNG compressed.
- Native loading.
- rendering in software or shader.

PNG files allow storing 32bit data, and offer native loading speeds. RGBE.PNG files are PNG’s with 32bit RGBE data. They offer superior compression and faster loading compared to .HDR files. For webGL1, these are the ideal format, and require only a single line in the shader to be unpacked.

(.RGBE.PNG files can be saved with hdrpng.js’ toHDRBlob method.)

### why .RGB9_E5.PNG ?

- RGB9_E5 32 bit, PNG compressed.
- native loading.
- native rendering (webGL2).

Similar to the RGBE format, the openGL working group decided on a format called RGB9_E5, with a 9 bit
mantissa for each component and a 5 bit shared exponent. This format was enabled in the browser with
the release of webGL2. If webGL2 is available, it is the way to go for HDR images as you will get
correct mip-mapping and filtering without any modifications to your shaders.

(.RGB9_E5.PNG files can be saved with hdrpng.js’ toHDRBlob method.)

Enjoy ;)

enki.