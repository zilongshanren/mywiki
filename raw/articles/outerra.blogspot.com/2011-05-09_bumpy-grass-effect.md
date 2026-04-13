---
title: Bumpy grass effect
url: https://outerra.blogspot.com/2011/05/bumpy-grass-effect.html
author: Outerra
published: '2011-05-09'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Recently I have got to those code corners again and decided to play with it more. It's using fractal channels to generate the bumps, subjecting it to several treatments - the effect being smaller on some types of grass, and also changing together with modulating colors.

Here's the result:

For comparison, here's how the same scene looked until recently:

The effect is most visible when the sun is lower, it's achieved just by normal lighting. It should be probably combined with another effect that will make it more attractive during noons - shades from grass blades, visible from the side.

Of course, an important thing will be to combine it with real 3D blades smoothly appearing up close, and to apply the effect on other types of vegetation visible at distance.

A short video showing the thing in motion:

## 12 comments:

Saw the bumpy grass post on ModDB and had to search for how you guys achieved this lol.



I'm not too clued up with texturing, but from the limited knowledge I understand, I would think a quick fix to have the grass retain the same effect during noon is to have the grass not react to directional light of the sun, instead as it is there, it should remain lit like that constantly regardless to the sun's position... So the only effect the sun will have in terms of light is directly on the texture itself without effecting the bump/normal mapping... Then when implementing the actual grass blades which will be limited to short view, it should look remarkably good!

But great stuff!!! Really admire what you guys are doing with this engine =)

Wow that looks really good!





A question about a fairly hard problem I can foresee: What about taller grasses, view obstructing grasses/objects.

In ArmA2 this has been a major issue because at longer view distances taller grasses are not rendered, where as they are up close. This unfairly or unrealistically shows objects that might normally be hidden at close distances.

Do you have any ideas on how to handle situations like that?

In ArmA2 BIS sort of gets around it by rendering a slightly higher terrain level and basically making the objects appear to be sunk into it, partially hiding them, but the effect is rather lack luster and not that effective.

You gonna write a paper about this?

I will properly ask on the forums but this should allow for tire tracks to be much much easier and cooler.

@Carcrash:





I think I'm going to implement also a simplified ambient occlusion computation there, it should enhance it for noons significantly.

@NoubertNou: This effect should serve as an envelope of vegetation, and upon coming up close it should be seamlessly replaced with a 3D representation. Where's that "up close" depends on vegetation size and on error metric used to determine the point.

So it's kinda similar as Arma2 (though I didn't see it), but much depends on actual implementation - we'll see. But we definitely want to address this weakness, it's one of issues we gathered on game forums that is quite significant for game play.

@Robert Gibson: I don't plan to write a paper about this one particular technique, but I'd like to write a more comprehensive one about various techniques used. It's also quite intertwined and dependent on each other.

@f12bwth:

Exactly. I have to make several modifications to my road system for it, but I expect it to be pretty cool :)

Yes, there is nothing worse than going prone in tall grass in ArmA2 and pretty much being visible at 100-200 meters away as if you were laying on open ground to the other team!



I think with the amount of 2D billboard like trees that you are generating, generating rough clutter at distances (beyond 50-100 meters) wouldn't be too hard, depending on the scenes content.

Good to hear you are thinking about this, because I think its one of the biggest issues in large area terrain engines (and pretty much anything else in terms of micro-details).

Cool!


P. S. If you can, please, do screens in future in PNG. The JPEG's gradient kills a picture.

I was curious on what your thoughts on using tessellation for this would be?

@Ryan: I'd say there's no point in using a tesselation shader here in this case, as we (have to) generate terrain tiles and textures to maintain a constant texel/pixel quality, and that alone creates near-optimal tesselation of world geometry, with fixed sized vbos.

porn for the eyes. this should be xxx-rated : )

Which can of fractals do you use for this effect ?

@NBY: The same one that we use for texture mixing and other stuff - I don't know if it's got another name, we call it wavelet noise with cubic basis by the way it's constructed.

Post a Comment