---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2021/09/25/the-command-pattern-with-scriptable-objects/
author: Bronson
published: '2021-09-25'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# The Command pattern with Scriptable Objects

![](../../assets/a10fcf74e64c20d4.png)

In this article, we’ll implement another classic programming pattern in Unity. This time, it’s the command pattern.

## Why use the Command Pattern?

At its core, the command pattern makes code more flexible. We use it to create functions that we can pass around our code as if they were variables. If you’re familiar with the concept of first-class functions from other programming languages, the command pattern is essentially an object-oriented way to mimic that behaviour. If you aren’t aware, first-class function support means that a given programming language can pass functions as arguments, return functions, store functions as data, etc. First-class function support is an exciting topic, but I’m focusing on storing functions as data for our purposes. Don’t worry though, the command pattern enables all the behaviour I mentioned.

Time to stop stalling though, let’s see how the pattern looks.

```
//Command.cs
using UnityEngine;
public abstract class Command
{
public abstract void Execute();
}
```


All we do is wrap the function inside an object. Since objects always have first-class support in object-oriented programming languages, this pattern works in any OOP language. C#, in particular, has other ways to implement this pattern, such as delegates and lambda expressions, but we won’t use them in this post. At this point, to create new commands, create a class and inherit from `Command`

, then write the custom code inside the `Execute`

method.

```
//JumpCommand.cs
public class JumpCommand : Command
{
public override void Execute()
{
Debug.Log("Jumped!");
}
}
```


Let’s demonstrate how to use this with a simple Monobehaviour.

```
public class Player : MonoBehaviour
{
public Command PrimaryCommand;
public Command SecondaryCommand;
void Update()
{
if (Input.GetKeyDown(KeyCode.Z))
{
PrimaryCommand.Execute();
}
if (Input.GetKeyDown(KeyCode.X))
{
SecondaryCommand.Execute();
}
}
}
```


We store the player’s abilities in the `PrimaryCommand`

and `SecondaryCommand`

fields using the command pattern. Doing so allows us to remap the commands without recompiling the code or even at runtime. So now that we support remapping actions without recompiling, let’s turn our commands into data that the Unity Editor understands.

## Storing Commands as Data

When it comes to storing Unity Editor data, our first thought should be Scriptable Objects. Wrapping data in Scriptable Objects automatically gives us full editor support, including serialization, references and drag and drop support. So how do we do it? It turns out it’s straightforward.

```
//Command.cs
using UnityEngine;
public abstract class Command : ScriptableObject
{
public abstract void Execute();
}
```


Modify the `Command`

to inherit from `ScriptableObject`

, and voila! Now when we subclass `Command`

, add the `CreateAssetMenu`

attribute. Doing so allows us to create a new file on disk that wraps the code. Then we can attach commands to our player component through the Inspector.

```
//JumpCommand.cs
[CreateAssetMenu]
public class JumpCommand : Command
{
public override void Execute()
{
Debug.Log("Jumped!");
}
}
```


If you haven’t seen this approach before, then hopefully, your mind is racing with potential uses. But we’re not done yet! Let’s pick up the example project from last week and use the command pattern to further improve the type object pattern.

## Combining the command pattern with the type object pattern

Last week we used the type object pattern to define monsters entirely in data. We wrapped the `MonsterType`

in a generic Scriptable Object containing all of a monster’s stats. But what if every monster had its unique list of abilities as well? Using the command pattern, we can assign a list of skills to each `MonsterType`

. Since monsters are created entirely in data, we design and remix them in the Editor through default Inspector behaviour.

Let’s modify `MonsterType`

to include commands.

```
using UnityEngine;
[CreateAssetMenu]
public class MonsterType : ScriptableObject
{
public int StartingHealth;
public int BaseSpeed;
public int BaseAttack;
public MonsterType[] Weaknesses;
```**public Command[] Commands;**
}


Now every `MonsterType`

Scriptable Object will contain a list of available commands that’s modifiable through the Inspector.

![](../../assets/aa9906fde7177a50.png)

At this point, the direction you expand in depends on your particular game. For example, you may decide that each `MonsterType`

has a list of available actions, but equip each monster instance with a subset of that list. In this case, store a separate list of equipped commands on the main `Monster`

class.

```
using UnityEngine;
public class Monster : MonoBehaviour
{
public int Health;
public int Speed;
public int Attack;
public MonsterType Type;
```**public Command[] EquippedCommands;**
void Start()
{
Health = Type.StartingHealth;
Speed = Type.BaseSpeed;
Attack = Type.BaseAttack;
}
public bool IsWeakAgainst(MonsterType type)
{
foreach (var weakness in Type.Weaknesses)
{
if (type == weakness)
return true;
}
return false;
}
}


## Matters of state

There’s one last challenge to address. More often than not, our commands require some state. What does that mean? For example, to perform an attack, we need to know the target and the damage. How do we solve this? The answer depends on your needs.

The simplest solution is to pass the necessary information into the `Execute`

method. In our example, our commands are abilities that monsters can use against each other. In this case, we can modify the base command class like so:

```
using UnityEngine;
public abstract class Command : ScriptableObject
{
public abstract void Execute(Monster owner, Monster target);
}
```


In this example, those two monster objects contain all the information we need. Additionally, any shared data can be attached to the command object itself.

```
using UnityEngine;
namespace TypeObjectPattern
{
[CreateAssetMenu]
public class AttackCommand : Command
{
```**public string ConsoleMessage;**
public override void Execute(Monster owner, Monster target)
{
Debug.Log($"{owner} {ConsoleMessage} {target}");
var attackDamage = Mathf.CeilToInt(owner.Attack * (target.IsWeakAgainst(owner.Type) ? 1.5f : 1f));
target.Health -= attackDamage;
}
}
}


![](../../assets/ea4f1734654abf96.png)

If that doesn’t work, you could choose to use `GetComponent`

in the command.

```
//ChargeData.cs
public class ChargeData : MonoBehaviour
{
public int Level;
}
```


```
//ChargeCommand.cs
[CreateAssetMenu]
public class ChargeCommand : Command
{
public override void Execute(Monster owner, Monster target)
{
if (!owner.TryGetComponent(out ChargeData data))
{
data = owner.AddComponent<ChargeData>();
}
++data.Level;
Debug.Log($"{owner} charged {data.Level} times");
}
}
```


In this example, every time the owner uses `ChargeCommand`

, the command grabs the runtime data through `GetComponent`

. If the data isn’t present, it’ll create a new one. Of course, using `GetComponent`

can be expensive if abused, so keep that in mind while using this approach. Please don’t make assumptions, though; profile it to determine whether it’s fast enough for your case.

## Wrap-Up

We’ve seen how we can use Scriptable Objects and the command pattern wrap functions and manipulate them as data inside the Unity Editor. Then, by combining this approach with the type object pattern, we can define our entities’ stats and abilities entirely in data. This allows designers to create and experiment with ideas without ever having to recompile the code. In other words, designers can focus on design.

**Take a peek at the example Github project ****here****. Learn more about the Command pattern from ****this chapter**** of Game Programming Patterns. If you want to show your support for my work, ****join my mailing list****. If you do, I’ll notify you whenever I write a new post.**