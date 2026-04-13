---
title: Workaround for client-side Blazor localization with .resx
url: https://gametorrahod.com/workaround-for-client-side-blazor-localization-with-resx/
author: Sirawat Pitaksarit
published: '2019-10-11'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

You can find ASP.NET localization solution on the net, which Microsoft provided `using Microsoft.Extension.Localization`

with some services like `IStringLocalizer`

. But that's for server side application, the client is expected to connect to this localizer with an HTTP header containing his language of choice and the server then decide which localized content to give back.

Blazor is strong because of WASM client side possibility. We don't need a server that know how to run ASP.NET C# code running anymore. This way we can upload the web to a simple host like Firebase Hosting which just distribute files, and benefit from its flexible worldwide CDN. There are problems I found trying to make localization works for client side.

You can checkout [this solution from j_sakamoto](https://dev.to/j_sakamoto/how-to-localize-texts-in-your-blazor-app-phn) as well. In this article instead I will try to keep using what Visual Studio provide ( `.resx`

and code gen, without modifying Blazor build process, etc.)

## How things normally should work

`.resx`

file contains key value pair of things in "neutral culture". The value part can be a simple `string`

or even binary data like images.

![](../../assets/7d1bb81514ab9e6b.png)

![](../../assets/34babc193e4f9001.png)

![](../../assets/ebe38a480b76afe1.png)

You copy paste to an another `.resx`

file with the same name, but added culture code before the extension like this `MyResource.th-TH.resx`

or `MyResource.ja.resx`

. There is no mechanism to maintain the fact that all variants still have the same key as the main one. I think this is one of a weakness of `.resx`

based localization. Anyways, it will try to fallback to the neutral one.

### .resx to .resources to .dll

`.resx`

won't be in your final product. Instead, this option on all `.resx`

will make sure they are embedded in the `.dll`

as `.resources`

.

Click on the top project name in the tree to see the `.csproj`

file. This is a part of input for `msbuild`

, the other parts lies in `Sdk=Microsoft.NET.Sdk.Web`

