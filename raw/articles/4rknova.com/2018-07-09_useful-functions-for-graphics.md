---
title: Useful Functions for Graphics
url: https://www.4rknova.com/blog/2018/07/09/01-useful-functions
author: Nikolaos Papadopoulos
published: '2018-07-09'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

In graphics, we often need a way to filter or smoothen out a signal. Below is a collection of some functions that can be used to do that along with their respective plots. The input signal x is assumed to be in the [-1, 1] value range:

### \(1.0 - |x|^a\)

| a = 0.5 | |
| a = 1.0 | |
| a = 2.5 | |
| a = 5.0 | |
| a = 25.0 |

### \(cos(\frac{\pi * x}{2.0})^a\)

| a = 0.5 | |
| a = 1.0 | |
| a = 2.5 | |
| a = 5.0 | |
| a = 25.0 |

### \(1.0 - |sin(\frac{\pi * x}{2.0})|^a\)

| a = 0.5 | |
| a = 1.0 | |
| a = 2.5 | |
| a = 5.0 | |
| a = 25.0 |

### \(min(cos(\frac{\pi * x}{2.0}), 1.0 - |x|)^a\)

| a = 0.5 | |
| a = 1.0 | |
| a = 2.5 | |
| a = 5.0 | |
| a = 25.0 |

### \(1.0 - max(0.0, |x| * 2.0 - 1.0)^a\)

| a = 0.5 | |
| a = 1.0 | |
| a = 2.5 | |
| a = 5.0 | |
| a = 25.0 |