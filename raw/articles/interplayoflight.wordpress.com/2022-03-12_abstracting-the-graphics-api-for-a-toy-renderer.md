---
title: Abstracting the Graphics API for a toy renderer
url: https://interplayoflight.wordpress.com/2022/03/12/abstracting-the-api-for-a-toy-renderer/
author: Kostas Anagnostou
published: '2022-03-12'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I’ve been asked a few times in DMs what is the best way to abstract the graphics API in own graphics engines to make development of graphics techniques easier. Since I’ve recently finished a first pass abstraction of DirectX12 in my own toy engine I’ve decided to put together a post to briefly discuss how I went about doing this.

Modern, low level APIs like DX12 and Vulkan are quite verbose, offering a lot of control to the developer but also requiring a lot of boilerplate code to set up the rendering pipeline. This prospect can seem like a daunting task to people that want to use such an API and often reach out to ask what is the best way to abstract it in their own graphics engines.

People have different reasons why they create their own graphics engines from scratch, one could be to learn a graphics API, another could be to learn more about modern renderers (multithreading, efficient submission, render graphs etc), others to implement graphics techniques.

My reason for developing a personal graphics engine (what I affectionately call a toy renderer) is primarily to implement and experiment with graphics techniques. In my day job I care a lot about performance, scalability and renderer architecture design. For my own projects not so much, I want something that will allow me to tinker with stuff without having to worry too much about efficient designs. The abstraction of my toy engine reflects this.

When I started implementing the (then new) DX12 engine I grabbed the [simplest sample](https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/Samples/Desktop/D3D12HelloWorld) I could find in the DirectX SDK and built upon it to create a simple deferred renderer to get a mesh rendering on screen. It took some effort and a lot of boilerplate code.

