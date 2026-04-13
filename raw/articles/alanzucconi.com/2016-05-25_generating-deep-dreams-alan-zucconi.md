---
title: Generating Deep Dreams - Alan Zucconi
url: https://www.alanzucconi.com/2016/05/25/generating-deep-dreams/
author: Alan Zucconi
published: '2016-05-25'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

The previous post in this series, [Understanding Deep Dreams](https://www.alanzucconi.com/2015/07/06/live-your-deepdream-how-to-recreate-the-inceptionism-effect/), explained what deep dreams are, and what they can be used for. In this second post you’ll learn how to create them, with a step by step guide.

In August 2015, Google Research released the full source code they have been using to generate their pictures. My guide is strongly inspired by [this one](https://github.com/BVLC/caffe/wiki/Ubuntu-14.04-VirtualBox-VM), which unfortunately didn’t work for many users. The following instructions will show how to virtualise Ubuntu 14.04.02 with VirtualBox, and how to run your very own deep dreams on it.

You can test this very technique using [DeepDreamThis](https://twitter.com/DeepDreamThis), a twitter bot that will create deep dreams out of the images you send to it. You can check a detailed guide on how to use it [here](https://www.alanzucconi.com/2015/07/15/deepdreamthis-how-to-deepdream-on-twitter/). You can also check [DeepForger](https://twitter.com/DeepForger), which uses neural networks to transfer artistic styles from a painting to a picture.

- Virtualise Ubuntu 14.04.02
- Install
[VirtualBox](https://www.virtualbox.org/) - Download the
[Ubuntu 14.04.02](http://releases.ubuntu.com/14.04.2/ubuntu-14.04.2-desktop-amd64.iso)iso - Create a new Virtual machine for “
*Linux / Ubuntu 64bit*“. - You’ll need at least 10Gb of space and at least 2048Mb of RAM
- In the Settings > Storage properties, add the downloaded iso of Ubuntu in the CD drive
- Run the virtual machine
- Install Ubuntu

- Install
- Install Guest Additions
- From the VirtualBox windows:
*Device*> “*Insert Guest Additions CD image*“ - Install
- Restart the machine

- From the VirtualBox windows:
- Install build essentials
`sudo apt-get install build-essential`

`sudo apt-get install linux-headers-`uname -r``


- Install
`caffe`

and`deepdream`

dependencies`sudo apt-get install -y curl libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev protobuf-compiler gfortran libjpeg62 libfreeimage-dev libatlas-base-dev git python-dev python-pip libgoogle-glog-dev libbz2-dev libxml2-dev libxslt-dev libffi-dev libssl-dev libgflags-dev liblmdb-dev python-yaml imagemagick python-opencv`

`sudo easy_install pillow`


- Download
`caffe`

`cd ~`

`git clone https://github.com/BVLC/caffe.git`


- Install
`caffe`

python dependencies`cd caffe`

`cat python/requirements.txt | xargs -L 1 sudo pip install`

`sudo ln -s /usr/include/python2.7/ /usr/local/include/python2.7`

`sudo ln -s /usr/local/lib/python2.7/dist-packages/numpy/core/include/numpy/ /usr/local/include/python2.7/numpy`


- Configure
`caffe`

`cp Makefile.config.example Makefile.config`

`nano Makefile.config`

- Uncomment the line
`# CPU_ONLY := 1`

- Under
`PYTHON_INCLUDE`

, replace`/usr/lib/python2.7/dist-packages/numpy/core/include`

with`/usr/local/lib/python2.7/dist-packages/numpy/core/include`


- Compile
`caffe`

`make pycaffe`

`make all`

`make test`

`make runtest`

- Be sure the output of
`make runtest`

doesn’t include any error `make distribute`


- Make
`pycaffe`

available to`python`

`sudo cp distribute/lib/libcaffe.so distribute/python/caffe`

`sudo cp -r distribute/python/caffe /usr/local/lib/python2.7/dist-packages/caffe`

`sudo nano /etc/ld.so.conf.d/caffe.conf`

`LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/caffe/distribute/python/caffe`


Write the full path to the`caffe/distribute/lib/`

folder; for instance:`/home/alanzucconi/caffe/distribute/lib/`

. Do not use`~`

.`sudo ldconfig`

- You should also put these lines in the
`.bashrc`

file, so that they are executed when your computer starts (remember to use the path to your folders):`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/caffe/distribute/python/caffe`

`export PYTHONPATH=$PYTHONPATH:~/caffe/distribute/python/`


- Download the GoogLeNet model
`cd ~/caffe/models/bvlc_googlenet`

`curl -O "http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel"`


- Download
`deepdream`

`cd ~`

`git clone https://github.com/google/deepdream.git`


- The code
- In the
`deepdream`

folder create a file called`dream.py`

- Fill it with the code below
`cd ~/deepdream`

`sudo python dream.py`


- In the

# imports and basic notebook setup from cStringIO import StringIO import numpy as np import scipy.ndimage as nd import PIL.Image from IPython.display import clear_output, Image, display from google.protobuf import text_format import cv2 import caffe showimages = True def showarray(a, fmt='jpeg'): a = np.uint8(np.clip(a, 0, 255)) f = StringIO() PIL.Image.fromarray(a).save(f, fmt) global showimages if showimages: a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB) cv2.imshow('image',a) cv2.waitKey(1) model_path = '../caffe/models/bvlc_googlenet/' # substitute your path here net_fn = model_path + 'deploy.prototxt' param_fn = model_path + 'bvlc_googlenet.caffemodel' # Patching model to be able to compute gradients. # Note that you can also manually add "force_backward: true" line to "deploy.prototxt". model = caffe.io.caffe_pb2.NetParameter() text_format.Merge(open(net_fn).read(), model) model.force_backward = True open('tmp.prototxt', 'w').write(str(model)) net = caffe.Classifier('tmp.prototxt', param_fn, mean = np.float32([104.0, 116.0, 122.0]), # ImageNet mean, training set dependent channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB # a couple of utility functions for converting to and from Caffe's input image layout def preprocess(net, img): return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data'] def deprocess(net, img): return np.dstack((img + net.transformer.mean['data'])[::-1]) def make_step(net, step_size=1.5, end='inception_4c/output', jitter=32, clip=True): '''Basic gradient ascent step.''' src = net.blobs['data'] # input image is stored in Net's 'data' blob dst = net.blobs[end] ox, oy = np.random.randint(-jitter, jitter+1, 2) src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift net.forward(end=end) dst.diff[:] = dst.data # specify the optimization objective net.backward(start=end) g = src.diff[0] # apply normalized ascent step to the input image src.data[:] += step_size/np.abs(g).mean() * g src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image if clip: bias = net.transformer.mean['data'] src.data[:] = np.clip(src.data, -bias, 255-bias) def deepdream(net, base_img, iter_n=10, octave_n=4, octave_scale=1.4, end='inception_4c/output', clip=True, **step_params): # prepare base images for all octaves octaves = [preprocess(net, base_img)] for i in xrange(octave_n-1): octaves.append(nd.zoom(octaves[-1], (1, 1.0/octave_scale,1.0/octave_scale), order=1)) src = net.blobs['data'] detail = np.zeros_like(octaves[-1]) # allocate image for network-produced details for octave, octave_base in enumerate(octaves[::-1]): h, w = octave_base.shape[-2:] if octave > 0: # upscale details from the previous octave h1, w1 = detail.shape[-2:] detail = nd.zoom(detail, (1, 1.0*h/h1,1.0*w/w1), order=1) src.reshape(1,3,h,w) # resize the network's input image size src.data[0] = octave_base+detail for i in xrange(iter_n): make_step(net, end=end, clip=clip, **step_params) # visualization vis = deprocess(net, src.data[0]) if not clip: # adjust image contrast if clipping is disabled vis = vis*(255.0/np.percentile(vis, 99.98)) showarray(vis) print octave, i, end, vis.shape clear_output(wait=True) # extract details produced on the current octave detail = src.data[0]-octave_base # returning the resulting image return deprocess(net, src.data[0]) img = np.float32(PIL.Image.open('sky1024px.jpg')) showarray(img) frame=deepdream(net, img) PIL.Image.fromarray(np.uint8(frame)).save("frames/a.jpg") frame=deepdream(net, img, end='inception_3b/5x5_reduce') PIL.Image.fromarray(np.uint8(frame)).save("frames/b.jpg") frame = img frame_i = 0 h, w = frame.shape[:2] s = 0.05 # scale coefficient for i in xrange(100): frame = deepdream(net, frame) PIL.Image.fromarray(np.uint8(frame)).save("frames/%04d.jpg"%frame_i) frame = nd.affine_transform(frame, [1-s,1-s,1], [h*s/2,w*s/2,0], order=1) frame_i += 1 cv2.destroyAllWindows()

**Lines 98 and 101** uses the `deepdream`

function to generate different dreams. The `end`

parameter is used to determine which layer we want to analyse. You can check which layers can be analysed by printing `net.blobs.keys()`

.

![deepdream](../../assets/c92cb3e69bd5c3ff.jpg)

I’ve created a [repository](https://drive.google.com/folderview?id=0B4nCcaMlgxV2flNrWXRwOGNLSEI1SDR2WnhLNVVPanUxOGtwT2lEUVlLTy14VUQzaF84cGs&usp=sharing) of all the layers you can query. Find an effect you like, and use the name of the file (without the extension) and the `end`

parameter. Just remember to replace any `__`

(double underscore) with a `/`

(Unix slash).

This post explained how to use the machine learning framework Caffe to generate deep dreams. Using a virtualised environment, however, might not be the best option. Neural networks require a lot of computational power, which is often unavailable in a virtual machine. For best performances, you should run deep dreams using a GPU.

This tutorial referred to the first, original tutorial released by Google Research. Other techniques have been evolved in the past months, including algorithms that works on videos.

#### Other resources

- Part 1.
[Understanding Deep Dreams](https://www.alanzucconi.com/?p=2334) - Part 2.
**Generating Deep Dreams**

[deepdream](https://github.com/google/deepdream): the GIT project used by Google Research;[Caffe](http://caffe.berkeleyvision.org/): the framework used to implement neural networks. Valid alternatives are[Theano](http://deeplearning.net/software/theano/)and[Torch](http://www.torch.ch/);[Running the deep dream](http://ryankennedy.io/running-the-deep-dream/): an alternative tutorial to run deep dreams;[neural-style](https://github.com/jcjohnson/neural-style): a Torch variation of deep dreams, used to transfer artistic styles;[neural-doodle](https://github.com/alexjc/neural-doodle): a tool that allows to draw in the style of a particular artist.

## Leave a Reply Cancel reply