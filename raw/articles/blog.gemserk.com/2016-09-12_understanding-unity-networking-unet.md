---
title: Understanding Unity Networking (Unet)
url: https://blog.gemserk.com/2016/09/12/understanding-unity-networking-unet/
published: '2016-09-12'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

The objective of this blog post is to give you a first look at Unity Networking ([Unet](http://docs.unity3d.com/Manual/UNetOverview.html)) based on my experience with it, and from my point of view.

## Introduction

[Unet](http://docs.unity3d.com/Manual/UNetOverview.html) is the Unity client/server architecture solution for networking, which provides the developer a [wide range of options](http://docs.unity3d.com/Manual/UNetUsingHLAPI.html) from high level logic like automatically synchronizing game objects state to low level like directly sending bytes through a network connection.

To have a quick understanding of how it *normally* works, here is a quick example. Imagine there are 3 machines connected, one server and two clients. Each machine is running the same game, that means the same code and the same Scene with same GameObjects. The code has a way to know if it is on a server or a client, and if has authority or not, and take action according to that. For example, for non player objects the server is the one with the authority and for player objects only one client has authority. Since it is a client/server architecture actions are processed on the server and then synchronized back to the clients.

note: I wrote *normally* because it is not always the case, you can have have objects created only on some clients, or on the server, etc.

## Unet

The idea here is to give you a quick look of what I explored so far.

The [NetworkManager](https://docs.unity3d.com/ScriptReference/Networking.NetworkManager.html) is Unet point of entrance. It is the way to host or join a game. It is responsible for creating the player object for each client, etc. As a Unity behaviour, it allows configuring the player prefab, start positions, different scenes for being offline or online, or even advanced stuff like configuring connection timeouts, etc.

All Unet network objects must have a [NetworkIdentity](https://docs.unity3d.com/ScriptReference/Networking.NetworkIdentity.html) behaviour, this is the way to identify an object is the same in different machines, used for synchronzation for example.

The [NetworkBehaviour](https://docs.unity3d.com/ScriptReference/Networking.NetworkBehaviour.html) is the base class for behaviours that want to know about networking. Subclasses of this class can override easy methods to be aware of networking events, automatically [synchronize fields](http://docs.unity3d.com/Manual/UNetStateSync.html), invoke methods on the server or on the clients, and to know current code has authority over the object or not (since normally all objects are created in each machine). Here is a code sample containing some of these concepts:

```
public class NetworkExampleClass : NetworkBehaviour
{
[SyncVar]
public int health;
int maxHealth = 100;
public Color myColor;
public GameObject bombPrefab;
public void Start()
{
if (isLocalPlayer) {
myColor = Color.blue;
} else {
myColor = Color.red;
}
if (isServer) {
Debug.Log ("Object started on server");
}
}
// only want to process this Unity callback on clients (avoid server update)
[ClientCallback]
public void Update()
{
// don't want to process on the client that is not the object owner, this works only
// for the player object I believe.
if (!isLocalPlayer)
return;
if (Input.GetMouseButtonUp (0)) {
CmdTakePotion(10);
}
if (Input.GetMouseButtonUp (1)) {
CmdSpawnBomb(UnityEngine.Random.insideUnitCircle * 100);
}
}
// send command to server to perform authoritative logic
[Command]
public void CmdTakePotion(int hitpoints)
{
health += hitpoints;
if (health > maxHealth)
health = maxHealth;
RpcShowPotionFeedback (hitpoints);
}
// send command to clients to perform visual logic
[ClientRpc]
public void RpcShowPotionFeedback(int hitpoints)
{
CreatePotionFeedback ();
}
public void CreatePotionFeedback(int hitpoints)
{
// TODO: create visual feedback for taking a potion
}
[Command]
public void CmdSpawnBomb(Vector2 position)
{
GameObject bombObject = GameObject.Instantiate (bombPrefab);
bombObject.transform.position = position;
// this spawns the object on all clients and syncrhonizes them with server object (identity, etc)
NetworkServer.Spawn (bombObject);
}
}
```


(note: this code may not compile, it wasn’t tested)

And here is a quick explanation of the example concepts:

**isServer**: this property lets you know if you are on the server or not.**hasAuthority**: this property lets you know if you have authority over the game object or not.**isLocalPlayer**: this property tells you if the gameobject represents the player on the local machine, to avoid for example moving another players gameobjects when processing the input.**[SyncVar]**: this field annotation it is a way to specify you need a field to be synchronized over the*same*game object running in each machine (the object identified by the same network id). For example, the health was decreased from 10 to 5 in the server, then all clients must show the change in the health bar.**[Command]**: this method annotation it is used on methods that want to be invoked from a client to run in the server, their names must start with Cmd prefix. For example, if you want to do damage over a unit you send that to the server since the server is the authority here.**[ClientRpc]**: this method annotation it is used on methods that want to be invoked from a server to run in all clients, their names must start with Rpc prefix. For example, the server detected some unit died (after it received damage), then it invokes a RpcUnitDeath(), so each client show the unit death animation.- Other methods annotations like
**[ClientCallback]**and**[ServerCallback]**are an easier way to not having to check isServer property in the code, it is used for Unity automatic gameobject callbacks like Update or Start methods. **NetworkServer.Spawn()**: it is the way to synchronize server creation of objects on clients, that means creating a game object on each client with the same network id.

For automatically synchronizing state there are already some behaviours like the [NetworkTransform](https://docs.unity3d.com/ScriptReference/Networking.NetworkTransform.html). These behaviours not only provide an automatic way to synchronize a GameObject common state but, in some cases, also a way to configure interpolation strategies. Here is a picture showing the NetworkTransform configuration:

Note: in my tests I couldn’t find a way to make the transform interpolation to look smooth. Even looking at [other developers examples](http://forum.unity3d.com/threads/unity-5-unet-multiplayer-tutorials-making-a-basic-survival-co-op.325692/), they normally create their own interpolation code to fix that.

Here is a video showing a quick example I did using Unet, there are two clients, the left one is also the server. Each player can control one hexagon by clicking where to move it, the movement logic is performed in each client machine and automatically synchronized using a NetworkTransform.

## Conclusion

The Unet high level concepts are a way to get, as fast as possible, a multiplayer game working, and depending the kind of game you are making, it may fit perfectly your needs. The low level access may give you a real control of what is happening behind the scenes in case you need to optimize your game networking usage.

As a developer, being flexible to use from high to low level stuff is always an advantage, and that is a really good point of Unet. Also, even though it wasn’t so easy to understand for me in my first tests, I believe the HLAPI is not hard to use and gives a good start point, and, like other Unity stuff, it is really good for quick prototyping.

Another really good point is that it is [open source](https://bitbucket.org/Unity-Technologies/networking) which means I can take a look at implementation details if I want, or understand how something work behind the scenes, or even propose bug fixes.

The bad part is that the documentation is not good, but that happens for all the Unity stuff, when you need to understand something in detail the documentation says nothing or it is even wrong. Also, the first Unet tutorial results wasn’t what I expected, the movement was really choppy and it didn’t work so well (I believe they updated it, I tried the one for Unity 5.3.x), that was something that made me think about Unet not being the solution I wanted for my games, but in the end it was just a really bad example of Unet features.

Also, if you are making an action game, I don’t know if Unet provides good support for [client side prediction, server reconciliation or lag compensation](http://www.gabrielgambetta.com/fast_paced_multiplayer.html) but it shouldn’t be a problem to implement what you need over Unet since it is very flexible.

Right now I am following another aproach of using low level send messages API since for my game I am trying to reduce the bandwidth cost by sending only player actioons and performing a [synchornized simulation](https://blog.gemserk.com/2016/08/30/lockstep-multiplayer-first-steps/), something I will try to write about in a future blog post.

## References

Some references in no specific order.