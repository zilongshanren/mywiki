---
title: Codegen for fast Vulkan
url: https://anteru.net/blog/2018/codegen-for-fast-vulkan
published: '2018-03-10'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you’re using Vulkan, you might have come across this [this document explaining how to get the best calling performance](https://vulkan.lunarg.com/doc/view/1.1.70.1/windows/loader_and_layer_interface.html#user-content-best-application-performance-setup). The gist is that instead of using the entry points provided by the loader, you should query the *real* entry points using `vkGetDeviceProcAddr`

and use those instead. This can yield significant performance gains when CPU limited, as it avoids an indirection through the loader. Querying all entry points doesn’t sound too bad in theory. The problem is there’s quite a few of them, so instead of typing this up manually, let’s use some code generation to solve the problem!

## Where to start?

If we want to auto-generate things, we need to find something machine readable first which we can parse and then use as the data source. Fortunately, the Vulkan specification is also available as an Xml file, as part of the normal repository. Let’s grab the [vk.xml](https://github.com/KhronosGroup/Vulkan-Docs/blob/v1.0.69-core/src/spec/vk.xml) and see what we can do with that! Now this looks quite promising: We see all types in there as well as all entry points. I’m going to use Python for the script we’re about to write, and if you see something like `./types/type`

, that’s [XPath](https://en.wikipedia.org/wiki/XPath) syntax to specify the path to the element(s) we’re looking at. If you’ve never used XPath before, don’t worry, we’ll use very simple XPath only!

Our task is find a all functions that can be loaded using `vkGetDeviceProcAddr`

, stuff them into a structure, and provide some method to query them off the device. Easy enough, let’s type up some example code so we know how our result is supposed to look like:

```
#ifndef VK_DIRECT_4E2E4399D9394222B329DDA74C76DD869EC8B8359E3626DD5706CDEE595FCB2C
#define VK_DIRECT_4E2E4399D9394222B329DDA74C76DD869EC8B8359E3626DD5706CDEE595FCB2C 1
#include <vulkan/vulkan.h>
struct VkDirect
{
using FT_vkAllocateMemory = VkResult (VkDevice device, const VkMemoryAllocateInfo* pAllocateInfo, const VkAllocationCallbacks* pAllocator, VkDeviceMemory* pMemory);
FT_vkAllocateMemory* vkAllocateMemory = nullptr;
using FT_vkFreeMemory = void (VkDevice device, VkDeviceMemory memory, const VkAllocationCallbacks* pAllocator);
FT_vkFreeMemory* vkFreeMemory = nullptr;
// many more functions here
void Bind (VkDevice device)
{
vkAllocateMemory = (FT_vkAllocateMemory*)vkGetDeviceProcAddr (device, "vkAllocateMemory");
vkFreeMemory = (FT_vkFreeMemory*)vkGetDeviceProcAddr (device, "vkFreeMemory");
// many more functions here
}
};
#endif
```


We see that we need a couple of things to succeed:

- The functions which can be queried
- The function signatures

Let’s get started with getting the functions!

## Getting the types

We want to use `vkGetDeviceProcAddr`

, and according to [its documentation](https://www.khronos.org/registry/vulkan/specs/1.0/man/html/vkGetDeviceProcAddr.html), this function is only valid for specific types. Quoting the specification here:

The function pointer

mustonly be called with a dispatchable object (the first parameter) that is`device`

or a child of`device`

.

All right, so we need to find all handle types which are somehow derived from `VkDevice`

. Looking at the Xml, we can see this bit:

```
<type category="handle" parent="VkDevice"><type>VK_DEFINE_HANDLE</type>(<name>VkQueue</name>)</type>
<type category="handle" parent="VkCommandPool"><type>VK_DEFINE_HANDLE</type>(<name>VkCommandBuffer</name>)</type>
```


That’s quite close to what we want. We note that the `name`

is the handle name, and then we can check the `parent`

until we arrive at `VkDevice`

. If `VkDevice`

is a parent or the type itself is `VkDevice`

, then the type matches our definition and should be included.

Unfortunately, there are two problems: The parents are not necessarily in order in the Xml (so we can’t link while we parse), and some objects have multiple parents. Finally, there are also some *alias* types which don’t have a parent at all! To solve this, we’re going to build a dictionary of the type and the set of its parents; and at the end we’re going to walk the parents recursively for every type. If any of the parents ends up being equal to `VkDevice`

, we have a winner! Let’s start typing:

```
def FindDeviceDispatchableTypes (tree):
# We search for all types where the category = handle
handleTypes = tree.findall ('./types/type[@category="handle"]')
# Ordered dict for determinism
typeParents = OrderedDict ()
# for each handle type, we will store the type as the key, and the set of
# the parents as the value
for handleType in handleTypes:
# if it's an alias, we just duplicate
if 'alias' in handleType.attrib:
name = handleType.get ('name')
alias = handleType.get ('alias')
# This assumes aliases come after the actual type,
# which is true for vk.xml
typeParents [name] = typeParents [alias]
else:
name = handleType.find ('name').text
parent = handleType.get ('parent')
# There can be more than one parent
if parent:
typeParents [name] = set (parent.split (','))
else:
typeParents [name] = set ()
def IsVkDeviceOrDerivedFromVkDevice (handleType, typeParents):
if handleType == 'VkDevice':
return True
else:
parents = typeParents [handleType]
if parents is None:
return False
else:
# If we derive from VkDevice through any path, we're set
return any ([IsVkDeviceOrDerivedFromVkDevice (parent, typeParents) for parent in parents])
deviceTypes = {t for t in typeParents.keys () if IsVkDeviceOrDerivedFromVkDevice (t, typeParents)}
return deviceTypes
```


We now have the set of handle types. The next step is finding the functions using those.

## Device functions

Find the functions could be really complicated if the dispatchable type could be everywhere, as we’d have to check all parameters then. Fortunately, Vulkan specifies that the dispatchable type always comes as the first argument, so we only have to check the first parameter, and if it’s in the set we just computed, we’re done. We’re going to iterate over all `./commands/command`

entries – those are the entry points. These look as following:

```
<command successcodes="VK_SUCCESS" errorcodes="VK_ERROR_OUT_OF_HOST_MEMORY,VK_ERROR_OUT_OF_DEVICE_MEMORY,VK_ERROR_TOO_MANY_OBJECTS,VK_ERROR_INVALID_EXTERNAL_HANDLE_KHR">
<proto><type>VkResult</type> <name>vkAllocateMemory</name></proto>
<param><type>VkDevice</type> <name>device</name></param>
<param>const <type>VkMemoryAllocateInfo</type>* <name>pAllocateInfo</name></param>
<param optional="true">const <type>VkAllocationCallbacks</type>* <name>pAllocator</name></param>
<param><type>VkDeviceMemory</type>* <name>pMemory</name></param>
</command>
```


We can ignore most of that. What we need is the `proto`

element, which contains the return type and the name, and then the first `param`

element. To build the signature, we also have to flatten the parameters back into plain text. Everything else can be ignored. Let’s wrap this into a function which returns the parsed data in an easy-to-digest list of dictionaries:

```
def FindAllDeviceFunctions (tree, deviceTypes):
functions = []
for command in tree.findall ('./commands/command'):
parameters = command.findall ('param')
if parameters:
firstParameter = parameters [0]
if firstParameter.find ('type').text in deviceTypes:
function = {
'return_type' : command.find ('proto/type').text,
'name' : command.find ('proto/name').text,
'parameters' : []
}
for parameter in parameters:
# This flattens ``<param>const <type>T</type> <name>N</name></param>``
# to ``const T N``
function ['parameters'].append (''.join (parameter.itertext ()))
functions.append (function)
return functions
```


You’d might think that’s all we need to stamp them out, but there’s one more thing we need to look at before we get going.

## Handling `#ifdef`


If we just dump everything, we’ll find out that it compiles fine on Windows (at least for 1.0.69), but on Linux, some entry points are not defined. Turns out, there’s quite a few things protected by a platform `#define`

. What we’re going to do is to find all those entry points, and wrap them into an `#ifdef`

block.

To find the protected bits, we have to look at the `./extensions`

. The way this they are structured is as following:

`/extensions/extension[@protect]`

– Each extension with protection has the`protect`

attribute (which is selected using`[@protect]`

)- Extensions specify entry points in
`./require/command`


For example, here’s one of those protected extensions:

```
<extension name="VK_KHR_external_memory_win32" number="74" type="device" requires="VK_KHR_external_memory" author="KHR" contact="James Jones @cubanismo" protect="VK_USE_PLATFORM_WIN32_KHR" supported="vulkan">
<require>
<!-- various fields omitted -->
<command name="vkGetMemoryWin32HandleKHR"/>
<command name="vkGetMemoryWin32HandlePropertiesKHR"/>
</require>
</extension>
```


We’ll just iterate over all extensions which have some protection, and then invert the index so we’re storing the function name as the key, and the protections as the value:

```
def GetFunctionProtection (tree):
extensions = tree.findall (f'./extensions/extension[@protect]')
result = {}
for extension in extensions:
protection = extension.get ('protect').split (',')
for command in extension.findall ('./require/command[@name]'):
result [command.get ('name')] = protection
return result
```


## Combining it all

Now we got everything in place, and the only remaining bit is to generate the code. We just iterate over the functions, create the type definitions and fields first. Then we iterate a second time to fill out the bind method. As a bonus, we take the file pointer to write into so we can redirect easily into a file:

```
def GenerateHeader (tree, functions, protection, outputStream):
import hashlib
def Write (s=''):
print (s, file=outputStream)
# Same tree will always result in the same hash
includeUuid = hashlib.sha256(ElementTree.tostring (tree)).hexdigest().upper ()
Write (f'#ifndef VK_DIRECT_{includeUuid}')
Write (f'#define VK_DIRECT_{includeUuid} 1')
Write ()
Write ('#include <vulkan/vulkan.h>')
Write ()
Write ('struct VkDirect')
Write ('{')
def UnpackFunction (function):
return (function ['name'], function ['return_type'], function ['parameters'])
for function in functions:
name, return_type, parameters = UnpackFunction (function)
if name == 'vkGetDeviceProcAddr':
continue
protect = protection.get (name, None)
if protect:
Write (f'#ifdef {" && ".join (protect)}')
Write (f'\tusing FT_{name} = {return_type} ({", ".join (parameters)});')
Write (f'\tFT_{name}* {name} = nullptr;')
if protect:
Write ('#endif')
Write ()
Write ('\tvoid Bind (VkDevice device)')
Write ('\t{')
for function in functions:
name, return_type, parameters = UnpackFunction (function)
if name == 'vkGetDeviceProcAddr':
continue
protect = protection.get (name, None)
if protect:
Write (f'#ifdef {" && ".join (protect)}')
Write (f'\t\t{name} = (FT_{name}*)vkGetDeviceProcAddr (device, "{name}");')
if protect:
Write ('#endif')
Write ('\t}')
Write ('};')
Write ()
Write ('#endif')
```


… and that’s it for today. You can find the whole script [here](https://anteru.net/files/2018/vkdirect.py) – enjoy!