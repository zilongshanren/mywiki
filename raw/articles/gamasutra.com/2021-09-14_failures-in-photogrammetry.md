---
title: Failures in photogrammetry
url: https://www.gamedeveloper.com/art/failures-in-photogrammetry
author: Steve Anderson
published: '2021-09-14'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Failures in photogrammetry

Discusses the use of Agisoft Metashape software (formerly PhotoScan) for photogrammetry and visual experimentation.

![](../../assets/fd4b63f19cb3f24a.png)

I had the chance to try out my home made photogrammetry calibration system in Joshua Tree last week. With temperatures in triple digits throughout the day, the only reasonable time for this type of activity is early in the morning when the Mojave is also at its most beautiful and wildlife are at their most active. I was surrounded by quail and lizards (no snakes) while setting up and plumbing/leveling the posts a little before dawn and a coyote loped by a few yards away, seemingly indifferent to my presence.

I have long suspected that photogrammetry would supply the key to my practical investigation of the conjunction of data and images following on the theoretical and historical research I did on this subject for Technologies of Vision. Although I have done small-scale experiments in the past with a hardware-based system (Occipital Structure Sensor) that captured infrared depth information to an iPad along with photographic textures, the Joshua Tree environment was orders of magnitude larger and more complex. In addition, my intended processing platform is the entirely software-based Metashape by Agisoft (previously PhotoScan), which generates all depth information from the photographs themselves.

Note: if you have somehow stumbled on this post and are hoping to learn the correct way to use Metashape, please look elsewhere. The internet is full of people -- many of whom don’t really know what they’re doing -- offering authoritative advice on how to use this particular piece of software and I don’t want to add myself to the list. While it’s true that my eventual goal is to gain proficiency with various photogrammetry workflows, I’m currently deriving at least equal pleasure from my near total inability to execute any part of this process as intended. Even the measuring sticks in the above image are of my own conception and may not serve any useful purpose whatsoever.

![image image](../../assets/8348ad2ad0830ee1.jpg)


I captured this segment of landscape three separate times, all using a DJI Mavic 2 Pro, but the drone was only in flight for one of the three capture sessions, partly because of unpredictable winds, but also because of not wanting to be reported on by the neighbors. The Joshua Tree Highlands area has declared itself a no-fly zone out of respect for the wildlife, so when I did put the drone up, I flew a grid pattern that was low and slow, capturing video rather than still images to maximize efficiency. As a side note, Metashape is able to import video directly, from which it extracts individual frames like the one above, but something went wrong at the photo alignment stage, and these images -- which should have generated my most comprehensive spatial mapping -- instead produced a faux-landscape that was more exquisitely distorted than any of the other processes I tried.

![image image](../../assets/29fb999bbe2f26b8.jpg)


The thumbnail array below comes from one of my terrestrial capture sessions, the first of which, in my exuberance, consisted of well over 500 images. When this image set took 30+ hours to generate a dense point cloud, I re-photographed the entire area at what I hoped would be a more reasonable total of around 70 images. Even when not in flight, the Mavicgenerates metadata for each image, including GPS coordinates and information about elevation, camera angle, focal length, etc. Metashape uses this data to help spatialize the images in a 3D environment, creating a visual effect that bears a distinct resemblance to the Field-Works series created -- I have no doubt through a much more laborious process -- by the Japanese media artist Masaki Fujihata beginning in the early 2000s.

![image image](../../assets/8ab2db7acebbdb7f.png)

![image image](../../assets/59d93fc5a1f64d0d.jpg)


When I wrote about Masaki’s work for Technologies of Vision, I offered Field-Works (above) as a good object that celebrated the gaps and imperfections in spatialized image systems, in contrast with the totalizing impulse and literal aspiration to world-domination represented by Google Earth. With this practice-based research, then -- my own “Field-Works” -- I remain equally driven by the desire to succeed at capturing a photorealistic landscape, with dimensional data accurate enough to inform an architectural plan, and a secret hope -- even an expectation -- that the result will instead turn out to be an interesting failure -- more like Clement Valla’s dazzling collection Postcards from Google Earth (below), where algorithmically generated photographic textures ooze and stretch in a failed attempt to conceal irregularities in the landscape.

![image image](../../assets/592eeb8517bb6db3.jpg)


In fact, my first experiment with transforming drone images into dimensional data resulted in just such an outcome. This scene from the back yard (where proximity to LAX also dictates a no-fly zone) grew increasingly interesting with each stage of distortion from image to point cloud to mesh to textured model. The drone never went higher than about 12 feet on two circular passes of about 10 images each and the model was deliberately selected to confound the software. The mesh platform of the wagon, covered with leaves that changed position when blown by the rotors of the Mavic confused the software enough to yield a kind of molten surface reminiscent of Valla, an effect that I have not been able to reproduce since.

![image image](../../assets/463b90467a870f57.jpg)

![image image](../../assets/bce32672c07dd4ca.jpg)


This first attempt was created using a free, open source Mac-compatible program called Regard 3D. Although I now have access to PCs with decent graphics processing capability through the VR lab at UCLA, I preferred to stay in the Mac environment to avoid multiple trips across town. In fact, the majority of this post was written while one photogrammetry program or another was rendering models, meshes or depth maps in the background. Although the results from Regard 3D were more than gratifying, I went ahead and purchased an educational license for Metashape and then immediately upgraded to the Pro version when I realized all the features that were withheld from the standard version. Metashape has the advantage of robust documentation -- going back to its days as PhotoScan -- and in-application help features as well as a very active community forum that seems relatively welcoming to people who don’t know what they’re doing.

