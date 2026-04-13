---
title: We don’t need new multimedia formats
url: https://fgiesen.wordpress.com/2010/10/04/we-dont-need-new-multimedia-formats/
published: '2010-10-04'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# We don’t need new multimedia formats

Following Google’s announcement of WebP, there’s been a lot of (justified) criticism of it based on its merits as an image coder. As a compression geek, I’m interested, but as both a creator and consumer of digital media formats, my main criticism is something else entirely: The last thing we need is yet another image format. This was already true when JPEG 2000 and JPEG XR were released. Never mind that their purported big compression advantages were greatly exaggerated (and based on dubious metrics); even if the standards had delivered clear-cut improvements on that front, they would’ve been irrelevant. **Improved compression rate is not a feature.** Not by itself, anyway. As someone who deals with content, I care about compression rate only as long as size is a limiting factor. As someone taking photos, I care whether all the pictures I shoot in one day fit onto my camera. Back when digital cameras were crappy, had low resolution and a tiny amount of storage, the JPEG compression made a big difference. Nowadays, we have 8 Megapixel cameras and multiple Gigabytes of storage *in our cellphones*. For normal usage, I can shoot RAW photos all day long and still not exhaust the space available to me. It’s done, problem solved. I might care about the size reduction once I start archiving stuff, but again, the 10:1 I get with plain JPEG at decent quality is plenty – a guaranteed 30% improvement on top of that (which JPEG2k/JPEG-XR/WebP don’t deliver!) is firmly into “don’t care” territory. It doesn’t solve any real problem.

The story is the same way for audio. MP3 offered an reduction of about 10:1 for CD quality audio at the right time, and made digitally archiving music practical. And we still gladly take the 10:1 on everything, since fitting 10x more on our MP3 players is convenient. But again, that’s only a factor of storage limitations that are rapidly disappearing. MP3 players started getting popular because they were smaller than mobile CD players and could (gosh!) store multiple albums worth of music (of course, back then “multiple albums” was a number in the single digits, and only if you compressed them greatly). Nowadays, most people can easily fit their complete music collection onto an iPod (or, again, their cellphone). Give it another 5 years and you’ll have enough space to fit it in as uncompressed WAV files if you choose to (not going to happen since most people now get music directly in MP3/AAC format, but it would be possible). Again, problem solved. Better audio compression remains an interesting problem with lots of fascinating ties to perception and psychology, but there’s just no real practical need for better audio compression these days. Audio just isn’t that much data.

Video is about the only mainstream type of content where the compression ratio still matters: 1080i60 video (as used in sports broadcasts for example) is about 90 megabytes *per second* in the subsamples YUV 4:2:0 color space it typically comes in, and about 350MB/s in the de-interlaced RGB color space we use for display. That’s unwieldy enough to need some serious compression (and partial or complete hardware support for decompression). And even the compressed representations are large enough to be unwieldy (we stick them onto Blu-ray discs and worry about the video streaming costs). So there’s still some future for innovation there, but even that window is rapidly closing. Blu-ray is probably the last disc format that was motivated partly by the need to store the amount of content needed for high-fidelity video. HDTV resolutions are gonna stay with us for a good while (HD is close enough to the internal resolutions used in movie production to make any further improvements subject to rapidly diminishing returns), and Blu-rays are already large enough to store HD content with good quality using current codec technology. BDXL is on the way; again, that’s just large enough for what we want to do with it. The next generation of video codecs after H.264 is probably still going to matter, since video is still a shitload of data right now. But we’ve been getting immensely better at large-scale image and signal processing (mainly with sheer brute force) and Moore’s law works in our favor. Five years ago, digital video was something done mainly by professionals and enthusiasts with the willingness to invest into expensive hardware. Nowadays, you can get cheap HD camcorders and do video postproduction on a normal laptop, if you’re willing to stomach the somewhat awkward workflow and long processing times. Ten years from now, a single 720p video will be something you can deal with as a matter of course on any device, just as you do with a single MP3 nowadays (…remember when encoding them took 2x as long as their runtime? Yeah, that was just 10 years ago).

