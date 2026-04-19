---
title: PCA image color compression experiment¶
url: https://30fps.net/notebooks/pcacolors
published: '2024-03-05'
source_blog: Computer Graphics & Programming with Pekka Väänänen — 30fps.net
source_site: https://30fps.net/
category: graphics
fetched: '2026-04-19'
---

Pekka Väänänen | [30fps.net](https://30fps.net/) |
*March 5th, 2024*

We can reduce an RGB image into two channels by finding the top two principal directions with Principal Component Analysis (PCA) and representing each pixels RGB values as a combination of those two. It's a bit like a continuous two-color palette.

The principal directions would also be need to be transmitted along the new two channeled image, just like in a paletted image.

```
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
# Load image with PIL:
image = Image.open('bliss.jpg')
image = image.resize((image.size[0]//8, image.size[1]//8))
image_data = np.array(image)/255.
flattened_image_data = image_data.reshape(-1, 3)
colors = [tuple(flattened_image_data[i]) for i in range(flattened_image_data.shape[0])]
# Perform PCA:
pca = PCA(n_components=2)
model = pca.fit(flattened_image_data)
reduced_data = model.transform(flattened_image_data)
result = reduced_data.reshape((*image_data.shape[:2],2))
reconstruction = pca.inverse_transform(result).reshape((*image_data.shape[:2],3))
fig, ax = plt.subplots(3,2,figsize=(14,16))
ax_in, ax_reco, ax_out_a, ax_out_b, ax_pri1, ax_diff = ax.flatten()
ax_in.imshow(image_data)
ax_reco.imshow(reconstruction.clip(0,1))
ax_out_a.imshow(result[...,0])
ax_out_b.imshow(result[...,1])
ax_in.set_title("Input image")
ax_reco.set_title("Reconstruction")
ax_out_a.set_title("Encoded channel 1")
ax_out_b.set_title("Encoded channel 2")
ax_pri1.scatter(reduced_data[...,0], reduced_data[...,1], c=colors)
ax_pri1.set_xlabel("Principal direction 1")
ax_pri1.set_ylabel("Principal direction 2 ")
ax_pri1.set_title("Image data distribution in PCA space")
ax_diff.imshow(np.mean(np.abs(image_data - reconstruction), axis=2))
ax_diff.set_title("L1 error between input and reconstruction")
for a in ax.flatten()[:4]:
a.axis('off')
ax_diff.axis('off')
plt.suptitle("Encoding image colors in two channels with PCA")
plt.show()
print('Principal components:\n', model.components_)
```

Seems to work quite well with most error in dark shades. Perhaps could be improved with a perceptual colorspace instead of RGB.

Copyright (c) 2024 Pekka Väänänen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.