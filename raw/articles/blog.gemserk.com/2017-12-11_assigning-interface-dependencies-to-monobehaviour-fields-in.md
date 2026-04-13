---
title: Assigning interface dependencies to MonoBehaviour fields in Unity Editor
url: https://blog.gemserk.com/2017/12/11/assigning-interface-dependencies-to-monobehaviour-fields-in-unity-editor/
published: '2017-12-11'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In Unity, Object’s public fields of type interface are not serialized, so that means it is not possible to configure them using the editor like you do with other stuff like dependencies to MonoBehaviours.

One possible way to deflect this problem is to create an abstract MonoBehaviour and depend on that instead:

```
public abstract class ServiceBase : MonoBehaviour
{
public abstract void DoStuff();
}
public class ServiceUser : MonoBehaviour
{
public ServiceBase service;
void Update()
{
service.DoStuff ();
}
}
```


This solution has some limitations. One of them is you can’t create a sub class of multiple base classes like you do when implementing interfaces. Another limitation is that you can’t easily switch between a MonoBehaviour implementation to a ScriptableObject implementation (or any other).

Working on Iron Marines and Dashy Ninja, I normally end up referencing a UnityEngine.Object and then in runtime I try to get the specific interface, like this:

```
public interface IService
{
void DoStuff();
}
public class CharacterExample : MonoBehaviour
{
public UnityEngine.Object objectWithInterface;
IService _service;
void Start ()
{
var referenceGameObject = objectWithInterface as GameObject;
if (referenceGameObject != null) {
_service = referenceGameObject.GetComponentInChildren<IService> ();
} else {
_service = objectWithInterface as IService;
}
}
void Update()
{
_service.DoStuff ();
}
}
```


Then, in Unity Editor I can assign both GameObjects and ScriptableObjects (or any other Object):

![](../../assets/191b9f4ba07b8a00.gif)


That works pretty well but I end up having the code of how to get the interface duplicated all around.

To avoid that, I made up two helper classes with the code to retrieve the interface from the proper location. These are InterfaceReference and InterfaceObject

## InterfaceReference

```
[Serializable]
public class InterfaceReference
{
public UnityEngine.Object _object;
object _cachedGameObject;
public T Get<T>() where T : class
{
if (_object == null)
return _cachedGameObject as T;
var go = _object as GameObject;
if (go != null) {
_cachedGameObject = go.GetComponentInChildren<T> ();
} else {
_cachedGameObject = _object;
}
return _cachedGameObject as T;
}
public void Set<T>(T t) where T : class
{
_cachedGameObject = t;
_object = t as UnityEngine.Object;
}
}
```


Usage example:

```
public class CharacterExample : MonoBehaviour
{
public InterfaceReference service;
void Update()
{
// some logic
service.Get<IService>().DoStuff();
}
}
```


The advantage of this class is that it could be simply used anywhere and it is already serialized by Unity. But the disadvantage is having to ask for specific interface when calling the Get() method. If that is only in one place, great, but if you have to do it a lot in the code it doesn’t look so good. In that case, it could be better to have another field and assign it once in Awake() or Start() methods.

## InterfaceObject

```
public class InterfaceObject<T> where T : class
{
public UnityEngine.Object _object;
T _instance;
public T Get() {
if (_instance == null) {
var go = _object as GameObject;
if (go != null) {
_instance = go.GetComponentInChildren<T> ();
} else {
_instance = _object as T;
}
}
return _instance;
}
public void Set(T t) {
_instance = t;
_object = t as UnityEngine.Object;
}
}
```


*Note: the Get() and Set() methods could be a C# Property also, which would be useful to allow the debugger to evaluate the property when inspecting it.*

Usage example:

```
[Serializable]
public class IServiceObject : InterfaceObject<IService>
{
}
public class CharacterExample : MonoBehaviour
{
public IServiceObject service;
void Update()
{
// some logic
service.Get().DoStuff();
}
}
```


The advantage of this class is that you can use the Get() method without having to cast to the specific interface. The disadvantage, however, is that it is not serializable because it is a generic class. In order to solve that, an empty implementation with a specific type must be created to allow Unity to serialize it, like it is shown in the previous example. If you don’t have a lot of interfaces you want to configure, then I believe this could be a good solution.

All of this is simple but useful code to help configuring stuff in the Unity Editor.

I am working on different experiments on how to improve Unity’s usage for me. Here is a [link to the project](https://github.com/gemserk/unity-experiments) in case you are interested in taking a look.

Thanks for reading