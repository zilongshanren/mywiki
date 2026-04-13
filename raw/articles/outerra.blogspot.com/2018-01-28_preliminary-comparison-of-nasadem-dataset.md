---
title: Preliminary comparison of NasaDEM dataset
url: https://outerra.blogspot.com/2018/01/preliminary-comparison-of-nasadem.html
author: Outerra
published: '2018-01-28'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Some early results from testing preliminary NasaDEM dataset (

[https://gis.stackexchange.com/questions/267134/what-is-nasadem-and-when-it-will-be-released](https://gis.stackexchange.com/questions/267134/what-is-nasadem-and-when-it-will-be-released))### Comparison in one of the extremely buggy areas in SRTM 1" (30m), tile s50w075:

Original SRTM 1" (30m) data here:

![]() |

SRTM1 here contains lots of errors, from artificial narrow peaks to holes and areas clamped to the sea level, as well as some negative heights.

SRTM3 (90m) dataset handles this area slightly better, with fewer holes, but it contains different linear artifacts and the elevations are sometimes dead wrong anyway, or the voids are filled from extremely coarse data:

![]() |

NasaDEM is supposed to be a new reprocessing of raw SRTM data, also using newer sources for void fills. Unfortunately, the preliminary dataset leaves a lot to be desired:

![]() |

For these corrections it's possible to use another global dataset that is without (significant) artifacts,

[Viewfinder Panoramas](http://www.viewfinderpanoramas.org/)with a global 3" coverage. This one fills SRTM voids using various local maps.

![]() |

### Comparison in previously OK area - river Amazon delta n00w051

![]() |

![]() |

So far it seems that the new dataset won't solve our existing problems and will introduce some new ones, although this is all preliminary and unofficial.

## No comments:

Post a Comment