And in the meantime, the last thing we need is yet more mutually incompatible formats with different feature sets and representations to make the lives of everyone dealing with this crap a living hell. If you don’t have any actual, useful features to offer (a standard lossy format with alpha channel would be nice, as would HDR support in a mainstream format) just **shut up** already.

Hi,

Size matters : it saves bandwidth, shorten content delivery, allows more traffic per month for the same price… (why do we gzip html/css/js content!?)

I guess flicker for example might be very happy to saves thousands of TB of storage (and bandwidth).

Each nail needs an appropriate hammer.

Good rant nonetheless :)

Word up.

GZip itself is another example. Deflate is from 1993 and in fact another good example. There are plenty of better algorithms available, some offering better compression at about the same CPU requirements (e.g. LZX which has been used in .CAB files since 1995!), and some more complex but offering significantly better compression for the content we put on the web (e.g. BZip2, LZMA, PPMD).

Why? Simple. GZip/ZLib/Deflate is a simple way to “just add compression” that gives you an instant 2:1 on text files and other structured content (simplifying here, but you get the idea). It solves the problem well enough for most people to just move on.

Sure flickr etc. would love to save bandwidth. But in the end they don’t even care enough to run something like jpgcrush on the images they host. Switching to another format entails decompressing lossy data and recompressing it with a different lossy codec; I don’t see photo sites willing to do this (The only ones that actually do are streaming video sites like YouTube etc.). Nearly every Web site in existence uses JPEG images. Yet still, HTTP has Deflate as a transfer encoding, but no lossless JPEG recompressor (which could be done completely transparently for the user).

I don’t mean to suggest that compression improvements in general are irrelevant. Obviously, particularly when you have hard limits (“this movie/game has to fit onto a DVD”), you’ll gladly take a 20% improvement if the increase in decoding cost is within your CPU budget, and similar when you’re really transferring large amounts of data (the threshold for “large amount of data” is somewhere between 20MB and 100MB these days – that’s when people start using LZMA etc.). But most users don’t have to deal with this kind of limitation, and user-generated-content sites wind up using the formats that its users prefer, inefficient or not.

If you want a compression ratio improvement to make a difference, it needs to make a big splash. 20% is big if everyone is running into the limits all the time. But if they’re not, you need at least a 2x improvement over the current de-facto standard to make people actually care.

+1 for the lossy video with alpha channel. :)

While you’re probably right in some respect, I have to disagree in general.

The one reason why we use Gzip and JPEG is because every browser supports it. Support is everything.

The reason why ever since 1984, Mac has sucked is because it doesn’t support Windows software, and it doesn’t properly interface with it, t’s that easy. Doesn’t matter if Mac is *actually* much better, it still sucks.

PNG was a big pain back when the only alternatives were JPEG and GIF, since Microsoft’s browser (which, hate it or love it, was important and still is) didn’t support them, and later only supported them with some JavaScript code that triggered an ActiveX warning. PNG was way better than GIF (not just because of size, but in every respect), yet it took forever to become accepted. Because, well you guessed it… because PNG sucked, if the most common browser at that time didn’t display it.

Similar can be said of JPEG2000, or ppmd compression. Who cares if they are any better, there’s hardly any software that will read it. You’ll always need to supply an alternative.

About compression ratios, the thing with bandwidth and storage is, sometimes you just *do* run against hard limits. My wife regularly downloads recordings from meetings (ranging from 45 mins to 3 hours) and archives them (to keep an evidence track on who agreed on what, in case). Incidentially, the servers used by the service provider doing the recordings don’t deliver much more than a hundred kilobytes per second, irrespective of what bandwidth you have. Gosh, she’d be super happy if instead of downloading 200MiB, she’d only have to download 20MiB. Or 5MiB.

Similar is true for my private camera and my MP3 player. Used to be they had a 16MB SD-card, which seemed to be an awful lot. Now they have 16GB of internal memory and a 64GB SDHC-card, which isn’t anything special.

Which is great, *except* you still only get 20MB/s sequential writes at best (reading is admittedly 2-3 times faster, but that is not nearly good enough either) and you get less than half that when it’s some 4000-5000 files you’re writing.

