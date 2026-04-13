---
title: Designing a new texture format
url: https://anki3d.org/designing-a-new-texture-format/
author: Panagiotis Christopoulos Charitos
published: '2013-09-15'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

In this article we will be discussing the whys and whats of the new AnKi texture format. First we will try to shade some light on the current texture formats and what are their limitations and later we will present the ankitex format in detail and how it solves these limitations.

The first thing we need do is to shed some light on OpenGL hardware, OpenGL drivers and how they need their textures served.


Textures more or less can be divided into multiple categories. They can be compressed and uncompressed also they can be 2D textures, 2D Array textures, 3D textures and Cube textures.

All modern GPUs offer some kind of texture **compression** and at the present time all of these compression methods are lossy. Unfortunately there is not a single standard compressed format out there. On desktop GPUs the most common is S3TC where mobile is more fragmented with ETC, PVRTC, ASTC and S3TC. For every format there is also a different texture file container, for example for S3TC is DDS and for ETC it’s PKM. Another quirk is that most of those formats don’t handle the alpha channel in the same way and some they don’t even support alpha (early versions of S3TC and ETC1).

Aside from compressed textures all driver and hardware implementations accept **uncompressed textures** as well in a simple to understand format. Uncompressed textures give the maximum quality but they have a huge impact on speed especially in mobile GPUs simply because they use more bandwidth. One interesting fact is that desktop GL drivers have the ability to compress those textures to a compressed format of their liking at runtime. Unfortunately this can be quite slow despite the fact that the drivers use the the “fast” path of their converter. Overall it’s better to forget this feature mainly because it doesn’t apply on mobile.

If an engine targets all GL implementations out there obviously it requires support for multiple formats. As we mentioned briefly every compressed format comes with it’s own container. Some containers support mipmapping (eg DDS) others not (PKM). If we decide to load a texture from the original containers we need a directory for that texture that will most likely contain a single DDS file, a number of PKM files and who knows what else applies to other formats. On multi-layered textures (eg cube maps) things can get more complicated.

Others tried to tackle the same problems by creating a unified texture container. Valve created valve texture, Epic created unreal texture and Khronos created it’s own format. For some of those formats the spec is widely available, for other it’s a trade secret.

# The AnKi texture format

For AnKi we designed a new texture file container that solves all of the above limitations. Despite the fact that probably another formats (like Khronos’) solve the same issues we decided to invent something new. Why reinventing the wheel someone may ask. Because it’s quite easy to design a new format and it’s accompanying converter and because it’s fun and challenging to code such things.

So, AnKi texture is designed to:

- Support a number of compressions including uncompressed
- Support 2D textures, 2D Array textures, 3D textures and Cube textures
- Support mipmapping
- Support square and non-square textures
- Be extendable and support other compressions
- Everything is packed in a single binary file

The file looks like this:

![anki_tex](https://anki3d.org/wp-content/uploads/2013/09/anki_tex1-158x300.png)


![anki_tex](https://anki3d.org/wp-content/uploads/2013/09/anki_tex1-158x300.png)

The header is described by this C structure:

struct AnkiTextureHeader { std::array<U8> magic; U32 width; U32 height; U32 depth; U32 type; U32 colorFormat; U32 compressionFormats; U32 normal; U32 mipLevels; U8 padding[88]; };

The *magic* should be “ANKITEX1”.

The *width* and *height* obviously give the size of the surface of the first mipmap. The depth is the number of layers for 2D arrays and the number of layers of mipmap level 0 for 3D textures.

The *type* is the following enum:

enum TextureType { TT_NONE, TT_2D, TT_CUBE, TT_3D, TT_2D_ARRAY };

The *color* format is:

enum ColorFormat { CF_NONE, CF_RGB8, ///< RGB CF_RGBA8 ///< RGB plus alpha };

The *compressionFormats* is a mask that states what compressed data are present in the ankitexture file:

enum DataCompression { DC_NONE, DC_RAW = 1 << 0, DC_S3TC = 1 << 1, DC_ETC = 1 << 2 };

The *normal* is a bool and tells if the texture is a normal map.

The *mipLevels* gives the number of mipmaps.

These information are used by AnKi to load the appropriate data and to determine the internal format of the texture.

- CF_RGB8 + DC_RAW = GL_RGB8
- CF_RGBA8 + DC_RAW = GL_RGBA8
- CF_RGB8 + DC_S3TC = GL_COMPRESSED_RGB_S3TC_DXT1_EXT
- CF_RGBA8 + DC_S3TC = GL_COMPRESSED_RGBA_S3TC_DXT5_EXT
- CF_RGB8 + DC_ETC = GL_COMPRESSED_RGB8_ETC2
- CF_RGBA8 + DC_ETC = GL_COMPRESSED_RGBA8_ETC2_EAC

The above conversions indicate what AnKi should pass to parameter internalFormat of glTexImageXX function.

AnKi currently has a loader that it’s located in the engine’s source code and a converter that uses a TGA file (or a number of TGAs) to create a .ankitex file.

The converter is named ankitexture.py and it’s a python script (located in trunk/tools/texture) that invokes a few external applications that either convert or do other image related things. At the moment the converter uses the:

*convert*and*identify*tools from the ImageMagic suite (opensource and available in most Linux distributions).*etcpack*that compresses an image to ETC (from Ericsson).*nvcompress*that compresses to S3TC (part of nvidia-texture-tools code.google.com/p/nvidia-texture-tools).

That’s it for today. Feel free to comment in the section bellow.