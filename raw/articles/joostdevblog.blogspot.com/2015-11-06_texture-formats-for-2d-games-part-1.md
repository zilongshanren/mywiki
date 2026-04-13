---
title: Texture formats for 2D games, part 1
url: http://joostdevblog.blogspot.com/2015/11/texture-formats-for-2d-games-part-1.html
author: Joost van Dongen
published: '2015-11-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers II](http://www.swordsandsoldiers2.com)or

[Awesomenauts](http://www.awesomenauts.com)using the right texture formats can make a big difference for visual quality, video memory, loading times and download size. What format works best varies depending on art style and platform and a good understanding of the options helps a lot in making the right choices.

This is a huge topic so I've split it into four posts. Today I'll cover the basics. The other three posts will discuss the more obscure palette textures, DXT and finally a comparison table of all the discussed techniques. This short series will get a bit technical at points but I've tried to make it as readable for artists as possible: knowing how your art will be compressed is important for game artists.

While the texture formats available for 2D and 3D games are the same, 2D games have different requirements, so it is interesting to approach this topic from a 2D standpoint. Also, 2D games usually don't have things like normal maps, roughness maps and reflection maps and mostly don't need high dynamic range (HDR) textures, so I won't be discussing the requirements of such special kinds of textures.

The first thing to realise is that transparency is extremely important in 2D games. While in a 3D game the shape of an object is generally determined by its polygons, the shape in a 2D game usually comes from transparency in the texture. In many 2D games the art is put on the screen by just having a simple rectangle with an image with transparency on it. Transparency is generally stored in the alpha channel, so the quality of the alpha channel is an important factor in 2D games.

![](../../assets/b4f092ac5c8d8364.jpg)

The most basic and highest quality texture format is a simple RGBA32 with 8 bits per colour channel. In total each pixel then uses 4 bytes, or 3 bytes if there is no alpha channel. These can be stored in various file formats, like TGA and BMP, but in the end in the videocard it's all the same. At

[Ronimo](http://www.ronimo-games.com)we use TGA for these. This image format is lossless: whatever your original image was, you get exactly that in the game. Note that compressed TGA isn't supported by videocards, so when using TGA you will need to use its uncompressed 32 bit or 24 bit format (depending on whether you have alpha).

![](../../assets/9ca6179a27830e55.jpg)

The big downside of this format is that it's huge. A 1024x1024 texture with alpha is already 4mb this way. Awesomenauts characters have a texture of nearly 4096x4096, containing all their animation frames. With simple RGBA, this would amount to a whopping 64mb of texture space for just a single character texture! This results in a simple conclusion: we need something smaller for the vast majority of our art. Even when you have several gigabytes of texture space available, full RGBA32 will fill it up really quickly. At Ronimo we only use TGA for images that are small and would lose too much quality when compressed. In practice this means we only use TGA for gradients.

![](../../assets/fffa278698332420.jpg)

One approach to reducing texture size is to use vector art and render that directly. This means you hardly need to use any textures at all since most colour and shape are defined by polygons instead of by a texture. It also means that artists need to use special vector tools like Illustrator and Flash. This is extremely limiting: more painterly styles are practically impossible this way. It also uses way more performance because in-game animation isn't simply swapping an image frame any more. Rendering vector art in real-time is a relatively complex and performance-heavy task.

Since vector tools are so limiting and since rendering vectors is a lot of work to program and much slower than textures, we don't use vector art in-game at all at Ronimo. We sometimes use vector tools when specific images are most easily made that way, but by the time they get to the game we always save the result as simple textures. Depending on your art style vectors might be a great option though!

![](../../assets/590dce4057a9ad65.gif)

A common suggestion from artists when discussing texture formats is to use JPG or PNG. These formats are excellent at achieving small image size with little visible loss. However, they aren't suitable for real-time games: videocards don't support these texture formats at all. That means that a texture that is stored on disk as JPG or PNG needs to be converted to something else to go into video memory, often growing the texture to the size of an uncompressed TGA. An important goal in choosing a texture format is to reduce the usage of video memory (usually to be able to store even more art there). Since JPG and PNG cannot be stored in video memory, they don't help there at all.

![](../../assets/3c1a645c44f9c017.png)

This doesn't mean these formats are entirely useless. In a game where the size on disk is most important you can use JPG for all the textures and then simply put them in the much larger RGB24 format in video memory. A game that famously did something like this is Rage (one of my favourite games of the past years). Rage needs to constantly stream in new textures, so the speed of reading from disk was a problem. To solve this they stored the files in a JPG-like format on disk, loaded that into memory, and then converted it in real-time to DXT to be used by the game. Such hardcore streaming tech is generally not necessary for 2D games though.

Videocards can only handle a very limited set of texture types. The three main approaches to reducing texture size without simply reducing their resolution are to use less bit-depth, to use palettes or to use the DXT format. Note that specific types of hardware might offer additional formats, so it can really pay off to look into the details of whatever platform you are developing for. Palettes and DXT will be separate blog posts, so let's look into reducing bit-depth now.

Using less bit-depth is the simplest approach to texture compression. For example, you can use a 16 bit format. Instead of using 8 bits per channel for RGB, you might use 5 bits for red, 6 for green and 5 for blue. Such an R5G6B5 format is 33% smaller than uncompressed 24bit RGB. It also means less colour depth, so especially gradients will look visibly worse. The difference is quite small though so for most textures this loss in quality is hardly noticeable and totally acceptable. The reason green is 6 bits while red and blue are 5 bits is that 16 doesn't divide by 3 equally. Human eyes are better at seeing in the green spectrum, so the extra bit is put in the channel where it matters most.

![](../../assets/45bf53db3262c72f.png)

If you need alpha there's often something like R5G5B5A1 available, which also uses only 16 bits per pixel, but at slightly greater compression costs. This specific format has only 1 bit for alpha, so pixels are either fully transparent or fully opaque. This not only means that partially transparent pixels aren't possible, but also that anti-aliasing on the image's edges is entirely lost. In 2D games anti-aliasing is usually part of the original art and stored in the texture. Losing this can be pretty bad for image quality, so I generally wouldn't advice using formats with only 1 bit for alpha. There are also other combinations, like R4G4B4A4, giving better alpha but significantly worse colours. If you hate your own game you can even use R2G3B3.

![](../../assets/2fa0e58b7cdffeea.png)

Videocards support many different combinations of bitrates per channel so it's useful to have a look and figure out what works for your purpose. Specifically interesting is L8A8: this is a greyscale texture (L for “luminance”) with high quality alpha. This is 50% smaller than full R8G8B8A8. If the original image is already greyscale this format doesn't result in any quality loss. If you happen to be making a game with many monochrome textures, this might be a relevant option. If you don't need alpha you can half the size again by using L8.

In our own games none of the formats discussed so far are used extensively. We use a little bit of R8G8B8A8 through TGA files for gradients, and L8A8 for fonts. The vast majority of our textures is DXT5, which I will discuss in part 3 of this short series. Next week I will first look into the format we used for

[Swords & Soldiers 1](http://www.swordsandsoldiers.com)on Nintendo Wii: palette textures. This format is often overlooked and usually quite a hassle to use, but for certain art styles it delivers an excellent combination of small textures with little quality loss, as I'll show next week.

*See also:*

-

-

-

-

[Texture formats for 2D games, part 2: Palettes](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-2.html)-

[Texture formats for 2D games, part 3: DXT and PVRTC](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-3-dxt.html)-

wow. tga uses way more memory than jpg but visual difference is very little

ReplyDeleteYeah, that's why TGA and BMP are hardly used on the web: JPG is much better for websites. Pity videocards cannot use JPG. :(

DeleteGreat stuff! We use TGA a lot for larger maps that require compression, since it allows for some neat tricks across the board.



ReplyDeleteMost important of those, to improve compression quality on PowerVR chips using PVRTC is to smear the RGB colours out across the alpha channel. A tool called Solidify B does this very nicely. And sometimes a light dither after that will improve results even more. For Gold Diggers we ended up using 2x resolution compressed maps for vehicles because they looked better, and were smaller.

Much of this is important to take into account when deciding how to make art, because doing a project and realizing late that 90% of your in-game art is not going to compress well is a real bummer.

Thanks for sharing! :)


DeleteYou mention you use TGA for things that require compression, what d you mean by that? Isn't that kind of contradictory, since TGA is normally uncompressed? Or do you mean that you keep the originals as TGA and automatically convert them to specific formats per platform (like PVRTC on PowerVR) when making a build?

Interesting read!

ReplyDeleteAre the palette textures an actual file format? Or is it a grayscale format w/ a shader to replace the colors in a pixel shader? (or even some graphics API thing :D?)

Spoilers, you'll see next week! :)

DeleteUsually(always) GPU's does not actually have 24bits format but they are padded to 4byte boundary per texel. So it's 32bits even when using rgb888.

ReplyDeleteReally? I'd be surprised if they were really that inefficient under the hood. Do you have a link where I can read about what formats they really support in hardware and what formats they work with inefficiently like that?

DeleteSmall ineffiency in memory footprint vs ineffiency every time texture is fetched from memory. If each pixel is not 1/2/5/8/16 aligned then it would't always fit to single cache line. So even if some oddball gpu would not pad texture to 4bytes it would incur performance hit.

DeleteSeems like a weird tradeoff since cachelines are relatively long so cross-cacheline-pixels would be rare. And it's not a "small inefficiency" in memory footprint: the texture becomes 33% larger, that's a lot.


DeleteStill, I can imagine you're right, it just seems like an odd choice to me.

Great idea for an article! Looking forward to the next part.

ReplyDelete