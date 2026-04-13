---
title: Snapshot Shaders Pro - Text Adventure
url: https://danielilett.com/snapshot-shaders-pro/text-adventure/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Text Adventure effect replaces the screen contents with text elements that simulate an ASCII text display. Different characters stand in for pixels with different luminance.

This effect requires the **Character Atlas** to be set in order to work properly.

![Text Adventure](../../assets/1acc01c94f370fbc.jpg)


# Parameters

**Character Size**- The on-screen size of each character, in pixels.**Character Atlas**- A texture containing the characters that will replace the image. An (nx)-by-y texture, where there are n characters, each of which is x-by-y pixels.**Character Count**- How many characters are contained within the Character Atlas.**Background Color**- The color of the background.**Character Color**- The color of the text overlaid onto the background.