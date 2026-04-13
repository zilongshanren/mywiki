---
title: Using Basis Universal Texture Compression with Metal
url: https://metalbyexample.com/basis-universal/
published: '2019-07-11'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

In this short article, we’ll take a look at a relatively new compressed texture format called Basis. Basis is developed by [Binomial, LLC](http://www.binomial.info), a company founded by Rich Geldreich (of [crunch](https://blogs.unity3d.com/2017/11/15/updated-crunch-texture-compression-library/) fame) and Stephanie Hurlburt.

Basis is unique among compression formats in that it emphasizes efficient transcoding between compressed formats. This means that a single .basis file can be transformed, at runtime, into a format that’s optimal for the target platform, without decompressing it in memory, saving space and bandwidth.

Although Basis is a commercial product, targeted predominantly at game developers, Binomial has [contributed](https://www.khronos.org/blog/google-and-binomial-contribute-basis-universal-texture-format-to-khronos-gltf-3d-transmission-open-standard) their Basis Universal reference encoder and transcoder to the Khronos Group in support of the glTF model format, under the Apache License 2.0.


As of this writing, Basis Universal supports transcoding to [PVRTC1](https://en.wikipedia.org/wiki/PVRTC) 4bpp RGB, [BC7 mode 6](https://docs.microsoft.com/en-us/windows/win32/direct3d11/bc7-format-mode-reference#mode-6) RGB, [BC1-5](https://docs.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-resources-block-compression#compression-algorithms), [ETC1, and ETC2](https://en.wikipedia.org/wiki/Ericsson_Texture_Compression) formats. If you’re familiar with Metal’s compressed texture formats, some of these will look familiar. In particular, all iOS devices that support Metal also support PVRTC1 and ETC2. All Macs that support Metal also support BC pixel formats.

Download the sample code for this article [here](http://metalbyexample.com/wp-content/uploads/MetalBasis.zip).

## Compressing Textures with Basis Universal

In order to use the Basis Universal format, we’ll need to create some .basis files. To do that, we’ll obtain the source for the reference encoder and build the `basisu`

command-line tool.

### Building the Basis Universal Encoder from Source

The easiest way to get the Basis Universal source is from [its Github repo](https://github.com/BinomialLLC/basis_universal), or you can download it directly [here](https://github.com/BinomialLLC/basis_universal/archive/master.zip).

Once you’ve unzipped the source, you can navigate to the source directory in Terminal and use a combination of CMake and make to build the `basisu`

binary:

cmake -D CMAKE_C_COMPILER=/usr/bin/clang -D CMAKE_CXX_COMPILER=/usr/bin/clang++ . make

If all goes well, you should have a `basisu`

binary in the `bin_osx`

directory.

### Using basisu on the Command Line

`basisu`

has many different options, but the simplest way to get started is to pass it a PNG file:

basisu -mipmap fox.png

This encodes the source image and writes it to a file named `fox.basis`

in the working directory.

Basis supports numerous texture types, including 2D, 2D array, 3D, and cubemap. To create a cubemap file, pass the `-tex_type cubemap`

option, along with 6 image file paths, in +X, -X, +Y, -Y, +Z, -Z order:

basisu -mipmap -tex_type cubemap cube_pos_x.png ... cube_neg_z.png

## Using Basis-Compressed Textures in Metal

Now that we have some Basis Universal files, let’s talk about loading them and using them with Metal.

### The Basis Transcoder API

The API of the Basis Universal transcoder is fairly straightforward. Currently, only a C++ API is available, which means it doesn’t play nicely with Swift. In order to work around this, I wrote a utility class (`MBEBasisTextureLoader`

) in Objective-C++ that can be used from Swift.

Because the API is still under active development at the time of this writing, I won’t talk about the parts that still seem to be evolving, just the core functions.

To start loading a Basis file, you create a `basisu_transcoder`

object. All transcoder-related types live in the `basist`

namespace, so that looks like this:

auto transcoder = new basist::basisu_transcoder(sel_codebook);

where the `sel_codebook`

is an implementation detail that’s likely to go away in the future. Consult the [Basis Universal documentation](https://github.com/BinomialLLC/basis_universal#transcoder-details) for the gory details.

To get ready to transcode the texture into your desired runtime format, load the texture file into memory, then call `start_transcoding`

:

bool success = transcoder->start_transcoding(data, dataSizeInBytes);

At this point, you can start using the API to learn about the contents of the file. The `get_texture_type`

function tells you whether the file contains a 2D texture, a 3D texture, a cubemap, etc.:

basist::basis_texture_type basisTextureType = transcoder->get_texture_type(data, dataSizeInBytes);

In my loader, I convert from this value to a corresponding `MTLTextureType`

with the following code:

case basist::cBASISTexType2D: return MTLTextureType2D; case basist::cBASISTexType2DArray: return MTLTextureType2DArray; case basist::cBASISTexTypeCubemapArray: return MTLTextureTypeCube; case basist::cBASISTexTypeVolume: return MTLTextureType3D;

The `get_total_images`

function allows you to determine how many images are in the file. In the case of a cubemap texture, this will be a multiple of 6, and in the case of a texture array, it will be the number of array slices:

uint32_t imageCount = transcoder->get_total_images(data, dataSizeInBytes);

Our next task is to iterate over the images and create one or more textures from them. Since each image can contain multiple mipmap levels, we’ll need to iterate over these as well for each image.

To get the information for an image, we use the `get_image_info`

function:

basist::basisu_image_info imageInfo; transcoder->get_image_info(data, dataSizeInBytes, imageInfo, imageIndex);

The image info struct contains various bits of information, such as the width and height of the image and the number of mipmap levels. With this information, we can create a `MTLTexture`

of the appropriate type. After that, it’s a matter of transcoding the texture data on a level-by-level basis.

For each level of the image, we can query its properties with the `get_image_level_info`

function:

basist::basisu_image_level_info levelInfo; transcoder->get_image_level_info(data, dataSizeInBytes, levelInfo, imageIndex, levelIndex);

At long last, we’re ready to get the data for the level and request that it be transcoded into our desired pixel format. To do that, we allocate a buffer large enough to hold the level (`levelData`

), then call the `transcode_image_level`

function to get the transcoded texture data:

bool didTranscode = transcoder->transcode_image_level( data, dataSizeInBytes, imageIndex, levelIndex, levelData, levelDataSizeInBlocks, transcoderFormat);

Here, `transcoderFormat`

is one of the target formats supported by Basis Universal. We can map from an `MTLPixelFormat`

to a `transcoder_texture_format`

with another utility function, excerpted here:

case MTLPixelFormatBC1_RGBA: return basist::cTFBC1; case MTLPixelFormatBC4_RUnorm: return basist::cTFBC4; case MTLPixelFormatBC7_RGBAUnorm: return basist::cTFBC7_M6_OPAQUE_ONLY; case MTLPixelFormatBC3_RGBA: return basist::cTFBC3; case MTLPixelFormatBC5_RGUnorm: return basist::cTFBC5; case MTLPixelFormatPVRTC_RGB_4BPP: return basist::cTFPVRTC1_4_OPAQUE_ONLY; case MTLPixelFormatEAC_RGBA8: return basist::cTFETC2;

If we manage to transcode successfully, we’re ready to copy the data into our Metal texture. We do that with the `replaceRegion:`

API on `MTLTexture`

:

MTLRegion region = MTLRegionMake2D(0, 0, levelInfo.m_width, levelInfo.m_height); [texture replaceRegion:region mipmapLevel:levelIndex slice:sliceIndex withBytes:levelData bytesPerRow:levelInfo.m_num_blocks_x * blockSizeInBytes bytesPerImage:0];

We repeat this for every level for every slice in the texture, after which we’re done loading.

### Loading Compressed Textures with Metal

The `MBEBasisTextureLoader`

in the sample code provides a somewhat simpler API for doing this work. It’s closely modeled after the `MTKTextureLoader`

class from MetalKit and has the appropriate Swift annotations to make it work well with Swift.

For example, here’s how we might load a Basis texture from our app bundle, requesting that it be transcoded into the BC7 Mode 6 format for use on macOS:

let basisLoader = MBEBasisTextureLoader(device: device) let foxURL = Bundle.main.url(forResource: "fox", withExtension: "basis")! let options: [MBEBasisTextureLoader.Option : Any] = [ .pixelFormat: MTLPixelFormat.bc7_rgbaUnorm.rawValue ] basisLoader.newTexture(URL: foxURL, options: options) { (texture, error) in imageView.texture = texture }

Note that we’re using an asynchronous loading method here. The loader class also provides synchronous methods. The loader uses concurrent `NSOperation`

s to load textures on a background thread when requested.

Download the sample code for this article [here](http://metalbyexample.com/wp-content/uploads/MetalBasis.zip).

## Results and Conclusion

In this article, we’ve looked at the Basis Universal compressed texture format and how to use it with Metal. With the open-sourced encoder and transcoder, Binomial has made efficient transcoding to various target platforms simple. And although the commercial suite of Basis products will be most useful to game studios, the Basis Universal offering is worth considering for your cross-platform texture compression needs.

andrewHey Warren! thanks for sharing the texture loader.

How do you think of basis compression vs something like astc or the other formats you explored in this previous article?