---
title: Using Custom Editors to interact with Unity ECS World
url: https://blog.gemserk.com/2020/08/13/using-custom-editors-to-interact-with-ecs/
published: '2020-08-13'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

# Introduction

After reading, [follow, retweet, like and or comment](https://twitter.com/arielsan/status/1294096960383856640) if you like it.

By default, the Unity’s Editor comes with tools like the Inspector window to help you visualize and modify GameObjects’s values while editing or even at runtime.

For example, if you add a MonoBehaviour like this one to your GameObject:

```
public class ExampleFieldsBehaviour : MonoBehaviour
{
public float totalHealth;
public float speed;
[SerializeField]
private int power;
}
```


It will be visualized by the default Inspector like this:

![](../../assets/e2d35822c5bed5fb.png)


With the upcoming [Unity ECS](https://docs.unity3d.com/Packages/com.unity.entities@latest/), GameObjects can still be used to design content with the [GameObject conversion](https://docs.unity3d.com/Packages/com.unity.entities@0.7/manual/gp_overview.html) workflow. However, at runtime, once the conversion was processed, even though those values can be edited (if you decided not to destroy the GameObject after the conversion) in the Inspector Window, they will not be synchronized to/from the corresponding Entity.

To visualize Entities’ values there is a new window named Entity Debugger that shows all its Components’ values in readonly mode. It also shows which systems are processing that Entity given its current Components.

# How to modify ECS values

In order to modify values using Unity ECS, custom tools have to be created. I want to share a possible way to do with the Unity’s Editor.

*Note: In general, modifying values at runtime could be direct in some cases (change the current health) but in others it might need you to know internal game logic to avoid leaving an invalid state.*

In a nutshell, the idea is to create one or more GameObjects per Entity, with one or more debug MonoBehaviours and, for each one of those, create a Custom Editor exposing interesting values and actions.

Here is an example of the result:

# Defining the structure

Let’s start with the ECS Components:

```
// Tag to identify the entities we want to debug
public struct UnitComponent : IComponentData { }
// The component to debug in the Custom Editor
public struct HealthComponent : IComponentData {
public int current;
public int total;
}
// Another component to perform damage to an entity
public struct Damage : IComponentData {
public Entity target;
public int damage;
}
```


Here is the MonoBehaviour used as debug intermediary and to create the Custom Editor later:

```
public class DebugEntityMonoBehaviour : MonoBehaviour {
// these are going to reflect the health value
public float current;
public float total;
// the reference to the entity
public Entity entity;
}
```


# Creating debug GameObjects per Entity

In order to create a debug object per Entity we want to debug, we are going to use a ComponentSystem and a [ISystemStateSharedComponentData](https://docs.unity3d.com/Packages/com.unity.entities@0.9/manual/system_state_components.html).

```
// This one just stores a reference to the debug object
public struct DebugEntitySystemComponent : ISystemStateSharedComponentData, IEquatable<DebugEntitySystemComponent>
{
public DebugEntityMonoBehaviour debug;
public bool Equals(DebugEntitySystemComponent other)
{
return Equals(debug, other.debug);
}
public override bool Equals(object obj)
{
return obj is DebugEntitySystemComponent other && Equals(other);
}
public override int GetHashCode()
{
return (debug != null ? debug.GetHashCode() : 0);
}
}
public class DebugEntitiesSystem : ComponentSystem
{
protected override void OnUpdate()
{
// create the debug stuff...
Entities
// we check only for entities with UnitComponent which are the ones we are interest on.
.WithAll<UnitComponent>()
.WithNone<DebugEntitySystemComponent>()
.ForEach(delegate(Entity entity)
{
var name = EntityManager.GetName(entity);
if (string.IsNullOrEmpty(name))
name = $"Entity{entity.Index}";
var go = new GameObject($"DebugFor-{name}");
var debug = go.AddComponent<DebugEntityMonoBehaviour>();
PostUpdateCommands.AddSharedComponent(entity, new DebugEntitySystemComponent
{
debug = debug
});
});
// update the debug stuff
Entities
.WithAll<UnitComponent, DebugEntitySystemComponent, HealthComponent>()
.ForEach(delegate(Entity entity, DebugEntitySystemComponent debug, ref HealthComponent health)
{
debug.debug.entity = entity;
debug.debug.current = health.current;
debug.debug.total = health.total;
});
// destroy the debug stuff...
Entities
.WithAll<DebugEntitySystemComponent>()
.WithNone<UnitComponent>()
.ForEach(delegate(Entity entity, DebugEntitySystemComponent debug)
{
GameObject.Destroy(debug.debug.gameObject);
PostUpdateCommands.RemoveComponent<DebugEntitySystemComponent>(entity);
});
}
}
```


This system will create a new debug GameObject for each Entity of interest (the ones with UnitComponent) that doesn’t have one yet, update it if it has one, and destroy it when the Entity was destroyed.

# Creating the Custom Editor

Now that there is one debug GameObject per Entity with the DebugEntityMonoBehaviour, it is time to create the Custom Editor:

```
[CustomEditor(typeof(DebugEntityMonoBehaviour))]
public class DebugEntityInspector : UnityEditor.Editor
{
public override void OnInspectorGUI()
{
var debug = target as DebugEntityMonoBehaviour;
var entityManager = World.DefaultGameObjectInjectionWorld.EntityManager;
EditorGUI.BeginChangeCheck();
var newCurrent = EditorGUILayout.IntField("Current Health", debug.current);
var newTotal = EditorGUILayout.IntField("Total Health", debug.total);
EditorGUI.BeginDisabledGroup(true);
EditorGUILayout.IntField("Percentage", debug.current * 100 / debug.total);
EditorGUI.EndDisabledGroup();
if (EditorGUI.EndChangeCheck())
{
entityManager.SetComponentData(debug.entity, new HealthComponent
{
current = newCurrent,
total = newTotal
});
}
if (GUILayout.Button("Perform Damage"))
{
var target = debug.entity;
var damageEntity = entityManager.CreateEntity(ComponentType.ReadWrite<Damage>());
entityManager.SetComponentData(damageEntity, new Damage
{
target = target,
damage = 5
});
}
if (GUILayout.Button("Destroy"))
{
var target = debug.entity;
entityManager.DestroyEntity(target);
}
}
}
```


Here is how it looks like:

![](../../assets/d8c5010dd6300c0b.png)


That’s it, now each time an Entity with a UnitComponent is created, the system will create a debug GameObject with the MonoBehaviour and start synchronizing values to show them in the Inspector. The CustomEditor will allow us to interact with ECS changing values or performing actions. Now new fields can be exposed and new actions can be created.

Watch again everything working together:

# Extend using Gizmos

We can also use Gizmos to draw other interesting information in the Scene view. As example, I created a new AttackComponent with the attack range.

```
public struct AttackComponent : IComponentData {
public float range;
}
```


Then modified the debug MonoBehaviour to support a new value and added the DrawGizmos method:

```
public class DebugEntityMonoBehaviour : MonoBehaviour
{
// previous stuff ...
public float attackRange;
private void OnDrawGizmos()
{
if (attackRange > 0)
{
Gizmos.color = Color.red;
Gizmos.DrawWireSphere(transform.position, attackRange);
}
}
}
```


And now extended the DebugEntitiesSystem with a new query to copy the attack range to the MonoBehaviour if there is an AttackComponent in the Entity.

```
// ....
Entities
.WithAll<UnitComponent, DebugEntitySystemComponent, AttackComponent>()
.ForEach(delegate(Entity entity, DebugEntitySystemComponent debug, ref AttackComponent attack)
{
debug.debug.attackRange = attack.range;
});
// ....
```


That will work, but all Gizmos are going to be drawn at 0,0, since our GameObjects are not considering the Entity’s position. Now, for that to make sense, we need to copy also the translation to the GameObject’s Transform, for that, I created another query:

```
// ....
Entities
.WithAll<UnitComponent, DebugEntitySystemComponent, Translation>()
.ForEach(delegate(Entity entity, DebugEntitySystemComponent debug, ref Translation t)
{
debug.debug.transform.position = t.Value;
});
// ....
```


So, for all Entities with Translation Component, the system will copy that value to the GameObject’s Transform.

Here is the result:

## Pros

- We can take advantage of all Unity’s Editor tools, even accessing the UnityEditor API. For example, we could Handles to move an Entity with a Translation Component.
- Since you have to create the inspector logic by hand, in some cases game logic can be reused for some actions and avoid breaking the game by touching values directly that could leave an invalid state.
- It is super easy to implement (we are following a similar approach with my dev team).
- Expose what you want, and even make the exposure optional, like rendering values only if the Entity has or not a Component.

## Cons

- Manually maintained, there is no auto generated inspector by default.
- Only usable in Unity’s Editor.
- Doesn’t scale so well, but I believe the automatic option (exposing all GameObject’s values) doesn’t either.

# Conclusion

I like that you can’t easily edit ECS values through the Entity Debugger nor the Inspector and to have to make your own tools. In my experience, you normally don’t want to change every value at runtime, maybe you do read some values to check the current game state and maybe, for some specific cases, you want to change a value or take an action to test some behaviour. In some way, it reminds me the [GDC talk about using different data schemas](https://www.gdcvault.com/play/1025284/Tools-Tutorial-Day-A-Tale) since the idea is to expose meaningful values to designers and debuggers which might involve some transformation in the middle.

Of course you can create a tool using reflection and automatically generating code to create these debug objects explained in the blog post but you will end up with tons of unused debug stuff and start working in a way to turn off unused values.

The technique presented here is a simple approach, might not scale so well but can be quickly implemented to have some visual tools to interact with the ECS World. I like it I would love to have this kind of tools in the builds and not only in the Unity’s Editor. I suppose a better approach could be to start creating tools integrated in the game depending a bit more to game concepts and logic. That solution could use Unity’s UI now that I think (I might try to work on that a bit and write another blog post).

In case you are interested in the code, [here is the Github project used for this article](https://github.com/acoppes/DebugToolsEcsExample).

It was a simple article but, as always, I hope you liked it and If you did, [follow, retweet, like and or comment](https://twitter.com/arielsan/status/1294096960383856640), thanks!!