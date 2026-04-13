---
title: GJS Improvements
url: https://blog.mecheye.net/2012/02/gjs-improvements/
author: Jasper St Pierre
published: '2012-02-04'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

Myself, Giovanni Campagna as well as Colin Walters have all been working hard trying to make GJS somewhat of a competitor to PyGObject, being a full introspection stack for the GNOME Desktop Environment. Rather than give you a bunch of history, let me just give you a quick taste. There’s much more to the landing than this, such as implementing your own signals, properties, as well as implementing interfaces, but it will take me a few days to come up with an exciting example that fully showcases the power that you now have.

const Lang = imports.lang; const Cogl = imports.gi.Cogl; const Clutter = imports.gi.Clutter; const Gio = imports.gi.Gio; const MyClutterActor = new Lang.Class({ Name: 'MyClutterActor', Extends: Clutter.Actor, vfunc_get_preferred_width: function(actor, forHeight) { return [100, 100]; }, vfunc_get_preferred_height: function(actor, forWidth) { return [100, 100]; }, vfunc_paint: function(actor) { let alloc = this.get_allocation_box(); Cogl.set_source_color4ub(255, 0, 0, 255); Cogl.rectangle(alloc.x1, alloc.y1, alloc.x2, alloc.y2); } }); const MyClutterEffect = new Lang.Class({ Name: 'MyClutterEffect', Extends: Clutter.DeformEffect, vfunc_deform_vertex: function(effect, width, height, vertex) { vertex.x += Math.random() * 20 - 10; vertex.y += Math.random() * 20 - 10; } }); let actor = new MyClutterActor(); let stage = new Clutter.Stage(); actor.animatev(Clutter.AnimationMode.EASE_IN_OUT_CUBIC, 2000, ['x', 'y'], [200, 200]); actor.add_effect(new MyClutterEffect()); stage.add_actor(actor); stage.show_all(); Clutter.main();

This is very cool. The code has a nice, clean feel to it (at first I didn’t even recognize it as JS) Keep up the good work!

Great work Jasper, Giovanni, and Colin! Thanks a lot for that!

Congratulations, looks awesome, considering it’s JS :)

Are lines 11 & 15 correct?

Although it doesn’t matter for these values, should they be:

vfunc…get_X….forX?

Nope. Clutter and GTK+ have “height for width” and “width for height” allocation. get_preferred_width might be called with a height value, and get_preferred_height might be called with a width value. Which one is called first depends on the actor’s request mode. This is intended for actors like text labels that don’t have one fixed size – the height of a block of text depends on its width.

Makes sense.

Thanks for explanation.

Wouldn’t it be possible to have something like this: ?

vfuncs: {

get_preferred_width: function () {},

…

}

the word vfuncs seems a bit confusing to me from a JS developer point of view, I wonder if we can make this any more “native”…

We discussed it, but I was unhappy with the implementation for that that I came up with. The main problem is chaining up to the parent vfunc, and exposing the vfunc on native types (if you’re subclassing Clutter.Rectangle for god knows what reason, you may want to chain up to Clutter.Rectangle.prototype.vfunc_get_preferred_width)