---
title: Instant Radiosity using Optix and Deferred Rendering
url: http://graphicsrunner.blogspot.com/2011/03/instant-radiosity-using-optix-and.html
author: Kyle Hayward
published: '2011-03-28'
source_blog: Graphics Runner
source_site: http://graphicsrunner.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![cornell_gi_0 cornell_gi_0](../../assets/e83c6bd60f19757d.img)


This comes a little later than I wanted, I hadn’t factored in Crysis 2 taking up as much of my time as it did last week :-)

I’ve been using Nvidia’s

[Optix raytracing API](http://www.nvidia.com/object/optix.html)for quite some time, and decided that a good introduction to Optix and what it can do for you would be using it in an Instant Radiosity demo. The demo is fairly large so I won’t cover all of it here, as that would be entirely too long of a post, but just the main parts.

**Instant Radiosity**

Instant Radiosity is a global illumination algorithm that approximates the diffuse radiance of a scene by placing many virtual point lights that act as indirect light. The algorithm is fairly simple: for each light in the scene you cast N photon rays into the scene. At each intersection the photon either bounces and another ray is cast or, through Russian Roulette, is killed of. At each of the intersections you create a Virtual Point Light (VPL) that has the same radiance value as the photon. Once you have these VPLs you render them as you would any other light source.

One optimization that the demo makes is to divide the scene into a regular grid. For each grid voxel, we find all the VPLs in the voxel and merge them together to form a new VPL that represents the merged VPLs. Any voxels that don’t contain any VPLs are skipped. This dramatically reduces the number of VPLs that we need to render, and trades off indirect accuracy for speed. The following couple of shots demonstrate this idea. The image on the left shows the VPLs as calculated from our Optix program. The image on the right shows the merged VPLs.

![scattered_vpl scattered_vpl](../../assets/16205b74863fdaa5.img)


![grid_vpl grid_vpl](../../assets/764038be50e379f1.img)


**Optix**

Optix is Nvidia’s ray tracing API that runs on Nvidia GPUs (on G80 and up). Giving an overview to optix could take many blog posts so I won’t go that in depth here. There are a couple of SIGGRAPH presentations that give a good overview:

[http://nvidia.fullviewmedia.com/siggraph2010/04-dev-austin-robison.html](http://nvidia.fullviewmedia.com/siggraph2010/04-dev-austin-robison.html)

[http://graphics.cs.williams.edu/papers/OptiXSIGGRAPH10/](http://graphics.cs.williams.edu/papers/OptiXSIGGRAPH10/)

To create an optix program you essentially need two things: a ray generation program and a material program ( essentially a shader ) that gets called when a ray intersects geometry. The ray generation program does exactly as it sounds, it generates rays. The program is called for each pixel of your program’s dimensions. Rays cast by your ray generation program will traverse the scene for intersections, once a ray intersects geometry it will call its material program. The material program is responsible for say shading in a classic ray tracer, or any other computation you want to perform. In our case we’ll use it to create our Virtual Point Lights. So lets get down to business.

Here we have the ray generation program that will cast rays from a light. In the case of our cornell box room, we have an area light at the ceiling and we need to cast photons from this light.

RT_PROGRAM void instant_radiosity() { //get our random seed uint2 seed = seed_buffer[ launch_index ]; //create a random photon direction float2 raySeed = make_float2( ( (float)launch_index.x + rnd( seed.x ) ) / (float)launch_dim.x, ( (float)launch_index.y + rnd( seed.y ) ) / (float)launch_dim.y ); float3 origin = Light.position; float3 direction = generateHemisphereLightPhoton( raySeed, Light.direction ); //create our ray optix::Ray ray(origin, direction, radiance_ray_type, scene_epsilon ); //create our ray data packet and launch a ray PerRayData_radiance prd; prd.radiance = Light.color * Light.intensity * IndirectIntensity; prd.bounce = 0; prd.seed = seed; prd.index = ( launch_index.y * launch_dim.x + launch_index.x ) * MaxBounces; rtTrace( top_object, ray, prd ); }

So here we cast a randomly oriented ray from a hemisphere oriented about the direction of the light. Once we have our ray, we setup a ray data packet that will collect data as this ray traverses the scene. To cast the ray we make a call to rtTrace, providing the ray and its data packet.

Next we have our material program. This program is called when a ray hits the closest piece of geometry from the light. And it is responsible for updating the ray data packet, placing a VPL, and deciding to cast another ray recursively if we’re under the maximum number of bounces.

RT_PROGRAM void closest_hit_radiosity() { //convert the geometry's normal to world space //RT_OBJECT_TO_WORLD is an Optix provided transformation float3 world_shading_normal = normalize( rtTransformNormal( RT_OBJECT_TO_WORLD, shading_normal ) ); float3 world_geometric_normal = normalize( rtTransformNormal( RT_OBJECT_TO_WORLD, geometric_normal ) ); float3 ffnormal = faceforward( world_shading_normal, -ray.direction, world_geometric_normal ); //calculate the hitpoint of the ray float3 hit_point = ray.origin + t_hit * ray.direction; //sample the texture for the geometry float3 Kd = norm_rgb( tex2D( diffuseTex, texcoord.x, texcoord.y ) ); Kd = pow3f( Kd, 2.2f ); //convert to linear space Kd *= make_float3( diffuseColor ); //multiply the diffuse material color prd_radiance.radiance = Kd * prd_radiance.radiance; //calculate the ray's new radiance value // We hit a diffuse surface; record hit if it has bounced at least once if( prd_radiance.bounce >= 0 ) { //offset the light a bit from the hit point float3 lightPos = ray.origin + ( t_hit - 0.1f ) * ray.direction; VirtualPointLight& vpl = output_vpls[ prd_radiance.index + prd_radiance.bounce ]; vpl.position = lightPos; //the light's intensity is divided equally among the photons. Each photon starts out with an intensity //equal to the light. So here we must divide by the number of photons cast from the light. vpl.radiance = prd_radiance.radiance * 1.0f / ( launch_dim.x * launch_dim.y ); } //if we're less than the max number of bounces shoot another ray //we could also implement Russion Roulette here so that we would have a less biased solution prd_radiance.bounce++; if ( prd_radiance.bounce >= MaxBounces ) return; //here we "rotate" the seeds in order to have a little more variance prd_radiance.seed.x = prd_radiance.seed.x ^ prd_radiance.bounce; prd_radiance.seed.y = prd_radiance.seed.y ^ prd_radiance.bounce; float2 seed_direction = make_float2( ( (float)launch_index.x + rnd( prd_radiance.seed.x ) ) / (float)launch_dim.x, ( (float)launch_index.y + rnd( prd_radiance.seed.y ) ) / (float)launch_dim.y ); //generate a new ray in the hemisphere oriented to the surface float3 new_ray_dir = generateHemisphereLightPhoton( seed_direction, ffnormal ); //cast a new ray into the scene optix::Ray new_ray( hit_point, new_ray_dir, radiance_ray_type, scene_epsilon ); rtTrace(top_object, new_ray, prd_radiance); }

With both of these programs created we need to launch our optix program in order to generate the VPLs. When we’re done running the optix program, we gather all the VPLs into a grid, merging lights that are in the same voxel. Once the VPLs are merged, we add them to the deferred renderer.

//run our optix program mContext->launch( 0, SqrtNumVPLs, SqrtNumVPLs ); //get a pointer to the GPU buffer of virtual point lights. VirtualPointLight* lights = static_cast< VirtualPointLight* >( mContext["output_vpls"]->getBuffer()->map() ); //the following block merges the scattered vpls into a structured grid of vpls //this helps dramatically reduce the number of vpls we need in the scene if( mMergeVPLs ) { //Here we traverse over the VPLs and we merge all the lights that are in a cell for( int i = 0; i < TotalVPLs; ++i ) { optix::Aabb node = mBoundingBox; //start with the root cell and recursively traverse the grid to find the cell this vpl belongs to int index = 0; if( FindCellIndex( mBoundingBox, -1, mVoxelExtent, lights[ i ].position, index ) ) { //make sure we found a valid cell assert( index >= mFirstLeafIndex ); //subtract the first leaf index to find the zero based index of the vpl index -= mFirstLeafIndex; float3& light = mVPLs[ index ]; light += lights[ i ].radiance; } } //once the VPLs have been merged, add them to the renderer as indirect lights int numLights = 0; int lastIndex = -1; for( int i = 0; i < mVPLs.size(); ++i ) { const float3& vpl = mVPLs[i]; if( dot( vpl, vpl ) <= 0.0f ) continue; numLights++; float3 radiance = vpl; D3DXVECTOR3 pos = *(D3DXVECTOR3*)&mVoxels[i].center(); Light light = { LIGHT_POINT, //type GetColorValue(radiance.x, radiance.y, radiance.z, 1.0f), //diffuse pos, //pos Vector3Zero, //direction 1.0f //intensity }; renderer->AddIndirectLight( light ); //also add as a light source so we can visualize the VPLs LightSource lightSource; lightSource.light = light; lightSource.Model = mLightModel; renderer->AddLightSource( lightSource ); } }

Now for some eye candy. The first set are your typical cornell box + dragon. In the Instant Radiosity shot you can see the light bleeding from the green and red walls onto the floor, the dragon and the box.

Direct lighting:

![cornell_dl_0 cornell_dl_0](../../assets/c46a707af22c67c9.img)


Direct Lighting + Indirect VPLs:

![cornell_gi_0 cornell_gi_0](../../assets/6ccf5f7712d63f0e.img)


Direct Lighting:

![cornell_dl_1 cornell_dl_1](../../assets/f559140a697025bb.img)


Direct Lighting + Indirect VPLs:

![cornell_gi_1 cornell_gi_1](../../assets/626ea17bc07d83df.img)


The next set is from the sponza scene. Here too you can notice the red bounced light from the draperies onto the floor and in the ambient lighting in the shadows.

Direct Lighting:

![sponza_dl_0 sponza_dl_0](../../assets/f60644bb43406ce4.img)


Direct Lighting + Indirect VPLs:

![sponza_gi_0 sponza_gi_0](../../assets/0e9adafce31de106.img)


Direct Lighting:

![sponza_nobounce sponza_nobounce](../../assets/5d58d003c24802c1.img)


Direct Lighting + Indirect VPLs:

![spona_bounce spona_bounce](../../assets/7112fce907049250.img)


Direct Lighting:

![sponza_dl sponza_dl](../../assets/df566a40a88704b9.img)


Direct Lighting + Indirect VPLs:

![spona_il spona_il](../../assets/5bf2fc0ebac82965.img)


**Notes**

To Build the demo you’ll need boost 1.43 or later. To run the demo you’ll need at least an Nvidia 8800 series or later ( anything Computer 1.0 compliant ).

Files of interest are in the Demo project: OptixEntity.cpp and InstantRadiosity.cu.

Controls:

Show VPLs : L

Toggle GI : I

Toggle Merge VPLs : M

**Download:**

Sorry for requiring two download links but skydrive limits file sizes to 50MB

[OptixInstantRadiosity Part 1](http://cid-b80a3031b5bfa52b.office.live.com/self.aspx/Public/OptixInstantRadiosity%5E_Part1.zip)- Code

[OptixInstantRadiosity Part 2](http://cid-b80a3031b5bfa52b.office.live.com/self.aspx/Public/OptixInstantRadiosity%5E_Part2.zip)- Assets

## 9 comments:

Nice results! Do your virtual point lights have shadows?

Thanks!


Not yet. I was going to save that for another post.

Clever! Good looking results too - Thank you for the post.

Hey! Nice work! I cannot get to the code. I think the file is missing

I appreciate your source code.

However, when I run it, only blue window appears in the screen, no other response. Is there anything not correctly set?

Are there any errors that show up in the output? Optix has changed quite a bit since this demo was made. Also what Cuda version do you have? I don't exactly remember what version of cuda this works with. Probably 3.x


I recently moved so don't have my dev machine hooked up yet, so I won't be able to debug for awhile.

I am using cuda 4.0 and OptiX 2.5.1. But the cuda build rules is v3.0.14 as you set it.

When I move the pure blue window, an error appears saying D3DERROR_INVALIDCALL at reset device function.

"HR(mGDevice->Reset(&mD3DPresentParams));"

I am using CUDA 4.0 and OptiX 2.5.1. The cuda building role is 3.0.14 as you set. I guess the bug has something to do with directX since I re-size or move the pure blue window, an error appears saying invalid Call at reset device function. I am not very similar with DirectX. Also no stand output nor log output.

What's more, if no window re-size or moving operation (I mean do not move the window), no valid image appears.

Post a Comment