---
title: Console debugging in Unity made easy - Alan Zucconi
url: https://www.alanzucconi.com/2015/08/26/console-debugging-in-unity-made-easy/
author: Alan Zucconi
published: '2015-08-26'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

One of the most interesting feature of Unity is the ability to extend its editor and standard components. This has allowed developers all around the world to create amazing extensions which dramatically improve Unity’s usability. And, in some cases, compensate for its shortages. A very intriguing feature which is not-so-well known is the ability to customise the messages in the debug console. Rather than give you a self proclaimed *ultimate* solution to console debugging, this post will cover different topics to help you creating your own.

### Rich Text support for Debug.Log

The standard logging function provided by Unity is `Debug.Log`

. As reported in its [documentation](http://docs.unity3d.com/ScriptReference/Debug.Log.html), it supports rich text tags. So, for instance:

Debug.Log("This is <color=red>red</color>!");

![a1](../../assets/68aa4515d71a059c.png)

Adding the `<color=red>`

tag does the trick. Unity supports `<i>`

for italic, `<b>`

for bold and `<size>`

to change the pixel size. We will see later how to improve `Debug`

even further.

For a full list of the supported colours, you can check [this page](http://docs.unity3d.com/Manual/StyledText.html).

### A better debug function

Something which bothers me deeply is the way the `Debug.Log`

function has to be fed. There are two main problems here: (1) `Debug.Log`

takes a single string and (2) its console output is quite chunky and doesn’t really allow for multi-lines. Let’s see what we can do about these things.

using System.Text; public static string Log (params object [] data) { StringBuilder sb = new StringBuilder(); for (int i = 0; i < data.Length; i++) { sb.Append(data[i].ToString()); sb.Append("\t"); } string s = sb.ToString(); Debug.Log(s); return s; }

The code above allows to use the newly debug function by passing a list of objects without getting worried about spacing and casts:

int length = 3; float average = 10.5f; // Old log Debug.Log("The object is " + this + " it has " + length + " elements and an average of " + average + " points"); // New log Log("The object is", this, "it has", length, "elements and an average of", average, "points");

### Retrieving caller information

The most useful feature of the Debug.Log function is that it explicitly tells the file and line of code which has generated it. .NET allows to retrieve the [caller information](https://msdn.microsoft.com/en-us/library/hh534540.aspx) by using the following syntax:

public function CallerInformation ( [System.Runtime.CompilerServices.CallerMemberName] string memberName = "", [System.Runtime.CompilerServices.CallerFilePath] string sourceFilePath = "", [System.Runtime.CompilerServices.CallerLineNumber] int sourceLineNumber = 0) { Debug.Log("Function: " + memberName + ", File: " + sourceFilePath + ", Line: " + sourceLineNumber); }

Unfortunately, I did not manage to get `Caller`

s annotations to work within Unity. An alternative, yet slower approach is to use the `Diagnostic`

class which allows to look inside the current [stack trace](https://msdn.microsoft.com/en-us/library/system.diagnostics.stacktrace(v=vs.85).aspx):

using System.Diagnostic; StackTrace stackTrace = new StackTrace(); StackFrame frame = stackTrace.GetFrame(1); // The caller frame string methodName = frame.GetMethod().Name; // Method name string fileName = frame.GetFileName(); // File name string lineNumber = frame.GetFileLineNumber(); // Line number

### Editor GUI

The rich text formatting is available on the majority of Unity elements. Including its GUI. Le’t say, for instance, that we want to extend the inspector of an already existing component. This will be expanded in a further tutorial, but let’s just say for now that all you have to do is to put this script in a folder called `Editor`

:

using UnityEngine; using UnityEditor; [CustomEditor(typeof(Camera))] public class CameraEditor : Editor { public override void OnInspectorGUI() { Camera myTarget = (Camera) target; GUIStyle style = new GUIStyle(); style.richText = true; GUILayout.Label("<size=30>This is a <color=yellow>CUSTOM</color> text</size>", style); this.DrawDefaultInspector(); GUILayout.Label("<size=30>This is a <color=red>CUSTOM</color> text</size>;", style); }

While `DrawDefaultInspector`

draws the inspector for the current object, `GUILayout.Label`

adds a text to it. By creating a `GUIStyle`

object with the `richText`

parameters set to `true`

, we can draw some formatted text:

![a2](../../assets/5e1b10b912af6731.png)

### Other resources

[DebugConsole](http://wiki.unity3d.com/index.php?title=DebugConsole): a scrolling, interactive debug console that you can use directly in your games;[mminer Console](https://gist.github.com/mminer/975374): another script for in-game console;[WWDebugWindow](https://github.com/kreso22/Unity-3D-Debug-console-with-color.): a simple, yet powerful script to write to the console;[Pimp my Debug.Log:](http://www.tallior.com/pimp-my-debug-log/)an interesting set of method extensions for the string class, perfect for`Debug.Log`

.

## Leave a Reply Cancel reply