---
title: 'Getting started with OpenCL, Part #3'
url: https://anteru.net/blog/2012/getting-started-with-opencl-part-3
published: '2012-11-05'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

The final part of the short introduction to OpenCL. In this part, we’ll be using images and implement a simple blur filter. You should start with the base application written in [the first part of this guide](https://anteru.net/blog/2012/11/03/2009/) as we won’t need anything [from the SAXPY example](https://anteru.net/blog/2012/11/04/2016/). Make sure to grab [the code](https://github.com/Anteru/opencltutorial/tree/34e5c9d901169fe4d7e1110a72590eb27a607490) before you continue reading.

We’ll be loading an image and filtering it using a small [gaussian blur](http://en.wikipedia.org/wiki/Gaussian_blur) filter. Instead of hard-coding the filter, we’ll provide it as an input argument to the kernel, which allows you to easily change it at run-time. The kernel will then sample all pixels inside the filter radius, multiply them with the filter weight and finally write the new value to the output image.

OpenCL is well suited for this problems as it has direct support for images. Anything you would expect on images just works: You can read and write any pixel directly, the data can be automatically converted and they can be sampled using a bilinear filter. Creating images is just the same as with buffers, but it requires an additional parameter to describe the format of the image:

```
static const cl_image_format format = { CL_RGBA, CL_UNORM_INT8 };
cl_mem inputImage = clCreateImage2D (context,
CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, &format,
image.width, image.height, 0,
const_cast<char*> (image.pixel.data ()),
&error);
CheckError (error);
```


This is the OpenCL 1.1 API, in OpenCL 1.2, you would use `clCreateImage`

which uses an image descriptor so only one function is necessary instead of providing 5 different overloads. The important part here is the format, in particular, the second part: `CL_UNORM_INT8`

. This indicates that the data is provided as 8-bit integers, and is stored as unsigned-normalized or `UNORM`

for short. Unsigned-normalized means that 0 maps to 0.0, and 255 maps to 1.0 when the data is read. It also requires you to read the data as floating point using `read_imagef`

. This is perfect for our use case, as we have to weight each sample using a floating point value.

The second part that is necessary for reading an image is a *sampler*. It describes how coordinates are interpreted and whether the image data should be filtered. In our case, we want to index pixels using integers, so we have to set `CLK_NORMALIZED_COORDS_FALSE`

, we want out-of-bounds accesses to be clamped (`CLK_ADDRESS_CLAMP_TO_EDGE`

) and we don’t want any filtering. Setting the filter to `CLK_FILTER_NEAREST`

means that the sampler should return the value of the nearest pixel to the requested pixel, without any interpolation. With this, we can assemble the complete kernel now:

```
__constant sampler_t sampler =
CLK_NORMALIZED_COORDS_FALSE
| CLK_ADDRESS_CLAMP_TO_EDGE
| CLK_FILTER_NEAREST;
float FilterValue (__constant const float* filterWeights,
const int x, const int y)
{
return filterWeights[(x+FILTER_SIZE) + (y+FILTER_SIZE)*(FILTER_SIZE*2 + 1)];
}
__kernel void Filter (
__read_only image2d_t input,
__constant float* filterWeights,
__write_only image2d_t output)
{
const int2 pos = {get_global_id(0), get_global_id(1)};
float4 sum = (float4)(0.0f);
for(int y = -FILTER_SIZE; y <= FILTER_SIZE; y++) {
for(int x = -FILTER_SIZE; x <= FILTER_SIZE; x++) {
sum += FilterValue(filterWeights, x, y)
* read_imagef(input, sampler, pos + (int2)(x,y));
}
}
write_imagef (output, (int2)(pos.x, pos.y), sum);
}
```


You should notice three things: First, we never define `FILTER_SIZE`

in the code, second, we use `get_global_id`

in two dimensions and third, we have a parameter specified as `__constant`

. The missing `FILTER_SIZE`

is easily explained: Instead of passing on the filter size into the kernel as a parameter, we will pass it using a `#define`

. This means we will have to recompile the program if we change the filter size, but it also allows the compiler to easily unroll the innermost loop. To pass a definition to the compiler, simply add `"-D FILTER_SIZE=1"`

to the list of options in the `clBuildProgram`

call.

We use a 2D domain in this example as it naturally maps to the 2D image; there’s no need to write a 1D to 2D mapping on our own. Finally, let’s see what that [ __constant](http://www.khronos.org/registry/cl/sdk/1.1/docs/man/xhtml/constant.html) means. As we learned in the second part, OpenCL has multiple address spaces. In the second example, we only used

`__global`

. `__constant`

is another address space where you can store read-only data. From the host side, it looks exactly the same as global memory, but some devices like GPUs do actually have special support for constant data which may result in better performance. That’s also the reason why it can be fairly small. OpenCL only guarantees that it is at least 64 KiB in size.The rest is business as usual: We create the images, run the kernel, and copy back the data. The example assumes that the image is stored as `PPM`

; you can convert any image to and from `PPM`

using [GIMP](http://www.gimp.org/). One minor difficulty arises from the fact that PPM is RGB only; OpenCL requires the image to be stored in RGBA, so we have to convert it. You should also use a larger test image, on a 4096 by 3264 pixels image, I can barely see all CPU cores working for a brief moment.

That’s all, I hope this quick introduction gives you a basic understanding of OpenCL. If you have any questions, feel free to comment, and depending on interest, I might do another series about advanced OpenCL.