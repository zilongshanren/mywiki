---
title: 'ShaderQuest Part 3: Shaders and Materials'
url: https://halisavakis.com/shaderquest-part-3-shaders-and-materials/
published: '2021-02-10'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This ShaderQuest post is brought to you by these awesome Patrons:

- Not Invader Zim
- Tiph’ (DN)
- orels1
- raingame

## Introduction

In this part of ShaderQuest, we’ll take a look at how shaders are created and handled in the context of game engines; specifically Unity and UE4. Once again, we won’t be actively diving in shader authoring techniques and concepts, but this part should help you get a better idea of how the stuff we mentioned in the previous parts and the stuff we’ll mention in future parts work in the context of the game engine.

## Materials

As we mentioned in [the previous part](https://halisavakis.com/shaderquest-part-2-introducing-shaders/) shaders define how 3D objects get rendered onto our screen. But, if you’re familiar with the use of game engines, you usually don’t assign shaders onto objects, but, instead, you assign **materials**.

Materials are essentially **instances of a shader**. They are defined by the shader they’re using and they expose properties that affect the overall visual result. Think of materials as objects of a class in conventional programming; the class defines the properties and functionality of the objects and many objects can be defined by the same one class.

As I’ve mentioned a lot of times already, shaders are pretty much the same anywhere; they follow the same logic and the hand-coded ones are already pretty low level with not a huge amount of abstractions, making the process of writing shader code similar across different platforms and environments. But, as you can imagine, game engines and other rendering environments implement their own wrappers around shaders in order to make them properly communicate with the rest of the engine’s components.

Let’s take a look at the interfaces that Unity and UE4 present us with for their materials:

### Unity

Assuming you have used Unity in some capacity, if you have put any game object in a scene, you would see that it has a material on its renderer (whether that’s its mesh, skinned mesh or sprite renderer). The materials define how said object will look in the scene and have specific properties exposed that you can use to adjust the end result. You probably have already seen the standard material that get’s set up when you create a material:

![](../../assets/b26dc04fe821ed83.png)

As I already said, how materials work is defined by the shader of which they’re instances, and that’s more obvious when you look at the top of the inspector:

![](../../assets/2ceb00d6e17b41a0.png)

This material, for example, is defined by Unity’s internal “Standard” shader, which provides physically-based visual results, reacting to a bunch of different factors that come from the environment around the object and from the object itself. For example, materials using the “Standard” shader get their color changed based on the lights in the scene, the ambient lighting, reflection probes, light probes etc. We can also assign textures on the material or change its colors, which allows different materials to react differently to the same environmental factors.

If we change the shader on that material to, say, Unity’s internal “Unlit/Color” shader, we’d see just these properties instead:

![](../../assets/0d897c1fdae71e87.png)

This shader only outputs a solid color and doesn’t take lighting and other environmental factors into account, so the main property it needs is just the color it outputs.

Going back to the standard shader, below you can find a quick rundown of the different exposed properties we can change on the material. I won’t go into too much detail as most of that stuff will be revisited when we make our own shaders.

Name | Description |
| Albedo | The base color of the material. The output of the albedo texture is multiplied by the color next to it. |
| Metallic | Defines which areas of the object will be treated as metallic and which will be considered to be non-metallic (or dielectric). The metallic texture can be a grayscale texture the values of which define how metallic the corresponding area is. |
| Smoothness | Defines the glossiness of certain areas of the material. While in the “Standard” shader this is just a slider, you can use the values of the alpha channel of the metallic texture to define which areas will be glossier than others. You can see that this is determined by the “Source” dropdown. Alternatively, you can use the values from the alpha channel of the albedo texture. |
| Normal map | A texture used to fake more surface detail, like smaller bumps and dents. Normal maps play a huge role in terms of lighting, and we’ll come back to them later in much more detail. |
| Height map | A texture used for an effect called parallax offset, used to fake depth within a surface without the need for additional geometry. Unity is using the texture’s green channel to get the height map information. |
| Occlusion | A texture used to fake ambient occlusion, darkening specific areas of the mesh where light wouldn’t easily escape. Unity is using the texture’s green channel to get the occlusion information. |
| Detail mask | A texture used to define where the secondary textures will be applied. Unity is using the texture’s alpha channel to get the masking information. |
| Detail textures | An extra albedo and normal map texture used for extra, smaller scale details. |

In URP a material with the Standard shader looks like this:

![](../../assets/7ed6aae1cb230672.png)

You can pretty much tell that the main properties are working the same way.

### Unreal Engine 4

UE4 is a bit different in terms of terminology, because “materials” in UE4 kind of double as both shaders **and** materials (as we know them in Unity). As mentioned in [the previous part](https://halisavakis.com/shaderquest-part-2-introducing-shaders/) UE’s material editor is a visual node-based shader authoring system, but it outputs materials that can be assigned to objects like in Unity.

However, while in Unity duplicating a material just makes a new material that’s referencing the same shader, duplication a UE4 material basically creates an identical shader, which is not ideal as it creates a lot of redundancy. That’s why UE4 also has **material instances** which behave more closely to Unity materials. In the material editor we can have properties like textures and values that we can choose to expose in order for them to be overridden in different material instances.

![](../../assets/aaa377ae8a3a09e5.png)

Opening a material instance will present you with an interface like the one above, where you can choose to override exposed parameters on the top right corner of the “Details” tab. That way, you can have a lot of different instances with different properties referencing the same original material.

## Creating and assigning shaders

This section won’t actually go through details on shader creation; it will instead cover the subject in its more literal sense which is creating the actual shader files/objects and assigning them to materials.

### Unity

#### Built-in pipeline

A shader file in Unity can be created in your project window by selecting “Create > Shader” and choosing the shader file that best suits your needs.

![](../../assets/32924c07236c49ca.png)

We’ll go into details on the different types of shaders in later parts but in a very surface level:

**Standard Surface Shader**: Choose this if you want to make a shader that implements Unity’s standard shading system, allowing your objects to react to lighting.**Unlit Shader**: Choose this for a more barebones, low-level shader, with no regards to lighting, shading or shadow casting/receiving out of the box. The “Unlit” part might be a bit misleading, because you can in fact implement lighting in these shaders yourself. I usually refer to these shaders as**vertex/fragment shaders**, as they have distinct vertex and fragment functions.**Image Effect Shader**: Choose this shader if you want to make an effect that gets applied to everything the main camera outputs. Image effect shaders are basically a slightly simpler version of the “Unlit Shader” and with minor changes they’re basically interchangeable.

At this stage you shouldn’t worry about the other two shader types (compute and ray tracing), as we’ll mostly be focusing on the aforementioned three.

#### URP

URP and HDRP shaders are created in the form of Shader Graphs:

![](../../assets/83416719ee358067.png)

We’ll be mostly interested in Lit Shader Graphs and Unlit Shader Graphs, as we probably won’t be looking into sprite shaders. The reason is that while there might be some special approaches around sprite shaders, the techniques used in other shader graphs will be easily transferrable.

As you can imagine, Lit Shader Graphs produce shaders that will be reacting to lighting information, while Unlit Shader Graphs produce shaders that don’t handle lighting calculations.

#### Assigning shaders

The name of your newly created shader will match the name of your shader file and, depending on the type of shader you created, it will be in a specific category.

In Unity you can assign a shader to a material in three ways:

- Dragging the shader onto an open material inspector

![](../../assets/24d76dc52e53f206.gif)

2. Right-clicking onto a shader file and making a new material

![](../../assets/f1c62fe26698f268.gif)

3. Finding your shader through the “Shader” menu in the material inspector

![](../../assets/e5715e3e8e6039eb.gif)

**Note**: Built-in surface shaders are by default in the “Custom” category, built-in unlit shaders are by default in the “Unlit” category and URP/HDRP shader graphs are under the “Shader Graphs” category.

### UE4

In UE4, creating a new material is fairly straightforward:

![](../../assets/7fbe734ee00734a1.gif)

In order to create a **material** **instance** of a material, we can just right-click on it and select “Create material instance”:

![](../../assets/61639fd57f1b4331.gif)

## Conclusion

This part might not have been that exciting; in fact I bet you knew most of that stuff. But for the sake of moving one step at a time, I felt that I should get that stuff out of the way before we get into more fun stuff!

In the next part we’ll actually open up some shaders and take a look at their different components and setups. I hope that sounds a bit more interesting!

See you in the [next part of ShaderQuest](https://halisavakis.com/shaderquest-part-4-shader-environment-architecture/) ❗

## Comments

Thanks!

Thanks a lot. It’s actually helpful.

Thanks for the tutorials. By the way, how often are you planning to release these tutorials?

Author

The goal is to not have more than 2-3 weeks between each post but, y’know, sometimes life happens 😅