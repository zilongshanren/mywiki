---
title: How to find the main colours in an image - Alan Zucconi
url: https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/
author: Alan Zucconi
published: '2015-05-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In a [previous post](https://www.alanzucconi.com/2015/05/26/how-to-retrieve-all-the-images-from-a-website/), I explained how I grabbed all the screenshots from [#ScreenshotSaturday](http://screenshotsaturday.com/). If that was something relatively easy to implement, ordering them by colour is slightly trickier. The problem here is that there is no standard way to find the main colours in an image. Quite the opposite, different techniques will produce very different results. Long story short: this is not really a problem for programmers, and that’s why it may be more interesting to discuss about it.

### Colour theory

Let’s say that we already have our screenshot. Now, we want to find its main colours. If you are familiar with Photoshop, a starting point is accessing the histogram which represents the distribution of colours. Peaks in the colour histograms can be associated with the main colours. [Conrad Chavez](http://creativepro.com/better-tools-for-tones-why-i-don-t-look-the-histogram/) wrote [a very detailed post](http://creativepro.com/better-tools-for-tones-why-i-don-t-look-the-histogram/) about it, if you are interested in this. The image below shows a level in 0RBITALIS which is predominantly blue and green; this can be seen directly from the colour histogram.

![rgb](../../assets/a8f765b242f7cfd9.png)

The approach I decided to use is based on few assumptions.

- The dominance of a colour is determined by how many pixels have that colour
- Two colours are different if the euclidian distance between its RGB components is high

The first sounds obvious, but it leads to a problem: in a real picture is extremely rare to find two pixels of the same colours. If an object is “blue”, it will have thousands of pixels of different shades of blue. The second assumption is needed to determine which colours are “close” to blue. The most common (although not the most visually pleasing) choice is to see colours are coordinates in the three-dimensional RGB space; the “distance” between two colours is then the linear distance between their 3D points.

Let’s start by loading an image.

# Load the image image = cv2.imread("image.png") image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Resize it h, w, _ = image.shape w_new = int(100 * w / max(w, h) ) h_new = int(100 * h / max(w, h) ) image = cv2.resize(image, (w_new, h_new));

It is worth noting that resizing an image doesn’t generally alter the proportion and distribution of its colours. However, working with smaller images will provide a substantial speed up. **Lines 5-10** resize the image preserving its width / height ratio.

### Step 1: Clustering colours with K-Means

Given these two assumptions, our problem can now be solved with clustering. We have a set of points, we need to group them according to similarities and we want to find the ones which better represent these groups. [K-means](https://en.wikipedia.org/wiki/K-means_clustering) is possibly the most basic, yet effective clustering algorithm which can be used. It has also the advantage of being very scalable. Scikit has its own implementation of K-means, and that’s what I’ve been using.

from sklearn.cluster import KMeans # Reshape the image to be a list of pixels image_array = image.reshape((image.shape[0] * image.shape[1], 3)) # Clusters the pixels clt = KMeans(n_clusters = 3) clt.fit(image_array)

**Line 4** flattens the image, so that is a single list of pixels. **Line 8** is where the actual clustering happens. Images in OpenCV are represented with NumPy matrices; an image of 800×600 pixels, will be an array of 800x600x3, where every pixel is represented by its R, G and B components. What K-Means does it taking these RGB values as points in a 3D space, and finding groups (clusters) among them.

### Step 2: Sort clusters by size

Now what’s left is to count how many pixels have been associated in each cluster. To do this, I’m using [Adrian Rosebrock](http://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/)‘s approach which quite elegantly defines the helper function `centroid_histogram`

:

# Finds how many pixels are in each cluster hist = centroid_histogram(clt) # Sort the clusters according to how many pixel they have zipped = zip (self.hist, clt.cluster_centers_) zipped.sort(reverse=True, key=lambda x : x[0]) self.hist, clt.cluster_centers = zip(*zipped) # By Adrian Rosebrock import numpy as np import cv2 def centroid_histogram(clt): # grab the number of different clusters and create a histogram # based on the number of pixels assigned to each cluster numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1) (hist, _) = np.histogram(clt.labels_, bins = numLabels) # normalize the histogram, such that it sums to one hist = hist.astype("float") hist /= hist.sum() # return the histogram return hist

**Line 2** finds how many pixels are in each cluster. That information is used in **lines 5-7** to sort them, so that the first cluster (index zero) is the ones with more pixels in it.

### Step 3: Clustering evaluation

The majority of tutorials basically stop here, without adding any other information. Developers who are experienced with K-Means know that we have skipped an important assumption: the number of clusters which are actually present in the image. That’s a parameter which K-Means requires and it has been initialised to 3 in this example. But what happens if the image has less then two clusters? This might happen if the image has only two dominant colours, or if the colours are not very well separated in the RGB space. In all these cases, there is a chance the clustering may yield very poor results. If you want to investigate further how well K-Means performed, we’ll have to use the [Silhouette coefficient](https://en.wikipedia.org/wiki/Silhouette_%28clustering%29). It’s a score given to the result of a clustering algorithm and it evaluates two different things: how tight are points within a cluster, and how well separated the clusters are. Scikit also has an implementation for the Silhouette coefficient.

metrics.silhouette_score(image_array, clt.labels_, metric='euclidean')

Values range from -1 to +1, with the latter indicating a good clustering. It is not uncommon to run K-Means several times in order to find the number of clusters which yields the best results.

bestSilhouette = -1 bestClusters = 0; for clusters in range(2, 10): # Cluster colours clt = KMeans(n_clusters = clusters) clt.fit(image_array) # Validate clustering result silhouette = metrics.silhouette_score(image_array, clt.labels_, metric='euclidean') # Find the best one if silhouette > bestSilhouette: bestSilhouette = silhouette; bestClusters = clusters;

Evaluation on the image above yields the following results, indicating the first one (two clusters) as the best one.

![cc](../../assets/4f5fd4f08cfcacc7.png)

Some pictures have a much better colour separation. Hence, clustering yields better results on them. For instance, the following screenshot from [PROTEUS](http://www.visitproteus.com/) is clustered very nicely. The silhouette evaluation indicates 8 as the best number of clusters.

![proteus](../../assets/4ebda92d104c099c.jpg)

### Conclusion

Finding the main colours within an image can be achieved using clustering. The most common technique is K-Means, which is scalable and effective. Despite this, images should be scaled down before any processing. It is important to pick the right number of cluster, to avoid misclassification.

In these examples we have clustered colours in the RGB space. Other articles suggest that the LAB colour space may produce better looking results. If you are interested in further readings, [Eddie Bell](https://twitter.com/ejlbell) has written [an interesting article](http://developers.lyst.com/data/images/2014/02/22/color-detection/) about colour detection and clustering.

**Part 1**:[How to retrieve all the images from a website](https://www.alanzucconi.com/2015/05/26/how-to-retrieve-all-the-images-from-a-website/)**Part 2**: How to find the main colours in an image**Part 3**:[The incredibly challenging task of sorting colours](https://www.alanzucconi.com/?p=2913)

## Leave a Reply Cancel reply