. I recommends [this excellent series](https://remibou.github.io/tags/#Blazor+internals+serie) if you want to know more about it.

Our resource files must be somewhere here or else they are not related to the build.

![](../../assets/fd258c8228b2a01b.png)

`EmbededResource`

is the command we are looking for. [Here](https://docs.microsoft.com/en-us/visualstudio/msbuild/common-msbuild-project-items?view=vs-2019#embeddedresource) is its documentation from msbuild.

Note that msbuild has `GenerateResource`

that is more directly to transform `.resx`

file into `.resource`

and stop there. But using `EmbededResource`

is like doing both `.resource`

to the linking `dll`

step. (Details : [https://docs.microsoft.com/en-us/visualstudio/msbuild/how-to-build-a-project-that-has-resources?view=vs-2019](https://docs.microsoft.com/en-us/visualstudio/msbuild/how-to-build-a-project-that-has-resources?view=vs-2019))

For individual tools that perform this task, you can use

and [resgen](https://docs.microsoft.com/en-us/dotnet/framework/tools/resgen-exe-resource-file-generator)

from command line.[Al](https://docs.microsoft.com/en-us/dotnet/framework/tools/al-exe-assembly-linker)

Also it corresponds to "Embedded resource" on the properties, you don't have to edit the `.csproj`

.

![](../../assets/925c426bf5e5c0d3.png)

### The satellite assembly

![](../../assets/07ac26df5f4629ac.png)

I have included some localized images in my `.resx`

file. It is expected that the 201KB size is because of included images. This bloated 201KB is the proof that my `.resources`

generated from `.resx`

is indeed inside this.

To confirm I can change from `EmbededResource`

to just `Resource`

. You can do it on the Property panel and it will be reflected in `.csproj`

.

![](../../assets/b18d68e2e688f1a9.png)

![](../../assets/55faf0638b44fb21.png)

![](../../assets/c13f52a5e6de49d4.png)

![](../../assets/59f29d7344651553.png)

Size of `dll`

reduced to just 15KB, and as expected it is now an error since there is no neutral resource in the main `dll`

anymore.

Notice an another folder `th-TH`

. It know to generate a separated folder to house what Microsoft called "[sattellite assembly](https://docs.microsoft.com/en-us/dotnet/framework/resources/creating-satellite-assemblies-for-desktop-apps?redirectedfrom=MSDN)". ([more](https://docs.microsoft.com/en-us/dotnet/framework/resources/#packaging-and-deploying-resources) [here](https://docs.microsoft.com/en-us/dotnet/framework/resources/packaging-and-deploying-resources-in-desktop-apps)) The point is that we can update the localized content without touching the main `dll`

. The `DuelOttersWebsite.dll`

outside is called neutral resource. The ~200KB size again is indeed indicating that my Thai-localized image is included. Combined with the neutral one outside I am sure I have both version of the image.

![](../../assets/8fb653fc9ac3c50f.png)

### ResourceManager

Now we need a way to get those `.resources`

out from `.dll`

. `ResourceManager`

is a class which [its constructor](https://docs.microsoft.com/en-us/dotnet/api/system.resources.resourcemanager.-ctor?view=netframework-4.8) accepts an `Assembly`

or `Type`

. After creating one, we can use `string`

key along with `CultureInfo`

to get the right resource according to localization.

It could use [11 steps of fallback process](https://docs.microsoft.com/en-us/dotnet/framework/resources/packaging-and-deploying-resources-in-desktop-apps#the-resource-fallback-process) to look for the correct culture for us. In this case if I ask with`fooBar`

key with `CultureInfo.GetSpecificCulture("th-TH")`

to

, it could first look for [GetString(String, CultureInfo)](https://docs.microsoft.com/en-us/dotnet/api/system.resources.resourcemanager.getstring?view=netframework-4.8#System_Resources_ResourceManager_GetString_System_String_System_Globalization_CultureInfo_)`.resources`

in the `.dll`

inside `th-TH`

folder then fallback to the neutral one.

### Static access code generation

But we don't even have to instantiate that `ResourceManager`

class. In the neutral `.resx`

file, choose Access Modifier to enables code generation. The generated file will already have correct usages of `ResourceManager`

, cached statically in the generated class.

![](../../assets/595a6bc75ed8f33e.png)

Note how Solution Explorer know to nest the generated class under the `.resx`

file for organization.

![](../../assets/13810217fdb44b88.png)

Also non-string value already have a correct returns. For example, that `GameLogo`

returns `byte[]`

because it is an image.

![](../../assets/e46616abb4660d3c.png)

Also you don't codegen on the language variant of `resx`

, do it on **only the main one**. It will error if you do but honestly I don't know what it meant.

![](../../assets/346de91c6b6bf48f.png)

Each term is using `CultureInfo`

which is overridable in the generated class, so even with one generated class from the neutral culture we should be able to make it arrive at a specific localization.

![](../../assets/a9d0ce1fc144d09c.png)

You can perform this codegen manually with `str`

option on the `resgen`

introduced earlier. It could also generate a class of JavaScript or C++ as well.

## Problems

It looks like we got everything ready, but if you build a Blazor client side app and try using the statically generated class to access localized resource (After overriding to preferred `CultureInfo`

), I found that it always fall back to neutral resource no matter what `CultureInfo`

I use.

My guess is that this setup should work in server environment, but since this is Blazor client side, it doesn't know how to copy the sattelite assembly to the final package. There is just the mail `dll`

with neutral resources there.

My guess came from looking at the `dist`

folder where we will upload to Firebase at the last step. There is your `dll`

inside `_framework`

and I cannot see the satellite assembly here for some reason. Only the neutral one. The size is 200KB, that means all my neutral terms and logo should be there but not the localized ones.

![](../../assets/ed53a2f4a3641334.png)

I have tried manually copy the `th-TH`

folder with satellite assembly to here but the program still cannot fallback resource properly. I guess in Blazor build process (which should be hard to interfere), it already links all the `dll`

to be ready for web assembly (statically?) and therefore any `dll`

added later have no effect.

At this point I don't know where to look other than tracing the compilation of Blazor. (which I recommends [this excellent series](https://remibou.github.io/tags/#Blazor+internals+serie)) For now, I think it is time to fallback to other appraoches.

### Failed approaches

First I tried using `resgen`

manually to go to just `.resources`

, and then copy all that to `wwwroot`

where it would be available at deployment. Also I disabled the built-in static class generator in Visual Studio and instead use the same functionality from `resgen`

.

![](../../assets/1311d5fc209ac847.png)

Integrated task runner includes Grunt and Gulp. ([https://devblogs.microsoft.com/aspnet/task-runners-in-visual-studio-2015/](https://devblogs.microsoft.com/aspnet/task-runners-in-visual-studio-2015/)) but since our tasks mainly deal with command line executables like `resgen`

, I used this plugin :

It allow us to write `.cmd`

then make it visible on Task Runner Explorer, so we could double click and run it as often as we want. Also I go edit the PATH environment variable to include the folder with `ResGen.exe`

to make my command able to just type `resgen`

.

```
resgen @ResponseFile.rsp
resgen /useSourcePath /str:cs Resources/LocalizationResource.resx
copy .\Resources\*.resources .\wwwroot\resources\
```


- The first line is blank because it output funny error if I don't. (??)
- First command use the "response file" (rsp) feature of
`resgen`

. Basically it is a list of commands. In there I do this :

```
/useSourcePath
/compile
Resources\LocalizationResource.resx
Resources\LocalizationResource.th-TH.resx
Resources\LocalizationResource.ja.resx
```


The output `.resources`

files will be in the same folder as `resx`

. We cannot use output path, so we need an another command to copy them.

- The 2nd command use
`/str`

option to generate a static class. It cannot be in the same`rsp`

because`/compile`

prevents all other commands and just accept a list of files from that point on. There is no need to move the generated class anywhere. - The final command copy the generated
`resources`

to`wwwroot`

.

After running thid `cmd`

via task runner, this is the result. I have highlighted related file on the solution explorer.

![](../../assets/e6bb649c4209f450.png)

Notice how generated static class wraps differently, it now encapsulates all my cultures not just the neutral one like when I was using the built-in generator.

Except, I forgot that `wwwroot`

is kinda server side. Available for request from HTML generated from Razor, but C# code `ResourceManager`

that I planned to use folder-based `.resources`

with

, could not get to them. Because the definition of "folder" for [ResourceManager.CreateFileBasedResourceManager](https://docs.microsoft.com/en-us/dotnet/api/system.resources.resourcemanager.createfilebasedresourcemanager?view=netframework-4.8)`resourcePath`

argument must be relative to the "current directory". What is a current directory for client side Blazor running in WASM and how could I get to `wwwroot`

from there? Honestly I don't know. Debugging `Directory.GetCurrentDirectory`

returns just `/`

with zero files when debugged again with `Directory.GetAllFiles`

. I was at wit's end and decided to keep the existing `dll`

pipeline as much as possible.

In a solution like j_sakamoto's [blog](https://dev.to/j_sakamoto/how-to-localize-texts-in-your-blazor-app-phn), the final result `.json`

could be put in `wwwroot`

. C# code could access it [by using HttpClient](https://github.com/jsakamoto/Toolbelt.Blazor.I18nText/blob/master/Toolbelt.Blazor.I18nText/I18nText.cs#L190) to access what is in the

`wwwroot`

shortly after app start. Then from that point it's all client side. We may be able to do the same to get `.resources`

from `wwwroot`

, but we then need to go deeper than `ResourceManager`

. We need to create a custom `IResourceReader`

that take a `resources`

stream from `wwwroot`

's content, which gives `ResourceSet`

to `ResourceManager`

. I decided I want to do something simpler that still keep those `.resources`

in the `dll`

.

### What to fix, what to keep

- Do not have to modify Blazor build process. This means we are stuck with "only main
`dll`

rules" somewhere inside. - Do not have to copy paste any resource manually, that means I prefer everything packed in the main
`dll`

. This may be a problem with bigger apps, but those kind of app should not do a pure client-side WASM Blazor in the first place I think. - Make all other languages packed in the main
`dll`

instead of as a satellite assembly, so they all go together to the client side Blazor app. Way to do this is simply stop using the smart suffix`.th-TH.resx`

and use something else so Visual Studio see it as a completely different resource, not a culture variant. A new problem is then`ResourceManager`

stopped seeing them as a culture variants and still cannot fallback properly. - I would like to keep using the generated class from
`resx`

, I would like to use this and have it regenerate as a part of Visual Studio tooling. - The
`ResourceManager`

inside that generated class is now wrong, since all our languages are now a completely unrelated resource. - Our next target is to
**hack**this`ResourceManager`

so it knows how to look for other`.resources`

according to the incoming`CultureInfo`

.

## A custom ResourceManager

It's a shame that the generated class is not a `partial`

, but we still can modify it from outside with reflection. Look at this `ResourceManager`

getter used internally in the static class. It has an underlying `resourceMan`

which will be created if it is `null`

. Therefore, if we plug a new one before it did, we can override it with a custom `ResourceManager`

that loads differently.

![](../../assets/d8d6a4932fd6520a.png)

In an attempt to prevent satellite assembly, I have changed all my `.resx`

extension to use `_`

instead.

![](../../assets/b549c24c696cb027.png)

`dll`

increasing from 200KB to about 600KB says that all languages are now together in my main `dll`

. I have 3 languages.

![](../../assets/b1b0778d614551af.png)

Next, we have to make our new "`ClientSideResourceManager`

" (that will be my class name) understand that these 3 separated resources entries are infact related. The resource are named with the assembly name, it's folder as its namespace, then finally the file name suffixed with `.resources`

.

```
DuelOttersWebsite.Resources.LocalizationResource.resources
DuelOttersWebsite.Resources.LocalizationResource_ja.resources
DuelOttersWebsite.Resources.LocalizationResource_th-TH.resources
```


Here's the final custom `ResourceManager`

.

```
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Resources;
using System.Threading.Tasks;
namespace DuelOttersWebsite.Resources
{
/// <summary>
/// A resource manager that knows how to look for a seemingly different resources in the same assembly as the neutral one,
/// and count them as its culture variants.
/// </summary>
/// <remarks>
/// You must follow the naming convention of resources packed in the dll as follows for them to count as the same set :
///
/// MyResource.resources
/// MyResource_ja.resources
/// MyResource_th-TH.resources
///
/// We use underscore instead of . to prevent Visual Studio from making a satellite assembly.
/// </remarks>
public class ClientSideResourceManager : ResourceManager
{
/// <summary>
/// <see cref="ResourceReader"/> need to create a read stream from assembly manifest to get to the .resources file.
/// </summary>
private Assembly NeutralResourceAssembly { get; }
/// <summary>
/// The full resource file name to use when no any other specific <see cref="CultureInfo"/> matches.
/// </summary>
private string NeutralResourceName { get; }
/// <summary>
/// <see cref="CultureInfo"/> is hash-equal when its culture is the same even if they are of different class instance.
/// </summary>
private Dictionary<CultureInfo, string> cultureInfoToResourceName = new Dictionary<CultureInfo, string>();
/// <param name="asm">A single assembly to search for the neutral resource and all other culture variants.</param>
/// <param name="resourceBaseName">
/// Put a name of neutral resource that will be in the .dll without .resources here.
///
/// If you use "Embedded resource" feature in Visual Studio, the name will be generated according to where
/// your .resx file is. Each folder hierarchy added a dot leading to the file name. But you can also change that
/// (https://blogs.msdn.microsoft.com/msbuild/2005/10/06/how-to-change-the-name-of-embedded-resources/)
///
/// This will be used to derive the name of other culture variants. This base name should contains no _ character.
/// </param>
public ClientSideResourceManager(Assembly asm, string resourceBaseName) : base()
{
this.NeutralResourceAssembly = asm;
string neutralResourceTypeName = resourceBaseName;
string[] names = NeutralResourceAssembly.GetManifestResourceNames();
bool foundNeutral = false;
foreach(var n in names)
{
Console.WriteLine(n);
if(n.Contains(neutralResourceTypeName))
{
//Try to extract the culture code part.
//This algorithm is quite crude but did the job.
int underscoreIndex = n.IndexOf("_");
if (underscoreIndex == -1)
{
this.NeutralResourceName = n;
foundNeutral = true;
}
else
{
//Get the code path with .resx, then remove the .resx and we got the code part only.
string code = (n.Split('_')[1]).Split('.')[0];
cultureInfoToResourceName.Add(CultureInfo.CreateSpecificCulture(code), n);
}
}
}
if(!foundNeutral)
{
throw new Exception("You should include a neutral culture resource of the name " + neutralResourceTypeName + ".resources");
}
}
/// <summary>
/// A utility class to instatiate this <see cref="ClientSideResourceManager"/> instance,
/// and put it in place of the default one in the generated static class from .resx file.
/// So you can continue using the generated class, and get correct culture fallback at client side power
/// from <see cref="ClientSideResourceManager"/> at the same time.
/// </summary>
/// <param name="classType">Class type of the generated class from .resx file.
/// Be sure to generate from only the neutral one.</param>
public static void HackResourceClass(Type classType)
{
var newRm = new ClientSideResourceManager(classType.Assembly, classType.FullName);
var fieldToHack = typeof(LocalizationResource).GetField("resourceMan", BindingFlags.Static | BindingFlags.NonPublic);
fieldToHack.SetValue(null, newRm);
}
/// <summary>
/// We have cached all possible names at constructor.
/// </summary>
protected override string GetResourceFileName(CultureInfo cultureInfo)
{
if(cultureInfoToResourceName.TryGetValue(cultureInfo, out var fileName))
{
return fileName;
}
else
{
return this.NeutralResourceName;
}
}
/// <summary>
/// Dispose it too!
/// </summary>
private IResourceReader GetReaderForCulture(CultureInfo cultureInfo)
=> new ResourceReader(NeutralResourceAssembly.GetManifestResourceStream(GetResourceFileName(cultureInfo)));
/// <summary>
/// It will be called automatically as a part of fallback process when a term is not found for one culture.
/// The <paramref name="culture"/> that is coming in will change automatically.
///
/// I guess the reader is also disposed by the caller that I didn't override.
/// </summary>
protected override ResourceSet InternalGetResourceSet(CultureInfo culture, bool createIfNotExists, bool tryParents)
=> new ResourceSet(GetReaderForCulture(culture));
}
}
```


In short, instead of the regular satellite assembly lookup algorithm, all the `override`

here make it only look at **one assembly**, and instead look for a file that has a culture code before `.resx`

prefixed with `_`

instead of a `.`


The normal way to use this class is instantiating `ClientSideResourceManager`

with my new constructor. It take an `Assembly`

, the single assembly to search for all cultures, and a `string`

of full name of resource that you think is embedded in the assembly. By Visual Studio default convention, if I put the `.resx`

file in a folder named `AAA`

it would be named `MyProjectName.AAA.ResourceName.resources`

. So I would have to input just `MyProjectName.AAA.ResourceName`

here. It knows how to take from this to any other `MyProjectName.AAA.ResourceName_??-??.resources`

as long as they are in the same assembly, upon using `GetString`

or `GetObject`

with any `CultureInfo`

provided! Those functionality should be in the `virtual`

method of the base class, and because I didn't touch them it should just works while taking in my custom pieces that I did `override`

them.

Moreover there is one helper `static`

method `HackResourceClass`

which let you even skip instantiating `ClientSideResourceManager`

altogether. The requirement is that you must have a generated static access point class first. It use reflection to edit the inside of that class. (that was unusable because the normal `ResourceManager`

inside insist to look for satellite assemblies) After calling this, the static generated class now magically works correctly because this helper method replaces the normal `ResourceManager`

inside with my custom one that look for culture variants by my new `_`

convention. This helper method could be pasted somewhere on intialization.

![](../../assets/87035489b9516602.png)

The end result is that, I can keep using the generated class without editing it because refection took care of the editing. Images being able to be in a `resx`

is a great help. However there are still difficulties when trying to add a new terms which I must remember to add it to all available localization files.

![](../../assets/12feb05f8234a5fe.gif)

Those language switcher button do not even need to provide `CultureInfo`

for the static generated class (e.g. `LocalizationResouce.Culture = __`

) since when culture is null, it look for UI culture of the current thread. I can instead use `Thread.CurrentThread.CurrentUICulture = __`

and all generated class would start using them. After setting culture of the thread I just need to `StateHasChanged()`

to all related components.

Because just any other files could also be embeded in the `dll`

by setting its property to "Embedded resource", there are potential to extend this `ClientSideResourceManager`

to be able to read localization from something like `json`

or `csv`

for better integration with external toolings. At that point I may learn how to make a NuGet package and open source it. But for now I am content with using `.resx`

.