---
title: Moving basis decomposition for images¶
url: https://30fps.net/notebooks/mbd-in-2d
published: '2024-03-16'
source_blog: Computer Graphics & Programming with Pekka Väänänen — 30fps.net
source_site: https://30fps.net/
category: graphics
fetched: '2026-04-19'
---

Pekka Väänänen | [30fps.net](https://30fps.net/) |
*March 16th, 2024*

This is an experiment in lossy 2D image compression inspired by the
2021 paper [ Moving Basis Decomposition for Precomputed Light Transport](https://arisilvennoinen.github.io/Publications/mbd.pdf) by Ari Silvennoinen and Peter-Pike Sloan.
This notebook is not easily understandable without reading the paper first but I wanted to have an implementation of the idea out there.

You can think of this as a variant of PVRTC ([paper pdf](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=1c9b763ecf4834c99b4aa475eccd99e61c6414bf)) technique.
At decoding time we bilinearly upsample two arrays **B** and **c**:

For each output pixel we compute a weighted sum of **B**'s interpolated colors using **c**'s interpolated weights.
At coding time numerical optimization constructs both arrays are found simultaneously.

Note that my approach here is much simplified than what proposed in the paper:

`newton-cg`

optimizer from the ```
"""
Setup:
- input image [H x W x D], D=3
- global PCA fit for L=2 components
- a dense "coefficient" tensor of shape [H x W x L]
- a sparse "basis" tensor of shape [N x M x L x D]
Both dense and sparse tensors are bilinearly interpolated.
"""
import time
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
image = Image.open('hulk1.jpg')
max_width = 400
image = image.resize((max_width, int(round(image.size[1]*(max_width/image.size[0])))))
image_data = np.array(image)/255.
basis_div = 16 # Basis vector downscaling factor
coeff_div = 2 # Coefficient vector downscaling factor
D = 3 # Input dimension
L = 2 # Number of D-dimensional basis vectors
H_input, W_input = image_data.shape[:2]
H, W = image_data.shape[0]//coeff_div, image_data.shape[1]//coeff_div
N, M = H//basis_div, W//basis_div
small_image_data = np.array(image.resize((W, H)))/255.
flattened_image_data = image_data.reshape(-1, 3)
flattened_small_image_data = small_image_data.reshape(-1, 3)
# Perform PCA
pca = PCA(n_components=L)
model = pca.fit(flattened_image_data)
reduced_data_small = model.transform(flattened_small_image_data)
init_coeff_small = reduced_data_small.reshape((*small_image_data.shape[:2],L))
recon_baseline_small = pca.inverse_transform(init_coeff_small).reshape((*small_image_data.shape[:2],D))
fig, (ax_input, ax_init) = plt.subplots(1,2, figsize=(10,6))
ax_input.imshow(image_data)
ax_input.set_title("Input image")
ax_init.imshow(recon_baseline_small.clip(0,1))
ax_init.set_title("Global PCA initialization")
plt.tight_layout()
print('PCA basis:\n', model.components_)
```

```
B = np.zeros((N, M, L, D))
B[..., :, :] = model.components_.copy()
c = init_coeff_small.copy()
print('B tensor shape:', B.shape)
print('c tensor shape:', c.shape)
assert B.shape == (N, M, L, D)
assert c.shape == (H, W, L)
```

```
import torch
import torch.nn
import torch.optim
from torchvision import transforms
import torch.nn.functional as F
from torchmin import Minimizer
def resize_tensor(x, h, w):
# pytorch has convention [batch x channels x height x width]
# so we go with [1 x C x H x W] for scaling
assert(len(x.shape) >= 3)
xt = x.reshape(1, -1, *x.shape[-2:])
xt_scaled = F.interpolate(xt, (h, w), mode='bilinear', align_corners=False)
# print(xt_scaled.shape)
return xt_scaled.reshape(*x.shape[:-2], *xt_scaled.shape[-2:])
def reconstruct(Bin, cin):
Bs = resize_tensor(Bin, Hs, Ws)
cs = resize_tensor(cin, Hs, Ws)
# Bs shape: [L x D x Hs x Ws]
# cs shape: [L x Hs x Ws]
# yhat shape: [D x Hs x Ws]
# Reconstruct each output pixel as a weighted sum of basis vectors.
# Weights are set in the 'cs' tensor.
yhat = torch.einsum('lij,ldij -> dij', cs, Bs)
return yhat
# Reconstruction resolution is [Hs x Ws] pixels
Hs, Ws = H_input, W_input
device = 'cuda'
# Center the target image 'y' to zero mean
center = torch.from_numpy(pca.mean_).reshape(3,1,1).to(device)
y = torch.from_numpy(image_data).to(device)
y = y.permute(2, 0, 1) - center
# Convert the initialized B and c numpy arrays to PyTOrch Bt and ct tensors
Bt = torch.from_numpy(B).to(device).to(torch.float64)
Bt = Bt.permute(2, 3, 0, 1).contiguous()
ct = torch.from_numpy(c).to(device)
ct = ct.permute(2, 0, 1).contiguous().to(torch.float64)
assert(Bt.is_contiguous()) # Make sure parameters lie in contigious memory
assert(ct.is_contiguous()) # in case want to use PyTorch's L-BFGS optimizer.
# Reconstruct initialized arguments on the CPU for a sanity check
Bs = resize_tensor(Bt.to('cpu'), Hs, Ws)
cs = resize_tensor(ct.to('cpu'), Hs, Ws)
Bs_np = Bs.detach().permute(2,3,0,1).cpu().numpy()
cs_np = cs.detach().permute(1,2,0).cpu().numpy()
reco_np = np.einsum('ijl,ijld -> ijd', cs_np, Bs_np)
output_start_np = reco_np + pca.mean_ # Undo centering
# Optimize
loss_fn = torch.nn.MSELoss()
# This optimizer seemed to work OK but I'm sure there are better options available.
# A simple stochastic gradient descent was way too slow to converge.
# Weight decay is applied to coefficients only to constrain the problem so that a unique
# solution is possible.
max_iter = 50
weight_decay = 0.5 * 0.001
optimizer = Minimizer([Bt, ct], method='newton-cg', options={'lr':1.00,'disp':2, 'max_iter': max_iter})
# The objective function to minimize
def f(Bt, ct):
pred = reconstruct(Bt, ct)
reg = torch.mean(ct**2)
return loss_fn(pred, y) + weight_decay * reg
# We don't have any traditional PyTorch optimizer loop but instead a single call
# to 'optimizer.step()' with a high number of iterations.
Bt.requires_grad_()
ct.requires_grad_()
def closure():
global losses
optimizer.zero_grad()
loss = f(Bt, ct)
return loss
optimizer.step(closure)
# Read off the result parameters and reconstruct an image
B_end = Bt.detach().permute(2,3,0,1).cpu().numpy()
c_end = ct.detach().permute(1,2,0).cpu().numpy()
Bs_end = resize_tensor(Bt.detach(), Hs, Ws).permute(2,3,0,1).cpu().numpy()
cs_end = resize_tensor(ct.detach(), Hs, Ws).permute(1,2,0).cpu().numpy()
output_t = reconstruct(Bt.detach(), ct.detach())
output_t += center # Undo centering
```

```
output = output_t.permute(1, 2, 0).cpu().numpy()
output = output.clip(0,1)
y_np = (y + center).permute(1,2,0).cpu().numpy()
y_np = y_np.clip(0,1)
baseline_error = np.mean((output_start_np - y_np)**2)
output_error = np.mean((output - y_np)**2)
baseline_diff = np.mean((output_start_np - output)**2)
print('Error at initialization: ', baseline_error)
print('Error after optimization: ', output_error)
print('Diff between init and result: ', baseline_diff)
```

```
# Compute the number of values in input image divided by values in the compressed representation.
# This isn't really fair because it assumes B and c would be stored with 8 bits per element but
# they are actually float64!
compression_ratio = image_data.size / (c.size + B.size)
fig, ax = plt.subplots(1,2,figsize=(14,6))
ax_input, ax_output = ax.flatten()
ax_input.imshow(image_data)
ax_output.imshow(output)
ax_input.set_title("Input image ")
ax_output.set_title(f"Reconstructed image\n({compression_ratio*100:.0f} % compression ratio)")
for a in ax.flatten():
a.get_xaxis().set_ticks([])
a.get_yaxis().set_ticks([])
plt.tight_layout()
plt.show()
print(f"Naive compression ratio: {compression_ratio*100:.0f} %")
```

In PVRTC the **c** array is stored at output resolution but here it's downsampled by 2x2 and interpolated, like mentioned in the beginning. Interpolation artifacts become very obvious in the cyan neon text. Without downsampling the result would be pretty much perfect but not as interesting :)

```
fig, ax = plt.subplots(4,2,figsize=(13,12))
ax_in, ax_reco, \
ax_out_a, ax_out_b, \
ax_basis1, ax_basis2, \
ax_diff1, ax_diff2 = ax.flatten()
ax_in.imshow(output_start_np.clip(0,1))
ax_reco.imshow(output)
plt.colorbar(ax_out_a.imshow(c_end[...,0]), fraction=0.02079, pad=0.)
plt.colorbar(ax_out_b.imshow(c_end[...,1]), fraction=0.02079, pad=0.)
def tonemap(x):
# Reinhard tonemapping that keeps the sign. But we clip it at the end anyway.
signs = np.sign(x)
xabs = signs*x
mapped = xabs/(1+xabs)
return (signs * mapped).clip(0,1)
ax_basis1.imshow(tonemap(Bs_end[..., 0, :])) # Colors of basis vectors need to mapped to [0,1] range
ax_basis2.imshow(tonemap(Bs_end[..., 1, :])) # so that they can be shown with 'imshow'.
ax_in.set_title("Global PCA initialization")
ax_reco.set_title("Optimized MBD reconstruction")
ax_out_a.set_title("Coefficients 1/2")
ax_out_b.set_title("Coefficients 2/2")
ax_basis1.set_title("Basis vectors 1/2 (tonemapped)")
ax_basis2.set_title("Basis vectors 2/2 (tonemapped)")
ax_diff1.imshow(np.mean(np.abs(output_start_np - output), axis=2))
ax_diff1.set_title("L1 error between initialization and reconstruction")
ax_diff2.imshow(np.mean(np.abs(image_data - output), axis=2))
ax_diff2.set_title("L1 error between input and reconstruction")
for a in ax.flatten():
a.get_xaxis().set_ticks([])
a.get_yaxis().set_ticks([])
plt.suptitle("Moving basis decomposition in 2D")
plt.tight_layout()
plt.show()
```

```
fig, ax_crop = plt.subplots(2,2,figsize=(9,9))
crop_x = 65
crop_y = 5
crop_w = 64
crop_h = 64
def take_crop(im):
return im[crop_y:(crop_y+crop_h),crop_x:(crop_x+crop_w)]
#output_start_np[(crop_y:crop_y
ax_crop.flatten()[0].imshow(take_crop(output_start_np.clip(0,1)))
ax_crop.flatten()[0].set_title("Global PCA initialization")
ax_crop.flatten()[1].imshow(take_crop(output))
ax_crop.flatten()[1].set_title("MBD reconstruction")
ax_crop.flatten()[2].imshow(take_crop(image_data))
ax_crop.flatten()[2].set_title("Input image")
ax_crop.flatten()[3].imshow(np.mean(np.abs(take_crop(image_data) - take_crop(output)), axis=2))
ax_crop.flatten()[3].set_title("L1 error between input and reconstruction")
for a in ax_crop.flatten():
a.get_xaxis().set_ticks([])
a.get_yaxis().set_ticks([])
plt.suptitle("Crop comparison")
plt.tight_layout()
plt.show()
```

In above crops, "Global PCA initialization" couldn't represent the green tone at all in which "MBD reconstruction" succeeds at. The bilinear interpolation artifacts pretty nasty though and a good reminder why this technique is meant for smoothly varying signals such as indirect lighting.

Copyright (c) 2024 Pekka Väänänen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.