---
title: How to retrieve all the images from a website - Alan Zucconi
url: https://www.alanzucconi.com/2015/05/26/how-to-retrieve-all-the-images-from-a-website/
author: Alan Zucconi
published: '2015-05-26'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Few weeks ago I posted on [Twitter](https://twitter.com/AlanZucconi/status/597037103848038400) few rather bizarre screenshots. A composition of all the submissions for [#ScreenshotSaturday](http://screenshotsaturday.com/), loosely ordered by colour. In this series of posts I’ll briefly explain how I did that using Python.

You can download the original pictures (16Mb, 71Mb, 40Mb, 13Mb) [here](https://www.patreon.com/posts/3455663).

### Step 1: How to retrieve all the screenshots

The first step is, of course, to download all the screenshots. After few attempts, I decided to physically copy them on my HDD so that I could attempt several different visualisation techniques and analysis without querying ScreenshotSaturday every time. All the pages with previous screenshots are reachable from *www.screenshotsaturday.com/week_x.html*, making it very easy to access. Then, we just had retrieve all the images linked in the page.

import cv2 from skimage import io from bs4 import BeautifulSoup def downloadScreenshotsFromWeek(week): # Url of the screenshot page url = "http://screenshotsaturday.com/week%d.html" % week r = requests.get(url) soup = BeautifulSoup(r.text) # Finds all the references to screenshots for link in soup.find_all('a', {"data-milkbox":"gall1"}): url = 'http://screenshotsaturday.com/' + link.get('href') # Avoids GIFs because not supported in cv2 if url.endswith('.gif'): continue # Downloads and converts into the right format image = io.imread(url) image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Saves the file i = url.rfind("/") file_name = url[i:] # File name, not file address cv2.imwrite(file_name, image)

**Line 9** uses `BeautifulSoup`

to navigate the DOM of the retrieved HTML document. For ScreenshotSaturday there isn’t a specific tag which identifies the screenshots. However, they are the only element to using `milkbox`

for the zoom-in effect. **Line 12** queries all of these hyperlinks.

The code refers directly to ScreenshotSaturday, but it can be easily adapted to any other website which has a similar structure.

A problem I’ve been experiencing is that some pictures are decoded wrongly. I believe this might be a problem with **line 21**, which makes strong assumptions on the way pixels are encoded.

## Step 2: Download from different pages

Now, to download all the screenshots:

for week in range(1, 237): downloadScreenshotsFromWeek(week)

Leave it on overnight and get 10Gb of space on your HDD.

### Conclusion

This series of post explains how to use Python to download all the images from a website. In the next posts I’ll discuss a more interesting (and less programming-oriented) topics: how to find the main colours in a image, using clustering techniques.

Before everybody tries to attempt this, I want to remember that the guys at ScreenshotSaturday might not be too happy if you overload their servers with too many requests. I grabbed the screenshots over a week, having some delay in between requests to spread out the traffic. *Download responsibly*.

**Part 1**: How to retrieve all the images from a website**Part 2**:[How to find the main colours in an image](https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/)**Part 3**:[The incredibly challenging task of sorting colours](https://www.alanzucconi.com/?p=2913)

## Leave a Reply Cancel reply