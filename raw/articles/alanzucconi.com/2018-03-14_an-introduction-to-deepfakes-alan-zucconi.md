---
title: An Introduction to DeepFakes - Alan Zucconi
url: https://www.alanzucconi.com/2018/03/14/introduction-to-deepfakes/
author: Alan Zucconi
published: '2018-03-14'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will cover the theory and practice of creating **deepfakes**: videos in which faces have been swapped using Machine Learning and Deep Neural Networks. If you are interested in learning more about this novel technique, this is the course for you.

After a theoretical introduction, this course will focus on how to make the most out of the popular applications [FakeApp](https://www.fakeapp.org/) and [faceswap](https://github.com/deepfakes/faceswap); most of the deepfakes you will find online (such as the ones featuring Nicolas Cage) have been created using them.

You can read all the posts in this series here:

**Part 1.**[An Introduction to DeepFakes and Face-Swap Technology](https://www.alanzucconi.com/?p=8372)- Part 2.
[The Ethics of Deepfakes](https://www.alanzucconi.com/?p=8300) - Part 3.
[How To Install FakeApp](https://www.alanzucconi.com/?p=8345) - Part 4.
[A Practical Tutorial for FakeApp](https://www.alanzucconi.com/?p=8482) - Part 5.
[An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) - Part 6.
[Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290) - Part 7.
[How To Create The Perfect DeepFakes](https://www.alanzucconi.com/?p=8331)

If you are interested in reading more about AI Art (Stable Diffusion, Midjourney, etc) you can check this article instead: [The Rise of AI Art](https://www.alanzucconi.com/?p=14358).

#### Introduction

Face detection has been a major research subject in the early 2000s. Almost twenty years later, this problem is basically solved and face detection is available as a library in most programming languages. Even face-swap technology is nothing new, and has been around for a few years.

In his article from 2016, [Face Swap using OpenCV](https://www.learnopencv.com/face-swap-using-opencv-c-python/), author Satya Mallick showed how to swap faces programmatically, warping and colour correcting Ted Cruz’s face to fit Donald Trump (below).![](../../assets/c3d70a51c25d4a7c.jpg)


When applied correctly, this technique is uncannily good at swapping faces. But it has a major disadvantage: it only works on pre-existing pictures. It cannot, for instance, morph Donald Trump’s face to match the expression of Ted Cruz.

That has changed in late 2017, when a new approach to face-swap has appeared on Reddit. Such a breakthrough relies on **neural networks**, computational models that are loosely inspired by the way real brains process information. This novel technique allows generating so-called **deepfakes**, which actually morph a person’s face to mimic someone else’s features, although preserving the original facial expression.

When used properly, this technique allows the creation of photorealistic videos at an incredibly low cost. The finale of Rogue One, for instance, featured a digital version of Princess Leia; a very expensive scene which required the expertise of many people. Below, you can see a comparison between the original scene and another one recreated using Deep Learning.

#### Creating Deepfakes

At the moment there are two main applications used to create deepfakes: [FakeApp](https://www.fakeapp.org/) and [faceswap](https://github.com/deepfakes/faceswap). Regardless of which one you will use, the process is mostly the same, and requires three steps: **extraction**, **training** and **creation**.

#### Extraction

The *deep-* in deepfakes comes from the fact that this face-swap technology uses **Deep Learning**. If you are familiar with the concept, you should know that deep learning often requires large amounts of data. Without hundreds (if not thousands!) of face pictures, you will not be able to create a deepfake video.

A way to get around this is to collect a number of video clips which feature the people you want to face-swap. The **extraction** process refers to the process of extracting all frames from these video clips, identifying the faces and aligning them.

![](../../assets/8e085845282c599d.png)

The alignment is critical, since the neural network that performs the face swap requires all faces to have the same size (usually 256×256 pixels) and features aligned. Detecting and aligning faces is a problem that is considered mostly solved, and is done by most applications very efficiently.

#### Training

**Training** is a technical term borrowed from Machine Learning. In this case, it refers to the process which allows a **neural network** to convert a face into another. Although it takes several hours, the training phase needs to be done only once. Once completed, it can convert a face from person A into person B.

![](../../assets/d5bcea95a7e62989.png)

This is the most obscure part of the entire process, and I have dedicated two posts to explain how it works from a technical point of view: [An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) and [Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290)). If you really want to create photorealistic deepfakes, a basic understanding of the process that generates them is necessary.

#### Creation

Once the training is complete, it is finally time to create a deepfake. Starting from a video, all frames are extracted and all faces are aligned. Then, each one is converted using the trained neural network. The final step is to merge the converted face back into the original frame. While this sounds like an easy task, it is actually where most face-swap applications go wrong.

![](../../assets/ae6a469862181b2c.png)

The **creation** process is the only one which does not use any Machine Learning. The algorithm to stitch a face back onto an image is hard-coded, and lacks the flexibility to detect mistakes.

![](../../assets/3cf2659148d4e65f.png)

Also, each frame is processed independently; there is no **temporal correlation** between them, meaning that the final video might have some flickering. This is the part where more research is needed. If you are using faceswap instead of FakeApp, have a look at [df](https://github.com/dfaker/df) which tries to improve the creation process.

#### Conclusion

Deep Learning has made photorealistic face-swap not just possible, but also accessible. This technique is still in its infancy and many more improvements are expected to happen in the next few years.

In the meantime, places like the [FakeApp forum](https://www.fakeapp.org/forum) or the [fakeapp GitHub page](https://github.com/deepfakes/faceswap/issues) are where most of the technical discussion around deepfakes is currently taking place. The community around deepfakes is constantly exploring new approaches, and developers are often very willing to share their creations. This is the case of user [ZeroCool22](https://www.fakeapp.org/forum/discussion-creations/jimmy-fallon-interviews-his-twin) which created a deepfake video of Jimmy Fallon interviewing himself.

Another interesting reading on the subject is [Exploring DeepFakes](https://hackernoon.com/exploring-deepfakes-20c9947c22d9).

It cannot be denied that deepfakes have finally shown the world a practical application of Deep Learning. However, this very technique has often been used without the explicit consent of the people involved. While this is unlikely to be an issue with videos such as the ones shown in this article, the same cannot be said when it is used to create pornographic content. This is why, before showing how to create deepfakes, the next lecture in this online course will focus entirely on the legal and ethical issues of deepfakes.

You can read all the posts in this series here:

**Part 1.**[An Introduction to DeepFakes and Face-Swap Technology](https://www.alanzucconi.com/?p=8372)- Part 2.
[The Ethics of Deepfakes](https://www.alanzucconi.com/?p=8300) - Part 3.
[How To Install FakeApp](https://www.alanzucconi.com/?p=8345) - Part 4.
[A Practical Tutorial for FakeApp](https://www.alanzucconi.com/?p=8482) - Part 5.
[An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) - Part 6.
[Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290) - Part 7.
[How To Create The Perfect DeepFakes](https://www.alanzucconi.com/?p=8331)

A special thanks goes to Christos Sfetsios and David King, who gave me access to the machine I have used to create the deepfakes used in this tutorial.

## Leave a Reply Cancel reply