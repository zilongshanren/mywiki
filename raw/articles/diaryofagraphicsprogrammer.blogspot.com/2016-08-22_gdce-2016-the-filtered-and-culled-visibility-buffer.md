---
title: GDCE 2016 - The filtered and culled Visibility Buffer
url: http://diaryofagraphicsprogrammer.blogspot.com/2016/08/gdce-2016-filtered-and-culled.html
author: Wolfgang Engel
published: '2016-08-22'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here is the executive summary: we built a rendering system that




Please download it from here

- Cluster culls and filters triangles for different views like main view, shadow view, reflection view, GI view etc. at the same time
- The optimized triangles are used to fill a screen-space Visibility Buffer or more Visibility Buffers for more views
- We then render lights, shadows, bounce lights with the optimized geometry based on visibility
- We can differ between visibility of geometry and shading frequency
- We can light per triangle or in so called object space

Please download it from here

## No comments:

Post a Comment