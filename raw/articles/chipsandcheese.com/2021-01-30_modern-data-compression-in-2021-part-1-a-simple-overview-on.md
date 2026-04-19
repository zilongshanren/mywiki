---
title: 'Modern Data Compression in 2021 Part 1: A Simple Overview on the Art of Image
  Encoding'
url: https://chipsandcheese.com/p/modern-data-compression-in-2021-part-1-a-simple-overview-on-the-art-of-image-encoding
author: BlueSwordM
published: '2021-01-30'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

In our current times, digital information is one of the most important facets of our society. We generate a lot of data, transport a lot of data, and store a large portion of that data. Managing such huge quantities of data is a large task: one that requires large quantities of energy, effort and time, and can cost a lot of money to keep a record of that data. Therefore, it is critical to use data as efficiently as possible to reduce all the costs surrounding it.

Before we begin on the subject, it is important to know the definition of 2 terms that will often be used in this article: encoding and decoding. Encoding is the concept of taking one type of data (such as binary information, 0s and 1s) and converting it into something else using a coder. A decoder is used to take the type of data format converted by a decoder and convert it into its raw form to be displayed by the receiving entity (such as when a translator translates a foreign language into one you understand). A codec is the specification format that encompasses both. That is why it is important to be specific: an encoder produces a stream respecting the codec specification that can be decoded

This is where the concept of compression is introduced: the goal of compression is to reduce data density while keeping the original data as readable as possible. In this regard, we have 2 types of compression: lossy and lossless. The former discards data while storing the remaining data using smart compression algorithms to minimize the perceptible loss of information, while the latter keeps all the data, and just tries to encode it more efficiently. Lossless compression is obviously used when you want to have a perfect copy of the data (mathematically lossless), like with text, where you don’t want to lose any of the readable data. In contrast, lossy compression is used to reduce the file size while keeping perceptual quality as high as possible at certain data rates. Both compression schemes can be applied on a large range of data: text, video, audio, images are the most prominent forms of data to are compressed. As most of you have already know, we will be talking about image compression, which will be separated in 2 parts, and will be part of a larger multi-part article encompassing audio and video compression as well.

Top: Original PNG. Bottom: JPG. As seen in this picture, there are almost no visible differences between the JPG encoded file and PNG, while the JPG image is 10% of the size of the original

BEFORE JPG

Let’s start with a historical lesson on image compression. Before the advent of the JPEG codec in 1992, general purposes lossy image compression wasn’t exactly a thing. GIF did exist starting in 1985, but that was a lossless format mostly used for animated sequences, so I won’t talk about it here.

Most of the techniques that were used to reduce data rates at the time were:

Reducing resolution (downsampling)

Reducing color depth (going from 24-bit color down to 8-bit color for example)

Changing from the commonly used RGB (Red Green and Blue) color space to the more perceptually optimized YCbCr color space (Y is luminance information, Cb and Cr are color differences between blue and red chroma components).

Chroma subsampling (reducing the sampling ratio for Cb and Cr)

Example of chroma subsampling

That last one is particularly interesting knowing that human vision is more sensitive towards luminance information differences vs chroma information differences. Since we know that color takes up 2/3 of the information of a YCbCr stream, it is possible to cut down the sampling rate for the color information. A full YCbCr stream is 4:4:4(full Y, full Cb, and full Cr) and takes up the highest bandwidth: a 4:2:2 stream takes up 66% of the original bandwidth, and a 4:2:0 stream (used for most video today) only uses about 50% of the original bandwidth to transmit. All of these techniques used together were used to cut down significantly on image file sizes. However, they came at a non-negligible quality loss, didn’t make images that much smaller, and as resolutions grew as the years passed by, these solutions became less and less useful in image compression. Soon enough, there was a new compression standard in the form of JPG.

1992 AND BEYOND: THE REST IS HISTORY

The initial JPG standard came out in 1992, and it was revolutionary. It was an efficient, fast, and high-quality lossy codec, especially for the time. Since then, it’s been the image codec of choice for most types of images, and it’s been improved over the years with advances in the standard itself and better encoders using more advanced techniques. It was so good it’s been serving us well for almost 30 years now. In fact, most of its base lossy encoding tools are still used today in most other image codecs, in either more advanced forms, or developed their own alternative solutions entirely, on both the lossless and lossy front.

THE BASIS OF JPG

To compress stuff, JPG has essentially 3 main steps in its encoding process:

Color space change and manipulation.

DCT 8×8 block splitting analysis and quantization.

Entropy coding+Huffman coding(lossless)

In the 1st step, a JPG encoder converts the usually RGB source into a YCbCr source, and then deciding whether or not to apply chroma subsampling (it does make a small efficiency difference due to how JPG works, but modern codecs are barely any more efficient when working with subsampled chroma).

In the 2nd step, it divides up the image components into 8×8 blocks (note the static block size), and the data inside of these blocks is converted to a frequenced domain representation using DCT conversion (a discrete cosine transform). After that, a fancy formula is used to convert the values inside of the block to frequency values or more accurately speaking, into transform coefficients. Each of the output values in the block is associated to a certain pattern of high/low frequency detail depending on its complexity. After that, we get to the lossy compression part: quantization (division+approximation of a value simply put). The high frequency components in the 8×8 DCT block are compressed more heavily (more quantization), which greatly reduces the amount of information in those high detail blocks, and the low frequency blocks (low complexity, like the sky) are compressed less heavily (less quantization), since compression of these is easier by their own lower frequency nature.

The final step involves doing some lossless data compression using entropy and Huffman encoding to compress the data further.

Overall, all of these steps create a final image that is visually lossless if compressed right at a very small percentage of the original size of the uncompressed image, all tightened up in a neat .jpg container (format box, a container literally). Even though it’s a great end consumption standard, the format does have its disadvantages, and has been stretched thin.

OTHER WORKS, AND THE FUTURE

Since JPG’s introduction, with the power of oversight, decades of engineering work and learning, many more formats have come out, but none until recently have had the power and might to completely dethrone the venerable JPG. Some have stayed, and most of them are relegated to niche uses. The most prominent one is the lossless FOSS (Free and Open-Source Software) PNG format introduced in 1996. Other formats like JPEG2000 have been introduced as an evolution over JPEG in some ways, with much more flexibility in its tools, but it has not been used much outside of specific corporate purposes due to its heavy patent portfolio making it difficult to use as a general standard. There has also been a rise of image codecs based on video codecs, such as WebP (VP8) and HEIF (HEVC) due to their appeal at very low bitrates.

We also have rather recent developments in image codecs written to overthrow the current JPG king: JPEG XL, a new futuristic format developed by none other than the JPEG committee that developed the same JPG we still use. There’s also another format on the horizon based on the open AV1 standard called AVIF, but I’m afraid I will have to end the article here. There will be a continuation of this series, with the 2nd part being all about the new main image formats being on the market today, how they compare against each other in different scenarios, reaching a conclusion to which codec has the highest chance of dethroning JPEG and becoming the new image coding standard. The 3rd part will be about audio codecs, and the last parts of this series will be about video codecs.

If you have any corrections you would like to write about and suggestions, write it in the

Sources:

https://jpeg.org/jpeg/workplan.html (JPEG specification from the JPEG group used to verify the statements about how the codec and encoder work)

https://gitlab.com/wg1/jpeg-xl (JPEG-XL repository and reference encoder/decoder and some talks about the format itself. To be continued in the next part).