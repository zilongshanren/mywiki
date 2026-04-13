---
title: Thermal Camera LUTs and colormaps for DaVinci Resolve
url: https://blog.frost.kiwi/Davinci-Resolve-thermal-luts/
published: '2024-03-01'
source_blog: FrostKiwi's Secrets
source_site: https://blog.frost.kiwi
category: graphics
fetched: '2026-04-13'
---

When writing [my previous article about LUTs in video games](https://blog.frost.kiwi/WebGL-LUTS-made-simple), I noticed that there is no straight forward way to colormap grayscale footage in [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve), a popular video editing and color grading suite for Windows, Linux and MacOS. On the internet you can find LUTs which attempt to color RGB video in the style of thermal camera footage, but I didn’t find standard colormaps.

I exported every colormap that [matplotlib](https://matplotlib.org/) supports as a 1D .cube file, so you can colormap footage in DaVinci Resolve. This is especially needed for thermal camera footage, when you want to adjust the color mapping more finely. The input is expected to be grayscale. You can [preview](https://blog.frost.kiwi#preview) them and [download](https://blog.frost.kiwi#download) the ones you need. Since it’s a .cube file, it should work for other Software with .cube input as well.

## Export Python script [#](https://blog.frost.kiwi#export-python-script)

Luckily, Python package [colour-science](https://www.colour-science.org/) supports exporting to the .cube [“Iridas/Adobe” format](https://drive.google.com/file/d/143Eh08ZYncCAMwJ1q4gWxVOqR_OSWYvs/view), which DaVinci Resolve uses for its LUTs. Double luckily, the format supports 1D LUTs, so no extra manipulation is needed.

If you want to perform the export yourself or need a colormap not listed, then you can use the Python script below. Required dependencies can be installed via `pip install colour-science matplotlib`

.

## Python export script [colormap-as-cube-lut.py](https://blog.frost.kiwi/colormap-as-cube-lut.py)

```
import argparse
import numpy as np
import matplotlib.pyplot as plt
from colour import LUT3x1D
from colour.io import write_LUT_IridasCube
def generate_and_export_lut(colormap_name, lut_size, file_name):
grayscale_values = np.linspace(0, 1, lut_size)
colormap = plt.get_cmap(colormap_name)
colors = colormap(grayscale_values)[:, :3]
lut = LUT3x1D(table=colors, name=f"Colormap {colormap_name}")
write_LUT_IridasCube(lut, file_name)
print(f"LUT file for {colormap_name} saved to {file_name}")
if __name__ == "__main__":
parser = argparse.ArgumentParser(description="Output a colormap as 1D .cube LUT")
parser.add_argument("--colormap", type=str, help="Name of the colormap to use.")
parser.add_argument(
"--lutsize", type=int, default=256, help="Size of the LUT. Default is 256"
)
parser.add_argument(
"--list-all", action="store_true", help="Print a list of all available colormaps"
)
args = parser.parse_args()
if args.list_all:
print("Available colormap names:")
for name in plt.colormaps():
print(name)
elif args.colormap:
file_name = f"{args.colormap}.cube"
generate_and_export_lut(args.colormap, args.lutsize, file_name)
else:
print(parser.format_help())
```


## Usage [#](https://blog.frost.kiwi#usage)

In the DaVinci Resolve **Settings** and **General**, you can add new LUT Folders. **Add** a Folder. In that folder create a subfolder, where your color maps will be in.

![](../../assets/5e15509c4826835b.png)


Download the required LUTs and put them into that subfolder. In DaVinci Resolve you can go to the color page, click on the **LUTs** tab and select our subfolder. If needed, you can right click in the folder pane and **Refresh** to re-scan the folder for LUTs.

![](../../assets/8b4d899c4c9e83d1.png)


That’s it, now you can apply colormaps to grayscale footage, coloring the footage.

## Preview [#](https://blog.frost.kiwi#preview)

Here you can preview all available colormaps, with the following video and the selectbox. Unless you have specific artistic goals or special data layout, you should use should use the perceptually uniform LUTs, because [reasons](https://blog.frost.kiwi/WebGL-LUTS-made-simple/#so-many-colors).

![](../../assets/c3cc195813e29f73.png)

## LUT collection [#](https://blog.frost.kiwi#lut-collection)

Here you can download the .cube files individually or [as one .zip](https://blog.frost.kiwi/colormaps-as-cube/colormaps-as-cube.zip)