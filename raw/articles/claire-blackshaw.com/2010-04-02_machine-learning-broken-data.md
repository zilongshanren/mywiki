---
title: 'Machine Learning: Broken Data'
url: https://claire-blackshaw.com/blog/2010/04/machine-learning-broken-data/
author: Claire Blackshaw
published: '2010-04-02'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Machine Learning: Broken Data](../../assets/4e402aebc4c1a4e8.png)

So I’ve been trying to normalise and format the data-set for consumption and processing. Some key points

- Random Corruptions
- Some Data is outside the specified range
- The module code column needs to be ignored as there is no way to convert it into input which is expressed as a float.
- Many entries are missing as much as 50% of the inputs
- The extremely corrupt data makes up 20%
- That 20% contains 90% of the negative results

My approach could be along several paths

- Missing Data is replaced by averaged data, hoping that it will not throw the results.
- Missing Inputs are not “fired” into the equation

Both of these approaches assume that the missing data is neutral, and the lack is not in some way significant. Also they require you to correctly identify the neutral position.

I don’t know what the best solution is so I have cloned the data down two paths

- Heavily corrupt data is removed from the training set, the test set uses averages established by training set for missing inputs.
- The inputs which tends to be missing or corrupt is removed, reducing the amount of inputs

So which was is best, what do you do with missing or corrupt data?