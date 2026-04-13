---
title: 'Unity Short: Building User Interfaces'
url: https://blog.eyas.sh/2020/11/unity-for-engineers-pt10-3-ui/
author: Eyas Sharaiha
published: '2020-11-26'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

For the third and final “short” of this week’s
[Unity for Software Engineers](https://blog.eyas.sh/tag/unity-for-software-engineers) (now updated
and [available as a book](https://leanpub.com/unity-for-engineers)), I give an
overview of building in-game User Interfaces in Unity. As a reminder, this
week’s installment is packaged as a series of short-form outlines, introducing
readers to the *breadth* of the Unity toolkit.

Just like [rendering](https://blog.eyas.sh/2020/10/unity-for-engineers-pt6-rendering/) and the
[Input System](https://blog.eyas.sh/2020/10/unity-for-engineers-pt3-input-system/), Unity has a few
technologies that can be used to render UI in a game. Unity’s documentation
includes a
[comparison of these UI toolkits](https://docs.unity3d.com/Manual/UIToolkits.html).
Of these, only two technologies can be used for *in-game* user interfaces. We’ll
discuss these here:

-
**Unity UI**(sometimes**UGUI**) is the*mature*, GameObject-based UI system in Unity.It is included by default in every Unity project in package form (

[com.unity.ugui](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/index.html)). -
**UI Toolkit**(sometimes**UIElements**) is the next generation UI system, inspired by HTML, CSS, and flexbox.While a basic form of the toolkit is shipped in every Unity Editor as part of the core editor experience, using the toolkit requires the

[com.unity.ui](https://docs.unity3d.com/Packages/com.unity.ui@latest/)package.`com.unity.ui`

is now a standard, production-ready package.

## Which Toolkit Should I Use? (2025 Update)

**Use the UI Toolkit.**

As of Unity 6, UI Toolkit is the recommended system for all user interfaces (Editor and Runtime). It provides better performance, a more modern workflow (HTML/CSS-like), and is feature-complete for most use cases (including world-space UI).

**Unity UI (UGUI)** is now considered the “traditional” path. It is still fully
supported and widely used, especially for maintaining existing projects, but new
projects should favor UI Toolkit.

Unlike Unity’s various render pipelines or the input system, Unity’s various UI toolkits are not mutually exclusive. You can combine them if necessary, though sticking to one is usually cleaner.

## Unity UI

Unity UI (UGUI) is GameObject-based. If a regular UI is represented in a node tree describing a document object model, a UGUI UI is represented in a nested tree of Game Objects.

To get started with UGUI, create a *Canvas* in your scene. While a canvas will
be rendered as a huge flat rectangle within the 3D scene view, the Canvas will
by default only render in *screen space* when the game is running.

### Layout and Positioning

Every Game Object under a Canvas will show a *Rect Transform* instead of a
regular 3D Transform. The Rect transform UI allows you to define the layout of
your object and its nested objects.

You can insert empty GameObjects within your tree hierarchy to define specific
layout groups, just as you might with an empty `<div>`

in HTML.

### Individual Components

Within your layouts, you can have various UI components. Particularly, *Text*
and *Image*.

Before using Text, it is recommended to install the
[TextMeshPro](https://docs.unity3d.com/Packages/com.unity.textmeshpro@latest/)
package, as it dramatically improves text rendering.

### Binding

Text and Image components can be controlled by C#, just as you would normally.
There’s nothing special about UI bindings; instead, you can create a C#
component that takes a reference to an `Image`

or `Text`

component and
sets/updates various values on that component.

For example, see this step-by-step article on
[Health bars in Unity](http://gyanendushekhar.com/2019/11/17/create-health-bar-unity-3d/)
using raw sprites and `Image.fillAmount`

.

## Closing

Writing UI in Unity can be cumbersome if you’re used to more modern reactive tooling, but it gets the job done. UGUI is GameObject-based and thus is relatively easy to reason about. The UI Toolkit allows you to use UXML and USS (similar to HTML and CSS, respectively) to define and style interfaces, but bindings and runtime instantiation are still cumbersome.

## Update Notes (2025)

This post was updated in 2025 to reflect the maturity of **UI Toolkit**:

**Maturity**: UI Toolkit is no longer in preview; it is the production standard for new projects.**Recommendation**: We now recommend UI Toolkit over UGUI for most modern development scenarios due to performance and workflow benefits.