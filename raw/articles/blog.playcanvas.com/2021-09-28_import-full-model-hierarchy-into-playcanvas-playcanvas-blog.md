---
title: Import Full Model Hierarchy into PlayCanvas | PlayCanvas Blog
url: https://blog.playcanvas.com/import-full-model-hierarchy-into-playcanvas
author: Steven Yau
published: '2021-09-28'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

The PlayCanvas team are very excited to fully release the [Import Hierarchy pipeline feature](https://developer.playcanvas.com/user-manual/assets/import-pipeline/import-hierarchy/) in the PlayCanvas Editor!

With this feature enabled, any imported FBX will create a Template asset which contains the full node hierarchy as entities representing sub-models of the model. This gives users greater flexibility in manipulating mesh instances in the model directly in the Editor.

Render assets will also be created that can be used with the Render Component and allow users to add an individual mesh instance of a model in the scene.

For example, an imported car FBX model would create several Render assets, doors, wheels, wipers etc. The wheel assets can be used independently from the rest of the car model to create a tire wall.

With the model hierarchy being editable in the Editor, this opens a number of uses that weren't possible before:

- Attach other Entities and/or models as part of another model's hierarchy such as adding a helmet to a character's head.
- Move/Rotate/Scale sub-models directly in the Editor such as moving/adding/removing chairs around a house model.
- Use the Render assets elsewhere in the scene for decoration or customization.
- Add components and/or scripts to individual nodes such as attaching particle effects to animated parts.

![Place Item in Hand](../../assets/a85ebfcf35e0d0b8.gif)

*Place an item in the hand of a character*

![Copy Parts of Hierarchy](../../assets/c4f543c16b641e1e.gif)

*Copy a sub-part of a imported asset*

However, please note that while the Model Component is compatible with both the Animation and Anim (State Graph) Component, the Render Component/Import Hierarchy feature is only compatible with the Anim (State Graph) Component.

Going forward, we will be marking the Model and Animation Components as 'legacy' but if you have an existing project using these components, please do not worry. **None of the existing functionality is being removed** and you will not be forced to update projects to the new pipeline for continued development. Although no new features will be added to the Model Component, the PlayCanvas team will continue to fix bugs with the existing pipeline until our next major version (2.0.0) of the engine at the earliest.

You can even mix both pipelines in the same project if you wish to take advantage of the features in the new pipeline in an existing project. However, please bear in mind that this can add complexity to the project code.

The Import Hierarchy asset task will be enabled by default for newly created projects. If you would like to use this feature in your existing project, please consult [User Manual](https://developer.playcanvas.com/user-manual/assets/import-pipeline/import-hierarchy/) for details.