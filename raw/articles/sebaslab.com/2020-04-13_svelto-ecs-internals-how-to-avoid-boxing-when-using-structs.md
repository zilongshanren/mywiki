---
title: 'Svelto.ECS Internals: How to avoid boxing when using structs with reflection
  - Seba''s Lab'
url: https://www.sebaslab.com/casting-a-struct-into-an-interface-inside-a-generic-method-without-boxing/
author: Sebastiano Mandalà
published: '2020-04-13'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

I had two interesting problems to solve during the development of Svelto.ECS, which in short are:

- Set an implemented property of a struct, but only when the struct implements a specific interface, from a generic method and without casting the struct to the interface
- Assign an object to a field of a struct, using reflection, without casting the struct to an object

#### Cast a struct to an interface when generic parameter constraints aren’t viable

In *Svelto.ECS* all the entity components are structs. They can either implement **IEntityComponent **or **IEntityViewComponent** and, optionally, **INeedEGID**.

When **INeedEGID **is used, the user is asked to implement a property, in the entity component, that holds the Entity ID. This Entity ID is updated automatically when it changes, this means that at run time I need to change it. Since I use generic methods to access this data, I cannot use the constraint **INeedEGID** for the entity component type, as it may or may not have it.

The way I solve this is to create a *field setter delegate* that takes as input the entity component. The delegate generating code checks if** T** implements or not **INeedEGID**, if it does, it returns a delegate that works for that type, casting the parameter **T** to **INeedEGID **and assigning the value to it. However, in c#, casting a struct to an interface means boxing and since my code is allocations 0, I had to find a solution for it.

My solution for the Svelto.ECS 2.x cycle was using dynamic generated code, like this:

```
public delegate void SetEGIDWithoutBoxingActionCast<T>(ref T target, EGID egid) where T : struct, IEntityComponent;
static class SetEGIDWithoutBoxing<T> where T : struct, IEntityComponent
{
public static readonly SetEGIDWithoutBoxingActionCast<T> SetIDWithoutBoxing = MakeSetter();
static SetEGIDWithoutBoxingActionCast<T> MakeSetter()
{
//HAS_EGID is the precached result of typeof(INeedEGID).IsAssignableFrom(typeof(T));
if (ComponentBuilder<T>.HAS_EGID)
{
#if !ENABLE_IL2CPP
Type myTypeA = typeof(T);
PropertyInfo myFieldInfo = myTypeA.GetProperty("ID");
ParameterExpression targetExp = Expression.Parameter(typeof(T).MakeByRefType(), "target");
ParameterExpression valueExp = Expression.Parameter(typeof(EGID), "value");
MemberExpression fieldExp = Expression.Property(targetExp, myFieldInfo);
BinaryExpression assignExp = Expression.Assign(fieldExp, valueExp);
var setter = Expression.Lambda<SetEGIDWithoutBoxingActionCast<T>>(assignExp, targetExp, valueExp).Compile();
return setter;
#else
return (ref T target, EGID value) =>
{
var needEgid = (target as INeedEGID);
needEgid.ID = value;
target = (T) needEgid;
};
#endif
}
return null;
}
}
```


I would then use the generated delegate like in this hypothetical example:

```
public void Test<T>(T component) where T:struct, IEntityComponent //note the constraint is IEntityComponent, I cannot add INeedEGID as it may or may not have it
{
if (ComponentBuilder<T>.HAS_EGID)
SetEGIDWithoutBoxing<T>.SetIDWithoutBoxing(ref component, new EGID(1, 1)); //I expect the EGID property to be assigned without boxing
}
```


As dynamically generated code cannot be used with *IL2CPP*, I used to fall back to a simple cast, which in native code doesn’t box (as far as my experiments showed to me). However I lately realised that the Unity implementation of the *.Net Standard 2.0 interfaces* do not implement ANY code that generates IL dynamically. In order to make Svelto.ECS (Unity) .net standard 2.0 compatible, I decided to get rid of dynamically generated code.

I made several experiments, but eventually *StackOverflow *came to the rescue and the solution was fascinating (because I would have never thought about it):

```
public delegate void SetEGIDWithoutBoxingActionCast<T>(ref T target, EGID egid) where T : struct, IEntityComponent;
static class SetEGIDWithoutBoxing<T> where T : struct, IEntityComponent
{
public static readonly SetEGIDWithoutBoxingActionCast<T> SetIDWithoutBoxing = MakeSetter();
public static void Warmup() { }
static SetEGIDWithoutBoxingActionCast<T> MakeSetter()
{
if (ComponentBuilder<T>.HAS_EGID)
{
var method = typeof(Trick).GetMethod(nameof(Trick.SetEGIDImpl)).MakeGenericMethod(typeof(T));
return (SetEGIDWithoutBoxingActionCast<T>) Delegate.CreateDelegate(
typeof(SetEGIDWithoutBoxingActionCast<T>), method);
}
return null;
}
static class Trick
{
public static void SetEGIDImpl<U>(ref U target, EGID egid) where U : struct, INeedEGID
{
target.ID = egid;
}
}
}
```


In fact, I have never thought that I could create, with reflection, a delegate to a generic method with constraint! When the delegate returned is called, **U** will be **T**, but for the compiler, it also implements **INeedEGID, **hence no need for boxing!

#### Set the value of a struct field with reflection without boxing

In my library I have another similar problem, but this time a bit more complicated. I have to be able to fill fields of a struct, using reflection, but without casting the struct to an object (which reflection wants me to do!). I initially solved this problem with dynamically generated code too:

