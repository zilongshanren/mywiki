---
title: jo_jpeg Release 1.60
url: https://www.jonolick.com/home/jo_jpeg-release-160
published: '2019-11-27'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
Its been a long time coming, but I finally got around to implementing sub-sampling U,V in the JPEG writer. This means many files are 20-30% smaller than before with very little visual quality loss. Sub-sampled UV is enabled automatically for quality levels <= 90. The new code functions exactly like it did before with the same API as before. Drop it in and enjoy!
|
## Archives
## Categories |