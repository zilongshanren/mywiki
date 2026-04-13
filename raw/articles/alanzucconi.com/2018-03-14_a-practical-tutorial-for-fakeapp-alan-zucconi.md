---
title: A Practical Tutorial for FakeApp - Alan Zucconi
url: https://www.alanzucconi.com/2018/03/14/a-practical-tutorial-for-fakeapp/
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
[How To Install FakeApp](https://www.alanzucconi.com/?p=8345) **Part 4.**[A Practical Tutorial for FakeApp](https://www.alanzucconi.com/?p=8482)- Part 5.
[An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) - Part 6.
[Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290) - Part 7.
[How To Create The Perfect DeepFakes](https://www.alanzucconi.com/?p=8331)

If you are interested in reading more about AI Art (Stable Diffusion, Midjourney, etc) you can check this article instead: [The Rise of AI Art](https://www.alanzucconi.com/?p=14358).

#### Introduction

As explained in the first lecture of this course, [An Introduction to DeepFakes and Face-Swap Technology](https://www.alanzucconi.com/?p=8372), creating a deepfakes requires three steps: **extraction**, **training** and **creation**.

#### Step 1. Extraction

To train your model, FakeApp needs a large datasets of images. Unless you have hundreds of pictures already selected, FakeApp comes with a handy feature that allows to extract all frames from a video. This can be done in the **GET DATASET** tab. All you need is to specify a link to an *mp4* video. Clicking on **EXTRACT** will start the process.

![](../../assets/d6771b6e5592e401.png)

If your original video is called `movie.mp4`

, the frames will be extracted in a folder called `dataset-video`

. Inside, there will be another folder called `extracted`

which contains the aligned images ready to be used in the training process. You might also see a file called `alignments.json`

, which indicates, for each aligned frame, its original position in the image from which it was extracted.

![](../../assets/e09582f6f2b9eae7.png)

After the extraction process is done, the only thing you need is the `extracted`

folder; you can delete all other files. Before proceeding to the next step, just make sure that the aligned faces are, indeed, aligned (picture below). The face detection fails fairly often, so expect some manual work to do.

Ideally, what you need is a video of person A and a video of person B. You’ll then need to run the process twice, to get two folders. If you have multiple videos of the same person, extract all of them an merge the folders. Alternatively, you can attach the videos one after the other using Movie Maker, or an equivalent program.

#### Step 2. Training

In FakeApp, you can train your model from the **TRAIN** tab. Under **Data A** and **Data B **you need to copy the path of the extracted folders. As a convention, Data A is the folder extracted from the background video, and Data B contains the faces of the person you want to insert into the Data A video. The training process will convert the face of person A into person B. In reality, the neural network is working in both directions; it does not really matter which one you choose as A and which one you choose as B.

![](../../assets/ae826545901074df.png)

You will also need a folder for the model. If this is your first time training from person A to person B, you can use an empty folder. FakeApp will use it to store the parameters of the trained neural network.

The training settings need to be set up before starting this process. In red, below, are indicates the ones that refer to the training process. **Nodes** and **Layers** are used to configure the neural network; **Batch Size** is used to train it on a larger number of faces. The meaning of these parameters is explained in depth in another post.

![](../../assets/f8d4aa6c9f5c7cfe.png)

If your GPU has less than 2GB of RAM, it is likely the highest settings you can run are:

You will have to adjust your settings depending on how much memory is available on your GPU. These are the recommended setting you should usually run, although this may vary based on your model.

Parameter | 2 GB | 8 GB |
Batch Size | 16 | 128 |
Nodes | 64 | 1024 |
Layers | 3 | 4 |

If you do not have enough memory, the process will fail.

**Monitor the progress. **While training, you will see a window that shows how well the neural network is performing. The GIF below shows three hours worth of training, using game developer [Richard Franke](https://twitter.com/AuntieRich) and his *alter ego* [Kitty Powers](https://twitter.com/MsKittyPowers) (with videos from [Kitty Powers’ Matchmaker](http://store.steampowered.com/app/285740/Kitty_Powers_Matchmaker/) and [Kitty Powers’ Love Life](http://store.steampowered.com/app/416870/Kitty_Powers_Love_Life/) trailers) as person B and person A, respectively.![](../../assets/56162066b41c3a6a.gif)


You can press **Q** at any time to stop the training process. To resume it, simply start it again using that same folder as model. FakeApp also shows a score which indicates the error committed while trying to reconstruct person A into B and person B into A. Values below 0.02 are usually considered acceptable.

**Step 3. Creation**

The process of creating a video is very similar to the one in GET DATASET. You need to provide the path to an mp4 video, and the folder of your model. That is the folder that contains the files: `encoder.h5`

, `decoder_A.h5`

and `decoder_B.h5`

. You will also need to specify the target FPS.

Pressing **CREATE** will automatically:

- Extract all the frames from the source video in the
`workdir-video`

folder, - Crop all faces and align them in the
`workdir-video/extracted`

folder, - Process each face using the trained model,
- Merge the faces back into the original frame and store them in the
`workdir-video/merged`

folder, - Join all the frames to create the final video.

![](../../assets/1d44a7fa71739e76.png)

In the settings (below), there is an option to decide if you want person A to be converted to person B (**A to B**) or person B to person A (**B to A**).

![](../../assets/98dfa318d30d325a.png)

The other options are used to merge the reconstructed face back into the frame. They will be discussed in details in a later post.

#### Conclusion

You can read all the posts in this series here:

- Part 1.
[An Introduction to DeepFakes and Face-Swap Technology](https://www.alanzucconi.com/?p=8372) - Part 2.
[The Ethics of Deepfakes](https://www.alanzucconi.com/?p=8300) - Part 3.
[How To Install FakeApp](https://www.alanzucconi.com/?p=8345) **Part 4.**[A Practical Tutorial for FakeApp](https://www.alanzucconi.com/?p=8482)- Part 5.
[An Introduction to Neural Networks and Autoencoders](https://www.alanzucconi.com/?p=8261) - Part 6.
[Understanding the Technology Behind DeepFakes](https://www.alanzucconi.com/?p=8290) - Part 7.
[How To Create The Perfect DeepFakes](https://www.alanzucconi.com/?p=8331)

A special thanks goes to Christos Sfetsios and David King, who gave me access to the machine I have used to create the deepfakes used in this tutorial.

## Leave a Reply Cancel reply