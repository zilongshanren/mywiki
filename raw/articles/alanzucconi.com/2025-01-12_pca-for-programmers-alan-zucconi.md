---
title: PCA for Programmers - Alan Zucconi
url: https://www.alanzucconi.com/2025/01/12/pca-for-programmers/
author: Alan Zucconi
published: '2025-01-12'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In today’s world, data is everywhere—and often, it’s overwhelming. Datasets can have hundreds or even thousands of features, many of which are redundant or noisy. Visualising data is an essential skill that allows Data Scientists to effectively highlight structures and relationships that would otherwise remain hidden.

This series of tutorials will focus on **Principal Component Analysis** (PCA), an essential tool in Data Analysis and Visualisation. PCA offers a compelling way to unlock hidden patterns, simplify data, and gain actionable insights. At its core, PCA is a way to literally *see* the data from a different perspective, so that its most important features are *seen* first.

Fully understanding PCA requires deep knowledge of Linear Algebra and Statistics, which can be intimidating to some. My aim with this tutorial is to provide a gentle and intuitive introduction to the subject, specifically tailored to programmers.

This first article in the series will feature little to no Maths, in favour of a more visual approach, with the aid of interactive charts and explorable examples.

## Introduction

The way we look at something can dramatically change how we perceive it. This is as true for everyday objects, as it is for data.

The profile of a sphere (or a circle) looks the same from every angle you look at it, but that is generally not true for other shapes. The profile of a box (or a rectangle), for instance, changes depending on its rotation. The interactive chart below shows how the horizontal and vertical projections of a rectangle change, based on its orientation ⬇️:

It is easy to see that when ![Rendered by QuickLaTeX.com \theta = 0](../../assets/0150deea1454606c.png)


The same logic can be applied to datasets, which are made of points, rather than being solid objects. But the principle is the same: there is a direction that makes the data appear as spread out as possible. PCA measures this variability through a statistical quantity called **variance**, which represents how much the points of a dataset differ from their mean. The interactive chart below shows how the spread of a dataset alongside the X axis changes, based on its orientation ⬇️:

Even in this scenario, there is a direction which maximises the projected variance on the X axis. In the context of PCA, this is known as the **first principal component**, and it represents the direction along which the data varies the most.

The

principal componentis the direction along which the data varies the most.

When we are analysing two-dimensional data, we can identify two principal components. They are the two directions along which the data varies the most. If you imagine the data being fit by an ellipsoid, the principal components can be thought of as its *width* and *height*. Likewise, a dataset in 3 dimensions will have 3 principal components, which can be thought of as the *width*, *height* and *depth* of the said ellipsoid.

PCA identifies the directions along which the data varies the most, and rotates it in such a way that the axes themselves are aligned with those directions. This means that PCA changes the frame of reference, so that the data is centred and aligned with the axes of the ellipsoid of best fit.

You can see the result of PCA running on our toy dataset in the charts below, and how it reprojects the data in the frame of reference which maximises the variance.

## A practical example

