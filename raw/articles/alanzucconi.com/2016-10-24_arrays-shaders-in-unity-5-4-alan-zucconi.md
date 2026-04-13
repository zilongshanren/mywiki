---
title: Arrays & Shaders in Unity 5.4+ - Alan Zucconi
url: https://www.alanzucconi.com/2016/10/24/arrays-shaders-unity-5-4/
author: Alan Zucconi
published: '2016-10-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post shows how to use arrays and shaders in Unity 5.4. Back in January I already covered this topic in an article called [Arrays & shaders: Heatmaps in Unity](https://www.alanzucconi.com/?p=2003). My original approach exposed an undocumented feature that allowed to pass arrays to shaders. Since then, Unity 5.4 has introduced proper support in its API. This tutorial replaces the previous article. If you have read the previous tutorial, you do not need any changes to your shader code and you can skip to Step 2.

- Step 1.
[The Shader](https://www.alanzucconi.com#step1) - Step 2.
[The Script](https://www.alanzucconi.com#step2) - Step 3.
[Limitations](https://www.alanzucconi.com#step3)

Every shader has a section called `Property`

, which allows to expose certain variables in the material inspector. At the time this article is written, Unity does not support an array type. Consequently, you cannot access arrays directly from the inspector. It’s worth notice that Unity supports a type called [2DArray](https://docs.unity3d.com/Manual/SL-TextureArrays.html), but that is reserved for texture arrays; what we want is an array of numbers instead.

All arrays, have to be declared as variables and initialised externally via a script. Arrays in shaders need to have a predefined length. If you don’t know in advance how many items you’ll need to store, allocate more space and keep a variable (for instance, `_ArrayLength`

) that will indicates how many items are actually present.

int _ArrayLength = 0; float _Array[10];

In the example above, both variables has been decorated with the `uniform`

keyword. This is because their value is changed from an external script, and we assume that those changes do not happen in between frames.

You can now look your array in the shader code like any other type of array:

for (int i = 0; i < _Length; i++) { ... float x = _Array[i]; ... }

If you want to use your shader, you need to initialise the array using an external script. The new API of Unity 5.4+ supports the following `SetFloatArray`

, `SetMatrixArray`

and `SetVectorArray`

. As expected, they are used to initialise arrays of `float`

, `Matrix4x4`

and `Vector4`

, respectively. This is a snippet on how to correctly use those functions:

float [] array = new float[] { 1, 2, 3, 4 }; material.SetFloatArray(array);

where `material`

is the Unity material that uses your shader. You can drag it directly from the inspector, or retrieving it via code:

Renderer renderer = GetComponent<Renderer>(); Material material = renderer.shaderdMaterial;

Unity 5.4 also supports global arrays. Those are properties that are set once and are then shared by all shaders. They work in a similar way, and have signatures `SetGlobalFloatArray`

, `SetGlobalMatrixArray`

and `SetGlobalVectorArray`

. However, they are static methods of the `Shader`

class.

### ⭐ Recommended Unity Assets

If you need to pass other types of arrays (such as `int`

, `long`

, `Vector3`

, …) you have to use the method that closely matches your needs. For instance, you can fit `int`

values in an array of `float`

s. Similarly, if you want to provide `Vector3`

s to your shader, you’ll need to wrap them into `Vector4`

s. You can automatically assign a `Vector3`

to a `Vector4`

, as Unity will automatically fit them in the right way, leaving the last coordinate set to zero. However, you cannot assign a `Vector3[]`

to a `Vector4[]`

.

The second consideration that you have to keep in mind it involves some poor design choices made by Unity. It seems that the first time that you use set an array (whether it’s locally or globally), Unity fixes the size of the array itself. For instance, if you initialise an array defined in the shader as `uniform float _Array[10];`

with a C# array defined as `float[] array = new float[5];`

, you will not be able to set more than 5 elements to your array. Whether this is a bug or a feature, it makes for some very nasty bugs. Waiting for this to be corrected, I advice you to initialise your arrays with the maximum size allowed, directly on the Awake function of a script:

void Awake () { material.SetFloatArray("_Points", new float[10]); }

Some users reported that once the arrays have been initialised, you need to restart the editor to be able to reset their size. Well, now you’ve been warned…

## Leave a Reply Cancel reply