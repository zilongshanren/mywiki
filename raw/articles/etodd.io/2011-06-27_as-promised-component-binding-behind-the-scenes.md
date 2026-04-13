---
title: 'As promised: Component Binding "BEHIND THE SCENES"'
url: https://etodd.io/2011/06/27/component-binding-behind-the-scenes/
published: '2011-06-27'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# As promised: Component Binding "BEHIND THE SCENES"

In the wake of [this brief description](https://etodd.io/2011/02/02/refactoring-with-components/) of my component binding system, I was asked to provide more details on its implementation. This article is my best attempt to do so!

This is a tale of intrigue, excitement, and wonder, in which I try to implement a component-entity system in C#, and stumble upon a remarkable paradigm that merges components with data binding.

Note: If you don't have at least a vague concept of component-entity design, [read this article first](http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/).

### Converting from OO to Component Binding

I started with an orthodox inheritance hierarchy. You've got a GameObject base class with Update and Draw methods. You've got subclasses for each type of object: Player, Camera, Object, Map, etc.

How to convert this hierarchy into components? I figured the one thing almost all the GameObjects had in common was a position, so I set out making a component to store that:

```
class TransformComponent : Component
{
public Vector3 Position;
public Quaternion Orientation;
public Vector3 LinearVelocity;
public Matrix Transform;
public override void Update(float dt)
{
this.Position += this.LinearVelocity * dt;
this.Transform = Matrix.CreateTranslation(this.Position) * Matrix.CreateFromQuaternion(this.Orientation);
}
}
```


Next, I created a ModelComponent, that would display a 3D model. This was easy because I already had a separate Model class that was already self-contained. I then wrote a factory to make my first entity: the player. Why a factory? Because it seemed to be the thing to do, and it sounded cool.

```
class PlayerFactory : Factory
{
public Entity Create(Main main)
{
Entity player = new Entity();
player.AddComponent(new TransformComponent());
player.AddComponent(new ModelComponent());
}
}
```


Now, how to get the model to show up at the position and orientation specified by the TransformComponent? I wanted the output Matrix from my shiny new TransformComponent to magically "go to" a model component. Or a camera component. Or a shader. Or whatever I wanted! That was the whole point of this disastrous endeavor.

### Magic Properties

I needed to create a mystical linkage between two Matrix properties. For that to happen, I would need a way to know when a property changed, so that I could update all the other properties bound to it. And for *that* to happen, I needed some kind of method that would be called whenever a property changed. So I created a Property object that could be templated to store any kind of object or primitive type. My components now looked like this:

```
class TransformComponent : Component
{
public Property<Vector3> Position = new Property<Vector3>();
public Property<Quaternion> Orientation = new Property<Quaternion>();
public Property<Matrix> Transform = new Property<Matrix>();
// ...
}
class ModelComponent : Component
{
public Property<Matrix> WorldTransform = new Property<Matrix>();
// ...
}
```


To write to one of these properties, I had to do this:

`this.Transform.Value = <blah>;`


It was a little ugly, but at least I had a property setter where I could put code to update other properties.

With that done, I created a Binding class to link properties together. Upon initialization, the Binding would let both properties know it existed. Both properties would save the Binding to private lists, and whenever their Value setter was called, they would notify all their Bindings, which would synchronize everything between the properties. The player factory method now looked like this:

```
public Entity Create(Main main)
{
Entity player = new Entity();
TransformComponent transform = new TransformComponent();
ModelComponent model = new ModelComponent();
player.AddComponent(transform);
player.AddComponent(model);
new Binding<Matrix>(model.WorldTransform, transform.Transform);
}
```


I ended up creating a few different types of Bindings which behaved in different ways. The most basic kind of Binding was one-way between properties of the same type, like the above example. But I quickly found that I needed a way to convert between property types. For example, in the player "state" component I had a Rotation float property that specified the 2D angle the player was facing. I needed to convert that to a Matrix for the Transform component. Through the magic of lambda functions, I ended up with this:

```
// Have the player face the direction he is going
new Binding<Matrix, float>(
transform.AbsoluteOrientation,
x => Matrix.CreateRotationY(x),
state.Rotation
);
```


I created Bindings that compiled values from multiple Properties. I created two-way Bindings. I created Bindings that were automatically re-evaluated every time their Properties were queried, even if nothing seemingly needed updating. They were all pretty trivial and really came in handy later on.

### Reaping the benefits: Bindings and declarative code

Bindings are really the strong point of this system. It makes your code declarative rather than procedural. Let's say you want to make a "crouch" ability that lowers the player's height when he's crouching. In standard OOP, you'd get something like this:

```
class CollisionObject : GameObject
{
float width;
float height;
float depth;
public override void Update(float dt)
{
super.Update(dt);
// ... do collision-checking with the width, height, and depth variables
}
}
class Player : CollisionObject
{
public Player()
{
this.width = 1.0f;
this.height = 2.0f;
this.depth = 1.0f;
}
public override void Update(float dt)
{
super.Update(dt);
if (Input.KeyIsPressed(Keys.Crouch))
this.height = 1.0f;
else
this.height = 2.0f;
// ... oodles of other update code...
}
}
```


Two years later, when you dig up this project and you want to know how the crouch function works, you'll have to look through the entire Player and CollisionObject code to understand it.

If we tried this with components, we might come up with an InputComponent that handles keyboard input, and a CollisionComponent that handles collision detection. Then in our factory method we might create a binding like this:

```
new Binding<float, bool>(
collisionComponent.Height,
x => (x ? 1.0f : 2.0f),
input.CrouchKeyPressed);
```


What changed? Rather than writing a *procedure* to update the player's height every single frame, we *declared* a relationship between the crouch key being pressed, and the player's height being decreased. With bindings, you can declare behavior almost like declaring HTML markup.

Still, sometimes you just need to write things procedurally. Don't worry, you can still write procedural code in your individual components. Just be sure to make each component self-contained, and then glue them all together with declarative bindings. Actually, while transitioning to the component system, you can take the "Blob" approach. That is, take all your current procedural code and cram it into a "Blob" component. You can then slowly separate it into more manageable components. Eventually each component will have a nice amount of self-contained procedural code, and you'll have a factory to glue it all together with declarative bindings.

### Setters and Getters

One problem I encountered early on was that a lot of my properties had getters and setters, and I didn't want to give up these convenient little methods. A few quick changes to the Property class, and I can do things like this:

```
public class AudioListenerComponent : Component
{
protected AudioListener listener = new AudioListener();
public Property<Vector3> Position = new Property<Vector3> { Editable = false };
public Property<Vector3> Forward = new Property<Vector3> { Editable = false };
public override void InitializeProperties()
{
this.Position.Get =
delegate()
{
return this.listener.Position;
};
this.Position.Set =
delegate(Vector3 value)
{
this.listener.Position = value;
};
this.Forward.Get =
delegate()
{
return this.listener.Forward;
};
this.Forward.Set =
delegate(Vector3 value)
{
this.listener.Forward = value;
};
}
}
```


Yes, you can even technically initialize the delegates inline with this really slick syntax:

```
public class AudioListenerComponent : Component
{
protected AudioListener listener = new AudioListener();
public Property<Vector3> Position = new Property<Vector3>
{
Editable = false,
Get = delegate()
{
return this.listener.Position;
},
Set = delegate()
{
this.listener.Position = value;
}
};
public Property<Vector3> Forward = new Property<Vector3>
{
Editable = false,
Get = delegate()
{
return this.listener.Forward;
},
Set = delegate(Vector3 value)
{
this.listener.Forward = value;
}
};
}
```


But then for some reason the compiler doesn't let you access the "this" keyword. Bummer.

### Commands

I soon realized that the Binding system was somewhat lacking. There was no way to bind events to each other. I wanted a way to say, "when this happens, do that". I followed the [MVVM design pattern](http://en.wikipedia.org/wiki/Model_View_ViewModel) and used Commands to make this a reality.

The Command class is practically a mirror image of the Property class. But instead of storing a value, it stores a function pointer. Whenever the Command is executed, it calls the function pointer and also executes any Commands that are bound to it with CommandBindings. Easy.

```
public class TimerComponent
{
public Command Command = new Command();
public void Update (float dt)
{
// ...
this.Command.Execute();
}
}
public class SoundComponent
{
public Command Play = new Command();
}
// Factory code...
new CommandBinding(footstepSoundComponent.Play, footstepTimer.Command);
```


Adding Commands with one or two parameters was fairly trivial.

### Conclusion

This pattern, like all design patterns, is not a silver bullet. I still have too many tight linkages in my code. But it's an improvement, and certainly a step toward self-documenting, maintainable code.

There's a lot more to this system, including how it all works with .NET serialization. I don't have time to cover it all, so for your browsing pleasure, [here are the core classes](http://code.google.com/p/component-binding/source/browse/#svn%2Ftrunk) extracted from my project. Hopefully they can be some use to you.

Thanks for reading!