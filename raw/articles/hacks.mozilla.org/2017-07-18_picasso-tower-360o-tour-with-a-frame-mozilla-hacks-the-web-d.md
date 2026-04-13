---
title: Picasso Tower 360º tour with A-Frame – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/07/picasso-tower-360o-tour-with-a-frame/
author: Salva
published: '2017-07-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A 360º tour refers to an experience that simulates an in-person visit through the surrounding space. This “walkthrough” visit is composed of scenes in which you can look around at any point, similar to how you can look around in [Google Street View](https://www.google.es/maps/@43.2695978,-2.9316727,3a,75y,236.29h,83.88t/data=!3m6!1e1!3m4!1sG4X6WA2-8yasKbgkKNR7HQ!2e0!7i13312!8i6656?hl=en). In a 360º tour, different scenes are accessible via discrete hotspots that users can enable or jump into, transporting themselves to a new place in the tour.

![The magenta octahedron represents the user’s point of view. The image covers the inner surface of the sphere.](../../assets/850b99bf5569ab8c.png)


![The magenta octahedron represents the user’s point of view. The image covers the inner surface of the sphere.](../../assets/850b99bf5569ab8c.png)

*The magenta octahedron represents the user’s point of view. The image covers the inner surface of the sphere.*

With A-Frame, creating such an experience is a surprisingly simple task.

## 360º panoramas

