---
title: C# for scripting - runtime compilation
url: https://etodd.io/2011/12/10/c-for-scripting-runtime-compilation/
published: '2011-12-10'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# C# for scripting - runtime compilation

I set out to add scripting support to Project Lemma the other day. End result: I can recompile C# scripts on the fly and cache the bytecode in DLLs. The best part: there's no special binding code, and no performance hit.

There are a lot of .NET scripting solutions out there. Here's a few I found in my research:

[IronPython](http://www.voidspace.org.uk/ironpython/hosting_api.shtml). Fully dynamic, kinda slow. Requires marshalling of some kind between the script world and .NET.[CSScript](http://www.csscript.net/). Very well supported, includes Visual Studio extensions and shell extensions. Compiles C# to bytecode at runtime, with caching. Scripts cannot be changed once loaded.[Lua](http://www.lua.org/). The industry standard in scripting. From what I understand, a little challenging to get working with .NET.

I decided to try out C# runtime compilation. Really, C# is the best scripting language I could ask for. If I succeeded, I could keep writing the same code I've been writing, but I could recompile it and see it in action with a keystroke instead of restarting the game!

## Setup

I started by writing a ScriptBase class that every script would inherit from.

```
public class ScriptBase
{
public static Main main;
protected static Entity get(string id)
{
return ScriptBase.main.GetByID(id);
}
}
```


"Main" is my main game class. The "get" function is a utility function I wanted to provide for the scripting environment. Using the ScriptBase class, I can add utility functions that can speed up the scripting process.

Next, I wrote a prefix and postfix for the script files. This will help the scripts actually look like scripts, i.e. not object oriented, pretty much just a list of statements to execute in order.

```
private const string scriptPrefix =
@"
using System;
using Microsoft.Xna.Framework;
// ...
namespace Lemma.Scripts
{
public class Script : ScriptBase
{
public static void Run()
{
";
private const string scriptPostfix =
@"
}
}
}
";
```


The idea is: compile the assembly, reflect it and get the Script type, then call the static Run function on it. Like so:

```
Type t = assembly.GetType("Lemma.Scripts.Script");
t.GetField("main", BindingFlags.Static | BindingFlags.Public | BindingFlags.FlattenHierarchy)
.SetValue(null, this.main);
this.scriptMethod = t.GetMethod("Run", BindingFlags.Static | BindingFlags.Public);
this.scriptMethod.Invoke(null, null);
```


## Compile some scripts already!

This code isn't particularly interesting, but I'll provide it for reference:

```
string scriptPath = ...;
string binaryPath = ...;
try
{
Assembly assembly = null;
using (Stream stream = TitleContainer.OpenStream(scriptPath))
using (TextReader reader = new StreamReader(stream))
{
CodeDomProvider provider = CodeDomProvider.CreateProvider("CSharp");</p>
CompilerParameters cp = new CompilerParameters
{
GenerateExecutable = false,
GenerateInMemory = false,
TreatWarningsAsErrors = false,
OutputAssembly = binaryPath
};
// Add references to all the assemblies we might need.
Assembly executingAssembly = Assembly.GetExecutingAssembly();
cp.ReferencedAssemblies.Add(executingAssembly.Location);
foreach (AssemblyName assemblyName in executingAssembly.GetReferencedAssemblies())
cp.ReferencedAssemblies.Add(Assembly.Load(assemblyName).Location);
// Invoke compilation of the source file.
CompilerResults cr = provider.CompileAssemblyFromSource(cp, Script.scriptPrefix + reader.ReadToEnd() + Script.scriptPostfix);</p>
if (cr.Errors.Count > 0)
{
// Display compilation errors.
StringBuilder builder = new StringBuilder();
foreach (CompilerError ce in cr.Errors)
{
builder.Append(ce.ToString());
builder.Append("\n");
}
this.Errors.Value = builder.ToString();
}
else
assembly = cr.CompiledAssembly;
}
}
catch (Exception e)
{
this.Errors.Value = e.ToString();
}
```


The goal here is to compile the script to a DLL so the next time the game runs, I could check if it already exists and just load the DLL instead of recompiling. You can do this with the CompilerParameters object, by setting GenerateInMemory to false and OutputAssembly to the path of the DLL you want to save.

## Recompiling scripts on the fly

Now the problem is, once we load the DLL, the .NET runtime locks the file until the program exits. There's no way to unload the library and unlock the file, unless we put it in a different AppDomain, which means we have to marshal data back and forth between the script and game, which defeats the purpose.

Since one of our requirements is being able to recompile the script without restarting the game, we need to find a way to load the DLL without locking the file. Enter [shadow copying](http://msdn.microsoft.com/en-us/library/ms404279.aspx). You can tell the .NET runtime to make a copy of every assembly it loads, and load the "shadow copy" instead of the real file. That leaves the original DLL free for us to rewrite. Great, so let's just enable shadow copying and we're done.

Unfortunately, life is never that easy. You can't enable shadow copying for an AppDomain once the domain has been created. You have to create a new AppDomain with the settings you want. Solution: create a tiny launcher executable that creates an AppDomain with shadow copying enabled, and then executes our game in that AppDomain. Here's the code:

```
public static void Main(string[] args)
{
string baseDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
AppDomainSetup setup = new AppDomainSetup();
setup.ShadowCopyFiles = "true";
setup.ApplicationBase = baseDirectory;
setup.PrivateBinPath = baseDirectory;
AppDomain domain = AppDomain.CreateDomain("", AppDomain.CurrentDomain.Evidence, setup);
domain.ExecuteAssembly(Path.Combine(baseDirectory, "Lemma.exe"), args);
}
```


Note: the AppDomainSetup.ShadowCopyDirectories property lets you provide a list of directories to limit the use of shadow copying. I tried to use it to specify that only the script DLLs be shadow copied, but it didn't work. YMMV.

Okay, so I fired up my game, compiled the script, went to delete the compiled DLL, annnnnd... still locked! What's going on?

I did some reflecting and found out the C# runtime compiler is kinda janky. It isn't, like I assumed, a .NET wrapper around some kind of compiler library. Instead, it actually invokes the C# compiler executable, then loads the resulting DLL. If you specify GenerateInMemory = true, it invokes the compiler with a temporary DLL file path and loads the temp file into memory.

Furthermore, it doesn't shadow copy the DLL when it loads it, even if the AppDomain is configured to do so. I'm guessing this is because it uses a different Assembly.Load function... don't quote me but I believe Assembly.LoadFile **does not** shadow copy files, while Assembly.LoadFrom **does**.

Anyway, to solve this, we can take advantage of the compiler's quirky nature here by **not** specifying an output assembly path. That will cause the compiler to generate a temporary file path for the output assembly. So it will still lock the DLL, but we don't care, because it's a temp file. Luckily, we can still read the DLL even though it's locked, so we can copy it to the path we originally wanted for later use.

Here's the modifications to our original compilation code:

```
CompilerParameters cp = new CompilerParameters
{
GenerateExecutable = false,
GenerateInMemory = false,
TreatWarningsAsErrors = false,
};
// ...
assembly = cr.CompiledAssembly;
File.Copy(cp.OutputAssembly, binaryPath, true);
```


The next time we load the script, we'll see the DLL at binaryPath and load it. But it will be automatically shadow copied. Mission accomplished!

## Conclusion

One disadvantage to this approach is that when you recompile a script, the old assembly remains in memory, and the temp DLL file will remain locked until the game exits. Like I said, there's no way to unload an assembly from a running AppDomain, and we don't want to put the scripts in another AppDomain. Luckily most script assemblies should be pretty small, and we'll only be recompiling scripts in the editor, not the final game. I can live with that.

I'm still in the middle of all this, but I thought I'd share what I've learned about .NET in the meantime. Might be useful if you're thinking about doing something similar. Here's two StackOverflow threads that helped me through this process:

[Recompiling code without AppDomains](http://stackoverflow.com/questions/1353456/recompile-c-sharp-while-running-without-appdomains)[Discussion about different .NET scripting solutions - lots of links](http://stackoverflow.com/questions/1067784/c-net-scripting-library)

Thanks for reading!