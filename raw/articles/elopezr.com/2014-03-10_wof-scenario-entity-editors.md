---
title: WoF Scenario/Entity Editors
url: https://www.elopezr.com/wof-scenarioentity-editors/
author: Redorav
published: '2014-03-10'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

The **Will of Flame Scenario Editor** is a level editor developed for the Android game Will of Flame. It is developed in Python and uses the python bindings of [wxWidgets](http://www.wxwidgets.org/), called [wxPython](http://www.wxpython.org/). It also uses the [PIL Imaging library](http://www.pythonware.com/products/pil/) for scaling, resizing, rotating and slicing/appending the scenario bitmaps. All images were drawn by my partner Antonio Hontoria. The editor currently has the following capabilities:

- Dynamic importing of images into layers (which the game uses for parallax effect). These images can be selected from the selection menu, which includes a preview, then dragged and dropped onto the level.

- Exporting of scenario information into a game-readable
**XML**. - Exporting of background tiles, which make background rendering and saving much more convenient and efficient. Sprite software such as TexturePacker makes this importing and packing easy.
- Moving and rotating of game entities into the game, such as enemies, scenario interactive elements, and non-interactive background elements. Can also hide or disable selection of layers to prevent misclicking.
- Entity statistics (number of entities in category, etc.)
- Several shortcuts. Ctrl+R enables rotation. Delete/Backspace deletes entities. Ctrl-Z restores deleted or moved entities. Arrow keys move entities slightly.

The editor requires several external libraries, so here is an ** executable for Windows **that comes with everything included (Mac and *nix users shouldn’t have trouble installing new libraries through the console, and Python normally comes preinstalled in new systems). The executable comes with a test scenario,

**test.scn**The

[source](https://dl.dropboxusercontent.com/u/14054799/Portfolio%20Uploads/Scenario_Editor_07src.zip)is also included.

The **Will of Flame Entity Builder** is a way to create complex entities made of parts, which are then loaded into the game behaving as a single entity. It was intended to create the hero for Will of Flame, and to create more complex final bosses.