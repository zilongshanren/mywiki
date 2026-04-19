---
title: Intro to Writing Toolbag Plugins
url: https://alain.xyz/blog/marmoset-toolbag-python-intro
author: Alain Galvan
published: '2021-03-26'
source_blog: Alain Galvan · Ray Tracing Driver Engineer at AMD
source_site: https://alain.xyz/
category: graphics
fetched: '2026-04-19'
---

Developing Marmoset Toolbag plugins with Python *can be challenging*. There's important questions that you may need to solve like:

How do you design UIs?

How do you import models and textures?

How do you export data like renders, materials, etc.

How do you configure a material, texture project, or your render settings?

How do you use external packages from PyPi?

![AutoComplete in Action](../../assets/8242df1b9da02f88.gif)


With the advent of *text editors* such as [Microsoft Visual Studio Code](https://code.visualstudio.com/), *AI assisted auto complete* with [Visual Studio IntelliCode](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode), and *language servers* such as [PyLance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), iterating your plugin's design can be very intuitive, and the questions you might have about a given piece of software's API can be more easily answered by the text editor's auto-complete in addition to our [documentation](https://marmoset.co/python/reference.html) and examples.

First, download **Visual Studio Code** with the link below:

Then, install the latest version of **Python** to your computer. Marmoset Toolbag is designed to run on Python 3.6 and above. Make sure to add Python to your environment variables in the advance options.

From there you'll need to install python packages from the [Python Package Index](https://pypi.org/) via the `pip`

command. You will need the Marmoset Toolbag package [ mset](https://pypi.org/project/mset/) for auto-complete support as well as remote execution.

![VS Code's Integrated Terminal](../../assets/ebc33ab88bbe8dd8.png)


Open up a terminal such as [VS Code's Integrated Terminal](https://code.visualstudio.com/docs/editor/integrated-terminal) with the shortcut `Ctrl + Shift + ~`

and run:

**Linting** is checking your code early for mistakes and let you know early where those mistakes are and how to fix them. There's a number of different packages available for linting. The Visual Studio Code team discusses the differences between different linters [here](https://code.visualstudio.com/docs/python/linting).

Visual Studio Code will present you with an option for them to download a linter for you, but if that option doesn't work you can always open up the terminal with

`CTRL + Shift + ~`

and type the following:

![PyLance Screenshot](../../assets/edc2df2b6595f1ac.png)


Finally, install the **PyLance** Visual Studio Code extension as well as **Intellicode**:

Now you should have everything you need for full autocomplete support!

![UIs Example Screenshot](../../assets/20e3c1300c0152e6.jpg)


Marmoset Toolbag uses an [imperative retained mode API](https://alain.xyz/blog/gui-architecture-with-graphics-apis#retained-mode) for designing UIs, so you must create UI elements, then add them as children of other elements:

```
import mset
import os
# Initialize UI Objects
window = mset.UIWindow("UI Test")
# 🗄️ Setup Drawer
# 🔘 Button
button = mset.UIButton("Close Button")
button.onClick = lambda: mset.shutdownPlugin()
# ⏯ Icon Button
icon_button = mset.UIButton()
icon_button.setIcon(os.path.abspath(os.path.join(
os.curdir, "data/gui/control/animationplay.tga")))
drawer = mset.UIDrawer(name="Settings")
drawer_window = mset.UIWindow(name="Drawer Window")
drawer.containedControl = drawer_window
drawer_window.addElement(button)
drawer_window.addReturn()
drawer_window.addElement(icon_button)
# 📜 Setup scroll box
scrollbox = mset.UIScrollBox()
scrollbox_window = mset.UIWindow(name="Scrollbox Window")
scrollbox.containedControl = scrollbox_window
# 📃 Lists
my_list = mset.UIListBox("List 1")
my_list.addItem("1")
my_list.addItem("2")
my_list.addItem("3")
scrollbox_window.addElement(drawer)
scrollbox_window.addReturn()
scrollbox_window.addElement(my_list)
# 🌟 Setup Main Window
# 🎚️ Sliders
slider = mset.UISliderInt(min=5, max=128, name="Slider")
# 🎨 Color Picker
picker = mset.UIColorPicker("Color")
# ✏️ Inputs
text = mset.UITextField()
text_float = mset.UITextFieldFloat()
# ✅ Checkbox
checkbox = mset.UICheckBox()
# 🍱 Add elements to Window
window.addElement(slider)
window.addReturn()
window.addElement(scrollbox)
window.addReturn()
window.addElement(picker)
window.addReturn()
window.addElement(text)
window.addReturn()
window.addElement(text_float)
window.addReturn()
window.addElement(checkbox)
# 2️⃣ Create Secondary Window
popup_window = mset.UIWindow("UI Popup Test")
```


![Importing Models Screenshot](../../assets/358e6f6226837402.jpg)


Perhaps you're automating rendering a number of different models, or have a lot of models that need to be batch imported from different places. The `mset.importModel(path: str)`

function is all you need to do to import a model to your scene. From there you can move it around by changing its position, or make it a child of something like say a Baker's Source children.

```
import mset
# 🏆 Model
model = mset.importModel("C:/mymodel.obj")
model.name = "My Imported Model"
model.position = [0.0, 2.0, 0.0]
```


There's a variety of different Objects you may want to configure in Marmoset Toolbag, let's go over a couple:

![Configuring Materials Screenshot](../../assets/be5140e75babdf25.jpg)


Materials can be configured to use a specific subroutine, and every parameter that exists can be modified to your liking.

```
import mset
# Create a Material
mat = mset.Material()
# 🔖 Set a subroutine
mat.setSubroutine("reflectivity", "Metalness")
# 🎛️ Edit a subroutine parameter
surface = mat.getSubroutine("surface")
tex = mset.Texture("C:/my_normal.png")
surface.setField("Normal Map", tex)
```


![Camera Screenshot](../../assets/32c87ddf5f477fd9.jpg)


All cameras in Toolbag can be controlled with Python, and you can adjust their transform parameters like their rotation, as well as lens settings like the camera limits (near, far), depth of field, post-processing.

```
import mset
cam = mset.CameraObject()
cam.name = "Python Camera"
# 🔬 Adjust camera limits
cam.limits.farLimit = 10
# 🔎 Adjust lens settings
cam.lens.dofEnabled = True
cam.lens.dofMaxBokehSize = 64.0
# ✨ Adjust post-processing
cam.postEffect.sharpen = 0.3
cam.postEffect.vignetteStrength = 0.4
cam.postEffect.bloomBrightness = 0.1
cam.postEffect.bloomSize = 4.0
```


![Renders Screenshot](../../assets/aa5917f76e6dab82.jpg)


Exporting renders is incredibly easy, there's 3 functions you can use to either render a single camera, or the images/video configuration set up in your Render Object.

```
import mset
# 📷 Render Main Camera
img = mset.renderCamera(path='C:/my_render.png')
# 📸 Render all images configured in the Render Object
mset.renderImages()
# 🎥 Render all videos configured in the Render Object
mset.renderVideos()
```


Marmoset Toolbag PluginS can take advantage of the entire Python Package Index and use that ecosystem to help solve problems like hooking Toolbag up to an HTTP server such as [Flask](https://flask.palletsprojects.com/en/1.1.x/) or to a machine learning framework such as [PyTorch](https://pytorch.org/) or [TensorFlow](https://www.tensorflow.org/).

A Toolbag Plugin that uses PyPi packages needs to have its files laid out as follows:

Your `requirements.txt`

would be a text file like the following:

The `__main__.py`

file would serve as the entry point to the plugin, and similar to other Python modules, you can have any file/folder structure you want.

![Burgers Procedural Geometry](../../assets/1c16fcc809acf5b5.jpg)


There's a lot more you can do with Marmoset Toolbag plugins than what we've discussed, from *procedural generation of geometry* to automating your *baking*, *rendering*, or *technical art* workflows.

For more examples of just what you can do, visit the `Examples`

folder in your Toolbag installation:

`<Your Toolbag Installation>/data/plugin/Examples`

`<Your Toolbag Application.app>/data/plugin/Examples`

As well as refer to our [reference documentation here](https://marmoset.co/python/reference.html).

Marmoset maintains a [library of user submitted plugins here](https://marmoset.co/toolbag/add-ons/).

The procedural meshes were done using a library I wrote called [Strange Attractors](https://github.com/alaingalvan/strange-attractors).

More general topics:

There's Visual Studio plugins for relevant tasks you may want to do in Toolbag such as custom shaders. We would recommend the [GLSL Lint](https://marketplace.visualstudio.com/items?itemName=CADENAS.vscode-glsllint) plugin for linting GLSL shader code.

The Theme used for Visual Studio Code in this blog post is called [Github Dark Classic](https://github.com/primer/github-vscode-theme-dark-classic).

The font used in this example was [MonoLisa](https://www.monolisa.dev/) with ligatures enabled. For a free option that's similar try [Fira Code](https://github.com/tonsky/FiraCode/wiki/VS-Code-Instructions).

The Windows Powershell terminal was styled using [Oh My Posh](https://ohmyposh.dev/), which works on all platforms.