PCS is typically performed on datasets with multiple features. You can imagine a dataset as a spreadsheet: each row corresponds to a specific specimen, and each column to a different measurement of that specimen. One notorious example often used by Data Scientists is the [Iris flower data set](https://en.wikipedia.org/wiki/Iris_flower_data_set), which records four different measurements for 150 iris flowers across three different species (*Iris setosa*, *Iris versicolor*, and *Iris virginica*).

![](../../assets/defddc8addbbd246.png)

*I. setosa*

![](../../assets/bad87e0ff2498094.png)

*I. versicolor*

![](../../assets/a03c623ede5946dd.png)

*I. virginica*

The Iris flower dataset contains four-dimensional data, as four features are measured for each flower. This makes it impossible to visually represent the data in its entirety with a single scatter plot.

| Species | Sepal length | Sepal width | Petal length | Petal width |
|---|---|---|---|---|
| I. setosa | 5.1 | 3.5 | 1.4 | 0.2 |
| I. setosa | 4.9 | 3.0 | 1.4 | 0.2 |
| … | … | … | … | … |
| I. versicolor | 7.0 | 3.2 | 4.7 | 1.4 |
| I. versicolor | 6.4 | 3.2 | 4.5 | 1.5 |
| … | … | … | … | … |
| I. virginica | 6.2 | 3.4 | 5.4 | 2.3 |
| I. virginica | 5.9 | 3.0 | 5.1 | 1.8 |

One simple way to go around that is to plot two variables against each other. The chart below, for instance, shows the relationship between the *petal length* and the *petal width* of the three species of irises measured:

It should be pretty clear that the data has a structure, and that the three populations are somewhat distinct, as they appear as three separate clusters. And it is easy to see that the two variables are also *correlated*: knowing one, can give you some information about the other one. For instance, if we measure a random iris flower and find that its petals are around 4 centimetres in length, it is likely to be an *Iris versicolor*, and its petal width will likely be around 1.2 centimetres. This is known as **classification** and, in this context, is the problem of finding the right species of an Iris, given its measurements.

Classification is a challenging problem, as flower petals have some inherent variability, and two species could have very similar measurements. For instance, if we measured a petal length of 5 centimetres, the classification would not be as clear-cut as the populations for *Iris versicolor* and *Iris virginica* somewhat overlap. This can be seen clearly in the **KDE plot** below, which shows the distribution of the petal lengths for the three species:

The best possible scenario for classification would be for the petal lengths to be arranged in three well-separate and compact clusters. Now let’s imagine for a second the opposite: what would be the absolute worst scenario? If all clusters were to be aligned on the X axis, distinguishing them solely based on the petal length would be very difficult—if not impossible.

At the beginning of the article we identified the principal component by rotating a rectangle. This is equivalent to rotating a line which passes through the mean, until we find one onto which the points appear as close as possible. The chart below shows exactly this, where all points are projected on the line which minimises their variability (in green):

If the data had been originally presented like that, the job of classifying flowers based on a single measurement along the green line would have been much harder, as the coordinates are as tightly packed as possible alongside that direction:

Conversely, we can imagine a different direction for the axis, which makes the points as spread out as possible (below, in red):

The improvement from the original distribution is small, but significant:

The green axis is aligned with the direction that *minimises* the variance (i.e.: it makes points as close as possible), while the red axis is aligned with the direction that *maximises* the variance. This means that it is the direction which makes the points as spread out as possible. Or, equivalent, the direction along which the data varies the most. In the context of PCA, these are respectively the second and the first principal components.

Because the data we are analysing has only two dimensions, there are only two directions in which it can vary. Consequently, there are only two principal components. The first one accounts for the direction of most variance, while the last one accounts for the direction of least variance.

For our subset of the Iris flower data, the first principal component is a line that passes through the dataset mean, and has an inclination of around 23 degrees. We can verify this by rotating the data and seeing that it is indeed the one associated with the maximum variance:

So far, we have identified the principal components geometrically. PCA actually offers an analytic way to calculate them which is much more computationally efficient. However, understanding how and why that works requires extensive knowledge of linear algebra. In this first article, we will identify all principal components visually. But in the next one we will see how to derive it mathematically and computationally.

## Classification

In the previous section, we have identified the principal component of the scatter plot between the petal length and the petal width. How is this helping with our classification problem?

Before we introduced the concept of a principal component, the best approach to classification was to rely on the petal length alone. This works because there is a strong correlation between the species and petal length itself. However, as we have seen before, the distributions of the petal lengths somewhat overlap, making it difficult to distinguish between *Iris veriscolor* and *Iris virginica* in some circumstances.

The principal component provides the best separation for those clusters, minimising their overlaps. If we classify flowers not based on a single measurement along the original X axis (i.e.: the petal length), but based on their projection along the principal component (which linearly combines both petal length and width), we can obtain a more reliable classification.

This should improve in performance of the classification, at the cost of now requiring two measurements instead of just one. But for most applications, it is an acceptable price to pay.

If we want to go down this path, we need to calculate the projection of each point onto the principal component. At the end of this article we will discuss the “correct” way to do that according to PCA; for now, let’s do it based on what we know so far. The principal component is a line that always passes through the mean; in the case of the Iris flower dataset, it has an inclination of around 23 degrees. What we can do is simply rotate the entire dataset by -23 degrees around the mean:

The rotation causes the principal component to be aligned with the horizontal axis. This means that the new X coordinate of each point is effectively the projection alongside the principal component. This is the new value we can use to classify our flowers!

Mathematically, the new ![Rendered by QuickLaTeX.com X'](../../assets/33c8f8101e550148.png)

![Rendered by QuickLaTeX.com Y'](../../assets/16d45f659cd6404d.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*} X' = \left(X - \mu_X\right) \cos{\left({-\theta^\circ}\right)} - \left(Y - \mu_Y\right) \sin{\left({-\theta^\circ}\right)} + \mu_X \end{equation*}](../../assets/3dd4e81e4b415a15.png)


(4) ![Rendered by QuickLaTeX.com \begin{equation*} Y' = \left(X - \mu_X\right) \sin{\left({-\theta^\circ}\right)} + \left(Y - \mu_Y\right) \cos{\left({-\theta^\circ}\right)} + \mu_Y \end{equation*}](../../assets/359a1626b3b8fc9b.png)


where:


: the petal length;

: the petal width;

: the rotation of the principal component (23 degrees, in our example);

: the average petal length;

: the average petal width.

The value for ![Rendered by QuickLaTeX.com X'](../../assets/33c8f8101e550148.png)


For instance, let’s try to classify the flower with petal length (![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

![Rendered by QuickLaTeX.com Y](../../assets/1f2dd83a021550bd.png)

![Rendered by QuickLaTeX.com 1.4](../../assets/65b1e1d23f3966d5.png)

![Rendered by QuickLaTeX.com 0.3](../../assets/6cc94210ff5725f8.png)

[3](https://www.alanzucconi.com#id3424905252)) to calculate its projection on the direction of maximum variance: ![Rendered by QuickLaTeX.com X'\approx 1.236](../../assets/5342f62703e83475.png)


(7) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align*} X' &= \Bigl(\underset{X}{\underbrace{1.4}} - \underset{\mu_X}{\underbrace{3.759}}\Bigr) & \cos{\Bigl(-\underset{\theta}{\underbrace{23}}^\circ\Bigr)} \\ & - \Bigl(\underset{Y}{\underbrace{0.3}} - \underset{\mu_Y}{\underbrace{1.199}}\Bigr) & \sin{\Bigl(-\underset{\theta}{\underbrace{23}}^\circ\Bigr)} \\ & + \underset{\mu_X}{\underbrace{3.759}} & \\ &\approx 1.236 & \end{align*} \end{equation*}](../../assets/8064f17f0dec3191.png)


In this case, it is easy to see ![Rendered by QuickLaTeX.com X'](../../assets/33c8f8101e550148.png)

*Iris setosa* cluster, so the classification is fairly unambiguous.

If we repeat this with a different entry (such as ![Rendered by QuickLaTeX.com 4.9](../../assets/e45276e099f85ce5.png)

![Rendered by QuickLaTeX.com 1.8](../../assets/e46c359c19a7b6f5.png)

![Rendered by QuickLaTeX.com X'=5.044](../../assets/a01f5b76690926ff.png)

*Iris versicolor* and the *Iris virginica* clusters. In this case, we can look at where they land on the KDE plot:

While it is true that the KDE value for *Iris virginica* is slightly higher than the one for *Iris versicolor*, they are both pretty close. If you are comfortable with a more probabilistic approach, you can simply calculate their relative proportion, and convert them into probabilities:

(8) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align*} P_{\text{setosa}}\left(x\right) &= \frac{KDE_{\text{setosa}}\left(x\right)}{KDE_{\text{setosa}}\left(x\right)+KDE_{\text{versicolor}}\left(x\right)+KDE_{\text{virginica}}\left(x\right)} \\ P_{\text{versicolor}}\left(x\right) &= \frac{KDE_{\text{versicolor}}\left(x\right)}{KDE_{\text{setosa}}\left(x\right)+KDE_{\text{versicolor}}\left(x\right)+KDE_{\text{virginica}}\left(x\right)} \\ P_{\text{virginica}}\left(x\right) &= \frac{KDE_{\text{virginica}}\left(x\right)}{KDE_{\text{setosa}}\left(x\right)+KDE_{\text{versicolor}}\left(x\right)+KDE_{\text{virginica}}\left(x\right)} \end{align*} \end{equation*}](../../assets/487ee08435dfabd1.png)


As it turns out:

(12) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align*} KDE_{\text{setosa}}\left(x\right) & \approx 0 \\ KDE_{\text{versicolor}}\left(x\right) & \approx 3.454 \\ KDE_{\text{virginica}}\left(x\right) & \approx 5.583 \end{align*} \end{equation*}](../../assets/2ae5078748ce8bac.png)


which leads to the following probabilities:

(13) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align*} P_{\text{setosa}}\left(x\right) & \approx 0 \% \\ P_{\text{versicolor}}\left(x\right) & \approx 38.2 \% \\ P_{\text{virginica}}\left(x\right) &\approx 61.8 \% \end{align*} \end{equation*}](../../assets/0baf5c7b6d339a70.png)


which confirms that the flowered we measured is more much more likely to belong to the *Iris virginica* species.

## Dimensionality Reduction

In the previous section, we have seen how the principal component can be used to improve the classification of flowers. PCA, however, is more often used for another task: **dimensionality reduction**. That is the problem of taking high-dimensional data, and finding a different way to represent it with fewer dimensions. This is possible because, generally speaking, not all dimensions are equally important, and because there might be correlations between them.

While there could be flowers with potentially any combination of sepal and petal lengths, in reality the three species measured in the Iris flower dataset fall into three distinct groups. This means that the dataset has a structure which we can take advantage of.

In the same way we have identified the direction of maximum variance between the petal lengths and widths, we could do the same between the sepal lengths and widths. This would reduce what was originally a four-dimensional dataset to two variables, which capture the principal components of the petal and sepal data. All points could be reprojected into this new 2D space, making it easier to visualise in a meaningful way multi-dimensional data.

Such an approach would be valid, but would also come with a certain degree of arbitrariness. The choice of finding the principal component between the petal lengths and widths, rather than—let’s say—between the petal lengths and sepal widths, is an arbitrary choice.

Luckily for us, PCA can be performed on data that has any number of dimensions: including the original Iris flower dataset. The process works in the exact same way, finding the direction along which the four-dimensional data varies the most. The principal component can still be represented with a line (although one that lives in a four-dimensional space), which can be thought of as the axis which maximises the variance.

The principal component is not the only direction in which the data exhibits some variance, which is why in a dataset in ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

**first principal component** is identified, PCA can be applied again to identify the **second** one. This is the direction of maximum variance, once all the variance from the first principal component has been removed from the data. Let’s see how to do that…

### First principal component

This process has a simple and intuitive geometrical explanation, but cannot be easily visualised in four dimensions. So please, allow me to describe it on a toy dataset which has only three dimensions:

The red line represents the principal component: it is easy to see that it passes through the direction in which the data is most spread out. Or, more formally, the direction which accounts for the maximum amount of variance in the data. You can drag all these 3D charts to rotate them.

### Second Principal Component

The principal component is not the only direction in which the data exhibits some variance. To identify the **second principal component**, we first need to remove all the variance across the first one. The variance indicates how spread out the points are along a certain direction, so removing all variance means collapsing them onto a 2D plane. You can use the slider below to collapse the variance across the principal component ⬇️:

In the chart above, each point also casts a “shadow” onto the three planes, to make it easier to visualise how the overall shape of the cloud of points changes.

The value of ![Rendered by QuickLaTeX.com s](../../assets/864f28b25521f331.png)

![Rendered by QuickLaTeX.com s=1](../../assets/f9c837208628ab93.png)

![Rendered by QuickLaTeX.com s](../../assets/864f28b25521f331.png)

![Rendered by QuickLaTeX.com s=0](../../assets/3cc76fca4a81db92.png)


By doing so, the entire dataset has collapsed from three dimensions to just two, as all points now lie on a 2D plane. Moreover, the way in which this plane is derived, makes it *always* orthogonal to the first principal component. Consequently, the new direction associated with the maximum variance on this plane (the second principal component, in green) will also be orthogonal with the first principal component.

The second principal component belongs to the 2D plane, and its calculation is not dissimilar to what we did at the beginning of the tutorial for the petal lengths and widths.

### Third principal component

Once the second principal component has been identified, we can repeat the exact same process. All variance across the second principal component is removed, by shrinking the data to what effectively becomes a line:

The dataset has now collapse into a single dimension, as all points lie on the same line. This is the third (and final) principal component, and accounts for the remaining variance in the data. If we repeat the process, all points would simply collapse onto the mean, as there would be no variance left to “spread out” the points.

Incidentally, the last principal component is also the direction along which the data varies the least. This is because all variance has already been accounted for by the previous principal components.

### PCA & the Iris Flower Dataset

We now have all we need to finally run PCA on the full Iris flower dataset. What you see below is the same dataset, reprojected using only its first two principal components:

Reconstructing the data using only two principal components means that some of the information (measured in terms of variability) is lost. A [scree plot](https://en.wikipedia.org/wiki/Scree_plot) can be used to plot the percentage of variance that each principal component adds to the final reconstruction. For instance, you can see in the scree plot below that the first principal component in the Iris flower dataset accounts for 92% of the original variation.

Scree plots can be very informative when deciding how many principal components is worth using to reconstruct a dataset. In the case of the Iris flower dataset, it turns out that even just one component could have been more than enough, as the remaining tree only accounts for a merely 8%.

### 📚 Recommended Books

## Summary

The first post in this series introduced the concept of **Principal Component Analysis**, one of the simplest tools to reduce the dimensions of a dataset, while trying to preserve much of its original structure.

PCA works by identifying the principal components, which are the directions along which the data exhibits the most variation. It works best under the following assumptions:

**Linearity:**the relationship between the variables that PCA is trying to capture must be linear;**Meaningful variance:**PCA assumes that the directions in which data varies the most are more important. This makes PCA very sensitive to scale, as changing the magnitude of one variable can drastically change the overall result;**Independency:**PCA assumes that the variables which the data comes from are independent/uncorrelated. As a result, the principal components identified by PCA are always orthogonal to each other. If the underlying structure of the data is non-orthogonal (i.e.: the data is somewhat skewed), PCA may not provide the best representation.

Running PCA typically produces the following results:

**Principal components:**the unit vectors aligned to the direction of maximum variance. If the data has

-dimensional there will be

principal components, and they are all orthogonal to each other;**Projected data:**the original dataset is centred around the mean, and the frame of reference is rotated/flipped to align with the principal components. Some implementations also scale the data alongside the principal components, so that the variance on each axis is

.**Explained variance:**the principal components are sorted by how much variance they explain. This allows to measure how much of the variability in the original data can be reconstructed using a subset of the principal components.

PCA often finds a variety of different applications, such as:

**Visualisation:**the lower dimensional representation of a dataset might be better suited for 2D or 3D scatter plots;**Modelling:**the original dataset (which can have many data points) can be replaced with a simpler model. In the case of PCA, this model is represented by the ellipsoid which best fits the original data;**Compression:**high-dimensional data can be compressed only by storing the dimensions which encode the most information. This is a*lossy*compression, as a certain amount of information is lost in the process.**Understanding:**the dimensionality reduction can help understand which measurements (or their combinations) are more important. For instance, for the purpose of identifying the species of a flower, certain measurements are more important than others.

In this article we have not yet explained how to analytically derive the principal components. This will be the subject of another article in the series.

## What’s next…

[PCA for Programmers](https://www.alanzucconi.com/?p=16494)(Part 1)[PCA for Programmers](https://www.alanzucconi.com/?p=16739)(Part 2) 🚧 (coming soon)

### Further readings

Interactive and explorables:

[Principal Component Analysis Explained Visually](https://setosa.io/ev/principal-component-analysis)[Visualizing PCA in 3D](https://bryanhanson.github.io/LearnPCA/articles/Vig_05_Visualizing_PCA_3D.html), featuring interactive charts

A more mathematical approach

## Leave a Reply Cancel reply