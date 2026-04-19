---
title: Shapes and forms of DX12 root signatures
url: https://asawicki.info/news_1778_shapes_and_forms_of_dx12_root_signatures
published: '2024-05-14'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Tue

14

May 2024

This article is for you if you are a programmer using **Direct3D 12**. We will talk about a specific part of the API: **root signatures**. I will provide a comprehensive description of various formats in which they can be specified, stored, and ways to convert between them. The difficulty of this article is intermediate. You are expected to know at least some basics of D3D12. I think that advanced developers will can also learn something new, as some of the topics shown here are not what we typically use in a day-to-day development with D3D12.

I will use C++ as the programming language. Wherever possible, I will also try to use standalone command-line tools instead of writing a custom code. To repeat my experiments demonstrated in this article, you will need two of these:

`PATH`

environmental variable, so you can open Command Prompt and just type "dxc" to use it.You don't need to know the command-line syntax of these tools to understand the article. I will describe everything step-by-step.

**Warning about DXC:** If you also have Vulkan SDK installed, very likely your `PATH`

environmental variable points to "dxc.exe" in that SDK instead of Windows SDK, which can cause problems. To check this, type command: `where dxc`

. If you find Vulkan SDK listed first, make sure you call "dxc.exe" from Windows SDK, e.g. by explicitly specifying full path to the executable file.

**Warning about RGA:** If you want to repeat command-line experiments presented here, make sure to use Radeon GPU Analyzer in the latest version, at least 2.9.1. In older versions, the commands I present wouldn't work.

A side note about shader compilation: Native CPU code, like the one we create when compiling our C++ programs, is saved in .exe files. I contains instructions in a common format called x86, which is sent directly to CPU for execution. It works regardless if you have an AMD or Intel processor in your computer, because they comply to the same standard. With programs written for the GPU (which we call shaders), things are different. Every GPU vendor (AMD, Nvidia, Intel) has its own instruction set, necessitating a two-step process for shader compilation:

In Direct3D 12, a root signature is a data structure that describes resource bindings used by a pipeline on all the shader stages. Let's see an example. Let's work with file "Shader1.hlsl": a very simple HLSL code that contains 2 entry points: function `VsMain`

for vertex shader and function `PsMain`

for pixel shader:

struct VsInput

{

float3 pos : POSITION;

float2 tex_coord : TEXCOORD;

};

struct VsOutput

{

float4 pos : SV_Position;

float2 tex_coord : TEXCOORD;

};

struct VsConstants

{

float4x4 model_view_proj;

};

ConstantBuffer<VsConstants> vs_constant_buffer : register(b4);

VsOutput VsMain(VsInput i)

{

VsOutput o;

o.pos = mul(float4(i.pos, 1.0), vs_constant_buffer.model_view_proj);

o.tex_coord = i.tex_coord;

return o;

}

Texture2D<float4> color_texture : register(t0);

SamplerState color_sampler : register(s0);

float4 PsMain(VsOutput i) : SV_Target

{

return color_texture.Sample(color_sampler, i.tex_coord);

}

I assume you already know that a shader is a program executed on a GPU that processes a single vertex or pixel with clearly defined inputs and outputs. To perform the work, it can also reach out to video memory to access additional resources, like buffers and textures. In the code shown above:

A **root signature** is a data structure that describes what I said above - what resources should be bound to the pipeline at individual shader stages. In this specific example, it will be a constant buffer at register b4, a texture at t0, and a sampler at s0. It can also be shown in form of a table:

| Root param index | Register | Shader stage |
|---|---|---|
| 0 | b4 | VS |
| 1 | t0 | PS |
| 2 | s0 | PS |

I am simplifying things here, because this article is not about teaching you the basics of root signatures. For more information about them, you can check:

To prepare for our experiments, let's compile the shaders shown above using commands:

dxc -T vs_6_0 -E VsMain -Fo Shader1.vs.bin Shader1.hlsl

dxc -T ps_6_0 -E PsMain -Fo Shader1.ps.bin Shader1.hlsl

Note that a single HLSL source file can contain multiple functions (`VsMain`

, `PsMain`

). When we compile it, we need to specify one function as an entry point. For example, the first command compiles "Shader1.hlsl" file using `VsMain`

function as the entry point (`-E`

parameter) treated as a vertex shader in Shader Model 6.0 (`-T`

parameter). Similarly, the second command compiles `PsMain`

function as a pixel shader. Compiled shaders are saved in two separate files: "Shader1.vs.bin" and "Shader1.ps.bin".

It is time to show some C++ code. Imagine we have D3D12 already initialized, our compiled shaders loaded from files to memory, and now we want to render something on the screen. I said a root signature is a data structure, and indeed, we can create one by filling in some structures. The main one is `D3D12_ROOT_SIGNATURE_DESC`

