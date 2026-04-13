---
title: Rendering Essentials in Unity, for Software Engineers
url: https://blog.eyas.sh/2020/10/unity-for-engineers-pt6-rendering/
author: Eyas Sharaiha
published: '2020-10-25'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

While most Software Engineers interested in game development will be most
excited about the *programming* aspect of making a game, you’ll need *some*
familiarity with graphics, animation, and sound to be successful. This is
especially true if you’re trying to work solo. While a wealth of assets and
resources are available in the
[Asset Store](https://assetstore.unity.com/top-assets/top-download?aid=1011leWs6)
(especially when it comes to reasonably-priced
[paid assets](https://assetstore.unity.com/top-assets/top-paid?aid=1011leWs6)),
there’s a decent amount you *still* need to know to execute well when putting
these resources together. In this installment, we’ll discuss Rendering, Render
Pipelines, and Lighting in Unity.

*This is Unity for Software Engineers
(now updated and
available as a book), a series for
those seeking an accelerated introduction to game development in Unity. More is
coming over the next few weeks, so
consider subscribing for updates.*

## Shaders & Materials

**Shaders** are programs that help transform a **mesh** (made out of *vertices*
and *faces*) into a 3D rendered image. Shaders are parameterized with any number
of properties, such as a *texture* image representing the surface’s appearance,
normal maps representing finer bumps on the mesh, and much more. The shader code
you write determines what kind of properties it receives if any.

In Unity, each *Rendering Pipeline* (discussed below) comes with its own set of
standard shaders. All rendering pipelines include a “Simple Lit” shader as the
most common shader, which helps render an object affected by lighting. In all
pipelines, the Simple Lit variation takes in a *base* color *or* texture, a
normal map, a smoothness map, and physically-based rendering inputs like
metallic and specular values as properties.1

A **Material** is effectively *an instance of a Shader*. It is an

*Asset*that uses a specific shader and defines all relevant input

*properties*on that Shader.

![Three simple materials using the same Shader, and some of the same textures, to achieve very different looks.](../../assets/493c64cb50c37c67.img)

The inspector page of three different materials using the Universal Render Pipeline’s *Simple Lit* shader.

- The first material uses a custom
*base*texture giving the shape its characteristic color. - The first and second materials use a custom
*normal map*texture giving the shape a bumpy appearance. - The second and third materials use a simple white color as their
*base color*. - The second and third materials use a high
*smoothness*value, this giving their surfaces a shiny, reflective appearance. - While both have the same
*smoothness*value, the rough normal map on the second material makes it appear significantly less reflective.

## Connecting Shaders to Game Objects

For a component to be visible in a game (and in your Scene editor), it needs to
have a *Renderer* component. There are multiple renderer components available,
but in 3D game design, you’ll most often be using the *Mesh Renderer*.

![An example of a Cube in a scene, hooked up to a custom material.](../../assets/f4c2313662a536e0.img)

Objects created from the *Game Object > 3D Object >* menu, such as *Cube*,
*Sphere*, *Capsule*, and others will automatically include:

- A Mesh Renderer component, linked to a default
*Simple Lit*material - An appropriate Collider component (“Box Collider” for a cube, “Sphere Collider” for a sphere, etc.), sized precisely to the object, and
- A
*Mesh Filter*component, which defines the Mesh the Renderer should use.

A **Mesh** is effectively Unity’s term for a 3D model. A Mesh is an *asset*
containing a description of an object’s *vertices* and *faces*. A mesh defines a
“swatch” of materials for each face. This way, you can have meshes (e.g., for an
entire building) where all exterior, floor, wall, and window materials are
described as separate materials. A Mesh doesn’t specify *what the materials are*
per se, but just that a given collection of faces have the same material.

When a mesh is selected in a Mesh Filter component, the Renderer’s *Materials*
array property can be used to hook up each material. If you mis-order your
materials in the above example, you can end up with a glass building and brick
windows. Unity’s primitive meshes only use a single material throughout all
faces of an object.

## Rendering Pipelines

In Unity, a
[Render Pipeline](https://docs.unity3d.com/Manual/render-pipelines.html) is the
system responsible for the end-to-end rendering of a scene. Historically, Unity
came with a single general-purpose system known as the **Built-in Render
Pipeline**. Starting with Unity 2018, Unity introduced the **Scriptable Render
Pipeline** (**SRP**) technology. Two SRP-based pipelines are included with
Unity:

- The
**Universal Render Pipeline**(**URP**): The default, optimized graphics pipeline for Unity. It provides a balance of performance and visual fidelity and is the standard for most projects, from mobile to high-end PC/Console. - The
**High Definition Render Pipeline**(**HDRP**): A high-fidelity pipeline targeting high-end hardware (PC, Consoles) for photorealistic graphics.

URP has replaced the old Built-in Render Pipeline as Unity’s standard. While the Built-in pipeline is still available, new features are primarily developed for URP and HDRP.

### What Should I Start Using Today?

If you are starting a new project in 2025, **use URP**.

The ecosystem has largely migrated to SRP (Scriptable Render Pipeline). Most
[assets](https://assetstore.unity.com/top-assets/top-download?aid=1011leWs6) on
the store support URP, and it is the most well-documented and supported path for
learning.

**URP**is the safe default for 99% of projects.**HDRP**is a choice you make if you*know*you need specific high-fidelity features and are targeting high-end hardware exclusively.

## Lighting

When I started with Unity, I expected to spend approximately ~0 minutes worrying
about lighting. It turns out that I underestimated two things: (a) the
difference good lighting makes in what my scene can look like, and (b) how hard
it is to have lighting that is both *good* and *performant*. By the way, I
highly recommend
[Unity’s Introduction to Lighting](https://docs.unity3d.com/Manual/LightingInUnity.html)
section of their user manual.

![Real-time Direct Light Only](../../assets/64e53a11737c3e52.img)

![Baked Global Illumination in addition to real-time Direct Light](../../assets/b71c89d6185fd7d9.img)

A simple scene constructed with primitive objects and a number of basic materials, shown under two lighting states.
**Above:** Two angles showing a scene with only real-time lighting.
**Below:** The same angles showing a scene with baked indirect lights,
in addition to real-time lighting.

In the real world, light travels from its sources and onto objects in the world.
Some of it is absorbed, and some of it scatters. An object in the shade will
still be visible, even though no direct light shines on it from the sun.
Computers can simulate a very realistic rendering using *ray tracing*, which
imitates the physics of light. But rendering an entire scene with ray tracing is
quite expensive, and broadly speaking, it can not be done reliably in real-time.

In the real-time context of a game, there are different strategies to deal with light. Let’s describe a few of these concepts:

*Direct* and *Indirect* Lighting

If a light ray leaving its source bounces on an object exactly once and reaches
the camera, the light is *direct*. The part of the object that the light bounced
off of is directly lit. This light is easy to compute, given the color,
intensity, and distance of the light and the physical properties of the
material.

Direct lighting and shadows due to a direct light are reasonably quick to
compute. Depending on the rendering pipeline, however, an object lit by
*multiple lights* in real-time will be rendered over multiple passes (one for
each light). Unity, for instance, will limit the maximum number of direct lights
that can influence an object.

Indirect lighting, on the other hand, is any *other* light that reaches the
camera. This is light that has bounced off any number of surfaces before
reaching us. Light coming directly or indirectly from a 3D scene’s skybox, which
is somewhat emissive, (imitating the scattered light throughout the sky that
illuminates the world) will contribute to indirect lighting.

Indirect lighting is crucial in rendering a realistic scene. Imagine a cube in a
daylight 3D scene. The faces of the cube in shadow should *not* appear
completely black.

For example, in the figure above, the left side predominantly shows shaded faces
of our 3D objects. Only *direct* lights are accounted for in the top-left
corner, thus making the objects appear excessively dark and hard to tell apart.

### Global Illumination

A scene’s *global illumination* (GI) represents the totality of light from all
sources. Unity offers no supported way to compute global illumination in real
time 1, and instead provides a

**Baked Global Illumination**system that uses a few techniques that work together to produce GI:

**Lightmapping**(a.k.a*baked lightmaps*) is the process of precomputing certain portions of global illumination in the scene.**Light Probes**are objects that allow lightmaps to take additional measurements in specific points in the scene for dynamic moving objects to interpolate.**Reflection Probes**are objects that allow reflective objects in their sphere of influence to show a reflection.

The Baked GI system offers a few lighting modes depending on your rendering pipelines. These lighting modes determine what light is included in baked lightmaps and how it should be blended with real-time lighting information to produce the final result.

The **baked indirect** Backed GI light mode, for example, will only include
*indirect lights* in the lightmap, and that with real-time direct lights.

Other than *what parts of GI are captured in a lightmap*, another critical
question is, *what object faces can have their lighting precomputed in a
lightmap*? Since **lightmapping is useless for an object that moves around**,
Unity provides us with a way of marking objects that are never supposed to move
as *Static*. When an object is marked as *Static*, then it will be included in
the lightmapping process. Your environment (ground, buildings, houses, roads,
trees, etc.) should all be marked as static, and therefore it will receive
high-quality precomputed lighting information.

A lightmap consists of one or more textures that record the state of the light (indirect or combined, depending on the light mode) on the surfaces of static objects and light probes.

![](../../assets/067c865ce41a03fb.img)

(a) A scene with only real-time direct lights active. Note the dark appearance of faces in the shadow.

![](../../assets/3fda6f876c909d56.img)

(b) A scene with baked indirect light. Direct lights and shadows are still in real-time. Note the smoother colors, for example, the dark area under the leftmost grey cube.

![](../../assets/c23c9bc7aed5de5f.img)

(c) A scene with entirely baked lightmaps. Notice the increased quality of the shadows.

![](../../assets/be19775f361103ea.img)

(d) A scene with entirely baked lightmaps in addition to reflection probes. Note the realistic colors around reflective objects.

Baking more of your lights will give you a better appearance and generally also better performance. However, you can only bake the parts of your scene that are static. Baking direct light means that your main light source should also be static (in other words, no day-night cycle for you).

What happens to *dynamic* objects that move around or animate? The standard
strategy here is to place **light probes** throughout your scene. Your dynamic
objects will then blend between their nearest probes to simulate indirect GI, in
addition to direct lights.
[The Brackeys video on light probes](https://www.youtube.com/watch?v=_E0JXOZDTKA)
is probably the best resource to learn more.

The last piece of the puzzle is **reflection probes**. Any object with any
degree of smoothness will take on some of the colors of its surroundings.
Reflection probes are objects that capture a spherical (or cubic) projection
from a certain point, and objects within their range are given that projection
as a reflection probe texture. The skybox in a 3D game also provides its own
reflection probe to reflect off the sky. Reflection probes can be *baked* or
*real-time*. Similar restrictions apply: a *baked* probe will only capture
static objects, while a *real-time* probe is slower but captures moving objects.
If you’re in a dynamic scene, a mirror might need a dynamic probe, but a subtly
shiny part of an object can probably be represented in higher quality with a
baked probe.
[Brackeys also has a video on Reflection probes](https://www.youtube.com/watch?v=lhELeLnynI8)
that I quite like.

## In Closing

With this, you should have the resources you need to design beautiful scenes that fit the style of your game. I hope you don’t end up spending hours in the night debugging lights or shadows in your game!

Unity’s
[Lighting Overview](https://docs.unity3d.com/2020.2/Documentation/Manual/LightingOverview.html)
documentation will make an excellent reference as you progress in your journey.

## Update Notes (2025)

This post was updated in 2025 to reflect the maturity of the Universal Render Pipeline (URP).

**URP as Standard**: Updated recommendations to reflect that URP is now the default standard for most new Unity projects, replacing the Built-in Pipeline.**Grass & Trees**: Removed warnings about vegetation limitations in URP, as these have been largely addressed in recent Unity versions.

## Footnotes

-
Unity offered a now-deprecated real-time GI system called

*Enlighten*.[↩](https://blog.eyas.sh#user-content-fnref-1)