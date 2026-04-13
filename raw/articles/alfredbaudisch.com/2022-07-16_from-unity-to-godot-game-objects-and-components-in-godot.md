---
title: 'From Unity to Godot: Game Objects and Components in Godot?'
url: https://alfredbaudisch.com/gamedev/from-unity-to-godot-where-are-my-game-objects-and-components/
author: Alfred Reinold Baudisch
published: '2022-07-16'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

**Coming from Unity, you just opened Godot for the first time and you can't find where are the Game Objects and Components?** Not only that, where are the Prefabs and the Levels? All you can see are four buttons under a label: "Create Root Node". What are Nodes? Where do I even add my custom scripts and create components?

**With this short guide, learn how to contextualize Unity's concepts of Game Objects, Components, Prefabs and Nested Prefabs in Godot with Nodes, Scenes, Node Trees and Scene Trees.**

![](../../assets/7fce4fe950b6fe48.png)

## Do you prefer video?

This article is also available as a video.

## Unity Building Blocks

In Unity, **Game Objects are the main building blocks of scenes**. But Game Objects by themselves do not do anything. They need Components. **Components add behaviours and properties to Game Objects.** A Game Object can contain any amount of Components, defining multiple behaviours, thus Game Objects are containers for components.

Unity has many built-in Components and **to build your own components, you write C# scripts** that inherit from MonoBehaviour. After writing a script, you attach it to a Game Object as a Component.

## Nodes aka Godot's Game Objects and Components

**Nodes are the building blocks of Godot**. But as opposed to Game Objects, Nodes are not absent of behaviours, **Nodes are the actual behaviours**, just like Unity's Components.

Every **Godot Node is a class type** (as in objected oriented programming "class"), for that reason the

**Node behaves as per its class implementation, with its own sets of methods, properties and signals (events)**.

## Composing Nodes

But since Nodes are Components, how do you compose Nodes together in order to combine all the needed behaviours like a Game Object?

For example, a Third Person 3D Character needs at least four different components:

- A Skeletal Mesh
- One or more Colliders
- A Camera
- A script that defines the controls, the physics and more

In Godot, **you can compose Nodes in a tree**. You can nest any amount of Nodes and arrange them in any combination as you like, there are no restrictions.

For that reason, for our Third Person Character example, we can arrange it with a Node of the type KinematicBody as the root and as a child all the other Nodes (or "Components"):

![](../../assets/d453cc837733dce3.png)


Or we could have a base Spatial Node (the base Node for 3D "components") as the root, and arrange the rest of the hierarchy in a completely different way as the previous composition:

![](../../assets/cab3f50068e0dff5.png)


Aren't we still missing the "Script" Component? Not exactly. In the previous screenshots, notice that there's a "paper" icon attached to some of the nodes. If you click any of those paper icons, you are going to open the script attached to it.

## Scripts

A Godot Node is a Component by itself. And a Node is always of a class type. If you want to add custom behaviour on top of it, you are going to attach a script to the Node. The script must inherit from the Node's base type or from a derived type of the selected Node type, this way you are effectively inheriting from the Node's base class (or from the already derived class) – a basic OOP concept.

![](../../assets/f7c5dd18cc00ba54.png)


By inheriting from the Node's type, **you can re-use all of the Node's base class methods, events and properties, override any of them, and of course, add new methods, new events and new properties**.

It's the same for both GDScript or C#.

![](../../assets/27bb1239c7093f7c.png)


