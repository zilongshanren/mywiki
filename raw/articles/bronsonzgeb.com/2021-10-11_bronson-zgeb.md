---
title: Bronson Zgeb
url: https://bronsonzgeb.com/index.php/2021/10/11/custom-lighting-in-shader-graph-part-2/
author: Bronson
published: '2021-10-11'
source_blog: Bronson Zgeb
source_site: https://bronsonzgeb.com
category: game programming
fetched: '2026-04-13'
---

# Custom Lighting in Shader Graph Part 2

![Toon Link in URP with Shader Graph](../../assets/6f8275631d1a4b1f.png)

In this article, we’ll continue to improve the workflow of the [previous article](https://bronsonzgeb.com/index.php/2021/10/04/custom-lighting-in-urp-with-shader-graph/), in which we created a process for converting Shader Graphs to a custom lighting function. [The last article](https://bronsonzgeb.com/index.php/2021/10/04/custom-lighting-in-urp-with-shader-graph/) ended with a manual workflow, so we’ll fully automate the process in this post. Along the way, we’ll learn about Asset Postprocessors, Reflection and Scriptable Singletons.

## What’s the goal?

We finished the previous article with a less-than-ideal workflow for converting Shader Graphs to our custom lighting function. After saving your changes, you’d select the Shader Graph, copy the code into a buffer, then process that buffer and save it to disk as a new shader. This workflow is too tedious to be helpful when experimenting with Shader Graph. What we’re going to do now is make the entire process automatic. In other words, every time you save your Shader Graph, the converted shader will receive the updates automatically. Let’s outline the steps to accomplish this:

- Detect when the user saves a Shader Graph.
- We can use an Asset Postprocessor for this.

- Copy the code of the saved Shader Graph into a text buffer.
- Generating the code is tricky because the API is internal, so we’ll use C#’s Reflection to accomplish this.

- Pass the generated code into our pipeline.
- Save the converted shader to disk.
- We’ll cache the destination file in a Scriptable Singleton, so the user only needs to interact with the Save File Dialog the first time.


Now that we have a plan let’s get to work!

## Shader Graph Asset Postprocessor

In case you’re not familiar, Unity has an API for writing asset postprocessors. This API allows users to run custom code in the asset import pipeline. Given that every time an asset changes, it gets reimported, we’ll write a Shader Graph asset postprocessor to detect whenever a user saves a graph.

```
using System.IO;
using UnityEditor;
public class ShaderGraphModificationProcessor : AssetPostprocessor
{
static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets,
string[] movedFromAssetPaths)
{
foreach (var importedAsset in importedAssets)
{
if (Path.GetExtension(importedAsset).ToLower() == ".shadergraph")
{
var guid = new GUID(AssetDatabase.AssetPathToGUID(importedAsset));
//TODO: Convert Shader Graph
}
}
}
}
```


Here’s an asset postprocessor that will check every asset for the file extension `.shadergraph`

. You can drop this file inside your project in a folder called `Editor`

, and it’ll immediately work. Next, we’ll convert the Shader Graph to text and copy it into a text buffer.

## Convert Shader Graph to Text

I dug into Shader Graph’s code to learn how to convert graphs to text. I found a `Generator`

class that can accept a `GraphData`

object and output the generated shader as a string. Unfortunately, the APIs are all internal, so we have to use Reflection to access them.

In case you don’t know, Reflection is a way to inspect and manipulate code at runtime. It has many uses. For our purposes, we’ll use it to locate the internal methods we want to use and invoke them. On an important note, we’re about to use a lot of runtime string lookups. That means that if any of these methods change in future versions of Shader Graph, this code may stop working. In other words, using Reflection is a bit frail.

So, inside `ShaderGraphImporterEditor.cs`

, we can locate the code that runs when you press “Copy Shader” in the Inspector.

```
public override void OnInspectorGUI()
{
.
.
.
if (GUILayout.Button("Copy Shader"))
{
AssetImporter importer = target as AssetImporter;
string assetName = Path.GetFileNameWithoutExtension(importer.assetPath);
var graphData = GetGraphData(importer);
var generator = new Generator(graphData, null, GenerationMode.ForReals, assetName, null);
GUIUtility.systemCopyBuffer = generator.generatedShader;
}
.
.
.
}
```


This code uses a local function `GetGraphData`

and passes the result into a `Generator`

constructor. Then, it extracts the generated shader code and stores it in the `systemCopyBuffer`

. To replicate this, we’ll get the `ShaderGraphImporterEditor`

assembly, locate the `GetGraphData`

method and invoke it with our Shader Graph. Then, we’ll locate the `Generator`

constructor and invoke that with the `GraphData`

. Finally, we’ll find the method to access the `generatedShader`

field, invoke that, and complete this step.

This next block of code searches all the loaded assemblies for the first one of the type `UnityEditor.ShaderGraph.ShaderGraphImporterEditor`

. Then, from that assembly, we retrieve the `ShaderGraphImporterEditor`

`Type`

itself. Finally, we search the static non-public methods inside that `Type`

and find one named `GetGraphData`

. By the way, local functions are functions defined inside of methods. In this case, the local function was turned into a static method at compile-time. That’s why `GetGraphData`

is a static method; its definition is inside `OnInspectorGUI`

.

```
var shaderGraphImporterAssembly = AppDomain.CurrentDomain.GetAssemblies().First(assembly =>
{
return assembly.GetType("UnityEditor.ShaderGraph.ShaderGraphImporterEditor") != null;
});
var shaderGraphImporterEditorType = shaderGraphImporterAssembly.GetType("UnityEditor.ShaderGraph.ShaderGraphImporterEditor");
var getGraphDataMethod = shaderGraphImporterEditorType
.GetMethods(BindingFlags.Static | BindingFlags.NonPublic)
.First(info => { return info.Name.Contains("GetGraphData"); });
```


With the method located, let’s invoke it. It requires an `AssetImporter`

as an argument, though, so we’ll make one. The next block creates an `AssetImporter`

from an asset `GUID`

and invokes the `getGraphDataMethod`

with a single argument.

```
var path = AssetDatabase.GUIDToAssetPath(guid);
var assetImporter = AssetImporter.GetAtPath(path);
var graphData = getGraphDataMethod.Invoke(null, new object[] {assetImporter});
```


Next, we’ll do a similar thing for the `Generator`

. First, get the `Type`

, then the constructor method, and finally, invoke the constructor with the appropriate arguments. I copied the arguments from the `ShaderGraphImporterEditor.cs`

file above.

```
var generatorType = shaderGraphImporterAssembly.GetType("UnityEditor.ShaderGraph.Generator");
var generatorConstructor = generatorType.GetConstructors().First();
var generator = generatorConstructor.Invoke(new object[]
{graphData, null, 1, $"Converted/{shaderGraphName}", null});
```


Finally, the last step is to get the generated shader code from the `Generator`

. So again: get the `Type`

, get the method, invoke the method.

```
var generatedShaderMethod = generator.GetType().GetMethod("get_generatedShader",
BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
var generatedShader = generatedShaderMethod.Invoke(generator, new object[] { });
```


Put the whole method together, and this is what you get.

```
public static void ConvertShaderGraphWithGuid(GUID guid)
{
var path = AssetDatabase.GUIDToAssetPath(guid);
var assetImporter = AssetImporter.GetAtPath(path);
if (assetImporter.GetType().FullName != "UnityEditor.ShaderGraph.ShaderGraphImporter")
{
Debug.Log("Not a shader graph importer");
return;
}
var shaderGraphName = Path.GetFileNameWithoutExtension(path);
var shaderGraphImporterAssembly = AppDomain.CurrentDomain.GetAssemblies().First(assembly =>
{
return assembly.GetType("UnityEditor.ShaderGraph.ShaderGraphImporterEditor") != null;
});
var shaderGraphImporterEditorType = shaderGraphImporterAssembly.GetType("UnityEditor.ShaderGraph.ShaderGraphImporterEditor");
var getGraphDataMethod = shaderGraphImporterEditorType
.GetMethods(BindingFlags.Static | BindingFlags.NonPublic)
.First(info => { return info.Name.Contains("GetGraphData"); });
var graphData = getGraphDataMethod.Invoke(null, new object[] {assetImporter});
var generatorType = shaderGraphImporterAssembly.GetType("UnityEditor.ShaderGraph.Generator");
var generatorConstructor = generatorType.GetConstructors().First();
var generator = generatorConstructor.Invoke(new object[]
{graphData, null, 1, $"Converted/{shaderGraphName}", null});
var generatedShaderMethod = generator.GetType().GetMethod("get_generatedShader",
BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
var generatedShader = generatedShaderMethod.Invoke(generator, new object[] { });
WriteShaderToFile(ConvertShader((string) generatedShader), path, shaderGraphName);
}
```


The worst is over! The last line plugs this into the pipeline from the previous article. Every time you save a graph, it’ll convert it and ask you where to put it. For our final step, let’s remember where the user chooses to save their converted graph, so they only have to deal with the File popup the first time.

## Tracking file paths

The easiest way to track our file paths is through a `ScriptableSingleton`

. This object serializes to disk, so it’ll persist through domain reloads as well as closing the project. I covered `ScriptableSingletons`

in a previous article, so I’ll run through the code quickly this time. Our object will store pairs of asset GUIDs. Using the GUIDs rather than the paths will allow our system to work even if we move files.

```
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
[FilePath("Assets/CustomForwardPass/Editor/ShaderGraphConversionSettings.asset",
FilePathAttribute.Location.ProjectFolder)]
public class ShaderGraphConversionToolSettings : ScriptableSingleton<ShaderGraphConversionToolSettings>,
ISerializationCallbackReceiver
{
readonly Dictionary<GUID, GUID> _shaderPairs = new Dictionary<GUID, GUID>();
#region Serialization
[SerializeField, HideInInspector] List<string> _shaderGraphGuids;
[SerializeField, HideInInspector] List<string> _convertedGraphGuids;
#endregion
public void AddFilePair(string shaderGraphPath, string convertedShaderPath)
{
var shaderGraphGuid = new GUID(AssetDatabase.AssetPathToGUID(shaderGraphPath));
var convertedPathGuid = new GUID(AssetDatabase.AssetPathToGUID(convertedShaderPath));
if (_shaderPairs.ContainsKey(shaderGraphGuid))
{
_shaderPairs[shaderGraphGuid] = convertedPathGuid;
}
else
{
_shaderPairs.Add(shaderGraphGuid, convertedPathGuid);
}
Save(true);
}
public string GetConvertedShaderPath(string shaderGraphPath)
{
var shaderGraphGuid = new GUID(AssetDatabase.AssetPathToGUID(shaderGraphPath));
if (_shaderPairs.TryGetValue(shaderGraphGuid, out GUID convertedShaderGuid))
{
return AssetDatabase.GUIDToAssetPath(convertedShaderGuid);
}
return null;
}
public void OnBeforeSerialize()
{
_shaderGraphGuids = new List<string>();
_convertedGraphGuids = new List<string>();
foreach (var shaderPair in _shaderPairs)
{
_shaderGraphGuids.Add(shaderPair.Key.ToString());
_convertedGraphGuids.Add(shaderPair.Value.ToString());
}
}
public void OnAfterDeserialize()
{
if (_shaderGraphGuids != null)
{
for (int i = 0; i < _shaderGraphGuids.Count; ++i)
{
var _shaderGraphGuid = new GUID(_shaderGraphGuids[i]);
var _convertedGraphGuid = new GUID(_convertedGraphGuids[i]);
if (_shaderPairs.ContainsKey(_shaderGraphGuid))
{
_shaderPairs[_shaderGraphGuid] = _convertedGraphGuid;
}
else
{
_shaderPairs.Add(_shaderGraphGuid, _convertedGraphGuid);
}
}
}
_shaderGraphGuids = null;
_convertedGraphGuids = null;
}
}
```


There’s one minor caveat with this code. I’m using a `Dictionary`

to pair a Shader Graph `GUID`

to its converted shader counterpart. Since Dictionaries don’t serialize, I convert the dictionary to two lists, then convert back to a dictionary on deserialization. Now let’s jump over to the code to write the shader to a file.

```
static void WriteShaderToFile(string shader, string shaderGraphPath, string defaultFileName)
{
var filePath = "";
if (!string.IsNullOrEmpty(shaderGraphPath))
{
filePath = ShaderGraphConversionToolSettings.instance.GetConvertedShaderPath(shaderGraphPath);
}
if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath))
{
filePath = EditorUtility.SaveFilePanelInProject("Converted Shader", defaultFileName, "shader",
"Where should we save the converted shader?");
}
if (!string.IsNullOrEmpty(filePath))
{
File.WriteAllText(filePath, shader);
AssetDatabase.ImportAsset(filePath);
AssetDatabase.Refresh();
ShaderGraphConversionToolSettings.instance.AddFilePair(shaderGraphPath, filePath);
}
}
```


If a destination file doesn’t exist when we write to disk, we’ll show a save file panel for the user to choose a destination. Otherwise, overwrite the existing converted shader.

## Wrap-Up

This article covered Asset Postprocessors to detect changes in Assets, Reflection to access internal Editor APIs, and Scriptable Singletons to store information. With this automated workflow, experimenting with Shader Graph and a custom lighting function is quick and easy.

**Try out the project ****here on GitHub****. If you want to support my work, ****join my mailing list****. If you do, I’ll notify you whenever I write a new post.**