. Let's fill in the structures according to the table above.

// There will be 3 root parameters.

D3D12_ROOT_PARAMETER root_params[3] = {};

// Root param 0: CBV at b4, passed as descriptor table, visible to VS.

D3D12_DESCRIPTOR_RANGE vs_constant_buffer_desc_range = {};

vs_constant_buffer_desc_range.RangeType = D3D12_DESCRIPTOR_RANGE_TYPE_CBV;

vs_constant_buffer_desc_range.NumDescriptors = 1;

vs_constant_buffer_desc_range.BaseShaderRegister = 4; // b4

root_params[0].ParameterType = D3D12_ROOT_PARAMETER_TYPE_DESCRIPTOR_TABLE;

root_params[0].ShaderVisibility = D3D12_SHADER_VISIBILITY_VERTEX;

root_params[0].DescriptorTable.NumDescriptorRanges = 1;

root_params[0].DescriptorTable.pDescriptorRanges = &vs_constant_buffer_desc_range;

// Root param 1: SRV at t0, passed as descriptor table, visible to PS.

D3D12_DESCRIPTOR_RANGE color_texture_desc_range = {};

color_texture_desc_range.RangeType = D3D12_DESCRIPTOR_RANGE_TYPE_SRV;

color_texture_desc_range.NumDescriptors = 1;

color_texture_desc_range.BaseShaderRegister = 0; // t0

root_params[1].ParameterType = D3D12_ROOT_PARAMETER_TYPE_DESCRIPTOR_TABLE;

root_params[1].ShaderVisibility = D3D12_SHADER_VISIBILITY_PIXEL;

root_params[1].DescriptorTable.NumDescriptorRanges = 1;

root_params[1].DescriptorTable.pDescriptorRanges = &color_texture_desc_range;

// Root param 2: sampler at s0, passed as descriptor table, visible to PS.

D3D12_DESCRIPTOR_RANGE color_sampler_desc_range = {};

color_sampler_desc_range.RangeType = D3D12_DESCRIPTOR_RANGE_TYPE_SAMPLER;

color_sampler_desc_range.NumDescriptors = 1;

color_sampler_desc_range.BaseShaderRegister = 0; // s0

root_params[2].ParameterType = D3D12_ROOT_PARAMETER_TYPE_DESCRIPTOR_TABLE;

root_params[2].ShaderVisibility = D3D12_SHADER_VISIBILITY_PIXEL;

root_params[2].DescriptorTable.NumDescriptorRanges = 1;

root_params[2].DescriptorTable.pDescriptorRanges = &color_sampler_desc_range;

// The main structure describing the whole root signature.

D3D12_ROOT_SIGNATURE_DESC root_sig_desc = {};

root_sig_desc.NumParameters = 3;

root_sig_desc.pParameters = root_params;

root_sig_desc.Flags = D3D12_ROOT_SIGNATURE_FLAG_ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT;

Variable `root_sig_desc`

of type `D3D12_ROOT_SIGNATURE_DESC`

is our data structure specifying the root signature. Let's call it a root signature **representation number #1**.

