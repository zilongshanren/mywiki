---
title: 'Optix.NET: a managed wrapper for Nvidia Optix'
url: http://graphicsrunner.blogspot.com/2012/02/optixnet-managed-wrapper-for-nvidia.html
author: Kyle Hayward
published: '2012-02-02'
source_blog: Graphics Runner
source_site: http://graphicsrunner.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Optix.NET may head in the direction of CUDAfy where you can create your optix programs in-line with your C#. The current downside with Optix.NET is that you cannot share structs/classes with your Optix programs as you can when working with the original c/c++ library.

The Optix.NET SDK also comes with a (at the moment very) basic demo framework for creating Optix applications. Such as a basic OBJ model loader and simple camera.

As I talked a little about last post on Instant Radiosity, the general flow of Optix is:

- Create a context
- This is similar to a D3D Device.

- Create material programs
- These will run when there is an intersection and are akin to pixel shaders.

- Create intersection programs
- These are responsible for performing ray-geometry intersection.

- Create the main entry program / ray-generation program
- These will launch eye rays in a typical pinhole camera ray-tracer

- Load geometry data and creating a scene hierarchy
- Perform ray-tracing and display results.

This small tutorial will walk through the steps of Sample 6 in the Optix.NET SDK and create a simple program that will ray-trace a cow and shade it with its interpolated normals.

**Creating the Optix Context**

Context = new Context(); Context.RayTypeCount = 1; Context.EntryPointCount = 1;

Here we uh create our rendering context :-). We also set the ray type count. This tells optix how many different types of rays will be traversing the scene (e.g. Eye rays, indirect rays, shadow rays, etc ). EntryPointCount sets the number of main entry programs there will be.

**Creating the material**

Material material = new Material( Context ); material.Programs[ 0 ] = new SurfaceProgram( Context, RayHitType.Closest, shaderPath, "closest_hit_radiance" );

This creates a material that the geometry will use and assigns a SurfaceProgram (similar to a pixel shader), and tells Optix to run this shader on the closest ray-geometry intersection so that there is propery depth sorting.

**Creating geometry**

Next the geometry is loaded. For brevehity’s sake that part is omitted, but I show the important part of how you get your geometry into Optix.

First we create geometry buffers, similar to vertex and index buffers in D3D, and fill them with the positions, normals, texture coordinates, and triangle indices.

//create buffer descriptions BufferDesc vDesc = new BufferDesc() { Width = (uint)mVertices.Count, Format = Format.Float3, Type = BufferType.Input }; BufferDesc nDesc = new BufferDesc() { Width = (uint)mNormals.Count, Format = Format.Float3, Type = BufferType.Input }; BufferDesc tcDesc = new BufferDesc(){ Width = (uint)mTexcoords.Count, Format = Format.Float2, Type = BufferType.Input }; BufferDesc iDesc = new BufferDesc() { Width = (uint)mIndices.Count, Format = Format.Int3, Type = BufferType.Input }; // Create the buffers to hold our geometry data Optix.Buffer vBuffer = new Optix.Buffer( Context, ref vDesc ); Optix.Buffer nBuffer = new Optix.Buffer( Context, ref nDesc ); Optix.Buffer tcBuffer = new Optix.Buffer( Context, ref tcDesc ); Optix.Buffer iBuffer = new Optix.Buffer( Context, ref iDesc ); vBuffer.SetData<Vector3>( mVertices.ToArray() ); nBuffer.SetData<Vector3>( mNormals.ToArray() ); tcBuffer.SetData<Vector2>( mTexcoords.ToArray() ); iBuffer.SetData<Int3>( mIndices.ToArray() );

Next we create a Geometry node that will tell Optix what intersection programs to use, how many primitives our geometry has, and creates shader variables to hold the geometry buffers.

//create a geometry node and set the buffers Geometry geometry = new Geometry( Context ); geometry.IntersectionProgram = new Program( Context, IntersecitonProgPath, IntersecitonProgName ); geometry.BoundingBoxProgram = new Program( Context, BoundingBoxProgPath, BoundingBoxProgName ); geometry.PrimitiveCount = (uint)mIndices.Count; geometry[ "vertex_buffer" ].Set( vBuffer ); geometry[ "normal_buffer" ].Set( nBuffer ); geometry[ "texcoord_buffer" ].Set( tcBuffer ); geometry[ "index_buffer" ].Set( iBuffer );

