---
title: Enum, Flags and bitwise operators - Alan Zucconi
url: https://www.alanzucconi.com/2015/07/26/enum-flags-and-bitwise-operators/
author: Alan Zucconi
published: '2015-07-26'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you’re a game developer chances are you’re familiar with the need to describe different variations of an attribute. Whether it’s the type of an attack (melee, ice, fire, poison, …) or the state of an enemy AI (idle, alerted, chasing, attacking, resting, …) you can’t escape this. The most naive way of implementing this is simply by using constants:

public static int NONE = 0; public static int MELEE = 1; public static int FIRE = 2; public static int ICE = 3; public static int POISON = 4; public int attackType = NONE;

The downside is that you have no actual control over the values you can assign to `attackType`

: it can be any integer, and you can also do dangerous things such as `attackType++`

.

### The enum construct

Luckily, C# has a construct called *enum* (for *enumeration*) which has been specifically designed for these situations:

// Outside your class public enum AttackType { None, Melee, Fire, Ice, Poison } // Inside your class public AttackType attackType = AttackType.None;

The definition of an *enum* creates a type which can support only a limited range or values. These values are given symbolic labels for clarity and are also returned as string when needed:

attackType = AttackType.Poison; Debug.Log("Attack: " + attackType); # Prints "Attack: Poison"

Internally, every label has an integer value. Enums starts from zero and every new label is assigned the next integer number. `None`

is zero, `Melee`

is one, `Fire`

is two and so on. You can change that by explicitly changing the value of a label:

