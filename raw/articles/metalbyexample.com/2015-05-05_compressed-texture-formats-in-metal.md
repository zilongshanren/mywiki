---
title: Compressed Texture Formats in Metal
url: https://metalbyexample.com/compressed-textures/
published: '2015-05-05'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

In this article, we will consider several GPU-friendly compressed texture formats. These formats allow us to trade some image quality for substantial improvements in disk usage and performance. In particular, we will look at the ETC2, PVRTC, and ASTC formats.

![The sample app showcases a variety of compressed texture formats](../../assets/7bcd1d2fa1a18a81.png)


## Why Use Compressed Textures?

In previous articles, we created textures by loading an image into memory, drawing it into a bitmap context, and copying the bits into a Metal texture. These textures used uncompressed pixel formats such as `MTLPixelFormatRGBA8Unorm`

.

Metal also supports several compressed formats. These formats allow us to copy image data directly into a texture without decompressing it. These formats are designed to be decompressed on-demand by the GPU, when the texture is sampled rather than when it is loaded.

The formats we will consider below are *lossy*, meaning they do not perfectly preserve the image contents, as a lossless format like PNG does. Instead, they trade a reduction in image quality for much smaller memory usage. Using compressed texture data therefore greatly reduces the memory bandwidth consumed when sampling textures, and is also more cache-friendly.

## A Brief Overview of Compressed Texture Formats

### S3TC

S3TC, also known as DXT, was the first compressed format to gain broad adoption, due to its inclusion in DirectX 6.0 and OpenGL 1.3 in 1998 and 2001, respectively. Although S3TC is broadly supported on desktop GPUs, it is not available on iOS devices.

### PVRTC

