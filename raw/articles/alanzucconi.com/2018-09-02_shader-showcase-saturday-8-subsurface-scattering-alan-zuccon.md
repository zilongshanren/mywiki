---
title: 'Shader Showcase Saturday #8: Subsurface Scattering - Alan Zucconi'
url: https://www.alanzucconi.com/2018/09/02/shader-showcase-saturday-8/
author: Alan Zucconi
published: '2018-09-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you ever placed a strong light source behind your hand, you might have noticed how light is able to filter through the skin. Even more interesting is the fact that light “travels” inside the skin, and can sometimes make the entire hand glow. This optical phenomenon is called **subsurface scattering** (or **SSS**) and is caused by individual photons penetrating the skin, bouncing (*scattering*) inside it, and finally exiting from a different point. For this reason, subsurface scattering is also called **subsurface light transport**.

Most semi-transparent materials exhibit a certain degree of SSS, which gives them a “smoother” look. Milk, for instance, owe its uniform colouration to the presence of fat molecules which diffuse and scatter visible light very well. Even solid materials can be subjected to SSS. Marble is a typical example, and this is the reason why most subsurface scattering demos feature marble statues. Skin, milk, marble and wax are the materials which most commonly owe their look to SSS, although this is an optical phenomenon that is present in virtually all non-metallic materials.


So if SSS is so important, why is it not more widely used? The answer is simple: it is extremely expensive. Simulating SSS means simulating how light scatters inside an object. To do this, one should track individual rays of light and account for their propagation (*transport*) inside each material. This is problematic also because 3D models are usually empty. If you want SSS to work correctly on – let’s say – a hand, you need to know not just how thick the hand is, but also how different tissues (skin, muscles, tendons, bones, …) scatter light. There are solutions available that, exactly for that reason, require multiple meshes. [Deep Subsurface Scattering](https://www.assetstore.unity3d.com/#!/content/70257?aid=1100l45Ay&pubref=az_sss_08) is possibly the most advanced SSS shader you can find of the asset store, and this is quite obvious simply by looking at the level of realism that can be achieved.

But for most applications, such an approach would be too expensive. This means that SSS, like most optical phenomenon, is often faked in modern 3D games. This is exactly what happens in the new **High Definition Render Pipeline** introduced in Unity 2018, which comes with its own SSS implementation. Technical artist [Adam Samson](https://twitter.com/adamshmamshon) posted a beautiful example of what the HDRP can achieve with minimal configuration. Adam is constantly posting intriguing videos showing his experiments, so make sure to follow him.

Playing with the new subsurface scattering tools in Unity's HDRP and I'm very impressed…

In other news this is the scariest thing I've ever made

[#madewithunity][#unity3d][pic.twitter.com/ivMB97uUSF]— Adam Samson (@adamshmamshon)

[August 27, 2018]

Even though now Unity supports subsurface scattering, this is only available on high-end devices and requires your project to be set up to use the HDRP. You can read more about how to do this in [The HD Render Pipeline Lit Shader](https://github.com/Unity-Technologies/ScriptableRenderPipeline/wiki/lit-shader).

If you are developing a game that needs to be released on mobile devices and cannot afford to switch to the HDRP, there are still alternatives. For any professional use, I strongly suggest [Translucent Subsurface Scattering](https://www.assetstore.unity3d.com/#!/content/53764?aid=1100l45Ay&pubref=az_sss_08), one of the best assets for subsurface scattering on marble and other solid materials.

Most engines approximate SSS relying on the **depth buffer**. That is a special offscreen texture (*buffer*) that contains, for each, pixel, its distance from the camera (*depth*). By carefully calculating the depth of back and front faces, it is possible to estimate the “thickness” of a model. Such an approach, however, does not work well in all contexts due to sorting issues.

One of the most interesting approaches to SSS has been proposed by Colin Barré-Brisebois and Marc Bouchard in a talk called [Approximating Translucency for a Fast, Cheap and Convincing Subsurface Scattering Look](https://colinbarrebrisebois.com/2011/03/07/gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look/). Their solution is integrated into the **Frostbite 2** engine, which was used for DICE’s **Battlefield 3**. Their approach is simple to implement and is very effective. I wrote a two-part tutorial on the topic, titled [Fast Subsurface Scattering in Unity](https://www.alanzucconi.com/2017/08/30/fast-subsurface-scattering-1/).

You asked for SUBSURFACE SCATTERING in

[@unity3d].

Your requests have been heard.[#MadeWithUnity][#gamedev][#unitytips][https://t.co/ebd4yUicQR][pic.twitter.com/wMMWeYxqLN]— Alan Zucconi (@AlanZucconi)

[August 30, 2017]

The tutorial I wrote inspired game developer [Edward del Villar](https://twitter.com/Ed_dV) to re-implement and adapt the effect to simulate tree leaves.

Sneak peak of a video tutorial I'm making showing some of the different ways to use Subsurface Scattering. Based on this great write-up by

[@AlanZucconi][https://t.co/m7gvkJnclq][pic.twitter.com/9xuv2VK00a]— Edward del Villar (@Ed_dV)

[August 16, 2018]

Edward is also posting video tutorials on YouTube. His channel ([PuckLovesGames](https://www.youtube.com/channel/UCdDjTRD-Mv-SlRguwlWBcKw)) is relatively new, but there is already a lot of interesting stuff.

Ultimately, SSS is an exceptionally complex phenomenon, and its approximation requires bespoken solutions for each material. A SSS shader that works well on uniform materials (such as wax, marble and milk) might not perform as well on complex ones (skin and leaves). For the latter, I would advise relying on [Subsurface Scattering](https://www.assetstore.unity3d.com/#!/content/124637?aid=1100l45Ay&pubref=az_sss_08), an asset specifically designed for realistic skin.

## Leave a Reply Cancel reply