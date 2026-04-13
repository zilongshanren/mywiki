---
title: Dithering Algorithm
url: https://www.elopezr.com/dithering-algorithm/
author: Redorav
published: '2014-03-09'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

An implementation of the Floyd-Steinberg dithering algorithm for very low-end Android devices, whose memory requirements were pretty strict. The phone couldn’t handle all the graphics in the 32-bit 8888 color format, and had to be scaled down to the **16-bit 1555** format. The graphics didn’t look as great as the artists had intended, therefore some form of dithering had to be applied. The maximum image size for the phone was 1024×512. The [Floyd-Steinberg](http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/) algorithm is a very well known dithering algorithm, with many variations that try different combinations of the error propagation matrix. I implemented the simplest one for speed. These versions are written in Java, as they targeted the Android platform, but a C++ port is coming.

I tackled the naive approach first, very flexible, very clean, and very **slow**. The lowest phone in our testbed, the Galaxy Ace, had to load ~900 images, dither them and load them into video memory. Therefore I inlined everything, removing all convenience function calls. This version uses a double integer array with the indices laid out as [RGBA component][pixel].

For the second approach I tried **inverting the indices**, to something like [pixel][RGBA component]. It is interesting that with smaller images, such as 800×480, there was a speedup. However, with bigger resolutions such as 1600×1200, performance suffers.

The third approach **removes the ifs in the error propagation matrix** by padding the destination array with one extra line at the bottom and the sides. The error is written into the matrix and simply discarded later, therefore mitigating the conditional performance penalty.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 | // Disperse the error using the Floyd-Steinberg Matrix // Notice how up to 4 ifs can be removed if(x + 1 < imgW) { imgData[0][i + 1] += (redError * 7 / 16); imgData[1][i + 1] += (greenError * 7 / 16); imgData[2][i + 1] += (blueError * 7 / 16); } if(y + 1 < imgH) { if(x > 0) { imgData[0][i + imgW - 1] += (redError * 3 / 16); imgData[1][i + imgW - 1] += (greenError * 3 / 16); imgData[2][i + imgW - 1] += (blueError * 3 / 16); } imgData[0][i + imgW] += (redError * 5 / 16); imgData[1][i + imgW] += (greenError * 5 / 16); imgData[2][i + imgW] += (blueError * 5 / 16); if(x + 1 < imgW) { imgData[0][i + imgW + 1] += (redError / 16); imgData[1][i + imgW + 1] += (greenError / 16); imgData[2][i + imgW + 1] += (blueError / 16); } } |

The last approach uses **scanline alternation** for a memory and performance optimization. Instead of loading a very big scratch array, it allocates two lines (plus the padding) and alternates between the current and next line. After each line processed, the result is written into the final buffer. There is a small performance advantage, and a very obvious big memory improvement.

1 2 3 4 5 6 7 8 9 10 | int[] imgData = new int[4 * NUM_SCANLINES * (m_textureWidth + H_PADDING)]; ... for (int y = 0; y < m_textureHeight - 1; ++y) { int curLine = y % NUM_SCANLINES; int nextLine = (y + 1) % NUM_SCANLINES; int lCurPad = (m_textureWidth + H_PADDING) * curLine; // Start of current line (wrapped) in padded array int lNextPad = (m_textureWidth + H_PADDING) * nextLine; // Start of next line (wrapped) in padded array ... |

Because OpenGL requires POT textures, some textures end up being pretty big. The biggest textures in the program were **512×512** and **1024×512**.

For a 512×512 image,

Approach | Time |
| Old | 47 ms |
| Inverted | 40 ms |
| If removal | 33 ms |
| Scanline | 30 ms |

For a 1024×512 image,

Approach | Time |
| Old | 54 ms |
| Inverted | 67 ms |
| If removal | 38 ms |
| Scanline | 35 ms |

For a 1920×1200 image,

Approach | Time |
| Old | 104 ms |
| Inverted | 107 ms |
| If removal | 74 ms |
| Scanline | 70 ms |

At 2560×1600,

Approach | Time |
| Old | 145 ms |
| Inverted | 153 ms |
| If removal | 111 ms |
| Scanline | 99 ms |

Note how performance degrades as images grow in size between the first two approaches, when fiddling with the order of the array indices, possibly related to how the Java VM handles them internally. The last two approaches employ a simple 1D array in order to avoid these performance discrepancies. The algorithm becomes a little more involved, but performance becomes more predictable.

All in all, the last algorithm performed **~30% faster** than the first one, consuming a negligible amount of memory (**2 * (imageWidth + padding) as opposed to imageWidth * imageHeight**).

The Eclipse project and source code can be found [here](https://dl.dropboxusercontent.com/u/14054799/Portfolio%20Uploads/Dithering_v05.zip).