In photography, [panoramas](https://en.wikipedia.org/wiki/Panoramic_photography) are essentially [wide-angle images](https://photography.tutsplus.com/articles/a-beginners-introduction-to-wide-angle-photography--photo-3765). Wide-angle means wide field of view, so the region of the physical space captured by the camera is wider than in regular pictures. A 360º panorama captures the space all the way around the camera.

In the same way that wide-angle photography requires special lenses, 360º panoramas require special cameras. You can read [Kevin Ngo’s guide to 360º photography](http://ngokevin.com/blog/360-photography/) for advice and recommendations when creating panoramas.

Trying to represent a sphere in a rectangular format results in what we call a [projection](https://en.wikipedia.org/wiki/List_of_map_projections). Projection introduces distortion —straight lines become curves. You will probably be able to recognize panoramic pictures thanks to the effects of distortion that occur when panoramic views are represented in a bi-dimensional space:

To undo the distortion, you have to project the rectangle back into a sphere. With A-Frame, that means using the panorama as the texture of a sphere facing the camera. The simplest approach is to use the `a-sky`

primitive. The projection of the image must be [equirectangular](https://en.wikipedia.org/wiki/Equirectangular_projection) in order to work in this setup.

By adding some bits of JavaScript, you can modify the `src`

attribute of the sky primitive to change the panorama texture and enable the user *to teleport to a different place* in your scene.

Getting equirectangular images actually depends on the capturing device. For instance, the Samsung Gear 360 camera requires the use of [official Samsung stitching software](http://www.samsung.com/us/support/answer/ANS00060538/) to combine the native dual-fisheye output into the equirectangular version; while the [Ricoh Theta S outputs both equirectangular and dual-fisheye images](https://developers.theta360.com/en/docs/introduction/) without further interaction.

![A dual-fisheye image arranges two fisheye images side by side](../../assets/d78dc50b649741e5.jpg)


![A dual-fisheye image arranges two fisheye images side by side](../../assets/d78dc50b649741e5.jpg)

A dual-fisheye image is the common output of 360º cameras. A stitching software can convert this into an equirectangular image.

## A 360º tour template

To create such an experience, you can use the **360 tour template** that comes with [ aframe-cli](https://github.com/aframevr-userland/aframe-cli). The

`aframe-360-tour-template`

encapsulates the concepts mentioned above in reusable [components](https://aframe.io/docs/0.6.0/core/component.html)and meaningful

[primitives](https://aframe.io/docs/0.6.0/introduction/html-and-primitives.html), enabling a developer to write semantic 360º tours in just a few steps.

`aframe-cli`

has not been released yet (this is bleeding edge A-Frame tooling) but you can install a pre-release version with `npm`

by running the following command:

```
npm install -g aframevr-userland/aframe-cli
```


Now you can access `aframe-cli`

using the `aframe`

command. Go to your workspace directory and start a new project by specifying the name of the project folder and the template:

```
$ aframe new tour --template 360-tour
$ cd tour
```


Start the experience with the following command:

```
$ aframe serve
```


And visit `http://127.0.0.1:3333`

to experience the tour.

### Adding panoramas

Visit my [Picasso Tower 360 gallery on Flickr](https://www.flickr.com/photos/152720752@N02/albums/72157686274077866) and download the complete gallery. (Images are public domain so don’t worry about licensing issues.)

Decompress the file and paste the images inside the `app/assets/images/`

folder. I will use just three images in this example. After you finish this article, you can experiment with the complete tour. Be sure to notice that the panorama order matches naming: `360_0071_stitched_injected_35936080846_o`

goes before `360_0072_stitched_injected_35936077976_o`

, which goes before `360_0073_stitched_injected_35137574104_o`

and so on…

Edit `index.html`

to locate the panoramas section inside the `a-tour`

primitive. Change current panoramas by modifying their `src`

attribute or add new ones by writing new `a-panorama`

primitives. Replace the current panoramas with the following ones:

```
<a-panorama id="garden" src="images/360_0071_stitched_injected_35936080846_o.jpg"></a-panorama>
<a-panorama id="corner" src="images/360_0074_stitched_injected_35936077166_o.jpg"></a-panorama>
<a-panorama id="facade" src="images/360_0077_stitched_injected_35137573294_o.jpg"></a-panorama>
```


Save and reload your browser tab to see the new results.

It is possible you’ll need to correct the rotation of the panorama to make the user face in the direction you want. Change the `rotation`

component of the panorama to do so. (Remember to save and reload to see your changes.):

```
<a-panorama id="garden" src="images/360_0071_stitched_injected_35936080846_o.jpg" rotation=”0 90 0”></a-panorama>
```


Now you need to connect the new sequence to the other panoramas with positioned hotspots. Replace current hotspots with the following one and look at the result by reloading the tab:

```
<a-hotspot id="garden-to-corner" for="garden" to="corner" mixin="hotspot-target" position="-3.86 -0.01 -3.18" rotation="-0.11 50.47 -0.00">
<a-text value="CORNER" align="center" mixin="hotspot-text"></a-text>
</a-hotspot>
```


Remember that in order to activate a hotspot, while in desktop mode, you have to place the black circle over the magenta octahedron and click on the screen.

### Placing hotspots

Positioning hotspots can be a frustrating endeavour. Fortunately, the template comes with an useful component to help with this task. Simply add the `hotspot-helper`

component to your tour, referencing the hotspot you want to place as the value for the `target`

property: `<a-tour hotspot-helper="target: #corner-to-garden">`

. The component will move the hotspot as you look around and will display a widget in the top-left corner showing the world position and rotation of the hotspot, allowing you to copy these values to the clipboard.

### Custom hotspots

You can customise the hotspot using [mixins](https://aframe.io/docs/0.6.0/core/mixins.html). Edit `index.html`

and locate `hotspot-text`

and `hotspot-target`

mixin primitives inside the *assets* section.

For instance, to avoid the need to copy the world rotation values, we are going to use [ngokevin’s lookAt component](https://github.com/ngokevin/kframe) which is already included in the template.

Modify the entity with `hotspot-text`

id to looks like this:

```
<a-mixin id="hotspot-text" look-at="[camera]" text="font: exo2bold; width: 5" geometry="primitive: plane; width: 1.6; height: 0.4" material="color: black;" position="0 -0.6 0"></a-mixin>
```


### Cursor feedback

If you enter VR mode, you will realise that teleporting to a new place requires you to fix your gaze on the hotspot you want to get to for an interval of time. We can change the duration of this interval, modifying the `cursor`

component. Try increasing the timeout to two seconds:

```
<a-entity cursor="fuse: true; fuse-timeout: 2000" position="0 0 -1"
geometry="primitive: ring; radiusInner: 0.02; radiusOuter: 0.03"
material="color: black; shader: flat">
```


Once you add `fuse: true`

to your cursor component, you won’t need to click on the screen, even out of VR mode. A `click`

event will trigger after `fuse-timeout`

milliseconds.

Following the suggestion in the article about the [ cursor component](https://aframe.io/docs/0.6.0/components/cursor.html#adding-visual-feedback), you can create the perception that something is about to happen by attaching an

`a-animation`

primitive inside the cursor entity:```
<a-entity cursor="fuse: true; fuse-timeout: 2000" position="0 0 -1"
geometry="primitive: ring; radiusInner: 0.02; radiusOuter: 0.03"
material="color: black; shader: flat">
<a-animation begin="fusing" end="mouseleave" easing="ease-out" attribute="scale"
fill="backwards" from="1 1 1" to="0.2 0.2 0.2"
dur="2000"></a-animation>
</a-entity>
```


### Ambient audio

Sound is a powerful tool for increasing the illusion of presence. You can find several places on the Internet offering royalty-free sounds like [soundbible.com](http://soundbible.com/royalty-free-sounds-1.html). Once you decide on the perfect ambient noise for the experience you’re creating, grab the file URL or [download it](http://soundbible.com/grab.php?id=1661&type=mp3) if not available and serve the file locally. Create a new folder `sounds`

under `app/assets`

and put the audio file inside.

Add an [ audio tag](https://aframe.io/docs/0.6.0/core/asset-management-system.html#preloading-audio-and-video) that points to the sound file URL inside the

`<a-assets>`

element in order for the file to load:```
<a-assets>
...
<audio id="ambient-sound" src="sounds/environment.mp3"></audio>
</a-assets>
```


And use the [ sound component](https://aframe.io/docs/0.6.0/components/sound.html) referencing the

`audio`

element id to start playing the audio:```
<a-tour sound="src: #ambient-sound; loop: true; autoplay: true; volume: 0.4"></a-tour>
```


Adjust the volume by modifying the `volume`

property which ranges from 0 to 1.

## Conclusion

360º tours offer first-time WebVR creators a perfect starting project that does not require exotic or expensive gear to begin VR development. Panoramic 360º scenes naturally fall back to regular 2D visualization on a desktop or mobile screen and with a cardboard headset or VR head-mounted display, users will enjoy an improved sense of immersion.

With [ aframe-cli](https://github.com/aframevr-userland/aframe-cli) and the 360º tour template you can now quickly set up the basics to customise and publish your 360º VR tour. Create a new project to show us your favourite places (real or imaginary!) by adding panoramic views, or start hacking on the template to extend its basic functionality. Either way, don’t forget to share your project with the

[A-Frame community in Slack](https://aframevr-slack.herokuapp.com/)and

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## 5 comments

AmosJuly 18th, 2017 at 18:44SalvaJuly 20th, 2017 at 08:24Stephanie HallbergJuly 28th, 2017 at 12:05UtopiahJuly 29th, 2017 at 00:08SalvaJuly 29th, 2017 at 15:29