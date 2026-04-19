---
title: Color quantization with a self-organizing map¶
url: https://30fps.net/notebooks/sompalette
published: '2024-03-08'
source_blog: Computer Graphics & Programming with Pekka Väänänen — 30fps.net
source_site: https://30fps.net/
category: graphics
fetched: '2026-04-19'
---

Pekka Väänänen | [30fps.net](https://30fps.net/) |
*March 8th, 2024*

The popular [ScreenToGif](https://www.screentogif.com/) recording tool includes a high quality color quantizer, called [ NeuralQuantizer](https://github.com/NickeManarin/ScreenToGif/blob/4baa71b554e84b9939c9d6c7a92eb86d465a8863/ScreenToGif.Util/Codification/Gif/Encoder/Quantization/NeuralQuantizer.cs#L336).
I assumed it would be a simple fully connected network but it's actually a one-dimensional

I implemented something similar in Python using some Riley Smith's neat [sklearn-som](https://pypi.org/project/sklearn-som/) library. This notebook shows how to do it.

```
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
image = Image.open('krull2.png')
image = image.resize((image.size[0]//4, image.size[1]//4))
image_data = np.array(image)[...,:3]/255. # RGB in [0,1]
image_flat = image_data.reshape(-1,3) # Nx3 shape
plt.imshow(image_data)
```

We initialize the palette ("weights") to a greyscale gradient like *NeuralQuantizer* does. This seems to give a much better starting point than the normally distributed noise done by default.

```
from sklearn_som.som import SOM
import time
start = time.time()
M = 256
print(f"Fitting a palette of {M} colors")
som = SOM(m=M, n=1, dim=3, lr=1.0, sigma=2, max_iter=3000, random_state=1234)
# Start with a greyscale palette. Create an Mx3 array with values in range [0,1].
som.weights = np.tile(np.linspace(0,1,M)[:,np.newaxis], (1,3))
som.fit(image_flat)
# Compute clusters and assignments
assignments = som.predict(image_flat)
# Extract a Mx3 array that's the colors the algorthm chose
palette = som.cluster_centers_.copy()[:,0,:]
assignments_image = assignments.reshape(*image_data.shape[:2])
output_image = np.take(palette, assignments, axis=0).reshape((*image_data.shape[:2],3))
# Take the palette indices that were actually used and pack them into an image.
uniq, counts = np.unique(assignments, return_counts=True)
used_colors = palette[uniq]
palette_image = np.zeros((16,M//16,3))
palette_image.reshape(-1,3)[:used_colors.shape[0]] = used_colors
print(f"Took {time.time()-start:.3f} seconds. Used {uniq.shape[0]} colors.")
```

```
# Plot the results
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
ax_input, ax_output, ax_assign, ax_palette = ax.flatten()
ax_input.imshow(image_data)
ax_input.set_title("Input image")
ax_output.imshow(output_image.clip(0,1))
ax_output.set_title(f"Output image ({used_colors.shape[0]} colors)")
ax_assign.imshow(assignments_image)
ax_assign.set_title("Palette indices")
ax_palette.imshow(palette_image.clip(0,1))
ax_palette.set_title("Palette")
for a in ax.flatten():
a.axis('off')
plt.suptitle("Color palette found with a self-organizing map")
plt.tight_layout()
plt.show()
```

The palette still follows the gradient we initialized it with but has been clearly fit to the image contents. The self-organizing map update rule moves nearby palette values to the same direction, keeping the palette "smooth" as can be seen above.

This palette seems pretty good to me. Still, it's wasting palette slots with very similar colors. With [a more colorful image](https://30fps.net/hulk-2008-still-result.png) that becomes quite apparent. I think this could be remedied by decreasing smoothing during optimization, so that at the end only single palette colors would be tuned without bothering any neighbors. The implementation in *NeuralQuantizer* seems to do this.

*Thanks to mankeli for encouraging me to study the original color quantizer code.*

Copyright (c) 2024 Pekka Väänänen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.