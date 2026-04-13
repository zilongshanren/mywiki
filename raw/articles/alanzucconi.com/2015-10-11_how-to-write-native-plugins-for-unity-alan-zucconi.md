---
title: How to Write Native Plugins for Unity - Alan Zucconi
url: https://www.alanzucconi.com/2015/10/11/how-to-write-native-plugins-for-unity/
author: Alan Zucconi
published: '2015-10-11'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Unity has the ability to import pieces of code written (and compiled) in other languages; they are called **Native Plugins**, and this tutorial will teach you how to build them.

- Step 1:
[Creating a C++ project](https://www.alanzucconi.com#step1) - Step 2:
[Writing the library](https://www.alanzucconi.com#step2) - Step 3:
[Compiling](https://www.alanzucconi.com#step3) - Step 4:
[Importing in Unity](https://www.alanzucconi.com#step4) - Step 5:
[Using in Unity](https://www.alanzucconi.com#step5) [Conclusion](https://www.alanzucconi.com#step6)

Source codes:

[Visual Studio 2015 C++ project](https://drive.google.com/file/d/0B4nCcaMlgxV2aDk3NjVSUU5kZ2M/view?usp=sharing)(DLL source code)[Unity package](https://drive.google.com/file/d/0B4nCcaMlgxV2dVFKVFM5eXdaR3c/view?usp=sharing)(including the DLL)

#### Managed and unmanaged plugins in Unity

Connecting different piece of code is not something which Unity invented. If you are a Windows user, is very likely you might have heard of DLLs, an acronym which means **Dynamic Link Libraries**. Similarly to standalone applications, they are compiled softwares. Unlike them, however, they cannot be executed directly since they are designed specifically to be used by other applications.

Unity supports two types of plugins: **managed** and **unmanaged**. The former are piece of code written in C# and compiled into a bytecode language called Common Intermediate Language (CIL). Managed plugins are as powerful as C# scripts, with the advantage of having their source codes compiled. Unmanaged (or native) plugins, instead, are piece of software written in other languages, typically C++. There are no constraints on what they can do, and since they are compiled in machine code they tend to be much faster than traditional scripts.

For this tutorial I will use Visual Studio 2015; as long as you know how to compile C++ code, you can chose whichever IDE you want. The first step to create an unmanaged C++ library is to create a project for it. Open Visual Studio, go to **File | New Project** and select **Visual C++ | Win32 Console Application**.

![01](../../assets/4eba1cdbd2477c6b.png)

After choosing a name for the project (TestDLL in this example), make sure to select **DLL** under **Application type**, and **Empty project** under **Additional options**.

![02](../../assets/6ca796914e890f10.png)

The Visual C++ solution is now ready and we can start writing our code.

![03](../../assets/0ca644da38976d72.png)

C++ code is generally split in two files. The functions definitions (called *header*) and their actual implementation (called *body*). While the body is written into *.cpp* files inside the folder **Resource files**, headers goes into **Header Files** and have extension *.h*. For this solution we will create a header and a body; the latter will contain all the functions we want to store in our DLL. You can create a file by right clicking in the relative folder, then selecting **Add | New Item**.

#### The body: TestDLLSort.cpp

Let’s start with the code that sorts our array.

#include "TestDLLSort.h" #include <algorithm> extern "C" { void TestSort(int a[], int length) { std::sort(a, a+length); } }

**Lines 5-7** uses the `std:sort`

function from the `algorithm`

library to sort the array. If you are familiar with C++11, this should be nothing new. The only addition is the `extern "C"`

block, which is necessary to export the references to `TestSort`

into the DLL.

#### The header: TestDLLSort.h

The definition of the body must be complete with a header. It has to contain the *prototype* of `TestSort`

, which is the *signature* of the function.

#define TESTDLLSORT_API __declspec(dllexport) extern "C" { TESTDLLSORT_API void TestSort(int a[], int length); }

The remaining code is necessary to create the DLL. The name `TESTDLLSORT_API`

is arbitrary and is used to mark all the functions exported. In more sophisticated pieces of software, `TESTDLLSORT_API`

should be binded to `__declspec(dllimport)`

depending on the situation. But in this toy example, this is not necessary.

The final step to complete in Visual Studio for our DLL is now to compile it. Make sure that your target is set to **Release** for the right platform (32bit or 64bit). Then, select **Build | Build Solution**.

![04](../../assets/af318b9f5e35471e.png)

On the bottom of the screen, you’ll see an output log on the console. It should look like this:

1>------ Rebuild All started: Project: TestDLL, Configuration: Release x64 ------ 1> TestDLLSort.cpp 1> Creating library C:\Users\Alan Zucconi\Documents\Visual Studio 2015\Projects\TestDLL\x64\Release\TestDLL.lib and object C:\Users\Alan Zucconi\Documents\Visual Studio 2015\Projects\TestDLL\x64\Release\TestDLL.exp 1> Generating code 1> All 30 functions were compiled because no usable IPDB/IOBJ from previous compilation was found. 1> Finished generating code 1> TestDLL.vcxproj -> C:\Users\Alan Zucconi\Documents\Visual Studio 2015\Projects\TestDLL\x64\Release\TestDLL.dll ========== Rebuild All: 1 succeeded, 0 failed, 0 skipped ==========

If you are experiencing a warning such as `warning C4273: inconsistent dll linkage`

, there might be ambiguity between the usage of `__declspec(dllimport)`

and `__declspec(dllexport)`

. If you are just trying to create a native plugin for Unity, stick with the latter.

![05](../../assets/d70a638dc6c68de3.png)

Following the previous compilation log, explore the project folders to find the compiled DLL. In this case it it placed in the folder **x64\Release**. This is the only file you need. The first step to make it work into Unity is to copy it with a folder called **Plugins**.

Native plugins are typically bounded to a specific OS or platform. You can use the Inspector to make sure each DLL is included in the right build.

Once imported, using a DLL is relatively simple. The first step is to define its *entry point*, which is done using the `DLLImport`

annotation. You need to specify the name of the DLL and the name of the function. It is then given an *alias*, which can be invoked like any other function.

using UnityEngine; using System.Runtime.InteropServices; public class TestDLL : MonoBehaviour { // The imported function [DllImport("TestDLL", EntryPoint = "TestSort")] public static extern void TestSort(int [] a, int length); public int[] a; void Start() { TestSort(a, a.Length); } }

The string used in `EntryPoint`

must match with the name used in the C++ library. However, you can call the function in the line below the way you want; this is how C# will call it from now on.

You should notice that Unity cannot check unmanaged DLLs in the editor; you’ll have to run the game to check whether the linkage has been successful or not. This is not the case with managed DLLs, which can be checked statically.

Native plugins are extremely important and can play a vital role in the development of your game. Their most significant advantage is the speed. While C# scripts are translated CIL, Unmanaged DLLs are compiled in machine code. You can try yourself by benchmarking the DLL created in this test. Sorting an array of 1000000 elements takes approximately 480ms with `Array.Sort`

, but only 65 with `std::sort`

. This is seven times faster! If your game has some heavy simulations (such as fluid dynamics or heavy AI stuff) you should consider moving that part of code in a C++ library.

#### Other resources

[Native plugins for Mac](http://unreferencedinstance.com/tutorial_cpp_unity3d/): a detailed article which covers most of the content here presented, but oriented for Mac developers;[Unity and DLLs](http://ericeastwood.com/blog/17/unity-and-dlls-c-managed-and-c-unmanaged): a tutorial to create managed (C#) and unmanaged (C++) plugins for Unity;[Writing plugins](https://unity3d.com/learn/tutorials/modules/beginner/live-training-archive/writing-plugins): an official video tutorial from Unity to create your first plugin with Visual Studio.

## Leave a Reply Cancel reply