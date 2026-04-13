---
title: How To Create The Perfect DeepFakes - Alan Zucconi
url: https://www.alanzucconi.com/2018/03/14/create-perfect-deepfakes/
author: Alan Zucconi
published: '2018-03-14'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

You can read all the posts in this series here:

- Part 1.
[An Introduction to DeepFakes and Face-Swap Technology](https://www.alanzucconi.com/?p=8372) - Part 2.
[The Ethics of Deepfakes](https://www.alanzucconi.com/?p=8300) - Part 3.
[How To Install FakeApp](https://www.alanzucconi.com/?p=8345) - Part 4.
[A Practical Tutorial for FakeApp](https://www.alanzucconi.com/?p=8482) - Part 5.
[An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) - Part 6.
[Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290) **Part 7.**[How To Create The Perfect DeepFakes](https://www.alanzucconi.com/?p=8331)

If you are interested in reading more about AI Art (Stable Diffusion, Midjourney, etc) you can check this article instead: [The Rise of AI Art](https://www.alanzucconi.com/?p=14358).

Photoshop and After Effects are used every day by professionals, but that does not mean that just installing either of them is all it takes to create photorealistic images and videos. Likewise, creating realistic face-swapped videos is hard. Like any artistic endeavour, the final result is a mixture of talent, commitment and right tools.

There are two critical processes involved in the making of any face-swap video: the **training** and the **creation**. Training is the process which (literally!) trains a neural network to deconstruct and reconstruct faces. Since the release of face-swapping technology, there have been countless discussions online on how to train a network to achieve photorealistic results. Let’s start by analysing the problem from a Machine Learning point of view.

The task of the neural network is to encode an image from person A, and reconstruct one with similar features to resemble another person B. Imagine you had a picture of a person A, and had to manually edit it to make it look like person B. The complexity of such a task largely depends on how different the two faces are. This is easy to understand, as more “changes” are necessary to convert A into B. The neural network works in a similar fashion, as a more complex mapping has to be learned.

What is the simplest task that a face-swapping neural network can be asked to perform? Because it is built on autoencoders, is to reconstruct face A from face A. This might seem trivial at first, but keep in mind that even morphing between images from the same person is far from being trivial. What makes the task easier, however, is that the autoencoders can focus on the facial expressions, rather than having to re-adapt to an entirely different bone structure, skin colour, and so on. This explains why some of the most well-crafted deepfakes feature people with similar faces.

The problem, however, goes beyond just faces. The neural network is not specifically designed to recognise them. Different lighting conditions and angles raise the complexity of the problem, as more steps are required not just to adjust the faces, but also to identify the relevant features. If the frames used for the training process exhibit high variability in the lighting conditions, then the encoder will be forced to include information about them in the **latent representation** of the face. This takes up space that could be used to better represent facial expressions, hence reducing the overall quality. This is called **underfitting**, and it indicates that the problem is too complex to be fully captured with the model chosen.

While that is certainly true, we also have to battle the opposite problem. If all the images provided look the same, the training process might fail to capture their true variability. The result is that the neural network will learn to reproduce the same image, rather than the same face. This is a problem called **overfitting**.

#### Training for Low-End GPUs (2GB)

So what is better? Including images that are very similar to simplify the problem, or adding shots taken in different lighting conditions to better generalise how the face should look like? The answer is that it depends. It is impossible to know how the neural network will respond, just by saying that the pictures are taken under the same light. Generally speaking, however, the more complex a problem is, the harder it is to solve it. Unless you are an expert, you should strive to help the neural network as much as possible.

If your aim is to perform face-swap on a single clip, you do not need a neural network that is able to perform face-swap in any condition. You only need one that works just once. The easiest way to achieve that, is by reducing the complexity of the problem. You can start by selecting the right videos:

**Use videos shot in similar lighting conditions.**Light does not only affect the colour of a scene. It also casts shadows on faces which are hard to match. This is because reproducing realistic shadows requires a three-dimensional understanding of the face geometry, which needs to be learned from two-dimensional images.**Choose people with similar faces.**This goes beyond the simple idea concept of “face”. Makeup, glasses and beards make the problem much more challenging. It is particularly difficult to use faces with features that go outside the face itself (such as long beards or occluding hair), as they will be cut out.**Choose people with similar skin tones.**One of the biggest downsides of face-swap is how faces, once converted by the neural network, are blended back into the video. The way it works simply smooths the edges of the image in a rather primitive way. If person A and B have very different skin tones, it will be difficult to merge them seamlessly. Keep in mind that certain implementations of face-swap adjust the colours of the reconstructed face to match the original skin tone. Such an operation, unfortunately, is performed on the entire image and will affect even areas that do not need to be corrected (such as the eyes and facial hair).

You can get good results very quickly if you use only two video clips; one for person A and one for person B, possibly shot under similar lighting conditions. After that, you can start pre-processing them:

**Split frames based on face orientation.**Instead of training a single network and use it on both clips, you should repeat the training process multiple times. If you are using FakeApp, the easiest way is to extract all frames from video A and B, and arrange them in three folders for frontal, three-quarter and side views.**Train different models.**You can train three different, one for each face orientation, so that each neural network only has to focus on detecting and converting facial expressions, and head movements. Rotating faces is also very challenging due to occluded features which need to be “guessed”.

What is left now is to split the target video and convert each segment with the model that it is more appropriate. Since the mapping to reconstruct faces should be much simpler, you can keep the settings low. This solution is perfect for people who do not have a powerful GPU and can only train neural networks with 3 layers or less.

#### Training for High-End GPUs (8GB)

If you have at your disposal a high-end GPU (such as an NVIDIA GTX 1080) you can push the training settings much further. This does not necessarily mean you will obtain better results, but that you can be confident the neural network will learn more complex mapping on its own.

Of the most complex feature to learn is, usually, shadows. This is because videos are taken in settings with different lighting conditions, and reproducing realistic shadows requires a three-dimensional understanding of the face structure. To learn this, your best bet is to provide enough pictures in different lighting conditions and angles. Make sure, however, that both datasets have similar angles

#### Different Resolutions

Most deepfakes look bad because the faces have a different resolution from the rest of the video. This creates artefacts that dramatically reduce the realism of the image.

This is caused, most of the time, by the way tools such as FakeApp works. Neural networks can only work on images that are of the same size. Once a face is detected, it is cropped and reshaped into a 256×256 image. Only the central 160×160 region is used for the training process, which is further downscaled to 64×64 pixels. Consequently, the reconstructed faces are also 64×64 pixels. When merged into a video, these newly created images are morphed back to match their original size. If you are using an HD video, it is likely the original face was larger than that, resulting in a blurred image.

![](../../assets/21f907e8a54bedcd.png)

The transformation causes the new face to look somehow blurred, something which is exasperated by compression artefacts.

There are two ways to resolve this issue. One is to train a neural network so that it can work with larger images. The problem, however, is not fully solved because if trained with low-resolution videos, it will be essentially fed with blurred images.

Another solution is to reduce the resolution of the video you want to face-swap, so that the target face is close to 256 pixels tall. If you up-scale the video once is converted, you will have a uniform resolution. The downside is that you are also sacrificing its original quality.

#### When To Stop the Training

The longer you train a model, the better it becomes. However, the better it is, the longer it takes to make a small improvement. This is problematic, as it is not trivial to decide when to stop the training process.

We can shine some light on this mystery by plotting the evolution of the score over time. In the vast majority of cases, it loosely follows an exponential decay. The chart below shows the score collected from the first 100 iterations training a neural network to convert Anisa Sanusi into Henry Hoffman.

#### Misleading Scores

Your objective is to create realistic deepfakes, not to reduce the score as much as possible. While it is true that lower scores usually produce better videos, this is not always the case. There are many operations you can do during the training process which will lower the score, although without improving the overall quality.

The score is calculated based on how well the neural network is able to reconstruct the face. And this check is done against a number of images taken randomly from the extracted faces. Their number depends on the **batch size**. A higher value means that the neural network has to match against more images. This slows down the training process, but typically results in more realistic images.

It is possible to change the batch size during training. As you can imagine, this might cause the score to fall or to rise sharply. The model (and its quality) has remained unchanged, but what has changed is how strictly we evaluate its progress.

That being said, changing the batch size could be a valuable tool. If done properly, you can slowly raise it so that the neural network can start from an easier task. Whether this will work on not for you is impossible to tell, as it really depends on each dataset.

#### Conclusion

You can read all the posts in this series here:

- Part 1.
[An Introduction to DeepFakes and Face-Swap Technology](https://www.alanzucconi.com/?p=8372) - Part 2.
[The Ethics of Deepfakes](https://www.alanzucconi.com/?p=8300) - Part 3.
[How To Install FakeApp](https://www.alanzucconi.com/?p=8345) - Part 4.
[A Practical Tutorial for FakeApp](https://www.alanzucconi.com/?p=8482) - Part 5.
[An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) - Part 6.
[Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290) **Part 7.**[How To Create The Perfect DeepFakes](https://www.alanzucconi.com/?p=8331)

## Leave a Reply Cancel reply