Copying my music collection to one of our MP3 players (obviously each of us got one of their own) takes around 2 1/2 hours. That’s 5 hours of my life lost for both. Gee, how nice it would be if it took just 5-10 minutes.

But even if a better audio compression existed that *only* reduced these 5 hours to 1 hour, I’d already be super happy (provided that the MP3 player can play still it back!).

It’s funny coming back to look at old posts like this one, because fgiesen’s statements are practically prophetic.

The very last comment bemoans the state of digital photography, and yet, where a 64gb SDHC card transferred at 20 MB/s a few years ago, today the cheapest $20 64gb UHS card transfers at 80 MB/s, and if you’re willing to spend the same $150 for a higher end UHS-2 card as you did for that slow 64gb SDHC card of yesteryear you can get 280 MB/s. The top of the line is currently the CFast 2 at 500 MB/s.

What used to take an hour now takes less than 4 minutes, and we do not appear to have hit any hard limit for transfer speeds.

And the pictures haven’t gotten much bigger either, because we’ve hit the practical limits of what our eyes can see, and the number of photons needed to accurately trigger the photo-cells of digital cameras. You don’t see much more than 16 megapixels in a camera these days unless it’s professional grade DSLR gear, which have gigantic image sensors and so can still capture accurate color at 40+ megapixels. Even then a lot of non-DSLR camera makers are sticking with 12 megapixels to get better color out of their smaller image sensor, because we’ve hit literal physical limits in the technology in that regard. A 12mp photo with accurate color looks significantly better than a 16mp photo and less accurate color.

Transfer speeds have increased by a factor of 30, but photo size has only roughly doubled. Compression, at this point, is not an issue for photos in almost every case.

It’s even true online. Today 1 gigabit internet is relatively common, and cable companies are suffering because so many people stream 1080p video over the internet. High-speed internet is common enough now that various services can simply assume that you have 200 mbps or faster internet service, and still not neglect a significant portion of their target internet user.

Lastly, 4k TV is a thing, but it’s very slow to catch on because frankly, it’s hard to tell the difference between it and 1080p except in very specific circumstances. We’re clearly bumping up against the edge of what is practical in that regard, but again fgiesen predicted that video would be the last to go.

Even so, it doesn’t look like a format beyond a large-format BlueRay will be needed, because more and more content is being delivered over the internet instead of via physical copies. Even buying some AAA video games in box stores just gets you a download key these days for 30+ gigabytes of content. Many of the remaining console games that do have a physical copy don’t ever install it, instead downloading the latest version of the game as soon as you put it into the machine.

It’s a totally different world for this sort of thing, and what are the most popular media formats even still? JPEG, GIF, MP3, and H.264. H.265 will probably replace H.264, as it does meet fgiesen’s 2x standard, but it hasn’t done so yet due to a 10 fold increase in processing requirements. H.265 is, however, much more suitable for parallel processing, which is the direction CPU’s have been going ever since Moore’s law started breaking down. The only way I see getting a video format winning the market after H.265 is if has 2x+ the compression of H.265 AND it is significantly amenable to parallel processing.

This is an interesting post in retrospect. Call me a cynic, but this sounds suspiciously like the argument I used to hear all the time that “we don’t need to worry about optimizing the software, because the hardware will be faster in a couple years anyway”. And I think we’ve all seen how that panned out.

Some of these predictions turned out to be pretty far off the mark. For example, audio compression. High-end phones in 2018 still commonly ship with 64gb storage and no sd card expansion. I have a 32gb phone from a few years ago, and I can’t fit my (medium-sized) music collection on it in mp3 format without converting it all to a lower quality. At 160kbps, it just barely fits, and leaves almost no room for anything else besides the OS and standard apps. And I’m adding more to it all the time. I’m lucky that 128kbps is good enough for my ears for my purposes, but the conversion still takes an eternity, and of course the transfer does too. Storing it all uncompressed? Forget about it!

Nevermind that most people *aren’t* on anything near high-end hardware. It’s easy for us developers to forget that. Large portions of the world’s population are still browsing the web on pitifully slow connections, and mobile data limits are still ever-present even for those of us with fancy first-world bandwidth. If you assume best-case hardware and usage for everything, the situations looks just peachy. But that’s not the reality most people are living in.