The PVRTC image format was introduced by Imagination Technologies, creators of the PowerVR series of GPUs at the heart of every iOS device. It was first described in a [2003 paper by Simon Fenney](http://fileadmin.cs.lth.se/cs/Education/EDA075/notes/fenney03texcomp.pdf).

PVRTC operates by downsampling the source image into two smaller images, which are upscaled and blended to reconstruct an approximation of the original. It considers blocks of 4×4 or 4×8 pixels at a time, which are packed into one 64-bit quantity. Thus, each pixel occupies 4 bits or 2 bits, respectively.

One significant limitation of using PVRTC format on iOS is that textures must be square, and each dimension must be a power of two. Fortunately, game textures are most commonly produced in dimensions that are compatible with this limitation.

### ETC

Ericsson Texture Compression (ETC) debuted in 2005. Similarly to PVRTC’s 4-bit-per-pixel mode, it compresses each 4×4 block of pixels into a single 64-bit quantity, but lacks support for an alpha channel. A subsequent version, ETC2, adds support for 1-bit and 8-bit alpha channels. ETC2 is supported by all Metal-compatible hardware, but PVRTC often offers better quality at comparable file sizes.

### ASTC

Advanced Scalable Texture Compression (ASTC) is the most recent compressed texture format supported by Metal. Developed by AMD and supported fairly widely on OpenGL ES 3.0-class hardware, this format incorporates a selectable block size (from 4×4 to 12×12) that determines the compression ratio of the image. This unprecedented flexibility makes ASTC a very attractive choice, but it requires an A8 processor at a minimum, making it unusable on devices such as the iPhone 5s.

## Container Formats

The compression format used by a texture is only half of the picture. In order to load a texture from disk, we need to know its dimensions (width and height) and its pixel format. This metadata is often written into the file itself, in the form of a *header* that precedes the image data. The layout of the header is described by the *container format* of the image. In this article, we will use two container formats: PVR and ASTC.

### The PVR Container Format

Not to be confused with the PVRTC compression format, the PVR container format describes how the data in a texture file should be interpreted. A PVR file can contain uncompressed data or compressed data in numerous formats (including S3TC, ETC, and PVRTC).

There are a few different, mutually-incompatible versions of the PVR format. This means that each version of PVR requires different code to parse correctly. For example, the header structure for the “legacy” format (PVRv2) looks like this:

struct PVRv2Header { uint32_t headerLength; uint32_t height; uint32_t width; uint32_t mipmapCount; uint32_t flags; uint32_t dataLength; uint32_t bitsPerPixel; uint32_t redBitmask; uint32_t greenBitmask; uint32_t blueBitmask; uint32_t alphaBitmask; uint32_t pvrTag; uint32_t surfaceCount; };

The header structure for the most recent version (PVRv3) looks like this:

struct PVRv3Header { uint32_t version; uint32_t flags; uint64_t pixelFormat; uint32_t colorSpace; uint32_t channelType; uint32_t height; uint32_t width; uint32_t depth; uint32_t surfaceCount; uint32_t faceCount; uint32_t mipmapCount; uint32_t metadataLength; };

There are more similarities than differences between the headers. The various fields describe the contained data, including the texture’s dimensions and whether the file contains a set of mipmaps or a single image. If the file contains mipmaps, they are simply concatenated together with no padding. The program reading the file is responsible for calculating the expected length of each image.

Note that the header also has `surfaceCount`

and (in the case of PVRv3) `faceCount`

fields, which can be used when writing texture arrays or cube maps into a single file. We will not use these fields in this article.

### The ASTC Container Format

The ASTC container format is custom-tailored to the ASTC compression format. The header indicates the compression block size, which allows you to select the correct pixel format when loading the data into texture memory and calculate the length of the texture data. Here is the layout of the ASTC header:

struct ASTCHeader { uint32_t magic; unsigned char blockDimX; unsigned char blockDimY; unsigned char blockDimZ; unsigned char xSize[3]; unsigned char ySize[3]; unsigned char zSize[3]; };

The `xSize`

, `ySize`

, and `zSize`

fields are 24-bit quantities, each encoded as three bytes. The compressed image data immediately follows the header.

## Creating Compressed Textures

There are various tools for creating compressed textures, both on the command line and with a GUI. Below, we’ll look at two tools, which allow us to create textures in the formats discussed above.

### Creating Textures with texturetool

As of Xcode 13 (released in 2021), texturetool has been superseded by TextureConverter, a more sophisticated tool with support for additional formats. It is installed alongside Xcode in the /usr/bin directory inside your developer tool path (e.g., /Applications/Xcode.app/Contents/Developer). For usage information, consider watching the WWDC 2021 session [“Discover Metal debugging, profiling, and asset creation tools”](https://developer.apple.com/videos/play/wwdc2021/10157/?time=1299)

Apple includes a command-line utility with Xcode called `texturetool`

that can convert images into compressed texture formats such as PVRTC and ASTC. At the time of this writing, it does not support the PVRv3 container format. Rather, it writes PVR files using the legacy (PVRv2) format, described above. With the `-e`

flag, you specify your desired container format: PVR, ASTC, or RAW (no header). With the `-f`

format you specify the compression type: PVRTC or ASTC. The `-m`

flag signifies that all mipmaps should be generated and written sequentially into the file.

Each compression format has its own flags for selecting the degree of compression. For example, to create a 4 bit-per-pixel PVRTC texture with a PVR legacy header, including all mipmap levels, use the following invocation of `texturetool`

:

`texturetool -m -e PVRTC -f PVR --bits-per-pixel-4 -o output.pvr input.png`


To create an ASTC-compressed texture in an ASTC container with an 8×8 block size using the “thorough” compression mode:

`texturetool -e ASTC -f ASTC --block-width-8 --block-height-8 --compression-mode-thorough -o output.astc input.png`


The `-m`

flag for generating mipmaps is ignored when writing a texture with an ASTC container.

### Creating Textures with PVRTexToolGUI

Imagination Technologies includes a tool in their [PowerVR SDK](http://community.imgtec.com/developers/powervr/installers/) that allows creation of compressed textures with a GUI. `PVRTexToolGUI`

allows you to import a PNG and select a variety of compression formats, including ASTC, PVRTC, and ETC2. Unlike `texturetool`

, this application uses the PVRv3 container format by default, so you should use code that expects the appropriate header format if you compress textures with this tool.

![The PVRTexToolGUI from Imagination Technologies allows the user to compress images in a variety of formats](../../assets/da6f4fc8576aebf3.png)


![The PVRTexToolGUI from Imagination Technologies allows the user to compress images in a variety of formats](../../assets/da6f4fc8576aebf3.png)

`PVRTexToolGUI`

has a command-line counterpart, `PVRTexToolCLI`

, that exposes all of the parameters available in the GUI and allows you to write scripts for rapidly batch-converting textures.

## Loading Compressed Texture Data into Metal

Loading compressed textures is a two-fold process. First, we read the header of the container format. Then, we read the image data described by the header and hand it to Metal. Regardless of the compression algorithm used, we do not need to do any parsing of the image data ourselves, since Metal is able to understand and decode compressed textures in hardware.

Creating a texture with compressed data is exactly the same as with uncompressed data. First, we create a texture descriptor with the appropriate pixel format and dimensions. If the texture has mipmaps, we indicate so with the `mipmapped`

parameter. For example, here is how we create a texture descriptor for a PVRTC texture with 4 bits per pixel for which we have mipmaps:

MTLTextureDescriptor *descriptor = [MTLTextureDescriptor texture2DDescriptorWithPixelFormat:MTLPixelFormatPVRTC_RGBA_4BPP width:width height:height mipmapped:YES];

We can then ask a device to produce a texture that matches this descriptor:

id<MTLTexture> texture = [device newTextureWithDescriptor:descriptor];

For each mipmap level in the image, we need to make a separate call to `-replaceRegion:mipmapLevel:withBytes:bytesPerRow:`

, as follows:

MTLRegion region = MTLRegionMake2D(0, 0, levelWidth, levelHeight); [texture replaceRegion:region mipmapLevel:level withBytes:levelData bytesPerRow:levelBytesPerRow];

Where `levelWidth`

and `levelHeight`

are the dimensions of the current mip level, `level`

is the index of the current mip level (the base level is index 0), and `levelData`

is a pointer to the mip level’s image data. `levelBytesPerRow`

can be computed as the length of the image data divided by the level’s height.

## The Sample App

The sample app includes a demonstration of all of the texture formats mentioned in this article. Tapping the “Switch Textures” button brings up a menu that allows the user to select among the various textures. The menu options for the ASTC options will not be available if the device on which the app is running does not support ASTC compression.

![The sample app allows you to select among several compression formats supported by Metal](../../assets/40a778ba3c268f80.png)


![The sample app allows you to select among several compression formats supported by Metal](../../assets/40a778ba3c268f80.png)

## Conclusion

In this article, we have discussed the merits of compressed textures and discussed a few of the available formats. We looked at how to create and load textures in the ETC2, PVRTC, and ASTC formats. Generally speaking, ASTC offers the best quality-to-size ratio on hardware where it is available. The PVRTC format should generally be preferred when targeting devices with the A7 processor.

### Acknowledgements

Conversations with [Shannon Potter](https://twitter.com/lucastizma) provoked my interest in this topic and encouraged me to write this article.

AndyCan you share the swift variant?

Warren MooreI never ported this code to Swift, nor am I aware of anyone doing so, but it should be pretty straightforward.

CheneyHi，Is there a method in the metal as same as glViewport in OpenGL, set the viewport ,to achieve split-screen？

Warren MooreYou can use the

`setViewport:`

method on your`MTLRenderCommandEncoder`

to set the viewport (NDC-to-window transform). It takes a`MTLViewport`

struct.Sarbarthacan you post the swift version too?

Warren MooreI don’t generally post Swift ports, since the actual API usage is the same between Objective-C and Swift. Having said that, some of the lower-level parts of this particular example might be a little tricky, due to Swift’s lack of specificity around alignment. In any case, my friend Marius’ post on textures covers how to load textures with

`MTKTextureLoader`

in Swift, which is the recommended approach these days. It can handle all of the formats mentioned here and more.VernellSince they share the same storage, any changes to the pixels of the new texture object are reflected in the calling texture object, and vice versa.

Peter MolnarHello.

How can I load PNG image as compressed texture on Mac? I was expecting the same behavior as in OpenGL but when I changed PixelFormat to BC1 it was not working correctly.

Warren MooreI’m not familiar with how OpenGL handles BCn textures, but I wouldn’t expect that loading RGBA data straight into a BC1 texture in Metal would work. You’d need to compress it offline with a tool like img2ktx, then load

thatdata.icalicHello Warren,

is it possible in metal programming to compute peak GFLOPS on ios and mac? something like clpeak(https://github.com/krrishnarraj/clpeak) on opencl, i curious about peak GFLOPS latest chip iphone and ipad(a11 and 10x).

latest snapdragon 835 gpu on oneplus 5:

Global memory bandwidth (GBPS)

float : 17.82

float2 : 19.30

float4 : 19.43

float8 : 20.38

float16 : 20.45

Single-precision compute (GFLOPS)

float : 294.65

float2 : 285.81

float4 : 311.02

float8 : 265.02

float16 : 308.34

half-precision compute (GFLOPS)

half : 570.72

half2 : 539.62

half4 : 610.79

half8 : 314.82

half16 : 313.73

No double precision support! Skipped

Integer compute (GIOPS)

int : 65.98

int2 : 68.05

int4 : 80.68

int8 : 79.25

int16 : 77.79

Transfer bandwidth (GBPS)

enqueueWriteBuffer : 8.71

enqueueReadBuffer : 8.98

enqueueMapBuffer(for read) : 3228.33

memcpy from mapped ptr : 8.99

enqueueUnmap(after write) : 1016.22

memcpy to mapped ptr : 8.97

Kernel launch latency : 214.91 us

source: https://forum.beyond3d.com/threads/clpeak-compute-gflops-with-opencl-on-android.60374/#post-2011570

Volodymyrwhy ASTC no need mipmaps?

Warren MooreIt’s not that ASTC doesn’t need mipmaps; rather, that

`texturetool`

doesn’t allow the creation of mipmap chains for ASTC images. It’s a limitation of the tool.Mike FarrellLooks like ETC2 loading was broken for NPOT textures. Assertion was failing and texture was corrupt.

This line fixed it for me

uint32_t widthInBlocks = (int)ceilf((float)width / blockWidth);

/////…….

(int)ceilf((float)width / blockWidth)

Mark HeathYou mention that BCx/DXTx compression, although not available in ios is broadly supported on desktop GPUs, does that include Mac desktops?