```
public static class FastInvoke<T>
{
#if ENABLE_IL2CPP
public static FastInvokeActionCast<T> MakeSetter(FieldInfo field)
{
if (field.FieldType.IsInterfaceEx() == true && field.FieldType.IsValueTypeEx() == false)
{
return (ref T target, object o) =>
{
object refo = target;
field.SetValue(refo, o);
target = (T) refo;
};
}
throw new ArgumentException("<color=teal>Svelto.ECS</color> unsupported field (must be an interface and a class)");
}
#else
//https://stackoverflow.com/questions/321650/how-do-i-set-a-field-value-in-an-c-sharp-expression-tree/321686#321686
public static FastInvokeActionCast<T> MakeSetter(FieldInfo field)
{
if (field.FieldType.IsInterfaceEx() == true && field.FieldType.IsValueTypeEx() == false)
{
ParameterExpression targetExp = Expression.Parameter(typeof(T).MakeByRefType(), "target");
ParameterExpression valueExp = Expression.Parameter(typeof(object), "value");
MemberExpression fieldExp = Expression.Field(targetExp, field);
UnaryExpression convertedExp = Expression.TypeAs(valueExp, field.FieldType);
BinaryExpression assignExp = Expression.Assign(fieldExp, convertedExp);
var setter = Expression.Lambda<FastInvokeActionCast<T>>(assignExp, targetExp, valueExp).Compile();
return setter;
}
throw new ArgumentException("<color=teal>Svelto.ECS</color> unsupported field (must be an interface and a class)");
}
#endif
}
public delegate void FastInvokeActionCast<T>(ref T target, object value);
}
```


This one was a bit trickier, because this time I don’t have any interface to rely upon. However the IL2CPP version shows again how simple the code I need is. It’s just that while in IL2CPP it doesn’t cause any problem, in c# that simple cost would cost an allocation.

In Svelto.ECS I achieve OOP abstraction through the **IEntityViewComponent**. It’s a struct that holds interfaces (one or more) that can hold ONLY value types returning properties, like this one:

```
public struct GridboxZoomEntityViewStruct : IEntityViewComponent
{
public IGridboxZoomComponent gridboxZoomComponent;
public EGID ID { get; set; }
}
```


When an entity is built, a list of *implementors *is passed to Svelto. The *implementors *must satisfy all the interfaces used inside the **IEntityViewComponents**.

so what Svelto must do is to match all the interfaces with all the *implementors *and in doing so it must not occur to any boxing either.

The way I would use the generated delegate like:

```
//field = grdboxZoomComponent / type = GridboxZoomEntityViewStruct
fieldSetterForType(ref entityViewComponent, implementor); //implementor implements IGridboxZoomComponent and must be assigned to gridboxZoomComponent without boxing. This code is generic so I can know about the fields to fill only through reflection.
```


To solve this problem, at the moment, I rely on reflection, looking for the fields and using the **SetValue FieldInfo** method. However **SetValue **would cast anything passed to an object, so the **IEntityViewComponent **struct would be boxed. To avoid this, I resorted again to dynamic generated code.

To get rid of the previous solution, I had to take advantage or some internals that really I would like to not use. Let’s see how I solved it (until I find a better solution at least):

```
public static class FastInvoke<T> where T:struct
{
public static FastInvokeActionCast<T> MakeSetter(FieldInfo field)
{
if (field.FieldType.IsInterfaceEx() == true && field.FieldType.IsValueTypeEx() == false)
{
int offset = MemoryUtilities.GetFieldOffset(field);
return (ref T target, object o) =>
{
unsafe
{
ref T pointer = ref Unsafe.AddByteOffset(ref target, (IntPtr) offset);
Unsafe.WriteUnaligned(ref Unsafe.As<T,byte>(ref pointer), o);
}
};
}
throw new ArgumentException("<color=teal>Svelto.ECS</color> unsupported field (must be an interface and a class)");
}
}
public delegate void FastInvokeActionCast<T>(ref T target, object value);
```


My reasoning here is that, if I find the offset of the field that represents the reference to the object, I could assign the object directly using unsafe code. I am stepping into a very dangerous territory here, because while the structs work in a similar way to what you would expect in c++, c# objects are another beast. They come in fact with some extra bytes that are used as header for GC, referencing, reflection and so on. Anyway I decided to bet on the idea. My first problem to solve was how to find the offset of the field I am looking for. This is the part I don’t like, as it heavily relies on the internal implementation and could break with future releases of .Net. The solution would be safe with Unity, as Unity actually provides officially a method to find the offset of a field in a struct. This is the code of **GetFieldOffset**:

```
public static int GetFieldOffset(RuntimeFieldHandle h) =>
Marshal.ReadInt32(h.Value + (4 + IntPtr.Size)) & 0xFFFFFF;
public static int GetFieldOffset(FieldInfo field)
{
#if UNITY_COLLECTIONS
return UnsafeUtility.GetFieldOffset(field);
#else
return GetFieldOffset(field.name);
#endif
}
```


I had to use a define, because **UnsafeUtility **is available only in Unity, while the other approach wouldn’t work with Mono. By the way, in case you wonder what GetFieldOffset(RuntimeFieldHandle) does, [well you can check the stack overflow answer where I stole it from.](https://stackoverflow.com/a/56512720/732761)

My bet eventually paid out, because the code:

```
ref T pointer = ref Unsafe.AddByteOffset(ref target, (IntPtr) offset);
Unsafe.WriteUnaligned(ref Unsafe.As<T,byte>(ref pointer), o);
```


worked at first try! (I never trust code working at first try).

Anyway. I don’t like this approach very much, so if you know an alternative solution, please let me know!

Not boxing structs is a big one specially with hardware protocols to avoid needless copying, boxing and unboxing. I might use your approach for a tricky problem I have. Thanks for the ideas and research done.