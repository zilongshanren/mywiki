---
title: Poor man's animation framework revisited
url: https://anteru.net/blog/2011/poor-man-s-animation-framework-revisited
published: '2011-05-02'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Recently, I [described the simple animation system](https://anteru.net/blog/2010/11/08/945/) I used for videos while at NVIDIA. After coming back, I’ve finally had some time to fix some remaining issues and and get a useful tool out of it. The core requirements remained the same:

- Frame-by-frame processing: No .avi or other intermediate files, only plain images.
- Leverage ImageMagick for the actual processing
- Parallel: Efficiently scale with core count

The ImageMagick part was working reasonable well, so I decided to stick with this. However, the original framework required to manually compute the frame offsets which made stitching cumbersome and blending nearly impossible. Looking closer at what was happening, it became quickly obvious that the framework was stream oriented, but it was not explicit anywhere.

## Ava

Enter Ava, the graph-based video processor. Right from the start, Ava is designed around the processing graph. For example, here is the graph for the SRAA video, which is already pretty big:

The key property is that the everything is designed around an image stream. Each node transforms one or more inputs into a single output; and can be evaluated independently of all other nodes. All frame indices are relative, that is, the graph can be easily composed as there is no “global” frame count. And finally, the processing order is bottom-up, or pull, instead of push. This means that each node executes its own inputs first before applying the transformation, minimising wasted work.

An interesting part is how the inputs are handled. As I use ImageMagick for the actual processing, the inputs have to present as files. What Ava does is while it walks the graph (where each node must have a unique name) it also generates unique file names for each node’s input and process. Generating them from the input side is necessary so that for instance a single node which gets piped into several other nodes does not continuously overwrite its own input. Of course, this means some duplicated work, but the net win is that there is no synchronisation whatsoever. Overwriting the same file all the time also has the added advantage that less file system flushes are necessary. Originally, I would delete each file and recreate it again for the next frame, but overwriting directly seems to be a tad faster on Windows.

All of the stuff used to generate the SRAA video is also really compact. There are 11 different node types in total (roughly 200 lines of Python), plus 300 for the graph and finally 100 lines or so of scaffolding. Individual frames can be easily piped into FFMpeg, so there is no comfort loss anywhere. The amount of code is smaller than the original framework, which had less features – mostly because the declarative part (the graph) is split into JSON instead of being intermingled with the processing code.

So much for the definitive version of the animation framework. I completely scrapped the old one in favour of Ava, and when reading the old blog post you should be aware that it was only a proof-of-concept while this here is the real McCoy.