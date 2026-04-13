---
title: Understanding Metal Enhancements in the A15 Bionic GPU
url: https://metalbyexample.com/metal-on-a15/
published: '2021-09-23'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

With the advent of iPhone 13 comes a new generation of Apple-designed system-on-a-chip: the A15 Bionic.

As has become expected, Apple has published a developer-oriented tech talk to explain the new and enhanced GPU features included in this latest cutting-edge offering. You can watch it [here](https://developer.apple.com/videos/play/tech-talks/10876/).

![](../../assets/2352e4abf694cb46.jpg)

The tech talk is the best official source of nitty-gritty details on the new chip, but I wanted to take the opportunity to add some commentary and context.


The enhancements we will discuss fall into three categories:

- Lossy texture compression
- Sparse depth and stencil textures
- SIMD shuffle-and-fill functions

## Lossy Compression

A15 Bionic is not the first A-series chip to include on-the-fly texture compression. A12 Bionic introduced lossless compression in 2018’s flagship devices (e.g. iPhone XS), and A14 Bionic improved frame buffer compression an additional 15% last year.

The new lossy compression in A15 Bionic provides 50% memory savings with relatively little loss in visual fidelity.

The API surface for enabling lossy compression is minimal. The new `compressionType`

property on `MTLTextureDescriptor`

holds a member of the `MTLTextureCompressionType`

enum, and specifying `MTLTextureCompressionTypeLossy`

(`.lossy`

in Swift) enables lossy compression. For many use cases, this will be the only required change to take advantage of lossy compression.

Lossy compression is applicable to most texture types 1, but it is perhaps most useful for reducing the size of intermediate and final render targets, where the accumulation of compression artifacts is minimal. This will be increasingly important as mobile display resolutions and pixel densities continue to rise over the coming years.

Most pixel formats support lossy compression, including 10-bit extended range formats. However, packed formats are not supported.

In terms of operations, lossy textures can be render targets, can be the source or destination of blit operations, and can be sampled and read. However, they cannot be used with shader write operations, which precludes some compute use cases.

Finally, lossy textures must use the *private* storage mode; they cannot be in shared or managed storage. This implies that [reading back texture data](https://developer.apple.com/documentation/metal/mtltexture/1516318-getbytes) on the CPU will entail an additional blit operation (along with the usual latency-stall tradeoff).

## New Sparse Texture Support

Now we turn our attention to another enhanced feature that can also enable significant memory savings: sparse depth and stencil textures.

Introduced in A13 Bionic, sparse textures allow you to control which regions (tiles) of large textures you want to keep in memory. Tiles can be dynamically mapped and unmapped to respond to the needs of the application. For example, the base mip levels of high-resolution texture maps could be unmapped when the mesh to which they apply is distant from the camera, to free up texture memory for objects closer to the camera.

A15 Bionic introduces support for sparse depth and stencil textures, expanding the set of supported sparse texture pixel formats. In the A15 Bionic tech talk, this feature is demonstrated through an explanation of Sparse Tiled Shadow Mapping (STSM). This technique closely follows the outline of [Cem Cebenoyan’s GDC 2014 talk](https://archive.org/details/GDC2014Cebenoyan) on sparse shadow maps.

Although not demonstrated in this year’s Apple video, certain uses of sparse textures can make use of [texture access counters](https://developer.apple.com/documentation/metal/mtlblitcommandencoder/3043910-gettextureaccesscounters?language=objc) to determine which regions should be made resident from frame to frame.

## SIMD Improvements

Metal’s SIMD-group instructions continue to get more powerful from year to year, and this release is no exception.

To complement the existing SIMD-group directional shuffle functions (`simd_shuffle_down`

, `simd_shuffle_rotate_down`

, `simd_shuffle_rotate_up`

, and `simd_shuffle_up`

), Metal on A15 Bionic includes the new `simd_shuffle_and_fill_up`

, `simd_shuffle_and_fill_down`

functions, which fill in the shifted-from vector indices from an ancillary data vector, rather than leaving them containing the values from the original vector.

This small but significant addition allows SIMD-groups to further exploit shared data without resorting to threadgroup memory. The example given in the video is a convolution kernel that is able to drastically reduce the number of required texture samples by shuffling sampled texel values from adjacent lanes as the convolution window slides over the image region being convolved by the threadgroup.

Similar functions have also been introduced for quadgroups: in addition to the `quad_shuffle_up`

/`quad_shuffle_down`

functions introduced alongside A13 Bionic, the new `quad_shuffle_and_fill_up`

and `quad_shuffle_and_fill_down`

serve the same purpose as the SIMD-group functions described above.

## Closing Thoughts

While the updates in A15 Bionic seem incremental, they have the potential to unlock richer content and higher resolutions on the newly-launched generation of Apple devices. With the memory savings and bandwidth reduction afforded by lossily compressed textures and sparse textures, Metal on iOS continues to make techniques previously affordable only on the consoles and PCs of several years ago into the mobile space.

-
With the notable exception of linear textures, whose layout is transparent to client code and therefore not eligible for compression (this exemption includes buffer-backed textures); and texture buffers.
[↩](https://metalbyexample.com#fnref-862-1)

Prof. Robert J SackerAnd of course Apple, after proclaiming it is 100% behind the scientific community, cuts OpenCL with minimal support for those of us who actually do GPU computing. Does anyone know of a good source of examples using Metal to compute on the GPU?

GracienI’ll surprise you. A good source of Metal compute sample codes is… Apple.