---
title: 'The Rendering of Castlevania: Lords of Shadow 2'
url: https://www.elopezr.com/castlevania-lords-of-shadow-2-graphics-study/
author: Redorav
published: '2015-11-28'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

[Castlevania Lords of Shadow 2](https://en.wikipedia.org/wiki/Castlevania:_Lords_of_Shadow_2)was released in 2014, a sequel that builds on top of

[Lords of Shadow](https://en.wikipedia.org/wiki/Castlevania:_Lords_of_Shadow), its first installment, which uses a similar engine. I hold these games dear and, being Spanish myself, I’m very proud of the work

[MercurySteam](https://en.wikipedia.org/wiki/MercurySteam), a team from Madrid, did on all three modern reinterpretations of the Castlevania series (Lords of Shadow, Mirror of Fate and Lords of Shadow 2). Out of curiosity and pure fandom for the game I decided to peek into the Mercury Engine. Despite the first Lords of Shadow being, without shadow of a doubt (no pun intended), the best and most enjoyable of the new Castlevanias, out of justice for their hard work I decided to analyze a frame from their latest and most polished version of the engine. Despite being a recent game, it uses DX9 as graphics backend. Many popular tools like

[RenderDoc](https://github.com/baldurk/renderdoc)or the newest tools by

[Nvidia](https://developer.nvidia.com/nvidia-nsight-visual-studio-edition)and

[AMD](http://developer.amd.com/tools-and-sdks/graphics-development/gpu-perfstudio/)don’t support DX9, so I used

[Intel Graphics Analyzer](https://software.intel.com/en-us/gpa)to capture and analyze all the images and code from this post. While having a bit of graphics parlance, I’ve tried to include as many images as possible, with occasional code and in-depth explanations.

**Analyzing a Frame**

This is the frame we’re going to be looking at. It’s the beginning scene of Lords of Shadow 2, Dracula has just awakened, enemies are knocking at his door and he is not in the best mood.

**Depth Pre-pass**

LoS2 appears to do what is called a depth pre-pass. What it means is you send the geometry once through the pipeline with very simple shaders, and pre-emptively populate the depth buffer. This is useful for the next pass (Gbuffer), as it attempts to avoid overdraw, so pixels with a depth value higher than the one already in the buffer (essentially, pixels that are behind) get discarded before they run the pixel shader, therefore minimizing pixel shader runs at the cost of extra geometry processing. Alpha tested geometry, like hair and a rug with holes, are also included in the pre-pass. LoS2 uses both the standard depth buffer and a depth-as-color buffer to be able to sample the depth buffer as a texture in a later stage.

The game also takes the opportunity to fill in the stencil buffer, an auxiliary buffer that is part of the depth buffer, and generally contains masks for pixel selection. I haven’t thoroughly investigated why precisely all these elements are marked, but for instance was presents higher subsurface scattering and hair and skin have its own shading, independent of the main lighting pass, which stencil allows to ignore.

- Dracula: 85
- Hair, skin and leather: 86
- Window glass/blood/dripping wax: 133
- Candles: 21

The first image below shows what the overdraw is like for this scene. A depth pre-pass helps if you have a lot of overdraw. The second image is the stencil buffer.

**GBuffer Pass**

LoS2 uses a deferred pipeline, fully populating 4 G-Buffers. 4 buffers is quite big for a game that was released on Xbox360 and PS3, other games get away with 3 by using several optimizations.

**Normals (in World Space):**

R8 | G8 | B8 | A8 |
Normal.r | Normal.g | Normal.b | SSS |

The normal buffer is populated with the three components of the world space normal and a subsurface scattering term for hair and wax (interestingly not skin). Opaque objects only transform their normal from tangent space to world space, but hair uses some form of normal shifting to give it anisotropic properties.

**Albedo:**

R8 | G8 | B8 | A8 |
Albedo.r | Albedo.g | Albedo.b | Alpha * AOLevels |

The albedo buffer stores all three albedo components plus an ambient occlusion term that is stored per vertex in the alpha channel of the vertex color and is modulated by an AO constant (which I presume depends on the general lighting of the scene).

**Specular:**

R8 | G8 | B8 | A8 |
Specular.r | Specular.g | Specular.b | Fresnel Multiplier |

dp3_pp r0.w, r2, r3 //float NdotV = dot(worldViewVector, normalizedWorldNormal);The specular buffer stores the specular color multiplied by a fresnel term that depends on the view and normal vectors. Although LoS2 does not use physically-based rendering, it includes a Fresnel term probably inspired in part by the [Schlick approximation](https://en.wikipedia.org/wiki/Schlick%27s_approximation) to try and brighten things up at glancing angles. It is not strictly correct, as it is done independently of the real-time lights. The Fresnel factor is also stored in the w component.

1 2 | add_pp r1.w, -r0.w, c13.w //float3 invNdotV = 1 - NdotV; pow r0.w, r1.w, c11.y //float p = pow(invNdotV, FresnelLevels.y); |

**Ambient Lighting:**

R8 | G8 | B8 | A8 |
Ambient.r | Ambient.g | Ambient.b | AO Constant |

mov_sat_pp r0.xyz, r3 // float3 clampPosNormal = saturate(normalizedWorldNormal); // Positive NormalsThe Ambient buffer stores colored ambient lighting and occlusion. It takes the input vertex color and multiplies it by a constant AO factor (different from the AO factor for the albedo). Static geometry uses lightmaps, as is standard practice in many games, but animated geometry using normal maps uses a different technique. My first hypothesis without looking at the code was that they would be using [spherical harmonics](http://www.ppsloan.org/publications/StupidSH36.pdf), but after looking at the assembly I think it’s based on a [technique](http://www.valvesoftware.com/publications/2006/SIGGRAPH06_Course_ShadingInValvesSourceEngine.pdf) described by Valve in 2006 for Half-Life 2.

1 2 3 4 | mul_pp r0.xyz, r0, r0 // float3 sqPosNormal = clampPosNormal * clampPosNormal; mul r1.xyz, r0.y, c2 // float3 n1 = sqPosNormal.y * PreCalcAOColors2; mad r2.xyz, c0, r0.x, r1 // float3 n2 = PrecalcAOColors0 * sqPosNormal.x + n1; mad_pp r0.xyz, c4, r0.z, r2 // float3 aoPosColor = PreCalcAOColors4 * sqPosNormal.z + n2; |

1 2 3 4 5 | mov_sat_pp r1.xyz, -r3 // float3 clampNegNormal = saturate(-normalizedWorldNormal); // Negative normals mul_pp r1.xyz, r1, r1 // float3 sqNegNormal = clampNegNormal * clampNegNormal; mul r2.xyz, r1.y, c3 // float3 m1 = sqNegNormal.y * PreCalcAOColors3; mad r4.xyz, c1, r1.x, r2 // float3 m2 = sqNegNormal.x * PreCalcAOColors1 + m1; mad_pp r1.xyz, c5, r1.z, r4 // float3 aoNegColor = sqNegNormal.z * PreCalcAOColors5 + m2; |

The technique works like this (look at the assembly to follow what I say): first the normal is calculated in world space, and the positive and negative components separated. Then those components are squared, and multiplied by two different matrices contained in PrecalcAOColors, which is passed as a constant. These matrices are described in the Valve paper as an Ambient Cube, containing six colors. It is a technique that was developed around the time that spherical harmonics were developed, but is more compact as it only uses 6 colors (9 are needed for the most basic spherical harmonics) and is faster to evaluate.

1 2 3 | add_pp r0.xyz, r0, r1 // float3 sumColors = aoPosColor + aoNegColor; mul r0.xyz, r0, c8.y // float3 finalColors = sumNormals * PrecalcAOLevels.y; mad_pp oC3.xyz, v1, c8.x, r0 // AO.xyz = VertexColor * PrecalcAOLevels.x + finalColors; |

After that both contributions are added and multiplied by a constant, and then added back again to the vertex colors. The last component is a constant coming from either the lightmap for static geometry, or the PrecalcAOLevels (light probes) for dynamic geometry.

**Lighting Stage**

After the GBuffer has been created, the lighting pass takes all those components and merges them with the realtime dynamic lights. LoS2 uses a combination of real-time lights and cubemaps to get the dark atmosphere that is characteristic of the game.

**Environment Background**

The first thing that happens during the lighting stage is a cubic environment is rendered to the far plane. We don’t see it because we’re inside the castle, so I need to put a shot where we go outside. In Dracula’s Castle, the backdrop is a hi-resolution, dark cloudy night sky with mountains. It is rendered as four separate quads that surround the player. Here is an outdoors shot where you can see the effect, and the actual cube that is used. Try rotating it to see what it looks like.

**Cube Pass**

I call this the cube pass because LoS2 renders a big cube that encompasses the environment as their main lighting pass. It’s an interesting decision, since this can also be done by simply rendering a full-screen quad. This pass renders all the environment lighting such as ambient lighting (read from the gbuffer pass) and reflections coming from a baked cubemap. This is the most expensive step of the main lighting pass. It’s not surprising given it’s sampling five textures (depth + 4 gbuffer) and a cubemap for every pixel on screen, plus computing all the lighting. Extracting the lighting equation is not straightforward, since many steps are hidden behind other steps and the logic is not always easy. After simplifying it, I think the equation reduces to this:

In the equation, environment means the texel read from the cubemap, K1 and K2 are a way of abstracting different scaling constants uploaded to the shader, and specular, ambient and albedo all come from the G-Buffer. SSS is the subsurface scattering, also computed from the G-Buffer parameters. Here you can see the cubemap used, the resolution is surprisingly low, 128×128.

[canvasio3D width=”320″ height=”320″ border=”0″ borderCol=”#333″ dropShadow=”4″ ambient=”#FFFFFF” backCol=”#FFFFFF” backImg=”…” mouse=”on” rollMode=”auto” rollSpeedH=”5″ rollSpeedV=”0″ objPath=”https://www.elopezr.com/wp-content/uploads/2015/12/CLOS2_Cubemap.obj” objScale=”50″ objColor=”#FFFFFF” lightSet=”8″ reflection=”off” refVal=”5″ objShadow=”off” floor=”off” floorHeight=”42″ lightRotate=”off” Help=”off”] [/canvasio3D]

[canvasio3D width=”320″ height=”320″ border=”0″ borderCol=”#333″ dropShadow=”4″ ambient=”#FFFFFF” backCol=”#FFFFFF” backImg=”…” mouse=”on” rollMode=”auto” rollSpeedH=”5″ rollSpeedV=”0″ objPath=”https://www.elopezr.com/wp-content/uploads/2015/12/CLOS2_Cubemap_Backface.obj” objScale=”200″ objColor=”#FFFFFF” lightSet=”8″ reflection=”off” refVal=”5″ objShadow=”off” floor=”off” floorHeight=”42″ lightRotate=”off” Help=”off”] [/canvasio3D]

**Fill Discrete Lights**

LoS2 uses point lights and spot lights, as many other games do, and also includes something I haven’t often seen, “box lights”. They’re basically a box that emits light, and from what I can see is generally used as a filler used to make metallic objects shine and bloom. The first slide below is the result of the cube pass, the following are the fill discrete lights with their bounding geometry. Keep in mind the images below are not how the final image is going to look. The lighting stage takes place in an HDR buffer and still needs to be tonemapped, which is why the colors don’t look right.

**Shadow Casting Lights**

The next lights to be rendered are shadow casting lights. Because these lights produce shadows, they first need to render their associated shadow maps, which they then sample in the lighting pass. Shadow map generation is interleaved with lighting and I won’t go into much more detail, below you can see the shadow maps for the main spotlight coming from the throne (not seen in the shot) and for a window. You can also see the kind of geometry used for the spotlight and the point light.

Aside from the shadow casting light, the last still contains a step where we add a bit of fog via a fog volume, mist, god rays and, for some reason, spider webs (you can see them hanging from the far column).

The approach to mist and godrays in this scene is nothing too fancy as they use simple geometry to simulate the effects. It’s very subtle so if it’s not clear what I mean by that consider the following images. The first two stills are the geometry that fakes these effects, and the last two are before and after the effect.

**Alpha Stage**

After all the opaque geometry has been rendered, all the transparent (or alpha) geometry must be rendered. There’s a very good explanation for why alpha geometry must go in a separate stage [here](http://www.john-chapman.net/content.php?id=13). The way LoS2 handles this problem is a common approach, to have a separate forward rendering path in the engine. What it means is: render each object, computing its lighting as you render it. The best examples for this type of geometry are glowing objects, particles, etc. If you look around the scene you will see that we’re still missing candle glows and fire, and Dracula’s arm hasn’t been rendered yet. This is because his arm is a special weapon, turning it into a particle emitter for the game.

**HDR to LDR**

After rendering all the geometry and light effects in the **H**igh **D**ynamic **R**ange buffer (which is 16 bits per pixel), we must transform those high range values into colors the monitor can display, or **L**ow **D**ynamic **R**ange. Bloom, exposure, lens flares and tonemapping also get factored in, with many intermediate buffers involved. I will detail them in this section.

**Luminance**

Before doing any calculations, there is an HDR to RGBA8 (LDR) range fitting step. We could potentially do all calculations in the HDR buffer, but they are slower than 8-bit buffers, so the game trades math for bandwidth. The first step basically calculates the luminance of the HDR pixel, divides the HDR pixel value by its luminance and also stores the luminance in the w component of the RGBA8 buffer. The colors in the following images look very odd because of this, but bear with me until the curtain is drawn!

1 2 3 4 5 6 7 8 | dp4_sat_pp r0.w, r1, c0.zzzw // float luminance = saturate(dot(hdrColor, float4(1/32, 1/32, 1/32, 1/255)); mul_pp r0.w, r0.w, c1.x // float luminance_255 = luminance * 255; frc_pp r1.w, -r0.w // float lumFrac = - frac(luminance_255); add_pp r1.w, r0.w, r1.w // float lumWhole_255 = luminance_255 - lumFrac; mul_pp r0.w, r1.w, c1.y // float lumWhole_0_32 = lumWhole_255 * 32 / 255; rcp_pp r0.w, r0.w // float invlumWhole_0_32 = 1 / lumWhole_0_32; mul_pp oC0.w, r1.w, c0.w // buffer.w = lumWhole_255 / 255; mul_pp oC0.xyz, r0, r0.w // buffer.xyz = hdrColor * invlumWhole_0_32; // hdrColor / luminance |

**Motion Blur**

Motion blur is achieved by creating a fullscreen motion difference render target, by using the current frame and last frame’s camera matrices. This effectively gives us a vector of “how much” and in which direction the camera has moved/rotated since last frame. This is also done for characters, since they have motion independent of the camera and can have motion blur by themselves (running, jumping, etc) The next shader then samples the previous color buffer several times in the direction of motion and merges all the colors together, creating the typical motion streaks. Since there is little motion blur in the main shot, I have captured another shot with the camera rotating around the player. Green regions in the image have little motion, whereas red indicates faster motion (in screen space).

**Dynamic Exposure**

Next the luminance is extracted from this buffer’s alpha channel and downsampled to another buffer half the size, and after that a chain of several smaller square textures is created from this downsampled buffer. These textures only sample and store the luminance, a popular technique to obtain the average luminance in a scene. As the square images are downsampled, they sample the neighboring pixels and obtain their average value. If this is done repeatedly until only one pixel is left, we effectively obtain a single pixel whose value is the average luminance for the entire scene. An image is worth a thousand assembly instructions, so here is the process:

**Bloom and lens flares**

Bloom uses a fairly standard technique, which consists of selecting pixels that are very bright (remember that HDR buffers contain colors that may be higher than 1) and downsampling to a smaller image, then repeatedly blurring them to get a soft highlight. After that, the bloom texture is composed onto the final image. LoS2 downsamples and blurs once, then adds lens flares and does a second blur pass. The game needs the first bloom pass to detect what parts of the image are very bright, as that is where they render the lens flares. This sometimes presents issues with very bright scenes, with too many distracting lens flare effects piling up on screen.

**Tonemapping**

Typically, the last step in any HDR to LDR chain would be tonemapping, and most games use [filmic operators](http://filmicgames.com/archives/75). I’m not familiar with the operator LoS2 is using. They have most certainly embedded it with gamma correction, so it’s surely hidden somewhere. The shader formula for the tonemapping is the following:

1 | finalColor = saturate(sqrt(FilmicParams.z * (1.0 - exp(-finalColor))) - Exposure.z); |

For this scene, FilmicParams.z = 1.33 and Exposure.z = 0.03. If I plot both this tonemapping operator and the square root typically used for gamma correction, I get this:

You can see that it preserves the general shape of the gamma correction up to the mid-greys, and then tones down the whites to be darker at the very end of the curve.

**Vignette**

For completeness, I mention the vignette effect, which uses a simple texture to give a more “Instagramy” look to the scenes. You can see how the final shot is darkened at the edges. Bright pink means not darken, bright blue means darken.

![CLOS2 Vignette](../../assets/db03806acd5907af.png)


The last step is a shader that mixes all of these effects onto the screen, in what is almost the final image. Since they all run in the same shader there are no steps I can show where they are incrementally added.

**Finishing Touches**

One of the last effects to be added is also one of the most immersive. It tries to mimic the tiny dust particles that accumulate in the lens of a camera and create interesting circular halos around images. Lots of small quads are rendered onto the screen with the textures shown to the right. These little specks are then multiplied by the background color of the bloom render target, creating an interesting camera lens effect. It’s more interesting in motion, in this shot you can see it on top of Dracula’s arm.

**AA & Sharpen Image**

The very final touch is to add a touch of antialiasing and a sharpen image pass. The sharpening of the image tries to compensate for the blurring introduced by the antialiasing if it’s too aggressive and give it more crispness.

**Links**

This post was inspired by [Adrian Courrèges](http://www.adriancourreges.com/)‘s series of graphics studies. Check his website out to see some very interesting graphics studies.

[Mercury Steam](http://mercurysteam.com/) is developing, at the time of writing, what is rumored to be a new installment in the Contra series. Stay tuned for their news.