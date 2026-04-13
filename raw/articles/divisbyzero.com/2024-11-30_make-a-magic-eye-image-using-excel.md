---
title: Make a “Magic Eye” image using Excel
url: https://divisbyzero.com/2024/11/30/make-a-magic-eye-image-using-excel/
author: Dave Richeson
published: '2024-11-30'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I’ve been on a weird kick lately making images using Excel. [Here’s [one post](https://divisbyzero.com/2024/11/13/making-the-mandelbrot-set-with-excel/). I hope to post more soon.] If you add a background color to each cell in a spreadsheet and resize the cell widths to make each one square, then you can zoom out so that each cell acts like a pixel in an image.

In this post, I show how you can create your own “Magic Eye” image using Excel. (I also give you an [Excel spreadsheet](https://divisbyzero.com/wp-content/uploads/2024/11/magiceyetemplate.xlsx) to get you started.) Technically these images are called [autostereograms](https://en.wikipedia.org/wiki/Autostereogram). These are two-dimensional images that appear three-dimensional when viewed correctly with your two eyes. Here are some tips for viewing these images.

- Relax your eyes.
- Let your eyes diverge. Look through the image as if it’s a window, and you are focusing on something beyond it.
- If there are similar patterns in the pixels, allow them to come together as one in your vision.

Here’s one example I made. You shoud see a flat background with one large copy of the letter π floating a little above the background (closer to you). I have several other examples at the end of this post. (These all work better on a larger screen—not on a phone screen.)

![](../../assets/c0ec386f4f428e11.png)


![](../../assets/c0ec386f4f428e11.png)

I’ll now share how I made these images and give you enough details to make your own. If you want to make your own, [download this Excel file](https://divisbyzero.com/wp-content/uploads/2024/11/magiceyetemplate.xlsx), which has my sample code in it.

The Excel file has three tabs at the bottom: the “Final” tab has the final image, the “Raw” tab contains the depth map for the image you’d like to create, and the “Parameters” tab allows you to adjust three parameters.

**Raw tab.** This tab contains the 300×300 “depth map” for the desired 3D image. In my π example above, there are only two depths—the background (corresponding to 0 in the cell) and the π in the foreground (1). If you want to design a more complex shape with more depth, you can have different values in the cells (they do not have to be integers). For instance, two of the images below show undulating surfaces with varrying depths.

I used ChatGPT to help create the depth map for π. First, I created the image shown below with a black π on a white background. I then uploaded it to ChatGPT and typed the following prompt.

`I am uploading a square black and white image. I would like a csv file with 300 rows and 300 columns that shows this image. In particular, I would like you to imagine shrinking this down to a 300x300 image, and then converting the white pixels to be 0 and the black pixels to be 1. `


![](../../assets/5b282e31026e6a95.png)


![](../../assets/5b282e31026e6a95.png)

For the two images showing surfaces, I begain with a top row and a left column that gave a sequence of points along the x- and y-axes, respectively. Then, I created a formula in each cell that evaluated a function at the corresponding x and y values. Here’s the code in cell B2 for one example.

`=SIN(SQRT(B$1^2+$A2^2))/SQRT(B$1^2+$A2^2)+1`


**Parameters tab.** This tab allows you to enter three values that will change the look of the final image: `numcolors,`

`backshift,`

and `multfactor.`


**Final tab. **The “Final” tab contains the final image. To view this page, you want to zoom far enough out that the entire image is visible. You don’t have to edit this page at all. It is generated using the information you provide in the other two tabs.

This page is a 300×300 grid, and each cell contains a number 1 through `numcolors.`

Excel’s “conditional formatting” colors the page automatically based on the number. (You can change the colors by changing the conditional formatting for these cells.)

Each cell has code like the following. (This code is in cell A1.)

```
=LET(
depth,Raw!A1,
numcolors,Parameters!$B$1,
backshift,Parameters!$B$2,
multfactor,Parameters!$B$3,
pixelshift,TRUNC(backshift-depth*multfactor),
IF(
COLUMN()>backshift,
OFFSET(A1,0,-pixelshift),
RANDBETWEEN(1,numcolors)
)
)
```


Here’s what it does. The general idea is that we want our two eyes to see two different horizontally-separated pixels of the same color as one pixel. The closer together the pair of pixels, the nearer to you the combined pixels will seem when looking at the image with both eyes.

For the first `backshift`

number of columns, the code randomly assigns a number (which we think of as a color): 1 through `numcolors.`

For the rest of the columns, the color of a pixel is the same as the color of some pixel to its left. For points on the flat background (corresponding to a depth of 0), each pixel is the same color as the pixel `backshift`

spaces to the left. My π example has `backshift`

= 40. The pixels we want to appear closer to us should be closer together; in this code, such a pixel is the same color as the one `backshift-depth*multfactor`

cells away. In our π example, we have `multfactor`

= 4, so a depth of 1 yields a shift of

That’s it! Have fun playing. Here are some examples.

This one shows a familiar mathematical variable.

![](../../assets/9b27a0b148b473ce.png)


![](../../assets/9b27a0b148b473ce.png)

This one shows a familiar mathematical symbol.

![](../../assets/09f791e8308a3e5d.png)


![](../../assets/09f791e8308a3e5d.png)

This one shows a surface: the graph of a multivariable function.

![](../../assets/46653e078c6218b0.png)


![](../../assets/46653e078c6218b0.png)

This one shows a surface: the graph of a multivariable function.

![](../../assets/d65419c16ceb8122.png)


![](../../assets/d65419c16ceb8122.png)

This one shows one of our earlier symbols again. I changed the pattern for the first few columns. That gave this repeating look.

![](../../assets/c6746d5e19204f5b.png)


![](../../assets/c6746d5e19204f5b.png)

This one shows one of our earlier symbols again. I changed the pattern for the first few columns. That gave this repeating look.

![](../../assets/235e698ea2dbaf82.png)


![](../../assets/235e698ea2dbaf82.png)

Heads up that the images seem to get compressed in the newsletter email, which messes them up in interesting ways.

Hmmm… That’s too bad. Good to know though!

Really cool! Though I’m getting a name error in excel when I open it in edit mode. What version of excel are you using?

Thanks! I just checked, and I’m using Excel version 16.91 (for Mac). I don’t know if any of the Excel functions I’m using are recent additions.

Looks like LET() is from Office 2021+ and, of course, 365. My 2016 version is too old :( using google sheets for now, but it’s slow. I used Photoshop to scale an image down to 300x300px image and the neural filter to make a depth grayscale map of that image and saved it to a bmp. I then found/made a quick python script (6 lines) to take the greyscale image and convert it to a csv.

Is there any special considerations for the parameters? Like will the defaults work for the undulating surfaces you show?