The first thing that called for abstraction was resources eg textures, rendertargets, constant buffers etc. Creating a series of Texture, Rendertarget and Buffer classes can nicely abstract this (I don’t want to add too much code to the post, [check this](https://github.com/microsoft/DirectX-Graphics-Samples/blob/master/Samples/Desktop/D3D12HelloWorld/src/HelloTexture/D3D12HelloTexture.cpp) for the code that is required to create a texture). For example the Texture class is using [stb](https://github.com/nothings/stb) to simplify texture loading:

```
Texture* texture = new Texture( filename, device, commandList);
```

Or to create constant buffer

```
Buffer::Description cbDesc;
cbDesc.m_elementSize = sizeof(MainViewGlobalCBData);
cbDesc.m_descriptorType = Buffer::DescriptorType::CBV;
m_mainViewCB = new Buffer(cbDesc, L"Main view CB");
```

This can easily be extended to support any type of buffer. The aim is to hide all common settings and state and expose only the ones that we need to differentiate between each buffer.

The next thing that called for abstraction, based of frequency of creation, was Root Signatures and Pipeline State Objects. This was trickier, the problem with this is not the code required to set it up so much but the amount of data it requires (and that it can be quite error prone if done wrongly). The Direct SDK samples’ [Miniengine](https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/MiniEngine) offers a pretty good abstraction one can base theirs on, but it still became cumbersome in the end, encouraging a lot of copy-pasting. I also disliked the two part setting up of this, a “Create” phase to create the root signatures and PSOs and the “Render” phase to actually use it, this created some friction given the limited available time I have to spend on implementing a technique.

For this one I had to bite the bullet and abstract it fully. I created a context that collects all resource setting during Render-time submission and just before the Draw it creates the root signature and the PSO based on what is already bound, for example:

```
m_context->Reset();
m_context->SetTexture(0, albedoRT);
m_context->SetTexture(1, normalsRT);
m_context->SetTexture(2, m_depthStencil);
m_context->SetBuffer(0, m_lightingCB);
m_context->SetBuffer(1, m_lightsCB);
m_context->SetBuffer(2, m_shadowAtlasCB);
m_context->SetSampler(0, SamplerPointClampDesc);
m_context->SetSampler(1, SamplerLinearWrapDesc);
```

For the first pass implementation I provide the register indices by hand, I didn’t implement any shader reflection to extract this information from the shader. The context wraps a command list, and with minimal changes it can be multithreaded (although I haven’t pursued this yet).

Also, all root signatures and PSO created are cached and reused, this is important to avoid the cost of recreating them every frame. For a good system to base caching in your own engine it is worth studying the [MiniEngine ](https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/MiniEngine)project in the DirectX SDK.

This abstraction was very liberating as it allowed me to mostly scrap the “Create” phase for root signatures and PSOs and made changing the render pass to add or remove resources a doddle. This opened the appetite for more.

Adding new resources, even with the new abstraction classes I discussed above (Texture, Buffer etc), has the overhead of managing them, create and store the pointers somewhere, ensure that I delete them in the end and also makes reuse trickier. Out goes manual management, in come Resource Managers.

```
Rendertarget::Description desc = {
m_width,
m_height,
DXGI_FORMAT_R8G8B8A8_UNORM,
D3D12_RESOURCE_FLAG_ALLOW_RENDER_TARGET,
clearColor
};
Rendertarget* albedoRT = m_rendertargetManager.FindOrCreate(L"AlbedoRT", desc);
```

The RendertargetManager for example not only creates the resource based on the description provided, it will also cache it and never create it again. It also supports transient rendertargets that can be used in one pass and returned to the pool to be used in another pass. It will also release all rendertargets when the application ends. Similar managers simplify management of textures, buffers etc.

What’s next, shaders!

```
D3D_SHADER_MACRO shaderMacros[] = { "ENABLE_RTR", "1", NULL, NULL };
ShaderDesc csDesc = { "Reflections_RT", L"HybridSSR.hlsl", "CSMain", "cs_5_1", D3DCOMPILE_ENABLE_UNBOUNDED_DESCRIPTOR_TABLES, shaderMacros };
m_shaderManager.Create(csDesc);
```

The shader is created only once, cached and can be retrieved by name. One note on accessing resources by string, it can be very flexible but it can be error prone. An enum may be safer.

Want to create a vertex shader? Just provide an input layout:

```
std::vector<D3D12_INPUT_ELEMENT_DESC> inputLayout = {
{ "POSITION", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 0, D3D12_INPUT_CLASSIFICATION_PER_VERTEX_DATA, 0 },
{ "NORMAL", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 12, D3D12_INPUT_CLASSIFICATION_PER_VERTEX_DATA, 0 },
{ "TEXCOORD", 0, DXGI_FORMAT_R32G32_FLOAT, 0, 24, D3D12_INPUT_CLASSIFICATION_PER_VERTEX_DATA, 0 }
};
ShaderDesc vsDesc = { "ShadowmapVS", L"ShadowmapPass.hlsl", "VSMain", "vs_5_1", 0, nullptr, inputLayout };
m_shaderManager.Create(vsDesc);
```

During Render I can retrieve the shader and set it to the context by simply calling

```
m_context->SetComputeShader(m_shaderManager.Get("Reflections_RT"));
```

The PSO creation pass will pick it up and add it to the PSO just before the dispatch.

Automating resource and state creation and management simplified implementing of rendering passes immeasurably. This for example is a complete, self contained, render pass to render GTAO in my toy engine:

```
Rendertarget::Description desc = { m_width, m_height, DXGI_FORMAT_R8G8B8A8_UNORM, D3D12_RESOURCE_FLAG_ALLOW_UNORDERED_ACCESS, { 0,0,0,0 } };
Rendertarget* gtaoRT = m_rendertargetManager.FindOrCreate(L"GTAORT", desc);
Rendertarget* normalsRT = m_rendertargetManager.Find(L"NormalsRT");
Buffer::Description cbDesc;
cbDesc.m_elementSize = sizeof(GTAOCBData);
cbDesc.m_descriptorType = Buffer::DescriptorType::CBV;
Buffer* gtaoCB = m_bufferManager.FindOrCreate(L"GTAO CB", cbDesc);
GTAOCBData cbData;
cbData.InvProjection = m_camera.m_invProjection;
cbData.WorldToView = m_camera.m_worldToView;
cbData.ViewToWorld = m_camera.m_viewToWorld;
cbData.RTSize = { (float)m_width, (float)m_height, 1.0f / m_width, 1.0f / m_height };
cbData.FrameIndex = m_frameCount;
m_bufferManager.Update<GTAOCBData>(gtaoCB, &cbData);
m_context->Reset();
ShaderDesc csDesc = { "GTAOCS", L"GTAO.hlsl", "CSMain", "cs_5_1" };
Shader* shader = m_shaderManager.Create(csDesc);
m_context->SetComputeShader(shader);
m_context->SetSampler(SamplerLinearClampDesc);
m_context->SetSampler(SamplerPointClampDesc);
m_context->SetTexture(m_depthStencil);
m_context->SetTexture(normalsRT);
m_context->SetBuffer(gtaoCB);
m_context->SetTextureRW(gtaoRT);
const uint32_t threadGroupSizeX = m_width / 8 + 1;
const uint32_t threadGroupSizeY = m_height / 8 + 1;
m_context->Dispatch(threadGroupSizeX, threadGroupSizeY, 1);
```

The context, having cached all resource, shader and state setting required for the Dispatch can create the root signature, PSO and actually bind the resources just before the actual dispatch.

This scheme encourages experimentation, it is easy to add and remove resources or create variations of a graphics technique. For my purposes, where I want to implement and iterate on graphics techniques, this is perfect. It is worth stressing that this approach works great for own projects but will not scale well for production code (hence the characterisation “toy engine”).

In all cases my answer to the question of how to abstract the graphics API is don’t, at least at the beginning. I have implemented a lot of personal graphics engines over the years and I’ve never started with the abstraction. In every case I have found that the need for abstraction will arise naturally as one starts to put together the engine and will change based on the use case and what people want out of the engine.