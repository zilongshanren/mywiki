---
title: '2D Art: Quick Manual for rendering line art in Maya'
url: https://www.gamedeveloper.com/art/2d-art-quick-manual-for-rendering-line-art-in-maya
author: Junxue Li
published: '2013-09-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)


![](../../assets/152957d415ac66a7.jpg)


Today, 2D game art production employs lots of 3D procedure. For example, 3D model aided 2D design, and 3D render plus 2D overpainting.

Now I give you a tip, which is useful in the design process: how to render 2D line art out of 3D models. Which is especially helpful for complicated objects or scenes, for example vintage furniture, regal interiors.

Let’s start with a simple example. We have this cabinet model, let’s see how to render its line art with Mental ray in Maya.![](../../assets/17614cfc0284977b.jpg)


1. Create a lambert shader, here is lambert2. Go to its shading group node, open the tag mental ray/contours.![](../../assets/d816376c3d34ee90.jpg)



Check the box Enable Contour Rendering. Here the Color is the color of the lines, you may want to change it to black. Width is the width of the lines. Please note it is not measured in pixels.


2. Go to the Render Settings editor, open this tag Features/Contours. Check the box Enable Contour Rendering. In a common sense, line art is black lines on white paper. So check Hide Source then change Flood Color to white.

Give a higher number for Over-Sample, for example 12, to produce clear cut lines.

And at the bottom section, link 2 contour shaders, which names are as indicated below.![](../../assets/2e66bf3cb60edef7.jpg)


These two shaders, find them in the Mental Ray contour shader groups.![](../../assets/12cf1e926bbf7f32.jpg)



3. If you have linked the right shaders, you should find these two node in Hypershader, the Utilities tag. As below:

Click the contour_contrast_function_levels shader(the one with the circle icon), open its attributes.


![](../../assets/5720efa4555a983d.jpg)


Check the boxes: Diff Label, Contrast ![](../../assets/67d31290fe968899.jpg)


4. Assign the shader you have just created, lambert2, to the cabinet. If you click render now, it should be the line art. ![](../../assets/5d6a765af317c0be.jpg)


5. The lines are generated based on an algorithm which checks the surface of the geometries(Curvature, angles,etc). Some times there are not lines at the places you want them, you may need to tweak 2 parameters in step #3, Zdelta, Ndelta. It’s complicated to explain them in mathematical terms, so the best way is to experiment different values by yourself.