The code may look scary at first, but if you analyze it carefully, I am sure you can recognize the parameters of the 3 resources to bind that we talked about earlier. This code is so complex because a buffer or a texture can be bound in multiple ways, differing in the number of levels of indirection. Describing it is out of scope of this article, but I explained it comprehensively in my old article: [Direct3D 12: Long Way to Access Data](https://asawicki.info/news_1754_direct3d_12_long_way_to_access_data).

There is also an even more general structure `D3D12_VERSIONED_ROOT_SIGNATURE_DESC`

that allows to use root signatures in versions higher than 1.0, but we won't talk about it in this article to not complicate things.

If you also use Vulkan, you may recognize that the equivalent structure is `VkDescriptorSetLayoutCreateInfo`

. From it, you can call function `vkCreateDescriptorSetLayout`

to create an object of type `VkDescriptorSetLayout`

, and then `VkPipelineLayout`

, which is roughly equivalent to the DX12 root signature.

In DX12, however, this is not that simple. There is an intermediate step we need to go through. Microsoft requires converting this data structure to a special binary format first. They call it "serialization". We can do it using function `D3D12SerializeRootSignature`

, like this:

ComPtr<ID3DBlob> root_sig_blob, error_blob;

HRESULT hr = D3D12SerializeRootSignature(&root_sig_desc, D3D_ROOT_SIGNATURE_VERSION_1_0,

&root_sig_blob, &error_blob);

// Check hr...

const void* root_sig_data = root_sig_blob->GetBufferPointer();

size_t root_sig_data_size = root_sig_blob->GetBufferSize();

An object of type `ID3DBlob`

is just a simple container that owns a memory buffer with binary data of some size. ("BLOB" stands for "Binary Large OBject".) This buffer we created here is our **representation number #2** of the root signature.

If we save it to a file, we can see that our example root signature has 188 bytes. It starts from characters "DXBC", just like the shaders we previously complied with `dxc`

tool, which indicates root signatures use the same container format as compiled shaders. I am not sure this binary format is documented somewhere. It should be possible to decipher anyway, as [DirectX Shader Compiler (dxc)](https://github.com/microsoft/DirectXShaderCompiler) is open source. I never needed to work with this binary format directly, and we won't do it here either.

![](files/DX12_root_signatures\root_sig_bin.png)


I guess Microsoft's intention was to encourage developers to prepare root signatures beforehand and store them in files, just like compiled shaders, so they are not assembled in runtime on every application launch. Is it worth it, though? Shader compilation is slow for sure, but would loading a file be faster than filling in the data structure and serializing it with `D3D12SerializeRootSignature`

? I doubt it, unless Microsoft implemented this function extremely inefficiently. Very likely, this additional level of indirection is just an extra unnecessary complication that Microsoft prepared for us. That wouldn't be the only case they did it, as you can read in my old article [Do RTV and DSV descriptors make any sense?](https://asawicki.info/news_1772_secrets_of_direct3d_12_do_rtv_and_dsv_descriptors_make_any_sense)

Note that if a serialized root signature is saved to a file and loaded later, it doesn't need to be stored in a `ID3DBlob`

object. All we need is a pointer to the data and the size (number of bytes). The data can be stored in a byte array like `char* arr = new char[size]`

, or `std::vector<char>`

(I like to use this one), or any other form.

With this extra level of indirection done, we can use this serialized binary root signature to create an object of type `ID3D12RootSignature`

. This is an opaque object that represents the root signature in memory, ready to be used by D3D12. Let's call it root signature **representation number #3**. The code for creating it is very simple:

ComPtr<ID3D12RootSignature> root_sig_obj;

hr = g_Device->CreateRootSignature(0, root_sig_data, root_sig_data_size,

IID_PPV_ARGS(&root_sig_obj));

// Check hr...

Having this root signature object, we can pass it as part of the `D3D12_GRAPHICS_PIPELINE_STATE_DESC`

and use it to create a `ID3D12PipelineState `

- a Pipeline State Object (PSO) that can be used for rendering.

D3D12_GRAPHICS_PIPELINE_STATE_DESC pso_desc = {};

pso_desc.pRootSignature = root_sig_obj.Get(); // Root signature!

pso_desc.VS.pShaderBytecode = vs_data; // Vertex shader from "Shader1.vs.bin".

pso_desc.VS.BytecodeLength = vs_data_size;

pso_desc.PS.pShaderBytecode = ps_data; // Pixel shader from "Shader1.ps.bin".

pso_desc.PS.BytecodeLength = ps_data_size;

pso_desc.RasterizerState.FillMode = D3D12_FILL_MODE_SOLID;

pso_desc.RasterizerState.CullMode = D3D12_CULL_MODE_NONE;

pso_desc.InputLayout.NumElements = _countof(input_elems);

pso_desc.InputLayout.pInputElementDescs = input_elems;

pso_desc.PrimitiveTopologyType = D3D12_PRIMITIVE_TOPOLOGY_TYPE_TRIANGLE;

pso_desc.NumRenderTargets = 1;

pso_desc.RTVFormats[0] = DXGI_FORMAT_R8G8B8A8_UNORM_SRGB;

pso_desc.SampleDesc.Count = 1;

ComPtr<ID3D12PipelineState> pso;

hr = g_Device->CreateGraphicsPipelineState(&pso_desc, IID_PPV_ARGS(&pso));

// Check hr...

If we have the serialized root signature saved to a file "RootSigFromCode.bin", we can also play around with assembling a PSO without any coding, but using Radeon GPU Analyzer instead. Try the following command:

rga -s dx12 -c gfx1100 --all-hlsl Shader1.hlsl --all-model 6_0 --vs-entry VsMain --ps-entry PsMain --rs-bin RootSigFromCode.bin --offline --isa AMD_ISA

The meaning of individual parameters is:

`-s dx12`

- selects DirectX 12 as the API. It is needed because this tool supports other APIs as well.`-c gfx1100`

- selects the GPU generation to use. `gfx1100`

means the latest generation of AMD GPUs at the moment I write this article, which is Radeon RX 7000 series.`--all-hlsl Shader1.hlsl`

- specifies input file with HLSL code.`--vs-entry VsMain --ps-entry PsMain`

- specifies entry points (function names) for vertex and pixel shader, respectively.`--rs-bin RootSigFromCode.bin`

- specifies the file with the serialized root signature.`--offline`

- enables offline mode, which allows RGA to work even without AMD graphics driver installed in the system, e.g. when you have an Nvidia or Intel card.`--isa AMD_ISA`

- enables the ISA (assembly) as the requested output and specifies the name to be used in output files.When succeeded, this command creates 2 text files with the disassembly of the vertex and pixel shader: "gfx1100_AMD_ISA_vert.isa", "gfx1100_AMD_ISA_pixel.isa". The pixel shader looks like this:

; D3D12 Shader Hash 0x46f0bbb15b95e2453380ad3c9765222a

; API PSO Hash 0xd96cc024d8cb165d

; Driver Internal Pipeline Hash 0xf3a0f055053cc59f

; -------- Disassembly --------------------

shader main

asic(GFX11)

type(PS)

sgpr_count(14)

vgpr_count(8)

wave_size(64)

// s_ps_state in s0

s_version UC_VERSION_GFX11 | UC_VERSION_W64_BIT // 000000000000: B0802006

s_set_inst_prefetch_distance 0x0003 // 000000000004: BF840003

s_mov_b32 m0, s4 // 000000000008: BEFD0004

s_mov_b64 s[12:13], exec // 00000000000C: BE8C017E

s_wqm_b64 exec, exec // 000000000010: BEFE1D7E

s_getpc_b64 s[0:1] // 000000000014: BE804780

s_waitcnt_depctr depctr_vm_vsrc(0) & depctr_va_vdst(0) // 000000000018: BF880F83

lds_param_load v2, attr0.x wait_vdst:0 // 00000000001C: CE000002

lds_param_load v3, attr0.y wait_vdst:0 // 000000000020: CE000103

s_mov_b32 s4, s2 // 000000000024: BE840002

s_mov_b32 s5, s1 // 000000000028: BE850001

s_mov_b32 s0, s3 // 00000000002C: BE800003

s_load_b256 s[4:11], s[4:5], null // 000000000030: F40C0102 F8000000

s_load_b128 s[0:3], s[0:1], null // 000000000038: F4080000 F8000000

v_interp_p10_f32 v4, v2, v0, v2 wait_exp:1 // 000000000040: CD000104 040A0102

v_interp_p10_f32 v0, v3, v0, v3 wait_exp:0 // 000000000048: CD000000 040E0103

s_delay_alu instid0(VALU_DEP_2) | instskip(NEXT) | instid1(VALU_DEP_2) // 000000000050: BF870112

v_interp_p2_f32 v2, v2, v1, v4 wait_exp:7 // 000000000054: CD010702 04120302

v_interp_p2_f32 v0, v3, v1, v0 wait_exp:7 // 00000000005C: CD010700 04020303

s_and_b64 exec, exec, s[12:13] // 000000000064: 8BFE0C7E

s_waitcnt lgkmcnt(0) // 000000000068: BF89FC07

image_sample v[0:3], [v2,v0], s[4:11], s[0:3] dmask:0xf dim:SQ_RSRC_IMG_2D // 00000000006C: F06C0F05 00010002 00000000

s_waitcnt vmcnt(0) // 000000000078: BF8903F7

v_cvt_pk_rtz_f16_f32 v0, v0, v1 // 00000000007C: 5E000300

v_cvt_pk_rtz_f16_f32 v2, v2, v3 // 000000000080: 5E040702

s_mov_b64 exec, s[12:13] // 000000000084: BEFE010C

exp mrt0, v0, v2, off, off done // 000000000088: F8000803 00000200

s_endpgm // 000000000090: BFB00000

We will not analyze it here in details, but it is worth nothing that we have 3 memory loading instructions here, which correspond to the operations we do in the pixel shader: `s_load_b256`

and `s_load_b128`

load the descriptors of the sampler s0 and the texture t0, which are then both used by `image_sample`

instruction to perform the texture sampling.

We talked about many different formats of root signatures already, and there will be more. It is time to show a diagram that gathers them all and presents transitions between them. This is the central part of our article that we will refer to. Note that we already talked about representations number #1, #2, #3, #4, which you can find on the diagram.

There is a way to convert a serialized root signature blob back to data structures. Microsoft offers function `D3D12CreateRootSignatureDeserializer`

for this purpose. It creates an object of type `ID3D12RootSignatureDeserializer`

, which owns structure `D3D12_ROOT_SIGNATURE_DESC`

and other structures referred by it. Example code:

ComPtr<ID3D12RootSignatureDeserializer> root_sig_deserializer;

hr = D3D12CreateRootSignatureDeserializer(root_sig_data, root_sig_data_size,

IID_PPV_ARGS(&root_sig_deserializer));

// Check hr...

const D3D12_ROOT_SIGNATURE_DESC* root_sig_desc = root_sig_deserializer->GetRootSignatureDesc();

// Inspect decoded root_sig_desc...

When using higher root signature versions, you need to use function `D3D12CreateVersionedRootSignatureDeserializer`

and interface `ID3D12VersionedRootSignatureDeserializer`

instead.

We are only in the middle of this article. This is because Microsoft prepared one more representation of the root signature - a text representation. For it, they defined a simple domain-specific language, which is fully documented on page [Specifying Root Signatures in HLSL](https://learn.microsoft.com/en-us/windows/win32/direct3d12/specifying-root-signatures-in-hlsl). As an example, our simple root signature presented in this article would look like this:

RootFlags(ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT),

DescriptorTable(CBV(b4), visibility=SHADER_VISIBILITY_VERTEX),

DescriptorTable(SRV(t0), visibility=SHADER_VISIBILITY_PIXEL),

DescriptorTable(Sampler(s0), visibility=SHADER_VISIBILITY_PIXEL)

I am sure you can recognize the same parameters we passed when we assembled a data structure describing this root signature in our C++ code. The text representation is clearly more concise and readable.

However, this is not exactly the way we specify root signatures in text format. It will go to our HLSL shader source file, but before we can put it there, we must pack it to a string defined using a `#define`

macro, so it takes the form of:

#define MyRootSig "RootFlags(ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT), " \

"DescriptorTable(CBV(b4), visibility=SHADER_VISIBILITY_VERTEX), " \

"DescriptorTable(SRV(t0), visibility=SHADER_VISIBILITY_PIXEL), " \

"DescriptorTable(Sampler(s0), visibility=SHADER_VISIBILITY_PIXEL)"

This is our root signature **representation number #5** on the diagram. It looks somewhat clumsy, but this is the way we need to format it. The backslash symbol "\" at the end of each line except the last one is necessary to continue the `#define`

macro in the next line. This is feature of the HLSL preprocessor, same as in C and C++ preprocessor.

We could simplify this macro by putting the whole string with our root signature in a single line, but I am not convinced it would make it more readable. Besides this, formatting root signatures like I shown above is the way recommended by Microsoft in their documentation.

If you think about converting a root signature back to the text representation, there is no ready function for that, but you can find such code in the RGA source, [file "source/radeon_gpu_analyzer_backend/autogen/be_rootsignature_dx12.cpp", class RootSignatureUtil](https://github.com/GPUOpen-Tools/radeon_gpu_analyzer/blob/b22f585016bb52260486af80ac470550eedb2264/source/radeon_gpu_analyzer_backend/autogen/be_rootsignature_dx12.cpp#L329). I marked it as an arrow leading from #1 to #5 on the diagram, described as "Custom code".

Having our root signature defined in the text format, packed into a `#define`

macro, and included in our HLSL shader source file is a first step. Just like a single HLSL file can contain multiple entry points to various shaders, it also contain multiple root signature definitions, so we need to specify the one to use. To do this, we can attach a root signature to the function used as the shader entry point, using `[RootSignature()]`

attribute with the name of our macro inside.

Here is the full contents of a new shader file "Shader2.hlsl" with root signature embedded:

struct VsInput

{

float3 pos : POSITION;

float2 tex_coord : TEXCOORD;

};

struct VsOutput

{

float4 pos : SV_Position;

float2 tex_coord : TEXCOORD;

};

struct VsConstants

{

float4x4 model_view_proj;

};

#define MyRootSig "RootFlags(ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT), " \

"DescriptorTable(CBV(b4), visibility=SHADER_VISIBILITY_VERTEX), " \

"DescriptorTable(SRV(t0), visibility=SHADER_VISIBILITY_PIXEL), " \

"DescriptorTable(Sampler(s0), visibility=SHADER_VISIBILITY_PIXEL)"

ConstantBuffer<VsConstants> vs_constant_buffer : register(b4);

[RootSignature(MyRootSig)]

VsOutput VsMain(VsInput i)

{

VsOutput o;

o.pos = mul(float4(i.pos, 1.0), vs_constant_buffer.model_view_proj);

o.tex_coord = i.tex_coord;

return o;

}

Texture2D<float4> color_texture : register(t0);

SamplerState color_sampler : register(s0);

[RootSignature(MyRootSig)]

float4 PsMain(VsOutput i) : SV_Target

{

return color_texture.Sample(color_sampler, i.tex_coord);

}

If you compile VS and PS from this file using commands:

dxc -T vs_6_0 -E VsMain -Fo Shader2.vs.bin Shader2.hlsl

dxc -T ps_6_0 -E PsMain -Fo Shader2.ps.bin Shader2.hlsl

New files "Shader2.vs.bin" and "Shader2.ps.bin" will have size greater than respective "Shader1.vs.bin" and "Shader1.ps.bin" we created earlier by exactly 168 bytes, which is similar to the size of our serialized root signature. This indicates that our root signature is bundled together with the compiled shader code. This is the representation number #6 on the diagram.

Shaders compiled with a root signature embedded can then be used in the C++/D3D12 code for creating a PSO without a need to specify the root signature explicitly. Variable `D3D12_GRAPHICS_PIPELINE_STATE_DESC::pRootSignature`

can be set to null. Our PSO creation code can now look like this:

D3D12_GRAPHICS_PIPELINE_STATE_DESC pso_desc = {};

pso_desc.pRootSignature = NULL; // Sic!

pso_desc.VS.pShaderBytecode = vs.data(); // Vertex shader from "Shader2.vs.bin".

pso_desc.VS.BytecodeLength = vs.size();

pso_desc.PS.pShaderBytecode = ps.data(); // Pixel shader from "Shader2.ps.bin".

pso_desc.PS.BytecodeLength = ps.size();

pso_desc.RasterizerState.FillMode = D3D12_FILL_MODE_SOLID;

pso_desc.RasterizerState.CullMode = D3D12_CULL_MODE_NONE;

pso_desc.InputLayout.NumElements = _countof(input_elems);

pso_desc.InputLayout.pInputElementDescs = input_elems;

pso_desc.PrimitiveTopologyType = D3D12_PRIMITIVE_TOPOLOGY_TYPE_TRIANGLE;

pso_desc.NumRenderTargets = 1;

pso_desc.RTVFormats[0] = DXGI_FORMAT_R8G8B8A8_UNORM_SRGB;

pso_desc.SampleDesc.Count = 1;

ComPtr<ID3D12PipelineState> pso;

hr = g_Device->CreateGraphicsPipelineState(&pso_desc, IID_PPV_ARGS(&pso));

// Check hr...

Similarly, we can use RGA to compile those shaders, assemble the PSO, and output AMD GPU assembly:

rga -s dx12 -c gfx1100 --all-hlsl Shader2.hlsl --all-model 6_0 --vs-entry VsMain --ps-entry PsMain --offline --isa AMD_ISA

Because we can use multiple shaders at different shaders stages (vertex shader, pixel shader, possibly also hull, domain, geometry, amplification, mesh shader...) when creating a PSO, and we attached a `[RootSignature()]`

attribute to all of them, you may ask what happens if some shader stages don't specify a root signature or specify a different one. Here are the rules:

D3D12 ERROR: ID3D12Device::CreateGraphicsPipelineState: Root Signature doesn't match Pixel Shader: Root signature of Vertex Shader doesn't match the root signature of Pixel Shader

When we have a root signature encoded in the text format, we can use it in two ways. One is attaching it to a shader entry point function using the `[RootSignature()]`

attribute, like we've seen in the previous section. The second one is compiling root signature alone. For this, we need to use dedicated command-line arguments for "dxc.exe" and specify the name of our macro.

Let's create a separate HLSL file with only the root signature, called "RootSig.hlsl":

#define MyRootSig "RootFlags(ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT), " \

"DescriptorTable(CBV(b4), visibility=SHADER_VISIBILITY_VERTEX), " \

"DescriptorTable(SRV(t0), visibility=SHADER_VISIBILITY_PIXEL), " \

"DescriptorTable(Sampler(s0), visibility=SHADER_VISIBILITY_PIXEL)"

Let's now use the following command to compile it:

dxc -T rootsig_1_0 -E MyRootSig -Fo RootSigFromHlsl.bin RootSig.hlsl

The output of this command is file "RootSigFromHlsl.bin", which is 188 bytes - exactly the same size as the file "RootSigFromCode.bin" we created earlier by filling in data structures in C++ and serializing them. Thus, we can say we just learned the way to create serialized root signature binary from the text representation. We can now connect two existing blocks in our diagram with the arrow leading from #5 to #2.

Note you can use our previous file "Shader2.hlsl" instead of "RootSig.hlsl" with the same effect. That file contains shader functions, but they just get ignored, as we only use the `MyRootSig`

macro.

Because there are so many ways of storing root signatures, Microsoft provided a possibility to convert between them using dedicated command-line parameters of DXC:

We can specify a compiled shader with a root signature embedded and extract only the root signature blob from it (connection from #6 to #2 in our diagram):

dxc -dumpbin -extractrootsignature -Fo RootSigExtracted.bin Shader2.vs.bin

The `-dumpbin`

parameter means that the input file (specified as the positional argument at the end) is a compiled binary, not a text file with HLSL source.

We can transform a compiled shader file into one with the embedded root signature removed. This path is not shown in the diagram. The output file "ShaderNoRootSig.vs.bin" has the same size (4547 B) as "Shader1.vs.bin" that we compiled previously without a root signature.

dxc -dumpbin -Qstrip_rootsignature -Fo ShaderNoRootSig.vs.bin Shader2.vs.bin

We can also join two binary files: one with compiled shader, one with root signature blob, and create a file with the shader and the root signature embedded in it. This is shown on the diagram as a path from #2 to #6.

dxc -dumpbin -setrootsignature RootSigFromCode.bin -Fo ShaderWithRootSigAdded.vs.bin Shader1.vs.bin

I've shown all these commands here, because it is very important to get them right. Microsoft did a terrible job here offering many options in the command-line syntax that can be misleading. For example:

`--help`

parameter, `-T rootsig_1_0`

profile is not shown among possible `-T`

options.`-E`

, while there is also parameter `-rootsig-define`

that looks like better suited for this task.`-Fo`

, while there is also parameter `-Frs`

that looks like better suited for this task, described as "Output root signature to the given file".Moreover, if you do it the wrong way, DXC prints some cryptic, unrelated error message or prints nothing, does nothing, and exits with process exit code 0. Not very helpful!

Radeon GPU Analyzer utilizes DXC internally, so it can be used to compile shaders from HLSL source code all the way to the pipeline state object (both stages of the shader compilation). That PSO is created internally just to extract the final ISA assembly from it. Here is a command we've seen before:

rga -s dx12 -c gfx1100 --all-hlsl Shader2.hlsl --all-model 6_0 --vs-entry VsMain --ps-entry PsMain --offline --isa AMD_ISA

However, RGA supports many more command-line options. Input shaders can be specified in HLSL format using `--all-hlsl FILE`

or per-stage `--vs FILE`

, `--ps FILE`

etc. with mandatory entry point function names passed as `--vs-entry NAME`

, `--ps-entry NAME`

, etc. Alternatively, we can specify compiled binary shaders as input. Then, the input is the intermediate shader representation, while RGA performs only the second stage of the shader compilation.

rga -s dx12 -c gfx1100 --vs-blob Shader2.vs.bin --ps-blob Shader2.ps.bin --offline --isa AMD_ISA

Similarly, a root signature can be specified in one of many ways:

1. Embedded in shaders, like in the 2 commands shown above, as our "Shader2" was compiled with the root signature.

2. From a separate HLSL file and specific `#define`

macro:

rga -s dx12 -c gfx1100 --all-hlsl Shader1.hlsl --all-model 6_0 --vs-entry VsMain --ps-entry PsMain --rs-hlsl RootSig.hlsl --rs-macro MyRootSig --offline --isa AMD_ISA

3. From a binary file with the serialized root signature:

rga -s dx12 -c gfx1100 --all-hlsl Shader1.hlsl --all-model 6_0 --vs-entry VsMain --ps-entry PsMain --rs-bin RootSigFromCode.bin --offline --isa AMD_ISA

4. None at all. Then, a root signature matching the compiled shaders gets auto-generated. This is a new feature of RGA 2.9.1.

rga -s dx12 -c gfx1100 --all-hlsl Shader1.hlsl --all-model 6_0 --vs-entry VsMain --ps-entry PsMain --offline --isa AMD_ISA

Up to this point, our discussion has centered around a C++ code specifically tailored for loading compiled shaders and establishing a PSO, typically for D3D12 rendering purposes, such as game development or other graphics applications. The compilation of shaders was exclusively carried out utilizing standalone command-line tools: DXC and RGA.

However, DXC shader compiler can also be used in form of a C++ library. Everything we can do with "dxc.exe" we can also do programmatically from our code by using equivalent library. To use the library:

`LoadLibrary`

"dxil.dll" and "dxcompiler.dll".`GetProcAddess`

of only one function: `DxcCreateInstance`

, as everything starts from it.I won't describe the library in details here. It is out of scope of this article, and the article is already very long. However, I would like to point to some interesting features:

1. Certainly, we can **compile a shader**. To do it, use function `IDxcCompiler3::Compile`

. Interestingly, we don't fill in data structures with specific parameters for the compiler, like we would normally expect from a programmatic API. Instead, we are asked to format a list of strings with parameters, same as we would pass to the command-line DXC, e.g.:

const wchar_t* arguments[] = {

L"-T ps_6_0",

L"-E PsMain",

// Etc...

};

Because we talk about root signatures here, it is worth noting that we can check if the compiled shader has one embedded. Calling `IDxcResult::GetOutput`

with parameter `DXC_OUT_OBJECT`

returns the compiled shader blob, `DXC_OUT_ERRORS`

returns a string with errors and warnings, while `DXC_OUT_ROOR_SIGNATURE`

tells us that the shader had a root signature attached.

2. The DXC library offers an interesting feature called **reflection**. It allows inspecting an existing compiled shader binary for various parameters, including inputs, outputs, and resource bindings. Inputs and outputs are vertex attributes or (in case of a pixel shader output) render targets written. The list of resource bindings is the most interesting for us here, because it allows to generate a root signature compatible with the shader.

Certainly, there isn't just one possible root signature compatible with a given shader, so a generated one may not align with your requirements. For example, a constant buffer b4 can be bound to a shader in one of 3 ways: as a 32-bit root constant, as a root CBV, or a descriptor table containing a CBV. Similarly, multiple subsequent slots like (b2, b3, b4) can be defined in a root signature as separate root parameters or as a single parameter with a descriptor table carrying `numDescriptors = 3`

. However, reflection can still be useful sometimes if you develop your own engine, and you want automate resource binding based on the shader code.

To use this feature, call `IDxcUtils::CreateReflection`

, pass the shader binary, and retrieve a new object of type `ID3D12ShaderReflection`

. You can then query it for parameters, like `ID3D12ShaderReflection::GetResourceBindingDesc`

. You can see an example of shader reflection used to generate the root signature in RGA source code - see file ["source/radeon_gpu_analyzer_backend/autogen/be_reflection_dx12.cpp"](https://github.com/GPUOpen-Tools/radeon_gpu_analyzer/blob/master/source/radeon_gpu_analyzer_backend/autogen/be_reflection_dx12.cpp) and other related places.

3. The DXC library also provides tools to **manipulate the binary container format**, enabling tasks such as extracting, adding, or removing a root signature from a shader. To use it, search the library header for interface `IDxcContainerReflection`

or a simpler function `IDxcUtils::GetDxilContainerPart`

, as well as interface `IDxcContainerBuilder`

. For example, you can check if a shader binary contains a root signature embedded using following code:

void* part_data = NULL; uint32_t part_size = 0;

HRESULT hr = dxc_utils->GetDxilContainerPart(&shader_binary,

DXC_PART_ROOT_SIGNATURE, &part_data, &part_size);

bool has_root_signature = SUCCEEDED(hr);

As for the policy regarding the usage of root signatures, do they need to match our shaders exactly? No, but the following rules apply:

`Texture2D<float4> normal_texture : register(t1)`

, but the root signature doesn't mention SRV at the slot t1, the PSO creation will fail with an error.You may ask: Can I just create one big all-encompassing root signature that defines all the resource bindings I may ever need and use it for all my shaders? Theoretically you could, but there are two main arguments against doing this.

`DescriptorTable(CBV(b0, numDescriptors=10))`

.On the other hand, switching root signature for every shader and rebinding all the root arguments can have its overhead too. If you look at Cyberpunk 2077, for example, you can see that they just use one big root signature for all graphics shaders and the second one for all compute shaders in the game. I am not disclosing any secret here. If you own the game on Steam or GOG, you can capture a frame using [PIX on Windows](https://devblogs.microsoft.com/pix/download/) and see it by yourself. If they could do it in a AAA game that looks and runs so well, do we really need to optimize better? 😀

Update 2024-05-15: In the comments below [my post on Mastodon](https://mastodon.gamedev.place/@Reg/112440830687368854), others disclosed that Frostbite engine by DICE, as well as the engine developed by Digital Extremes take the same approach.

This article offers a comprehensive description of various formats of root signatures in Direct3D 12. We've explored some C++ code along with the utilization of command-line tools such as the DXC shader compiler from Microsoft and the Radeon GPU Analyzer (RGA) from AMD. A root signature can be authored or stored as:

`D3D12_ROOT_SIGNATURE_DESC`

.`ID3D12RootSignature`

object.`ID3D12PipelineState`

, which is the final object used during rendering.`#define`

macro.We've learned how to use these representations and how to convert between them.

[Comments](https://asawicki.info/news_1778_shapes_and_forms_of_dx12_root_signatures#disqus_thread) |
[#directx](https://asawicki.info/news?x=tag&tag=directx) [#rendering](https://asawicki.info/news?x=tag&tag=rendering)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1778_shapes_and_forms_of_dx12_root_signatures&linkname=Shapes+and+forms+of+DX12+root+signatures)