Now we create a GeometryInstance that pairs a Geometry node with a Material (that we created earlier ).

//create a geometry instance GeometryInstance instance = new GeometryInstance( Context ); instance.Geometry = geometry; instance.AddMaterial( Material ); //create an acceleration structure for the geometry Acceleration accel = new Acceleration( Context, AccelBuilder.Sbvh, AccelTraverser.Bvh ); accel.VertexBufferName = "vertex_buffer"; accel.IndexBufferName = "index_buffer";

We then create an Acceleration structure ( or Bounding Volume Hierarchy ) that will create a spatial data structure that will optimize the ray traversal of the geometry. Here we create the Acceleration node with a Split BVH builder and a BVH traverser. This informs Optix how the BVH should be built and traversed. We also give the Acceleration structure the name of the vertex and index buffers so that it can use that data to optimize the building of the Split BVH (assigning the names of the vertex and index buffers is only required with Sbvh and TriangkeKdTree AccelBuilders ).

Next we create a top-level node to hold our hierarchy. We give it the acceleration structure and the geometry instance. Optix will use this top-level node to begin its scene traversal.

//now attach the instance and accel to the geometry group GeometryGroup GeoGroup = new GeometryGroup( Context ); GeoGroup.Acceleration = accel; GeoGroup.AddChild( instance );

**Create ray generation program**

Now comes the creation of our main entry ray generation program and set it on the Context. This will be responsible for creating pinhole camera rays.

Program rayGen = new Program( Context, rayGenPath, "pinhole_camera" ); Context.SetRayGenerationProgram( 0, rayGen );

**Create the output buffer and compile the Optix scene**

Finally, we create our output buffer, making sure to define its format and type. The BufferType in Optix defines how the buffer will be used. The BufferTypes are: Input, Output, InputOutput, and Local. The first three are self explanatory. Local sets up the buffer to live entirely on the GPU, which is a huge performance win in multi-gpu setups as it doesn’t require us copying the buffer from GPU memory to main memory after every launch. Local buffers are typically used for intermediate results ( such as accumulation buffers for iterative GI ).

BufferDesc desc = new BufferDesc() { Width = (uint)Width, Height = (uint)Height, Format = Format.UByte4, Type = BufferType.Output }; OutputBuffer = new OptixDotNet.Buffer( Context, ref desc );

Now we setup shader variables to that will hold our top level GeometryGroup, and OutputBuffer. Then Compile Optix (this will validate our node layout and programs are correct) and build the acceleration tree, which only needs to be done on initialization or when geometry changes.

Context[ "top_object" ].Set( model.GeoGroup ); Context[ "output_buffer" ].Set( OutputBuffer ); Context.Compile(); Context.BuildAccelTree();

**Ray-tracing and displaying results**

To ray-trace the scene we call Launch and give the size of our 2D launch dimensions and the index of our main entry program (zero).

Context.Launch( 0, Width, Height );

And to display the results, we get a pointer to the output buffer, and we use OpenGl’s draw pixels:

BufferStream stream = OutputBuffer.Map(); Gl.glDrawPixels( Width, Height, Gl.GL_BGRA, Gl.GL_UNSIGNED_BYTE, stream.DataPointer ); OutputBuffer.Unmap();

Results:

![cow cow](../../assets/7ed709d3ae3c102e.img)


And that’s pretty much it. A pretty simple program for doing GPU ray-tracing :-).

The current source, samples, and built executables are freely downloadable. Currently, I’ve got 5 samples that mimic the Optix SDK samples and will continue to add more to test functionality and eye candy.

You can download the current release and source here:

[http://optixdotnet.codeplex.com/](http://optixdotnet.codeplex.com/)

Or get the source directly with Mercurial here:

[https://hg01.codeplex.com/optixdotnet](https://hg01.codeplex.com/optixdotnet)

## No comments:

Post a Comment