For example, by adding a script to a [KinematicBody Node](https://docs.godotengine.org/en/stable/classes/class_kinematicbody.html), you have all methods and properties available to make a character (or any other moving physics object).

With C#, you inherit from the same base class: `public class YourCustomClass : KinematicBody.`


## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## Custom Node Types (Custom Components)

Defining a class name is not mandatory for scripts in Godot. You can freely attach scripts to Nodes, and your code will add and/or override behaviour from the base class. But if you add a class name to your script with `class_name`

, you are **effectively creating a custom Node Type, which will also appear in the Add New Node dialog, alongside Godot's built-in Node types.**

![](../../assets/4500ae72a2fc541b.png)


Not only that, you could create a new script that inherits from your previously KinematicBody script that defines yet another new type of character, inheriting from your current implementation.

![](../../assets/fba8e427f2ad68f2.png)


Or with C#: `public class MyInheritedCharacter: My3DCharacter`

.

It's worth noting that you can also extend a script you created in another script by [extending the script path](https://godotengine.org/qa/35166/extending-script-files), even if the script does not have a custom `class_name`

.

## Scenes aka Godot's Prefabs

You learned that Nodes are arranged and composed in trees. The next step is re-using and/or re-combining those trees, as well instantiating them. For example, what use is to create a 3rd Person Character Node Tree, if it exists in a single place? How to you place in-game? How can you place more than one character? How can you use your character to also serve as NPCS? How can we package those Node Trees in order to have a single source of truth for a certain composition and behaviour and then instance and even inherit from them?

In Unity, prefabs serve this purpose. You can define one or more nested Game Objects as prefabs. Not only that, you can nest Prefabs within Prefabs, as if you change the base Prefab, it's reflected across all instances (even inside the nest Prefabs), while at the same time, you can override properties in instanced Prefabs.

Godot has the exactly same functionality, which goes beyond the concept of "prefabs" (i.e. serving as a prefab is just one of the usages of what we are going to see).

The answer are Scenes. You can save any Node Tree or even any branching of a Node Tree as a Scene – in the same way that you can save any Game Object or any branching of it as a Prefab.

The saved Scene is then going to be a file in the file system that you can drag and drop in any other Scene and Node Tree, or use the Instance Child Scene button or of course, also instance it with code.

The scene is going to be added to the Node Tree as a Node itself. In the end, Scenes are a Tree of Nodes, being effectively a Node by itself – remember that in our 3D Character, we composed it with some Nodes, then saved it as a Scene

You can identify it as Scene by the Clapperboard icon alongside the Node name. If you click the clapperboard icon, you are going to open the scene. If you open the Scene again, make changes to the it, all instanced Nodes of this scene are also going to be updated, just like Unity prefabs.

## Scene Inheritance and Overrides

And since Scenes are Nodes, just like Nodes, a Scene can also inherit from another Scene. This way, you create children Scenes that inherits everything from the parent Scene, while being able to also override and/or add new elements to it.

Consider a base 2D scene that defines a script with a collider and a custom script:

![](../../assets/3e52d23296fb4718.png)


A New Inherited Scene can be created with the "CollectableItemTile" Scene as the parent:

![](../../assets/658272695fdf8c5a.png)


All of the parent's Scene nodes are inherited, and we can also click to go to the parent Scene:

![](../../assets/a4e387d911ee4b91.png)


And of course, we can also override the base Scene by either adding new nodes or by changing properties in the Inspector:

![](../../assets/9c815a3ec2d6a7a9.png)


If the base Scene is changed, the inherited scenes receive the new changes as well. Just like with Nodes, because Scenes are Trees of Nodes, and those Tree of Nodes are Nodes themselves.

## Scene Tree aka Godot's Nested Prefabs

In a new Scene Node Tree, you can add many different Scenes as Nodes and also add new standalone Nodes (remember that whenever a Node has a clapperboard icon, it's an instanced Scene).

![](../../assets/9cf3f8cfc28b86e2.png)


As we saw previously, a new Scene can inherit from another Scene. And you can keep stacking Scenes on top of Scenes, and those by themselves also have their own instances or inherited Scenes. This hierarchy is the **Scene Tree**.

![](../../assets/2a913b41fcbd3714.png)


![](../../assets/2a913b41fcbd3714.png)

With the Scene Tree, you have Godot's:

- Prefabs
- Nested Prefabs
- And Levels.

**Godot's Levels are in the end just Scene Trees, which in turn are Scenes which in turn are Node Trees, which leads to Nodes**.

## Resources aka Godot's Scriptable Objects

As a last concept, understand that **Scenes are Godot Resources, for that reason they are saved as Resources, i.e. readable text files and they can be treated as just like any Resource in Godot.**

You can use Godot Resources just like Unity's ScriptableObjects (but it goes further, with even more flexibility).

In the end, **everything in Godot is a Node and a Resource.** Nodes and Resources are the two main Godot's fundamental concepts.

Unfortunately, Resources are out of the scope of this article, but check the links below to see more.

## Where to learn more?

- Godot's excellent documentation pages
[Nodes and Scenes](https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html)and[Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html). - My course
is a masterclass about Godot's concepts, mostly important on GUI and Godot Resources in-depth. No Godot and GDScript knowledge required. With the course, you are going to learn extensible user interfaces with Godot, but mostly important dynamic data driven systems, check the trailer below.[Godot Engine Course: Data Driven Inventory System and Complex UIs](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) - Available on
[Itch](https://bit.ly/GodotUI)or[Skillshare](https://skl.sh/35VyvE1)(one month free).

## Support content and open-source Projects

Did you like the content? Do you want to support my content or my open-source projects?

- Buy me a coffee:
[https://ko-fi.com/alfredbaudisch](https://ko-fi.com/alfredbaudisch) - PayPal:
[https://bit.ly/AlfredBaudischPaypal](https://bit.ly/AlfredBaudischPaypal) - Join my YouTube channel as Super Member:
[https://bit.ly/AlfredBaudischJoinChannel](https://bit.ly/AlfredBaudischJoinChannel) - Become a patron via Patreon:
[https://www.patreon.com/alfredbaudisch](https://www.patreon.com/alfredbaudisch) - Check
[my game Brazilian Street Food Simulator](https://alfredbaudisch.com/projects/games/brazilian-street-food-simulator/)and add it to your[Steam Wishlist](https://store.steampowered.com/app/2125110/Brazilian_Street_Food_Simulator/?utm_source=alfredbaudisch&utm_campaign=unity_article)

## See more

- Did you know that
**Godot is incredibly good and lightweight to write general usage software, tools and apps?**Check my[Godello](https://github.com/alfredbaudisch/Godello)project (**a clone of Trello made with Godot**) as well**my upcoming**.[Godot's Book: Developing Software, Tools and Apps](https://bit.ly/GodotBook) - My Zelda Breath of the Wild
**Inventory System made with Godot in my course is**.[open-source](https://github.com/alfredbaudisch/GodotDynamicInventorySystem) - I also have other Godot open-source projects, check my
[Github](https://github.com/alfredbaudisch/). - And I also have a growing YouTube gamedev channel where I talk about Godot (and Unreal Engine, Blender and more), and where I also publish my Indie Gamedev Podcast, check it out:
[youtube.com/alfredbaudischcreations](https://youtube.com/alfredbaudischcreations) [Follow me on Twitter](https://twitter.com/alfredbaudisch)for a lot of Godot Experiments, Gamedev, Art (and more, so do not expect only Godot talk!).- This article is also published on my
[Medium magazine](https://alfredbaudisch.medium.com/from-unity-to-godot-game-objects-and-components-in-godot-84594874efdc).

![Godello Godot Drag and Drop](../../assets/1482ceaa52a4a110.gif)