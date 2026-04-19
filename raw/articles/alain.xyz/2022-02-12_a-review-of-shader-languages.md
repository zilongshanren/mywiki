---
title: A Review of Shader Languages
url: https://alain.xyz/blog/a-review-of-shader-languages
author: Alain Galvan
published: '2022-02-12'
source_blog: Alain Galvan · Ray Tracing Driver Engineer at AMD
source_site: https://alain.xyz/
category: graphics
fetched: '2026-04-19'
---

Shaders are a set of instructions (so a *program* or *kernel*) that execute on programmable steps of a given GPU pipeline, be it a raster pipeline, compute, ray tracing, etc.

They could be used to *transform vertices*, *shade pixels in raster based rendering*, *handle intersections* of primitives in ray tracing, *machine learning*, *perform general computations*, and much more. Shaders execute on a Single-Instruction-Multiple-Data (SIMD) architecture, where groups of processing cores execute the same instruction across large swaths of data.

Depending on the vendor this can mean different things. For instance, on AMD hardware a kernel executes across groups of 32 or 64 *work-items* (or *dispatch threads*) called *wavefronts* (or *thread groups*). These work-items execute on a small processor that handles scalar logic, vector logic, and scalar/vector memory stored in the local cache of the group or in GPU memory. [[AMD 2020]](https://alain.xyz#ref_rdna2020)

There are a number of shader languages used in real-time rendering:

| Abbreviation | Language | Official Graphics APIs | Transpiling |
|---|---|---|---|
| HLSL | High Level Shading Language | DirectX | Both `dxc` and `glslang` support HLSL → SPIR-V |
| GLSL | OpenGL Shading Language | Vulkan / OpenGL | GLSL → SPIR-V → HLSL |
| MSL | Metal Shading Language | Metal | SPIR-V → MSL via SPIR-V Cross |
| WGSL | WebGPU Shading Language | WebGPU | `naga` or `tint` → SPIR-V |

With the addition of other platform specific languages such as *PlayStation Shading Language (PSL)*, experimental languages such as [Rust to SPIR-V](https://github.com/gfx-rs/rspirv), and the older C for Graphics (Cg) used in older Unity 3D code [[Doppioslash 2018]](https://alain.xyz#ref_doppioslash2018). Depending on which platform/API you're targeting, you'll be stuck with one of these languages.

The shader language world is *fragmented by design* given there's so many vendors and APIs, but every shading language is similar enough to C that one can easily switch between them. Depending on the language, there could be an API specific intermediary representation (IR) of the shader code, and each vendor (AMD, NVIDIA, Intel, Qualcomm, etc.) converts that IR to their machine code at the driver level.

| IR Abbreviation | Description | Official Graphics APIs |
|---|---|---|
| DXIL | DirectX Intermediate Language | DirectX 12 |
| DXBC | DirectX Bytecode | DirectX 11 / 12 |
| SPIR-V | Standard Portable Intermediate Representation | Vulkan / OpenGL |
| RDNA ISA | AMD 5-7000 Series Instruction Set Architecture | N/A |
| PTX | NVIDIA Parallel Thread Execution VM and ISA | N/A |
| SASS | NVIDIA Bytecode | N/A |

Let's review some of the similarities and differences between shader languages, their features, how they execute, and how to approach writing shaders for your applications.

We'll review a **vertex shader** in HLSL, GLSL, MSL, and WGSL where we:

Access data received from the *Input Assembly* step of the graphics pipeline.

Pass data to the next step of the graphics pipeline.

Receive data through *uniforms* or *constant buffer views*.

In addition, we'll review a **compute shader** in each of those languages where we:

Read and write to buffers.

Perform atomic operations.

Share data across thread groups.

From there we'll go over how to approach compiling those shaders and include them in your applications.

Nearly all shading languages are very similar to C, and have all the usual features associated with C.

In addition, shading languages feature a standard library of intrinsic functions available in the global namespace for performing common math operations. These standard functions include:

Vector Math (matrix multiplication, vector addition, dot products). Some languages overload `operator*`

, others use a function `mul`

.

Transcendentals (Sin, Cos, Log, etc.) Some languages distinguish `tan(v)`

and `tan2(a, b)`

.

Neighbor Operations (derivatives) with minor differences in function names.

Logic (checking all members of a boolean vector with `all()`

, etc.)

GPGPU memory synchronization such as `atomicAdd`

.

Most of these functions are even named the same, but some are slightly different (HLSL's `frac`

vs GLSL's `fract`

) or so simple that they're not included in other languages like HLSL's `saturate()`

vs `clamp(val, 0.0, 1.0)`

.

**High-Level Shading Language (HLSL)** is arguably the best language for writing shaders, as it's very well supported, separates samplers and textures (unlike GLSL), and has common language features like:

`#include`

and much more [as of HLSL 2021](https://devblogs.microsoft.com/directx/announcing-hlsl-2021/).

For more details on the HLSL language, review the following:

```
// ❎ HLSL Vertex Shader
struct Constants
{
row_major float4x4 modelViewProjection : packoffset(c0);
float4x4 inverseTransposeModel : packoffset(c4);
float4x4 view : packoffset(c8);
};
ConstantBuffer<Constants> constants : register(b0);
struct VertexInput
{
float3 position : POSITION;
float3 normal : NORMAL;
float2 texCoord : TEXCOORD;
};
struct VertexOutput
{
float4 position : SV_Position;
float3 normal : NORMAL;
float2 texCoord : TEXCOORD;
};
VertexOutput main(VertexInput vertexInput)
{
float4 position = mul(float4(vertexInput.position, 1.0f), constants.modelViewProjection);
float3 outNormal = mul(float4(vertexInput.normal, 1.0), constants.inverseTransposeModel).xyz;
float2 outTexCoord = vertexInput.texCoord;
VertexOutput output;
output.position = position;
output.normal = outNormal;
output.texCoord = outTexCoord;
return output;
}
```


If you want globally accessible shader constants (like how uniforms worked in older APIs), you can use the keyword `cbuffer`

.

```
cbuffer cb : register(b0)
{
row_major float4x4 modelViewProjection : packoffset(c0);
float3 origin : packoffset(c4);
float time : packoffset(c5);
};
// Later...
float4 position = mul(float4(vertexInput.position, 1.0f), modelViewProjection);
```


HLSL is unique in that it describes attribute inputs with [ semantics](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics) (for example,

`float3 position : POSITION`

), though you can and `ATTRIB`

. You can also use this syntax to describe other things about your variable similar to a bitfield, such as alignment or what buffer/texture/sampler registers correspond to a given variable.HLSL shaders are very intuitive, they have an input, and output. They can have global constants or constants contained in a constant buffer.

Now let's look at a compute shader:

```
// ❎ HLSL Compute Shader
struct Constants
{
float time : packoffset(c0);
};
ConstantBuffer<Constants> constants : register(b0);
Texture2D<float4> albedoTex : register(t1);
Texture2D<float4> pbrLutTex : register(t2);
SamplerState gSampler : register(s0);
RWTexture2D<float4> tOutput : register(u0);
groupshared float groupData[4];
namespace random
{
float foo()
{
return 16.0;
}
}
[numthreads(8, 4, 1)]
void main(uint3 groupThreadID : SV_GroupThreadID,
uint3 groupID : SV_GroupID,
uint groupIndex : SV_GroupIndex,
uint3 dispatchThreadID: SV_DispatchThreadID)
{
tOutput[dispatchThreadID.xy] = float4( float(groupThreadID.x) / random::foo(), float(groupThreadID.y) / 16.0, dispatchThreadID.x / 1280.0, 1.0);
}
```


You can easily define compute shader intrinsic values as arguments of the main function and expect those to be passed in, and name them whatever you might like. Otherwise this is practically the same as a vertex shader and as we'll see, the same across languages.

**OpenGL Shading Language (GLSL)** is the standard shader programming language for Khronos APIs such as Vulkan, OpenGL 4.x through optional extensions for different versions of GLSL, and WebGL. There's a few fundamental differences between GLSL and other languages:

Vector types use the prefix `vec`

(for example, `vec4`

instead of `float4`

and `mat4`

instead of `float4x4`

)

Samplers and texture bindings are tied together. This is a big difference and area of contention, as this isn't necessary and other languages separate these two data structures.

Feature wise however GLSL is similar to HLSL, with support for `#include`

through optional extensions and similar intrinsic functions.

The **GLSL** code begins with layout declarations that define exactly how each struct and object is laid out in memory. Each `location`

corresponds to an address pointing to a maximum of 4 single precision floats. The keyword `in`

denotes that this data is coming from the **Input Assembly** step of the graphics pipeline, and the keyword `out`

denotes that this is data being passed to the next step of the graphics pipeline (`in`

could be described as *passing a reference*).

The uniforms in this shader are struct based, and are bound to sets and binding indexes. Uniforms can be *Uniform Buffer Objects (UBOs)* where the last parameter can be an n-dimensional matrix if needed, or the could be *Samplers*. Note you don't need to denote the namespace of the parameters of the UBOs, each name is unique and accessible in the global namespace (`model.transform == transform`

).

It's worth noting that there's a wide range of supported versions of GLSL and OpenGL, with

GLSL ES 1.0being the version used for WebGL, andGLSL ES 3.0used for WebGL 2.

In the `main`

function we perform our shader logic and write our output position and varying variables. Note that the use of the keyword `main`

can be set to anything you would like.

```
// 🌋 GLSL Vertex Shader
#version 450
struct VertexInput
{
vec3 position;
vec3 normal;
vec2 texCoord;
};
struct VertexOutput
{
vec4 position;
vec3 normal;
vec2 texCoord;
};
struct Constants
{
mat4 modelViewProjection;
mat4 inverseTransposeModel;
mat4 view;
};
layout(set = 0) uniform Constants constants;
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoord;
layout (location = 0) out vec3 outNormal;
layout (location = 1) out vec2 outTexCoord;
void main()
{
vec4 position = constants.modelViewProjection * vec4(position, 1.0f);
outNormal = (constants.inverseTransposeModel * vec4(normal, 1.0)).xyz;
outTexCoord = texCoord;
gl_Position = position;
}
```


Compute shaders are generally the same as HLSL, though each built-in value passed in HLSL is just a global in GLSL. Writing data to an image is done through a function instead of the array syntax. There's also no need to annotate the main function to specify what kind of shader it is, since that's written out at compile time to SPIR-V.

```
// 🌋 GLSL Compute Shader
#version 450
layout(local_size_x = 8, local_size_y = 4, local_size_z = 1) in;
layout(binding = 0, std140) uniform Constants
{
float time;
} constants;
layout(binding = 0, rgba32f) uniform readonly writeonly image2D tOutput;
shared float groupData[4];
float foo()
{
return 16.0;
}
void main()
{
imageStore(tOutput, gl_GlobalInvocationID.xy,
vec4(float(gl_SubgroupInvocationID.x) / foo(),
float(gl_SubgroupInvocationID.y) / 16.0,
gl_GlobalInvocationID.x / 1280.0, 1.0));
}
```


In **Metal Shading Language (MSL)** there is no `uniform`

keyword, everything that is a buffer could be a uniform. Similar to HLSL, attributes are passed as arguments in the main function, with directives to denote where that data is coming from. Unlike HLSL or GLSL, data to be passed to later stages of the pipeline is returned by the main function.

Metal vector types are named the same as HLSL, and the intrinsic functions are nearly all the same as well.

```
// 🤖 Metal Vertex Shader
#include <metal_stdlib>
#include <simd/simd.h>
using namespace metal;
struct Constants
{
float4x4 modelViewProjection;
float4x4 inverseTransposeModel;
float4x4 view;
};
struct VertexOutput
{
float3 normal [[user(locn0)]];
float2 texCoord [[user(locn1)]];
float4 position [[position]];
};
struct VertexInput
{
float3 position [[attribute(0)]];
float3 normal [[attribute(1)]];
float2 texCoord [[attribute(2)]];
};
vertex VertexOutput main(VertexInput in [[stage_in]],
constant Constants& constants [[buffer(0)]],
uint gl_VertexID [[vertex_id]],
uint gl_InstanceID [[instance_id]])
{
VertexOutput out = {};
float4 position = constants.modelViewProjection * float4(in.position, 1.0);
out.normal = (constants.inverseTransposeModel * float4(in.normal, 1.0)).xyz;
out.texCoord = in.texCoord;
out.position = position;
return out;
}
```


Metal's input/output model is much more clear than in other languages, where the main function shows those bindings, and this applies to their compute shaders as well (denoted with the keyword `kernel`

).

```
// 🤖 Metal Compute Shader
#include <metal_stdlib>
#include <simd/simd.h>
using namespace metal;
struct Constants
{
float time;
};
float foo()
{
return 16.0;
}
kernel void main(
uint3 groupThreadID [[ thread_position_in_threadgroup ]],
uint3 groupID [[threadgroup_position_in_grid]],
uint groupIndex [[thread_index_in_threadgroup]],
uint3 dispatchThreadID [[thread_position_in_grid]],
constant Constants& constants [[buffer(0)]],
texture2d<float, access::read_write> tOutput [[texture(0)]])
{
threadgroup float groupData[4];
tOutput[dispatchThreadID.xy] = float4( float(groupThreadID.x) / foo(), float(groupThreadID.y) / 16.0, dispatchThreadID.x / 1280.0, 1.0);
}
```


**WebGPU Shading Language (WGSL)** is pretty unique, with a syntax that's a bit like JavaScript, Rust, C, and Apple Metal. It's evolved a lot over its development, it used to be much more verbose [[Maxfield 2018]](https://alain.xyz#ref_maxfield2018) but has since become a blend of Metal Shader Language and HLSL.

Vector types are unique in that they are similar to both HLSL and GLSL, but have a more clearly defined size for each type.

```
// 🌐 WGSL Vertex Shader
struct Constants
{
modelViewProjection: mat4x4<f32>,
inverseTransposeModel: mat4x4<f32>,
view: mat4x4<f32>
};
struct VertexOutput
{
@builtin(position) position: vec4<f32>,
@location(0) normal: vec3<f32>,
@location(1) uv: vec2<f32>
};
@group(0) @binding(0) var<uniform> constants : Constants;
@vertex
fn main(@location(0) position: vec4<f32>,
@location(1) uv: vec2<f32>) -> VertexOutput {
var vsOut: VertexOutput;
vsOut.position = constants.modelViewProjection * vec4<f32>(position, 1.0);
vsOut.position = constants.inverseTransposeModel * vec4<f32>(normal, 1.0);
vsOut.uv = uv;
return vsOut;
}
```


Compute shaders are similar to GLSL, with similar names for built-in values such as the global invocation ID, etc:

```
// 🌐 WGSL Compute Shader
struct Constants
{
time: f32
};
@group(0) @binding(0) var<uniform> constants: Constants;
@group(0) @binding(1) var tOutput: texture_storage_2d<rgba8unorm,write>;
fn foo() -> f32
{
return 4.0;
}
@compute @workgroup_size(8, 4, 1)
fn main(@builtin(local_invocation_id) localInvocationID: vec3<u32>,
@builtin(workgroup_id) workgroupID: vec3<u32>,
@builtin(local_invocation_index) localInvocationIndex: u32,
@builtin(global_invocation_id) globalInvocationID: vec3<u32>) {
var color = vec4<f32>(
(f32(localInvocationID.x) / 8.0) + sin((f32(globalInvocationID.x) / 160.0) + (constants.time * 0.01)),
f32(localInvocationID.y) / foo(),
f32(globalInvocationID.y) / 360.0,
255
);
textureStore(tOutput, vec2<i32>(globalInvocationID.xy), color);
}
```


**OpenCL** looks incredibly similar to both Apple Metal and OpenGL. While the idea of a graphics pipeline doesn't exist in OpenCL, a compute kernel in other APIs is essentially the same thing.

```
struct Constants
{
float time;
uint width;
uint height;
};
float foo()
{
return 16.0;
}
__kernel void main
(
__constant Constants constants,
__global float4* tOutput
)
{
uint localId = get_local_id(0);
uint workgroupId = get_group_id(0);
uint globalId = get_global_id(0);
int x = globalId % constants.width;
int y = globalId / constants.width;
if (x >= width || y >= constants.height)
{
return;
}
tOutput[pixel_idx] = (float4)((float)(x) / foo(), (float)(y) / 16.0, (float)(x) / 1280.0, 1.0);
}
```


Yak-shave: When I press "F5" now in this side project, cmake actually detects if I've changed shaders, compiles them to SPIR-V, converts that to hex in a .c file, compiles those c files into a lib, and then links it to the exe so I can reference the bytecode without file reads. ~

[Jeremy Ong (@m_ninepoints)]

You should *always aim to compile your shaders in advance* to your target graphics API's IR. This will result in a noticeable improvement in performance, since you no longer have to wait for shaders to compile before submitting commands. Some languages however encourage you *not to compile shaders to an IR* such as GLSL with older versions of OpenGL (though you can now use SPIR-V thanks to extensions) or WebGPU Shading Language (WGSL), and for those you can minify/obfuscate them similar to JavaScript for production.

```
# ❎ DirectX
dxc.exe -T lib_6_3 -Fo assets/triangle.vert.dxil assets/triangle.vert.hlsl
# 🌋 Vulkan / OpenGL
dxc.exe -spirv -Fo assets/triangle.vert.spv assets/triangle.vert.hlsl
```


HLSL Shaders can be compiled offline to DXIL with [DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler).

If you want to output SPIR-V, you will need to pass the `-spirv`

flag as well as [annotate your HLSL with SPIR-V decorators](https://github.com/microsoft/DirectXShaderCompiler/blob/master/docs/SPIR-V.rst#specialization-constants).

[GLSLang Validator](https://github.com/KhronosGroup/glslang) is Khronos' reference front end for GLSL, and can compile it to SPIR-V.

The `metallib`

compiler is available in the command line in any recent MacOS installation.

```
// Vulkan (glslang.h)
SH_IMPORT_EXPORT int ShCompile(
const void* shHandle,
const char* const shaderStrings[],
const int numStrings,
const int* lengths,
const EShOptimizationLevel,
const TBuiltInResource *resources,
int debugOptions,
int defaultVersion = 110, // use 100 for ES environment, overridden by #version in shader
bool forwardCompatible = false, // give errors for use of deprecated features
EShMessages messages = EShMsgDefault // warnings and errors
);
```


Vulkan introduces offline shader compilation, so to compile you'll need to either write a compiler to SPIR-V or use the official compiler. GLSLang even supports compiling HLSL to SPIR-V, though this feature is still experimental.

```
// OpenGL
GLuint shader = glCreateShader(VETEX_SHADER);
glShaderSource(shader, srcStr);
glCompileShader(shader);
GLint isCompiled = 0;
glGetShaderiv(shader, GL_COMPILE_STATUS, &isCompiled);
if(isCompiled == GL_FALSE)
{
GLint maxLength = 0;
glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &maxLength);
std::vector<GLchar> errorLog(maxLength);
glGetShaderInfoLog(shader, maxLength, &maxLength, &errorLog[0]);
}
```


OpenGL is pretty straight forward, you send it the string and check if it's valid. Alternatively, newer versions of OpenGL let you load SPIR-V directly.

```
// DirectX
HRESULT WINAPI D3DCompile(
in LPCVOID pSrcData,
in SIZE_T SrcDataSize,
in_opt LPCSTR pSourceName,
in_opt const D3D_SHADER_MACRO pDefines,
in_opt ID3DInclude pInclude,
in_opt LPCSTR pEntrypoint,
in LPCSTR pTarget,
in UINT Flags1,
in UINT Flags2,
out ID3DBlob ppCode,
out_opt ID3DBlob ppErrorMsgs
);
```


DirectX like OpenGL supports compiling shaders at runtime, however both now support loading both bytecode or shader strings.

```
id<MTLLibrary> library = [self.device newDefaultLibrary];
id<MTLFunction> vertexFunc = [library newFunctionWithName:@"vertex_main"];
id<MTLFunction> fragmentFunc = [library newFunctionWithName:@"fragment_main"];
```


Rather than managing shader modules yourself, in Metal, you can create libraries of shader functions and load those as needed. If you need to grab the main of a given library's function list, you can use the `newFunctionWithName`

method.

So long as a shader is written in valid GLSL or HLSL, transpiling it to either GLSL, HLSL, or MSL is possible with [SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross). You may need to annotate some parts of your shader though with API specific information.

```
# 🌋 Compile shaders to SPIR-V binary
glslangValidator -V triangle.vert -o triangle.vert.spv
glslangValidator -V triangle.frag -o triangle.frag.spv
# ❎ HLSL
spirv-cross triangle.vert.spv --hlsl --shader-model 50 --set-hlsl-vertex-input-semantic 0 POSITION --set-hlsl-vertex-input-semantic 1 COLOR --output triangle.vert.hlsl
spirv-cross triangle.frag.spv --hlsl --shader-model 50 --set-hlsl-vertex-input-semantic 0 COLOR --output triangle.frag.hlsl
# ⚪ OpenGL ES 3.1
spirv-cross triangle.vert.spv --version 310 --es --output triangle.vert.glsl
spirv-cross triangle.frag.spv --version 310 --es --output triangle.frag.glsl
# 🤖 Metal
spirv-cross triangle.vert.spv --msl --output triangle.vert.msl
spirv-cross triangle.frag.spv --msl --output triangle.frag.msl
```


In addition, WGSL compilers can also transpile directly:

```
# 🦊 Mozilla Naga
# https://github.com/gfx-rs/naga
# ⚪ Convert the WGSL to GLSL vertex stage under ES 3.20 profile
cargo run my_shader.wgsl my_shader.vert --profile es310
# 🤖 Convert the SPV to Metal
cargo run my_shader.spv my_shader.metal
```


Shading languages are similar to each other, with minor differences in keywords, but different underlying designs philosophies such as the union of samplers and textures in GLSL, or the buffer attribute model of Metal. It's not too difficult to work around these differences though, and bridge the gap between HLSL, GLSL, MSL, and WGSL.

There's a few areas that we didn't go over that are worth reviewing such as:

Ray Tracing Shaders - DirectX 12 and Vulkan share the same type of ray tracing shaders, but Metal takes a more unique approach.

Meshlet Shaders - These can be reviewed in their own posts, but are currently limited to DirectX 12 and Vulkan.

Each shader language has documentation pages that go over their nuances in more detail:

The [HLSL Reference](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-intrinsic-functions) can be reviewed in from their documentation page.

The [GLSL Reference](https://www.khronos.org/registry/OpenGL-Refpages/gl4/index.php) is combined with OpenGL's reference, it's a bit tough to parse through, but anything with `gl_`

or without a `glCamelCase`

is part of GLSL.

The [MSL Reference](https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf#page=138) details their intrinsic functions, keywords, etc.

The [WGSL Reference](https://gpuweb.github.io/gpuweb/wgsl/#builtin-functions) features everything about the language from intrinsic functions to decorators.

The [OpenCL C Reference](https://www.khronos.org/registry/OpenCL/specs/3.0-unified/html/OpenCL_C.html) showcases the kernel language used for OpenCL. Even though the language is for compute only, it's extremely similar to GLSL and worth a look.

It's also worth reviewing vendor ISAs to better understand what instructions your shader will eventually become:

The AMD [RDNA2 ISA](https://developer.amd.com/wp-content/resources/RDNA2_Shader_ISA_November2020.pdf) reference guide will help you better architect your shaders by showing what instructions DXIL and SPIR-V ultimately become in AMD hardware.

NVIDIA's [Parallel Thread Execution (PTX) ISA](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html) shows what your shader IR will eventually become on NVIDIA hardware, and describes the instructions CUDA cores can execute.

It's also worth reviewing the test suite for the various compilers for these languages:

[DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler) can also output SPIR-V code, and would serve as a better tool from translating HLSL to GLSL than say, SPIR-V Cross.

[GLSLang](https://github.com/KhronosGroup/glslang) is Khronos' official GLSL compiler, and besides compile SPRIR-V it can also reflect GLSL and even compile some HLSL.

[Mozilla Naga](https://github.com/gfx-rs/naga) is the Firefox WGSL compiler written in Rust.

[Google Tint](https://dawn.googlesource.com/tint/) is Chromium's WGSL compiler.

[SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross) can convert SPIR-V to GLSL, HLSL, and MSL easily.

Tim Jones ([@ tim_jones](https://twitter.com/_tim_jones_)) released a VS Code Plugin called

There's also a number of videos, blog posts, and projects that focus on shaders:

[The State of Shader Tooling in Vulkan](https://www.youtube.com/watch?v=uhhwREjtMY0&t=1681s) by David Neto ([@dneto1969](https://twitter.com/dneto1969)) contrasts different shader IRs and their compilers. You can find the [slides here](https://www.khronos.org/assets/uploads/developers/library/2018-gdc-webgl-and-gltf/1-Vulkan-Whats-New-GDC_Mar18.pdf). (Thanks for sharing this and the WGSL compilers on Twitter David!)

[Slang](https://github.com/shader-slang/slang) is an new shading language that compiles to GLSL, HLSL and SPIR-V, a spiritual successor of Cg.

AMD released a talk titled [Trip Down the Shader Compiler Pipeline](https://www.youtube.com/watch?v=_ilAL-1-moA&list=PL-ZzkbB7kcKjoE3-q_-6eL49XRqqcWZeJ&index=19), which reviews how shaders go from source code to their vendor specific IR.

Matthäus G. Chajdas ([@NIV_Anteru](https://twitter.com/NIV_Anteru)) released a blog post [detailing how HLSL and GLSL map to each other](https://anteru.net/blog/2016/mapping-between-HLSL-and-GLSL/).

[Dzmitry Malyshau](http://kvark.github.io) [benchmarked the Rust WGSL shader compiler Naga with different compilers](http://kvark.github.io/naga/shader/2022/02/17/shader-translation-benchmark.html).

[Shader Model 6.0](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/hlsl-shader-model-6-0-features-for-direct3d-12) adds new features to HLSL that are worth reviewing here, with [Shader Model 6.7](https://devblogs.microsoft.com/directx/in-the-works-hlsl-shader-model-6-7/) providing new Gather operations.

The [Shader Playground](https://shader-playground.timjones.io/) by [Tim Jones](http://timjones.io/) ([@ tim_jones](https://twitter.com/_tim_jones_)) provides an easy interface to see what your shaders compile to in various ISAs for different vendors/APIs.

Adam Sawicki ([@Reg__](https://twitter.com/Reg__)) released an [article detailing the difference between the two shader compilers of DirectX 12 ](https://asawicki.info/news_1719_two_shader_compilers_of_direct3d_12). (Thanks @raphlinus from Hacker News for this and all the feedback!)

I wrote a variety of blog posts that may be worth reviewing as well:

If you're curious about shader debugging, visit this article [comparing different graphics API debugging tools](https://alain.xyz/blog/graphics-debugging).

Visit my blog post [comparing different modern graphics APIs](https://alain.xyz/blog/comparison-of-modern-graphics-apis) to get more insights into how shaders and their host APIs differ in design.

| [AMD 2020] |
| [Doppioslash 2018] |
| [Maxfield 2018] |