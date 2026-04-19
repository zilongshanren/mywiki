---
title: Efficiently split a NumPy array into tiles¶
url: https://30fps.net/notebooks/split-to-tiles
published: '2024-11-07'
source_blog: Computer Graphics & Programming with Pekka Väänänen — 30fps.net
source_site: https://30fps.net/
category: graphics
fetched: '2026-04-19'
---

Pekka Väänänen | [30fps.net](https://30fps.net/) |
*November 7th, 2024.*

Sometimes in image processing you'd like to work with an image in tiles, in square blocks of pixels I mean.
The tiles can be used for [vector quantization](https://30fps.net/notebooks/image-vq/), for example.
You can split the image with a simple loop like this:

```
img = ... # load image of shape [h x w]
B = 8 # tile size in pixels
bh, bw = image.shape[0] // B, image.shape[1] // B # size in tiles
tiles = np.zeros((bh, bw, B, B))
for y in range(bh):
for x in range(bw):
single_tile = img[
(y * B):((y+1) * B),
(x * B):((x+1) * B)]
tiles[y, x] = single_tile
```

Unfortunately it gets slow for large images.
Fortunately it's possible to do the same thing **1000x faster** with some array reshaping trickery.
The code below is also **15x faster** than scikit-image's [ view_as_blocks](https://scikit-image.org/docs/stable/api/skimage.util.html#skimage.util.view_as_blocks) function that does the same thing.

```
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
def split_to_tiles(img, B):
"""
Splits an image into an array of BxB pixel tiles.
Parameters:
img (ndarray): The input image to be split.
B (int): The size of each tile in pixels. It must be a positive integer.
Returns:
ndarray: A 2D array of shape [height/B, width/B] containing the BxB pixel tiles extracted from the image.
The array is read only.
Raises:
ValueError: If the input is not a 2D image.
"""
if len(img.shape) == 2:
h, w = img.shape
elif len(img.shape) == 3:
h, w, C = img.shape
else:
raise ValueError(f"Unspported image shape {img.shape}")
# Image size measured in tiles instead of pixels
bh, bw = h//B, w//B
if h%B != 0 or h%B !=0:
print(f"Cropping image to a multiple of tile size {B}")
h = bh * B
w = bw * B
img = img[:h, :w]
if len(img.shape) == 2:
tiles = img.reshape(bh, B, bw, B) # [bh x B x bw x B]
tiles = tiles.transpose(0, 2, 1, 3) # [bh x bw x B x B]
elif len(img.shape) == 3:
tiles = img.reshape(bh, B, bw, B, C) # [bh x B x bw x B x C]
tiles = tiles.transpose(0, 2, 1, 3, 4) # [bh x bw x B x B x C]
return tiles
img = data.camera()
fig, ax1 = plt.subplots(1,1)
ax1.imshow(img, cmap=plt.cm.gray)
plt.show()
tiles = split_to_tiles(img, 16)
print(f"{tiles.shape=}")
fig, ax = plt.subplots(4,4)
for y in range(4):
for x in range(4):
ax[y][x].imshow(tiles[8+y,14+x], cmap=plt.cm.gray, vmin=0, vmax=255)
ax[y][x].axis('off')
plt.show()
```

The tiles are a read-only view to the image so the following won't work:

```
# tiles[10, 10][:] = 0
# Would throw "ValueError: assignment destination is read-only"
```

The inverse operation of a split is implemented in the same way:

```
def merge_tiles_to_image(tiles, B):
"""
Merge an array of tiles back into a single image.
The inverse operation of split_to_tiles.
Args:
tiles (numpy.ndarray): 4D or 5D array of BxB pixel tiles.
Shape: [bh, bw, B, B] for grayscale or
[bh, bw, B, B, C] for RGB.
B (int): The size of each tile used when splitting.
Returns:
numpy.ndarray: Original image before splitting.
Shape: [h, w] for grayscale or [h, w, C] for RGB.
"""
bh, bw = tiles.shape[:2]
# Handle cases with one channel and multiple channels separately.
if len(tiles.shape) == 4: # [bh, bw, B, B] input shape
image = tiles.transpose(0, 2, 1, 3) # [bh, B, bw, B] reorder block axes
image = image.reshape(bh*B, bw*B) # [h, w] collapse back to pixels
elif len(tiles.shape) == 5: # [bh, bw, B, B, C] input shape
image = tiles.transpose(0, 2, 1, 3, 4) # [bh, B, bw, B, C] reorder block axes
image = image.reshape(bh*B, bw*B, -1) # [h, w, C] collapse back to pixels
return image
img2 = merge_tiles_to_image(tiles, 16)
diff = np.sum(np.abs(img2 - img))
print(f"Image difference (should be zero): {diff}")
```

We can also make vectors of the tiles. This is useful for analysis such as clustering where you don't care about the spatial relationships between the pixels of a tile.

```
X = tiles.reshape(-1, tiles.shape[2] * tiles.shape[3])
print(f"Data array X shape: {X.shape}")
print(f"The {X.shape[1]}-element vectors look like this:\n")
print(X[10])
```

```
from skimage.util import view_as_blocks
# Benchmark the naive for loops implementation versus the new implementation
def split_to_tiles_naive(img, B):
h, w = img.shape[:2]
bh, bw = h//B, w//B
tiles = np.empty((bh, bw, B, B))
for y in range(bh):
for x in range(bw):
single_tile = img[
(y * B):((y+1) * B),
(x * B):((x+1) * B)]
tiles[y, x] = single_tile
return tiles
import timeit
rounds = 1000
naive_time = timeit.timeit(lambda: split_to_tiles_naive(img, 16), number=rounds)
scikit_time = timeit.timeit(lambda: view_as_blocks(img, (16, 16)), number=rounds)
new_time = timeit.timeit(lambda: split_to_tiles(img, 16), number=rounds)
print(f"Naive took: {naive_time*1000:.3f} ms")
print(f"scikit took: {scikit_time*1000:.3f} ms")
print(f"New took: {new_time*1000:.3f} ms")
print()
print(f"New time is {(naive_time / new_time):.2f} x faster than naive")
print(f"New time is {(scikit_time / new_time):.2f} x faster than scikit-image")
```

I was actually surprised to see a speed difference this large :) Allocating the **tiles** array outside the naive function had roughly the same speed as the code above.
The [scikit-image implementation](https://github.com/scikit-image/scikit-image/blob/a160f384523ac70173d069954b7084bee79fb68e/skimage/util/shape.py#L8-L93) uses [ np.stride_tricks.as_strided](https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html) which for some reason is clearly slower than just the reshape + transpose trick we do here.

*Update: Added scikit-image mention and its benchmark numbers after publishing this notebook.*

Copyright (c) 2024 Pekka Väänänen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.