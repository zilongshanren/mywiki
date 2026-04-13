---
title: 'Unity Tips #1 - Alan Zucconi'
url: https://www.alanzucconi.com/2016/02/17/unity-tips-1/
author: Alan Zucconi
published: '2016-02-17'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the first part of a series of posts dedicated to the most useful, short and sweet tips to make the most out of Unity. Today we will focus on interesting features of the editor which can really speed up your workflow.

You can use the hashtag [#UnityTips](https://twitter.com/search?q=%23unitytips) to find many more tips posted by developers all around the world.

#### In-editor Arithmetic Expressions

All the numerical fields in the inspector support basic arithmetic expressions.

![unity](../../assets/f33172095b7af13a.gif)

Numerical values are automatically assumed as either `int`

or `float`

and the trailing `f`

is not required.

#### Snapping

Unity supports several snapping options.

- Press
`Ctrl`while moving an object to snap its position:![snap](../../assets/50877438187882b9.gif)


This works even when scaling and rotating an object. - You can configure the amount of snap in
**Edit > Snap Settings…**. - Holding
`V`allows to snap to the vertex of a mesh:![vertex](../../assets/d787878873b186f6.gif)


#### Move along Local Axes

![global](../../assets/babe02841552bbc0.gif)

When an object is selected, the move handlers are aligned with the global axes. By switching to **Local Mode** instead, you can move an object along its rotated axes.

The Local / Global toggle is found under the menu.

![g](../../assets/313f33697cd34627.gif)

#### Copy / Paste Colours

You can copy and paste colours.

![colour](../../assets/1c8dfa7627577248.gif)

#### Save Changes made in Play Mode

One of the most frustrating bits of Unity is that all the changes made to an object in Play Mode are deleted once you stop the game. There’s a way to go around this.

- Enter in
**Play Mode** - Made all the changes you need to your object
- From the
**Inspector**, right click on the name of your component and then select**Copy Component** - Exit from
**Play Mode** - Right click again on the component name and select
**Paste Component Values**

#### Asset duplication

You can duplicate an asset by selecting in the **Project window** `Ctrl`+`D`.

#### Resizeable Preview and Maximised Game

- The
**Preview window**is often too small and cannot be easily expanded in the Inspector window. Right click on it will move it into a floatable, resizeable and expandable version.

![preview](../../assets/13782edeb1d97da9.gif)

- Similarly, the
**Game window**can be resize without restarting the game. Just right click on its tab and select**Maximize**:

![unity2](../../assets/2b573eb6d7adb8b0.png)

#### Stay Focused on Objects

You have several options to control the camera of the inspector:

- Press
`F`when an object is selected to focus on it; this will also zoom on it. - Double click on an object to centre it on the camera.
- Press
`Shift`+`F`to lock the editor camera onto the selected object. The camera will follow your object, even if it moves.

#### Asset Store Search

![asset search](../../assets/a0cbef3466fdc410.gif)

Searching something on the Asset Store often breaks the flow of your work. Luckily, Unity supports a fast method to search assets on the Store. To do this, you can simply type something in the search bar of the **Project window**; then, select **Asset Store** instead of **Asset**. The assets are grouped in two categories: free and paid.

## Leave a Reply Cancel reply