---
title: 'Game Barcode: A Study of Colours in Games - Alan Zucconi'
url: https://www.alanzucconi.com/2015/11/18/gamebarcode-a-study-of-colours-in-games/
author: Alan Zucconi
published: '2015-11-18'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial shows how to download videos from YouTube and to process their frames with Python; I have used this technique to create **game barcode**, an image created by sorting the colours in each frame of a particular video. You can see some of most intriguing here:

- FEZ (
[video](https://www.youtube.com/watch?v=UIQIcOlCxas),[2000px](http://i.imgur.com/ugDnAWg.png))![colours_FEZ_600](../../assets/a4d83bb6f7b1488b.png)

- Journey (
[video](https://www.youtube.com/watch?v=Kri4703kpmw),[2000px](http://i.imgur.com/BRhvvS7.png))![colours_Journey_600](../../assets/5281c152e0a1b08b.png)

- Super Mario World (
[video](https://www.youtube.com/watch?v=AqturoCh5lM),[2000px](http://i.imgur.com/kUSMkTx.png))![colours_SuperMarioWorld_600](../../assets/51712445bffd1e38.png)

- Fallout 4 (
[video](https://www.youtube.com/watch?v=REx5cs9d3Vw),[2000px](http://i.imgur.com/01WY47S.png))![colours_Fallout4_GhostRobo_600](../../assets/05eaf1c473d16065.png)


This tutorial is divided in four parts:

[Introduction](https://www.alanzucconi.com#intro)- Step 1.
[Processing a video](https://www.alanzucconi.com#step1) - Step 2.
[Processing a frame](https://www.alanzucconi.com#step2) - Step 3.
[Generating the barcode](https://www.alanzucconi.com#step3) - Step 4.
[Downloading from YouTube](https://www.alanzucconi.com#step4) [Conclusion](https://www.alanzucconi.com#outro)

The idea for this tutorial came to me after reading a post on Reddit titled [The average color of every frame of a given movie](https://www.reddit.com/r/dataisbeautiful/comments/3rb8zi/the_average_color_of_every_frame_of_a_given_movie/). I immediately wanted to apply this technique to games. The main reason is that games, compared to movie, have much smoother transitions. This allows to see how colours change very clearly. On top of that, I wanted to explore this concept further, by applying the techniques I’ve discussed in [The Incredibly Challenging Task of Sorting Colours](https://www.alanzucconi.com/2015/09/30/colour-sorting/). I tested my hypothesis on a short clip from a game I am working on, and the result was quite stunning.

![colours_StillTime_600](../../assets/046ad1a3d4d2901f.png)

Another important reason why I wanted to use games rather than movies, is that working with the latter brings you dangerously close to the neutral zone of piracy and copyright infringement. Switching to games, however, you are forced to used a particular Let’s Play video. All the game barcodes in this post have been generated from Let’s Plays I have found on YouTube. I have no affiliation with their respective creators. You can see all the game barcodes [here](http://imgur.com/a/dE3yt).

Let’s start with a top-down approach. Each movie is processed by the `process_video`

function. Frames are extracted using the library [OpenCV](http://opencv.org/), then passed through `process_frame`

which returns the list of sorted colours within that frame.

import cv2 def process_video (input_movie, size=(2000,100)): colours = [] # Takes the frames of the video cap = cv2.VideoCapture(input_movie) while cap.isOpened(): flag, frame = cap.read() if not flag: continue # Processes the frame colours_frame = process_frame(frame, size[1]) colours.append(colours_frame) # Generates the final picture generate_pic(colours, size)

Finally, all the sorted colours are given to `generate_pic`

which joints them together to create the final picture.

Processing a frame is relatively straightforward. First, the frame is reduced in size to save time and memory. Then, is it reshaped into an array and sorted. For this process I have chosen to sort the colours in the HSV space, since it is more consistent across different frames. In the last step, the sorted array is converted back into an image and interpolated to the requested size using `cv2.resize`

.

import numpy as np import colorsys def process_frame (frame, height=100): # Resize and put in a single line image = resize_image(frame) image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) image = image.reshape((image.shape[0] * image.shape[1], 1, 3)) # Sort the pixels sorted_idx = np.lexsort( (image[:,0,2], image[:,0,1], image[:,0,0] ) ) image = image[sorted_idx] # Resize into a column image_column = cv2.resize(image, (1, height), interpolation=cv2.INTER_AREA) return image_column

The function to resize the original frame is this one:

def resize_image (image, size=100): # Resize it h, w, _ = image.shape w_new = int(size * w / max(w, h) ) h_new = int(size * h / max(w, h) ) image = cv2.resize(image, (w_new, h_new)); return image

The final step to create the image is to join all the sorted columns together. We also convert the image back to RGB.

def generate_pic (colours, size): # Generates the picture height = size[1] img = np.zeros((height,len(colours),3), np.uint8) # Puts the colours in the image for x in range(0, len(colours)): for y in range(0, height): img[y,x,:] = colours[x][y,0] # Converts back to RGB img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB) cv2.imwrite("barcode_full.png", img)

If you want to resize the image to a more manageable size, you can use this code:

image_1 = cv2.resize(img, size, interpolation=cv2.INTER_AREA) cv2.imwrite("barcode_%d.png" % size[0], image_1)

Since many Let’s Play are on YouTube, it makes sense to invest some time to download them directly. I have used [pafy](https://pypi.python.org/pypi/pafy), a Python library which allows to query YouTube.

# Download the video video = pafy.new('https://www.youtube.com/watch?v=Re5NFApk9dQ') resolution = video.getbestvideo(preftype="mp4") input_movie = resolution.download(quiet=False) # Process it process_video(input_movie) os.remove(input_movie)

If you work is derivative (i.e.: if you are using someone else video), **don’t forget to credit them**.

If you are curious to see this technique applied to movies, there is a nice selection here.

#### Other resources

[The Colors of Motion](http://thecolorsofmotion.com), (discussion on[Reddit](https://np.reddit.com/r/dataisbeautiful/comments/3rcz3y/the_colors_of_motion_oc/cwmww1b))[Movie Barcode](https://moviebarcode.tumblr.com/)

## Leave a Reply Cancel reply