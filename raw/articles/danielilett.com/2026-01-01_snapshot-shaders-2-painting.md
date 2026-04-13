---
title: Snapshot Shaders 2 - Painting
url: https://danielilett.com/snapshot-shaders-2/painting/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Applies a painting-style filter onto the screen according to the chosen painting medium:

**Oil**- Uses a Kuwahara filter to remove texture detail while preserving object edges.

# Parameters

**Drawing Mode**- Choose which painting algorithm to use, with the following choices:*Oil*.**Kernel Size**- How many nearby pixels to consider when using the*Oil*painting filter.