![image image](../../assets/29304e28aa997714.png)


For my second backyard test, I chose slightly more conventional (solid) surfaces and included some reference markers -- 8′ measuring sticks and Agisoft Ground Control Points (GCPs -- seen in lower right and left corners of the image above) to see if these would help with calibration for the mapping in Joshua Tree. Metashape handled the process effortlessly, resulting in a near-photorealistic 3D model. The measuring sticks allowed me to confirm the scale and size of objects in the final model, but the GCPs could not have functioned as intended because I didn’t manually enter their GPS coordinates. Instead, the software seems to have relied on GPS data from the Mavic and I’m not sure my handheld GPS unit would have been any more accurate at locating the GCPs anyway. In fact, when I got to Joshua Tree, although I dutifully printed out and took a bunch of GCP markers like the one below with me, I forgot to use them and didn’t miss having them when reconstructing the landscape.

![image image](../../assets/60d5d7a6b3b0758b.jpg)


Although images like this, which are designed to be read by non-human eyes, have been in public circulation for decades -- QR codes, bar codes, etc. -- they continue to fascinate me as fulcrum-objects located at the intersection of data and images. When Metashape “sees” these patterns in an imported image, it ties them to a system of spatial coordinates used to verify the lat/long data captured by the drone. When used correctly, the visual/human register takes precedence over the data systems of machines and satellites. Although unintentional, my failure to use the GCPs may have been a gesture of unconscious resistance to these systems’ fetishization of Cartesian precision.

![image image](../../assets/1437f1d5ed1e5ad2.jpg)


After 36 hours of processing my initial set of 570 images (mapped by location above on the left), Metashape produced a “dense point cloud” (right) representing all vertices where the software identified the same visual feature in more than one image. Although the area I intended to map was only about 5000 square feet, the software found vertices extending in all directions -- literally for miles -- across the Joshua basin. A bounding box (below) is used to exclude outlying vertices from the point cloud and to define a limited volume for the next stages of modeling.

![image image](../../assets/693053e447b0f74e.png)


The point cloud can also be viewed using the color information associated with each vertex point (below). This begins to resemble a low-resolution photographic representation of the landscape, which also reveals the areas (resembling patches of snow on the ground) where image-data is missing. Likewise, although the bounding box has removed most outlying information from the distant hillsides, many vertices have still been incorrectly mapped, appearing as sparse clouds against the white background. Metashape has the ability to scan and remove these artifacts automatically by calculating the confidence with which each vertex has been rendered, but they can also be deleted manually. Still not fully trusting the software, I removed the majority of these orphan points by hand, which also allowed me to exclude areas of the model that I knew would not be needed even though they might have a high confidence value. Under other circumstances, of course, I am totally opposed to “cleaning” data to minimize artifacts and imperfections, but the 30+ hours of processing required to render the initial cloud had left me scarred and impatient.

![image image](../../assets/1b3cbe752f8e0cb9.png)


The next step is to create a wireframe mesh that defines the surfaces of the model, transforming the point cloud into a dimensional web of triangles. With tens of millions of potential vertices to incorporate, the software may be set to limit the mesh to a maximum number of triangular faces, which in turn, determines the final precision of the model.

![image image](../../assets/bb2b4e3a6362a002.png)


At this point, the model can be rotated in space and a strong sense of the overall contours of the landscape is readily apparent. The aesthetics of the wireframe are also exquisite in their own right -- admittedly perhaps as a result of my fascination with the economical graphic environment of the early 80s Atari game Battlezone (below) -- and there is always a part of me that wants to export and use the wireframe as-is. In fact, I assume this is possible -- though I haven’t yet tried it -- and I look forward to figuring out how to create 3D flythroughs and/or navigable environments with these landscapes rendered as an untextured mesh.

![image image](../../assets/dc539011367209fc.jpg)

![image image](../../assets/00fbcc8bf727864e.png)


The final stage in creating the model is for Metashape to generate textures based on the original photographs that are mapped onto the mesh surfaces. At this stage, gaps in the point cloud are filled in algorithmically, eliminating the snow effect on the ground. By limiting the size of the model and deleting as many artifacts as possible, the final texturing was relatively quick, even at high resolution, and the resulting model is exportable in a variety of 3D formats.

![image image](../../assets/a59a8d7ffd519bf0.png)


Metashape also offers the ability to generate digital elevation maps (DEMs), which register relative heights of the landscape signified by color or shape. I’m reasonably certain that the DEM image below is the result of some egregious error, but it remains among my favorite outputs of this exercise.

![image image](../../assets/7740ad12ad79e4ef.jpg)


The final image included here is the single frame used by the photogrammetry software for texture mapping. Although it gives the appearance at first glance of being an aerial photograph of a strangely featureless landscape, this file is actually an indexed palette of all the color and texture combinations present on all surfaces of the 3D model. If photogrammetry constitutes the key technology operating in the interstices between data and images, these files are arguably the most liminal of all its components. Neither mimetic nor computational, they provide visual information (“pixel-data”) that is necessary to the perceptual phenomenon of photorealism, while denying the pleasures of recognition. In a literal sense, this single image contains every color and texture that may be seen in the 3D model, rendered here as an abstraction fully legible only to the eyes of the machine.

![image image](../../assets/0b0fa3efe61db35e.jpg)