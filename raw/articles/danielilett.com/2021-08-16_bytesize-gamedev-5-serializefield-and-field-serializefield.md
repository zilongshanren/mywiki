---
title: 'Bytesize Gamedev #5 - [SerializeField] and [field:SerializeField]'
url: https://danielilett.com/2021-08-16-bytesize-5-serialize-field/
author: Daniel Ilett
published: '2021-08-16'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Do your scripts have a lot of variables that you need to modify in the Inspector, but you want to keep `private`

in your scripts? Read on!

Bytesize Gamedev is a series of shorter game development tutorials.

Hang out with me and other shader enthusiasts over on [Discord](https://danielilett.com/(https:/discord.gg/tPQEUwPpb3)) and share what you’re working on!

Let’s start with a tiny example script.

```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class Player : MonoBehaviour
{
private int maxHealth;
public int Health { get; private set; }
public void GetHit(int damage)
{
Health -= damage;
// Do other things here.
}
}
```


Some of you might not use C# properties, so let’s break this down. `maxHealth`

is a standard variable, and `Health`

is a property - we’re using special syntax here to say we can `get`

its value from other scripts, but we can only `set`

its value within this script. This one is called an **auto-implemented property** because it creates its **backing field** automatically. There’s [more about properties](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties) on Microsoft’s website if some of that went over your head, but we’re here to talk about how to use them in Unity.

As we know, `private`

fields won’t appear in the Unity Inspector, but we can add an attribute called `[SerializeField]`

to keep it private while forcing Unity to display it. Let’s stick that on both `Health`

and `maxHealth`

.

```
[SerializeField]
private int maxHealth;
[SerializeField]
public int Health { get; private set; }
```


![Perfect if you need to keep things private in scripts but you need to set values in the Editor. [SerializeField].](/img/bytesize/part5-just-serialize.png)

*Perfect if you need to keep things private in scripts but you need to set values in the Editor.*

Now we can set the value of `maxHealth`

inside Unity. But what about `Health`

? Despite using `[SerializeField]`

, we don’t see it here. We need to use a slightly different attribute here called `[field:SerializeField]`

.

```
[field:SerializeField]
public int Health { get; private set; }
```


![Not many people know you can do this! [field:SerializeField].](/img/bytesize/part5-field-serialize-field.png)

*Not many people know you can do this!*

Et voila - now we can expose auto-implemented properties in the Inspector! Only later versions of Unity make the name look pretty, and I’m unsure exactly when this was added - but it’s an invaluable bit of information.

Thanks for reading *Bytesize Gamedev*, your one-stop shop for shorter game development tips, tricks and tutorials!