public enum AttackType { None, // 0 Melee, // 1 Fire, // 2 Ice = 4, // 4 Poison // 5 }

Casting an *enum* to int will return its integer value. To be fair, *enums *are actual integers.

What makes *enums* even so interesting is the fact that they are automatically integrated in the Unity inspector. If a public field is an *enum*, it will conveniently appear like a dropdown menu:

![enum1](../../assets/181cb0af23dfa68c.png)

### Enums and Flags

The vast majority of developers use *enums* just as we’ve seen before. There’s much more we can do with them though. The first limitation is that standard *enums* can only hold a value at a time. What if we are using a melee weapon with a fire attack (a fire sword?!)? To solve this problem, *enums* can be decorated with `[Flags]`

. This allows them to be treated as *bit masks*, storing multiple values between them:

[Flags] public enum AttackType { None = 0, Melee = 1, Fire = 2, Ice = 4, Poison = 8 } // ... public AttackType attackType = AttackType.Melee | AttackType.Fire;

In the example above, `attackType`

both holds `Melee`

and `Fire`

values. We’ll see later how it is possible to retrieve these values. But first we need to understand how this is actually working. *Enums* are store as integers; when you have consecutive numbers, their bit representations look like this:

// Consecutive public enum AttackType { // Decimal // Binary None = 0, // 000000 Melee = 1, // 000001 Fire = 2, // 000010 Ice = 3, // 000011 Poison = 4 // 000100 }

If we want to use `[Flags]`

at its best, we should use only powers of two for the values of our labels. As you can see below, this means that every non-zero label has exactly one `1`

in its binary representation, and that they are all in different positions:

// Powers of two [Flags] public enum AttackType { // Decimal // Binary None = 0, // 000000 Melee = 1, // 000001 Fire = 2, // 000010 Ice = 4, // 000100 Poison = 8 // 001000 }

At this stage, the variable `attackType`

can be seen as a series of bits, each one indicating if it has or not a certain property. If the first bit is one, it is a melee attack; if the second bit is one, it is a fire attack, if the third bit is one it is an ice attack, and so on. It is important to notice in order for this to work, labels have to be manually initialised as powers of two. We will see later in this post how to do it more elegantly. Lastly, since *enums* are normally stored into `Int32`

, it’s unwise to have an *enum* with more then 32 different labels.

To be fair, you can use *enums* even without `[Flags]`

. The only thing it does is allowing a nicer output of *enums* when they are printed.

### Bitwise operators

A bit mask is, essentially, an integer value in which several binary property (yes/no) are independently stored in its bit. In order to pack and unpack them we need some special operators. C# calls them bitwise operator, because they work on a bit to bit basis, ignoring carries unlikely addition and subtraction operators.

#### Bitwise OR

Setting a property is possible using the *bitwise OR *:

attackType = AttackType.Melee | AttackType.Fire; // OR attackType = AttackType.Melee; attackType |= AttackType.Fire;

What the bitwise OR does is setting the bit in the i-th position to `1`

if either one of its operands has the i-th bit to `1`

.

// Label Binary Decimal // Melee: 000001 = 1 // Fire: 000010 = 2 // Melee | Fire: 000011 = 3

If you print `attackType`

you’ll get a user-friendly result: `Melee | Fire`

. This unfortunately doesn’t happen with the inspector; Unity doesn’t recognise the new type and simply leaves the field empty:

![enum2](../../assets/75dfeda0e8ba06bc.png)

If you want the mixed type to appear, you’ll have to define it manually in the *enum*:

[Flags] public enum AttackType { // Decimal // Binary None = 0, // 000000 Melee = 1, // 000001 Fire = 2, // 000010 Ice = 4, // 000100 Poison = 8, // 001000 MeleeAndFire = Melee | Fire // 000011 }

![enum3](../../assets/9d2fc8777d0e0c4e.png)

#### Bitwise AND

The complementary operator to the bitwise OR is the *bitwise AND*. It works in the exact same way, with the exception that when applied with two integers it keeps only the bits which are set in both of them. While bitwise OR is used to set bits, bitwise AND is typically used to unpack property previously stores in an integer.

attackType = AttackType.Melee | AttackType.Fire; bool isIce = (attackType & AttackType.Ice) != 0;

Applying the bitwise AND between `attackType`

and `AttackType.Ice`

sets all the bits to zero, excepts the one relative to `AttackType.Ice`

itself; its final value is determined by `attackValue`

. If the attack vas indeed an icy one, the result will be exactly `AttackType.Ice`

; otherwise zero:

// Label Binary Decimal // Ice: 000100 = 4 // MeleeAndFire: 000011 = 3 // MeleeAndFire & Ice: 000000 = 0 // Fire: 000010 = 2 // MeleeAndFire: 000011 = 3 // MeleeAndFire & Fire: 000010 = 2

If bitwise operators are making your head spinning, .NET 4.0 has introduced the method `HasFlag`

which can be conveniently used as follow:

attackType.HasFlag(AttackType.Ice);

Now, you need to be careful about the fact that `None`

has been represented with the value zero. As a result, our original approach will fail to check for `None`

: `(attackType & AttackType.None) != 0`

always return false, since `attackType & 0`

is always zero. A possible way to avoid this is to check against the original value:

bool isNone = (attackType & AttackType.None) == AttackType.None;

When it comes to `None`

, this behaviour might or might not be what you want. Just be aware that the standard .NET implementation of `HasFlag`

uses our latest example. If you don’t want to go crazy, you can also define `None`

as 1 instead. Just remember that is preferable to [always have a zero value in an enum](https://msdn.microsoft.com/en-us/library/ms182149.aspx).

#### Bitwise NOT

There is another useful bitwise operator, which is the *bitwise NOT.* What it does is simply inverting all the bits of an integer. This can be useful, for instance, to unset a bit. Let’s say we want our attack to stop being firey and become icy instead:

attackType = AttackType.Melee | AttackType.Fire attackType &= ~ AttackType.Fire; attackType |= AttackType.Ice;

By negating the property `AttackType.Fire`

we are left with a bitmask which has all `1`

s, except for a zero in the position relative to the fire property. When AND-ed with `attackType`

, it will leave all the other bits unchanged and unset the fire property.

#### Bitwise XOR

After OR, AND and NOT, we cannot not mention the bitwise XOR. As the name suggest, it is used to xor bits in the same position of an integer variable. The xor (or exclusive or) of two binary values is true only if one or the other is true, but not both. This has a very important meaning for bit masks, since it allows to toggle a value.

attackType = AttackType.Melee | AttackType.Fire; attackType ^= AttackType.Fire; // Toggle fire attackType ^= AttackType.Ice; // Toggle ice

#### Bitwise shifts

The last two operators to work with bit masks are the bitwise shifts. Taken a number, they literally shift its bits right (>>) or left (<<). If you have a decimal number, let’s say “1” and you shift it of one position to the left, you’ll have “10”. Another shift and you’ll get “100”. If shifting one position in base ten is equivalent to multiply (or divide) by ten, shifting one position in base two is equivalent to multiply (or divide) by two. This is why bitwise shifts can be used to easily create powers of two:

[Flags] public enum AttackType { // // Binary // Dec None = 0, // 000000 0 Melee = 1 << 0, // 000001 1 Fire = 1 << 1, // 000010 2 Ice = 1 << 2, // 000100 4 Poison = 1 << 3, // 001000 8 }

### Conclusion

This posts introduces *enums*, *flags* and *bitwise operators*. You can use the following functions to better work with them:

public static AttackType SetFlag (AttackType a, AttackType b) { return a | b; } public static AttackType UnsetFlag (AttackType a, AttackType b) { return a & (~b); } // Works with "None" as well public static bool HasFlag (AttackType a, AttackType b) { return (a & b) == b; } public static AttackType ToogleFlag (AttackType a, AttackType b) { return a ^ b; }

The technique described in this post is flexible enough to be adapted not just to attack types but also to inventory systems, item properties and finite state machines.

You should also check [this other tutorial](http://www.sharkbombs.com/2015/02/17/unity-editor-enum-flags-as-toggle-buttons/) on how to extend the inspector for a more user friendly *enum* interface:

![ToggleButtonFlags](../../assets/9e050326fc8a20af.gif)

If instead you prefer a dropdown menu, you should check Unity’s [EnumMaskField](http://docs.unity3d.com/ScriptReference/EditorGUILayout.EnumMaskField.html).

## Leave a Reply Cancel reply