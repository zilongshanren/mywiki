---
title: Platform Specific Resources
url: https://bitsquid.blogspot.com/2011/12/platform-specific-resources.html
author: Niklas
published: '2011-12-22'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

This is nice for two reasons. First, access to target hardware can be limited. In a perfect world, every artist would have a dev kit for every target platform. In practice, this might not be economically possible. It might not even be

*electrically*possible (those main fuses can only take so much). Being able to preview and play console/handheld content on PC is better than nothing, in this less-than-perfect world.

Second, since all our editors use the engine for visualization, if we have specified a handheld device as our source platform, all the editors will automatically show the resources as they will appear on that device.

This new feature gives me a chance to talk a little bit about how we have implemented support for platform specific resources, something I haven’t touched on before in this blog.

The BitSquid Tech uses the regular file system for its source data. A resource is identified by its name and type, both of which are determined from the path to the source file:

Note that even though the name

*is*a path, it is not treated as one, but as a unique identifier. It is hashed to a 64-bit integer by the engine and to refer to a resource you must always specify its full name (and get the same hash result). In the compiled data, the raw names don’t even exist anymore, the files are stored in flat directories indexed by the hash values.

In addition to name and type a resource can also have a number of properties. Properties are dot-separated strings that appear before the type in the file name:

Properties are used to indicate different variants of the same resource. So all these files represent variants of the same resource:

```
buttons.texture
buttons.ps3.texture
buttons.en.x360.texture
buttons.fr.x360.texture
```

The two most important forms of properties are

*platforms*and

*languages*.

*Platform properties*(x360, ps3, android, win32, etc) are used to provide platform specific versions of resources. This can be used for platform optimized versions of units and levels. Another use is for controller and button images that differ from platform to platform. Since BitSquid is scripted in Lua and Lua files are just a resource like any other, this can also be used for platform specific gameplay code:

```
PlayerController.android.lua
```

*Language properties*(en, fr, jp, it, sv, etc) are used for localization. Since all resources have properties, all resources can be localized.

But the property system is not limited to platforms and languages. A developer can make up whatever properties she needs and use them to provide different variants of resources:

```
bullet_hit.noblood.particle_effect
foilage.withkittens.texture
```

Properties can be resolved either at data compile time or at runtime.

Platform properties are resolved at compile time. When we compile for PS3 and a resource has

*ps3*specific variants, only those variants are included in the compiled data. (If the resource doesn’t have any ps3 variants, we include all variants that do not have a specified platform.)

Language properties and other custom properties are resolved at runtime. All variants are compiled to the runtime data. When running, the game can specify what resource variants it wants with a

*property preference order*. The property preference order specifies the variants it wants to use, in order of preference.

```
Application.set_property_preference_order {”withkittens”, ”noblood”, ”fr”}
```

This means that the game would prefer to get a resource that has lots of kittens, no blood and is in French. But if it can’t get all that, it will rather have something that is kitten-full than blood-free. And it prefers a bloodless English resource to a bloody French one.

In other words, if we requested the resource

*buttons.texture*with these settings, the engine would look for variants in the order:

```
buttons.withkittens.noblood.fr.texture
buttons.withkittens.noblood.texture
buttons.withkittens.fr.texture
buttons.withkittens.texture
buttons.noblood.fr.texture
buttons.noblood.texture
buttons.fr.texture
buttons.texture
```

To add support for different source and destination platforms to this system all I had to do was to add a feature that lets the data compiler use

*one*platform for resolving properties and a

*different*platform as the format for the runtime files it produces.


ReplyDeletekingroot

kingroot apk

downlaod apk directly from here.

WOW! I Love it...



ReplyDeleteand i thing thats good for you >>

REVIEW MOVIE

HOROSCOPE

NEW MOVIE

HOW TO

Thank you!

This blog is very helpful. Yellowstone Coat

ReplyDeleteHay, This is Areal. I like this website pretty much. Great info. Hi and thanks for the web blogs. We offer all academic service available at reliable price and after best grades.

ReplyDeleteonline dissertation consulting service

A touch of authenticity and a dash of ruggedness – that's what the john dutton jacket brings to your wardrobe. As a true symbol of Yellowstone's timeless appeal, this jacket is both functional and fashionable. Unleash your inner cowboy with this captivating piece

ReplyDeleteLooking to exude rugged charisma like Rip Wheeler from Yellowstone? Look no further than the rip wheeler black cotton jacket collection. These jackets boast the same tough and resilient qualities as the character, allowing you to embrace your inner cowboy while staying stylish and warm

ReplyDeleteIf you're ready to unleash your inner cowboy like John Dutton, look no further for an authentic suede jacket than our store. We offer the best prices and a wide selection of high-quality jackets that exude rugged elegance. Embrace the classic Western style and channel the spirit of your favorite Yellowstone character with our premium collection. Whether you're a fan of the show or simply admire the timeless cowboy look, our john dutton jacket season 3 will make you feel like you're riding the range with confidence and style. Saddle up and get yours today!

ReplyDeleteExcelling in academia often involves leveraging the expertise of the best essay services. These services go beyond traditional boundaries, providing students with a platform to refine their writing skills and gain insights that transcend the ordinary.

ReplyDeleteA prebuilt gaming PC delivers high performance and convenience straight out of the box—no assembly required!

ReplyDeleteLabubu Doll pakistan brings a playful twist to tradition—cute, quirky, and impossible not to love!

ReplyDeleteIf anyone here is looking for a simple solution for event entertainment, you might want to check out a wedding photo booth app by Zilla Booth. I like the idea of using an iPad-based setup instead of renting a traditional booth.

ReplyDelete