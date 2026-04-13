---
title: 'Unity Short: Pathfinding with NavMesh'
url: https://blog.eyas.sh/2020/11/unity-for-engineers-pt10-1-pathfinding/
author: Eyas Sharaiha
published: '2020-11-22'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

For the 10th installment of
[Unity for Software Engineers](https://blog.eyas.sh/tag/unity-for-software-engineers) (now updated
and [available as a book](https://leanpub.com/unity-for-engineers)), we’ll be
doing things a bit differently. Instead of a single long-form article going
in-depth on a single topic, I will be releasing a collection of short-form
overviews over the course of this week. The goal: introduce readers to a
*breadth* of the Unity toolkit.

## Pathfinding with NavMesh

Pathfinding is a common system in video games; you might have enemies that need
to move throughout the scene to reach and attack a player, or a point-and-click
game where you command the main character by simply clicking at a destination,
or a real-time strategy game where *all* units navigate around obstacles and
each other dynamically.

Pathfinding is a well-studied and well-understood problem in computer science. You need a sense of the navigable area, the location of any obstacles, and a tried-and-tested pathfinding algorithm, like A*, repeatedly running as a scene changes.

Unity, for its part, provides a decent, performant implementation in the
[NavMesh Navigation System](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/index.html).

The NavMesh system consists of:

-
A

**NavMesh**(Navigation Mesh): A*static**pre-computed*definition of all walkable areas in the scene.A NavMesh is defined by a

component and`NavMeshSurface`

*baked*ahead of time. -
Dynamic NavMesh

[obstacles](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/CreateNavMeshObstacle.html).This allows you to constrain the pre-computed static NavMesh with obstacles that appear, disappear, or change during run-time.

-
This allows you to

*add additional paths*within or between a NavMesh. For example, modeling a jump between two levels within a NavMesh or a connection between two disjoint meshes (for example, if you have multiple scenes loaded simultaneously in an open-world setting, you can only navigate between each scene’s mesh via NavMesh Links). -
A collection of

**NavMesh Agents**that move about the mesh.A

`NavMeshAgent`

is athat can be added to any object. In C#, it can be found in the[component](https://blog.eyas.sh/2020/10/unity-for-engineers-pt5-object-component#component)`UnityEngine.AI`

namespace. By default, a`NavMeshAgent`

will control the position and rotation of its object via.`NavMeshAgent.SetDestination(Vector3)`

A

`NavMeshAgent`

can also be used to provide pathfinding capabilities through methods like`NavMeshAgent.CalculatePath`

and others, allowing the developers to use that path in other ways.

## Using a NavMesh Agent

Assuming you have already
[baked your NavMesh](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/CreateNavMesh.html),
you are ready to start using your first NavMesh Agent. Remember to re-bake your
scene when you add new obstacles (walls, etc.) or your layout changes.

```
using UnityEngine;
using UnityEngine.AI;
[RequireComponent(typeof(Animator), typeof(NavMeshAgent))]
public class NavMeshMover : MonoBehaviour
{
[Header("Animation")]
private Animator _animator;
private int _speedParam;
[Header("Navigation")]
private NavMeshAgent _agent;
private void Awake()
{
_animator = GetComponent<Animator>();
_speedParam = Animator.StringToHash("Speed");
_agent = GetComponent<NavMeshAgent>();
}
public void NavigateTo(Vector3 destination)
{
float distance = Vector3.Distance(transform.position, destination);
if (distance > _agent.stoppingDistance)
{
_agent.destination = destination;
}
else
{
transform.LookAt(destination, Vector3.up);
}
}
private void Update()
{
_animator.SetFloat(_speedParam, _agent.velocity.magnitude);
}
}
```


An external component can then control *how* to move from one place to the
other. For a player, it could be based on mouse clicks on various destinations.
For an enemy, it could be based on developer-written AI logic based on its
field-of-view, distance to a player, etc.

You can also decide to de-couple your “Mover” interface from this
`MonoBehaviour`

. For example, you might also want a `TeleportMover`

or
`FancyCustomAdvancedAlgorithmMover`

. You can do that in a few ways:

-
Extract an interface

`IMoverComponent`

:`public interface IMoverComponent { void NavigateTo(Vector3 destination); }`

and implement it:

`public class NavMeshMover : MonoBehaviour, IMoverComponent { // ... }`

Using

`GetComponent<IMoverComponent>()`

will give you the interface you want.The drawback is that interfaces don’t work with serialized fields. That means that if you’re referencing the mover component explicitly from the inspector, you won’t be able to do that. In that case:

-
An abstract

`MonoBehaviour`

could work.`public abstract class MoverComponent : MonoBehaviour { public abstract void NavigateTo(Vector3 destination); }`

Your

`NavMeshMover`

can then only implement`MoverComponent`

. You can now explicitly set that using the inspector, or use`[RequireComponent(typeof(MoverComponent))]`

where needed. The disadvantage here is that a component can not use multiple inheritance from multiple abstract classes.

## Update Notes (2025)

This post was updated in late 2025 to reflect the current state of the NavMesh system.

**NavMesh Package**: The navigation system has moved to the`com.unity.ai.navigation`

package.**NavMeshSurface**: The preferred way to bake NavMeshes is now using the`NavMeshSurface`

component, rather than the global Navigation window. This supports prefabs and runtime baking.**NavMeshLink**:`OffMeshLink`

has been deprecated and replaced by`NavMeshLink`

, which offers more features and better integration.