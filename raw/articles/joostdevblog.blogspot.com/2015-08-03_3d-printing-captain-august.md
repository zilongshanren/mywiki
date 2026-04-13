---
title: 3D printing Captain August
url: http://joostdevblog.blogspot.com/2015/08/3d-printing-captain-august.html
author: Joost van Dongen
published: '2015-08-03'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Let's first have a look at the result:

![](../../assets/8564191bb2294d05.jpg)


![](../../assets/8564191bb2294d05.jpg)

*Click for high resolution*I used a model I made in 2007 of

[Captain August](http://www.captainaugust.com/), a webcomic that ran until 2010. The author of Captain August is a friend of mine, Roderick Leeuwenhart, and I made this 3D print as a birthday gift for him.

[Awesomenauts](http://www.awesomenauts.com)players might be familiar with Roderick's work as a writer: he wrote the voice scripts for a bunch of the latest additions to Awesomenauts, including Ksenia, Rocco and the Wildlife Documentary Announcer. Roderick also writes books: he wrote the "Pindakaas en Sushi" series. This title means "Peanut Butter and Sushi", which must be a delicious combination since I personally came up with the name. ^_^

![](../../assets/389442fc1cf150f0.jpg)


![](../../assets/389442fc1cf150f0.jpg)

*Click for high resolution*To 3D print a model it needs to be one mesh without intersecting polygons, and the mesh needs to be without holes. When modelling for normal rendering geometry is often a lot of interesting objects and this mesh is no exception. The arms stick through the body, the eyes through the head, etc. To fix this I filled all the holes in all the individual objects by hand, and then used the boolean union tool to combine all the objects into one mesh and get rid of all the intersections. This crashed a lot because of the high polycounts (and probably also because I use the ancient 3dsmax 2009), but after a bunch of tries it worked and I got a usable model.

![](../../assets/507baedd0bffa236.gif)

For the 3D printing I used

[Shapeways](https://www.shapeways.com/), a company specialised in 3D printing on demand with all kinds of different materials. They even do expensive stuff like silver, but that wasn't intended here.

I uploaded my 3D model into their system to see whether it would accept it. Shapeways runs a lot of automatic tests to find problem areas and it found a bunch that I had to fix. The biggest thing to look out for is whether walls and wires are not too thin. 3D printers can print fine details, but those might not be strong enough. The limits depend on the material and I suppose also the manufacturing process. With the Color Sandstone material I wanted to use, details cannot be smaller then 3mm (there are some further details to this, check the Shapeways site for more info).

In this case I had to fix things like the long pointy nose and the fingers. The fix was rather easy: I just made them thicker, and in case of the nose I also cut off the thinnest part at the end. I performed the fixes on the original model and then redid the boolean union step (including the crashes).

![](../../assets/0440a078029eb054.jpg)

A bit more subtle is that the model needs to be balanced and not snap. Shapeways describes this as the "Sandcastle Rule: if this structure was made of wet sand, would it break?" However, exactly what the limits are is unclear, so I had no idea how far I could go. To be on the safe side I just made the legs and arm a lot thicker and asked Shapeways whether it would work. Within two days they had a look and emailed it would be fine. The model indeed worked out well so apparently this was enough.

3D printers cannot interpolate normals, so polygon smoothing does not work for them. This means that if you make something for 3D printing, you need to turn off all surface smoothing. If the model is not smooth enough at that point, you need to add polygons to make it smoother. In this case I was lucky: the Captain August model was made entirely through low-poly modelling with meshsmooth in mind. I could just increase the number of meshsmooth iterations to get more polygons and thus smoother surfaces. The end result is around 200,000 triangles.

![](../../assets/cf3afeec42daa16d.jpg)

To do a colour model Shapeways wants either a texture or vertex colours. Since my 3D model is mostly just flat coloured parts I made a quick texture with those colours and that's it.

This is one aspect where I think I could have done a better job: since notches and details are so tiny on a figurine they don't get the shading and sharp shadows that a full-sized model would and thus are less visible. A Warhammer model painter once told me you need to paint the lighting to compensate for this. I didn't think of that for Captain August and I think he might have looked better had I done this. For example, I could have made the insides of the creases a bit darker.

Shapeways does a lot of different materials, at very different price points. I wanted a full-colour figurine and didn't want to pay too much so I went for the Color Sandstone material. This is an interesting material: as the name suggests it looks like sand, but it is really a hard material.

![](../../assets/75b6c83f3296c6e5.jpg)

From up close this material looks really weird. I wonder whether it was the inspiration for the strange material of the character Joy in Pixar's brilliant new movie

[Inside Out](https://www.youtube.com/watch?v=seMwpP0yeu4). It looks a bit similar. Looking at

[this](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiS6wiy94VhdEb8cC-pw3b2RHMH4ub2q8i0jwoQj-0u6Xy8IIYSgUl7z28ms05wKHAueGI3QHASVSqCZ_ZPhm7SAA3A6o8aA7pXA6SlsnREjsgUhPzgwNCm21JJMElJ9oyBDHpN7Pznx-I/s1600/PixarPost+-+Inside+Out+Press+Event+32.jpg)concept art it probably wasn't, but I couldn't resist an excuse to mention how awesome Inside Out is (yes, I know, I'm a Pixar fanboy).

![](../../assets/59504c4cc62adb73.jpg)

An interesting aspect of most current 3D printing techniques is that they print in layers. If you look closely, you can often still see those layers. In this model this is especially noticeable at the top of the head and in the wood. My wood mesh has a noise applied to it to make it look less flat. In the 3D print this generates unintended layer patterns that actually look pretty cool. However, in some spots it looks a bit too much like a map of terrain heights.

![](../../assets/5a0cbb922bf86562.jpg)

It turned out to be surprisingly difficult to make good sharp pictures of an object this small. I tried several lenses and lighting conditions to be able to make sharp pictures. I also tried a bathtub trick that I heard about somewhere: I put the figurine in an empty bathtub, giving an exciting all-white background. Pity the lighting conditions in my bathroom were pretty bad so these photos aren't as good as hoped. Still, funny idea.

![](../../assets/7ecd0e81590c71d6.jpg)

To conclude this blogpost, here are a bunch of pictures of Captain August under several angles:

![](../../assets/451c8480ff7b4635.jpg)

![](../../assets/e13f4e3cab58bb02.jpg)

![](../../assets/aac5299830af71bf.jpg)

![](../../assets/2f2545d643257603.jpg)


![](../../assets/2f2545d643257603.jpg)

*Click for high resolution*I'd love to do more art for 3D printing at some point, but for the moment the price of the actual 3D printing is just too high to do just for the fun of it. I'll first have to look for a good excuse to try this again. Maybe another birthday or something? ^_^

## No comments:

## Post a Comment