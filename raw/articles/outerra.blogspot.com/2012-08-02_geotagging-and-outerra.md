---
title: Geotagging and Outerra
url: https://outerra.blogspot.com/2012/08/geotagging-and-outerra.html
author: Outerra
published: '2012-08-02'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In the recent unstable build of Anteworld we have implemented a feature that was on our mind for some time already - embedding positional information into the screenshots. Anteworld (and the Outerra engine itself) primarily focuses on planet Earth, rendering real locations using the available elevation data that are then further refined by fractal algorithms. It occurred to us that we could add meta info to screenshots captured from the program, recording the current position and orientation so that these screenshots can be used in other programs that can recognize it to retrieve the position and use it with mapping and other services.

For this purpose we have switched to the JPEG format for captured screens so that we could attach EXIF headers with GPS positional info. The structure of the EXIF format is quite awkward and in my opinion uselessly complicated; instead of a simple extendable text format it uses an indirectly addressed structure with a rigid format, inheriting from TIFF structure. However, the format is rooted deeply and used everywhere.

Geo location can be recorded in special GPS section, where it is possible to record the usual stuff - latitude, longitude, altitude and more. Unfortunately, the standard-defined orientation only counts with the heading angle and doesn't expect someone might need pitch and roll. After a bit of search I found that it was already addressed in

[exiftool](http://www.sno.phy.queensu.ca/%7Ephil/exiftool/)by adding custom fields for GPSPitch and GPSRoll, and so I've decided to use these unofficial extensions so there's at least one quite widely used tool that can recognize it too.

With the positional info embedded within the generated screenshots you can open the image with image viewers such as XnView or IrfanView, which can read it and open a mapping web application, passing in the location data.

For example, the following screenshot can be opened in Xnview:

From there you can go via Edit -> Metadata ->

[Open GPS Location in GeoHack](http://toolserver.org/%7Egeohack/geohack.php?language=en¶ms=27.338229_N_84.615014_E_), which provides quick links to open the location in

[Google Maps](https://maps.google.com/maps?ll=27.338229,84.615014&spn=0.3,0.3&t=m&q=27.338229,84.615014),

[OpenStreetMap](http://www.openstreetmap.org/index.html?mlat=27.338229&mlon=84.615014&zoom=11&layers=B000FTF), as a dual view in

[Topomapper](http://www.topomapper.com/splitscreen.html?zoom=11&lat=27.338229&lon=84.615014&layers=00000000B0), or in lots of other services.

Google Earth in its recent versions doesn't recognize the location from jpg files (when using Add->Photo), though it supposedly worked in earlier versions.

### Jumping into photos

The second, perhaps more interesting part of the geotagging functionality implemented in Outerra is the ability to read the positional info from the screenshots back when starting Outerra, and setting up the camera position and orientation accordingly. This can be used to explore interesting locations that others discover just by using their images, or to use images to store saved locations instead of having to use separate camera position files.

Obviously, this can be used also with images originating from other sources - digital cameras and smartphones with GPS and optional orientation sensor, images geotagged manually etc. It's a quick way to see how a given location looks in Outerra. A couple of examples tested with Outerra:

The direction in the next one (from Iphone) is somewhat off, GPS info says the heading is 255 degrees, but it seems to be more to the north, also by the Google Maps:

As usual, mountainous areas would benefit from using 30m data.

Well. Obviously still a lot of work ahead of us ;-)

## No comments:

Post a Comment