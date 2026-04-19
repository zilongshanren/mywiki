---
title: Intel's Panel Self Refresh (PSR) Feature
url: https://www.4rknova.com/blog/2022/09/01/intel-panel-self-refresh
author: Nikolaos Papadopoulos
published: '2022-09-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

I was browsing ebay the other day, looking around for used Lenovo Thinkpads, and came across a x270 which was listed at a very low price. It came without a hard drive and had a few issues, including a cracked top lid. Overall, it looked like it required a fair amount of work to get to a good state. I did some research and was able to find all the parts I needed at a low cost so I decided that I could make a fun project out of restoring it.

I’ve spend a few days working on it and I am very happy with the result. I am actually using it right now to write this blog post.

Replacing the top lid was a fairly invasive process. I couldn’t find any reference material online so I had to take it all apart and figure things out along the way. After putting everything back together, I pressed the power button and was happy to see the boot screen.

I then spent a few hours installing Linux and Windows on it and running a few tests to verify that all the hardware was operational.

Everything was looking good, until I noticed a subtle flickering of the screen backlight. I double checked and this was happening on both Linux and Windows so my first guess was that the screen was damaged while I was working on the lid. However, after some research online I discovered that this was not the case.

As it turns out, Intel iGPUs have a power saving feature [1] called

*Panel Self Refresh (PSR)*which is known to cause flickering in some instances.

The fix was to simply turn that feature off. Note that this will result in higher power consumption.

# Linux

In Linux, use the kernel parameter:

```
i915.enable_psr=0.
```


There are many ways to achieve that but the simplest one would be to use a GUI tool such as *“Grub Customizer”*.

![02](../../assets/ee3086f258ecc586.png)


# Windows

Under Windows, use the *“Intel Graphics Command Center”* tool to disable the feature.

![02](../../assets/4dcc9d78dc5c66d4.png)