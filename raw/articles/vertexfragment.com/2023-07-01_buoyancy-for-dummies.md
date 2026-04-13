---
title: Buoyancy for Dummies
url: https://www.vertexfragment.com/ramblings/buoyancy-for-dummies/
author: Steven Sell
published: '2023-07-01'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

Buoyancy adds an extra layer of realism to a game or simulation, allowing objects to float (or sink or neither). This ramble will provide a brief high-level overview of what is needed to add buoyancy to your project if you are a dummy, like me!

Typically in games a simplified model of the buoyant force is used, known as [Archimedes Principle](https://en.wikipedia.org/wiki/Archimedes%27_principle). In its most common form, the buoyant force which pushes upwards on the object is defined as:

$$F_{buoyant} = \rho V g$$

Where,

- \( \rho \) is
[the density](https://en.wikipedia.org/wiki/Density)of the displaced fluid. The density of water varies based on temperature (and salinity), but for simplicity we tend to use 1000 \( kg \over m^3 \),[which is it’s approximate peak density at 4 °C](https://www.usgs.gov/special-topics/water-science-school/science/water-density). - \( V \) is the volume of the displaced fluid.
- \( g \) is gravity.

At a high-level any object with a density less than your fluid (which we will assume to be water) will float, regardless of mass. An object with density greater than water will sink, and an object with density equal to water will do neither and remain in stasis. The rate at which the object rises or sinks is dependent on how close to the fluid density it is.

An object with a density of < 100 will effectively sit on top of the water (like a beach ball), a density of 500 will sit with half of its surface under the water, and as it gets closer to 1000 less and less will be above the water.

Applying the buoyant force to an object is relatively simple, just like the force function. However there is one important point of the formula that must be taken into consideration: \( V \) is the volume of the *displaced* fluid, not the volume of the object. As only a part of the object may be in the water, we need a way to know just how much of the object is displacing water.

For this particular approach to buoyancy, voxelization is used to split the object into distinct chunks that then individually apply buoyancy to the overall shape. While there are other approaches, such as mesh triangle slicing, they rely on slightly different buoyancy and force forumulas.

Once, as part of your object/entity definition, the object bounds are sliced into a collection of voxels. Each voxel as a whole is considered to be either under or above the water. Creating a voxelized representation of an object (whether using its render bounds or a collider) is relatively straightforward. [An example utility is provided in this gist](https://gist.github.com/ssell/652dfcd726a8ae57bd17cfdd21dfc260).

It should be noted that this simplified approach to buoyancy is more the suitable for most games which only require things like items, logs, simple rafts, etc. to float in the water. However it can be lacking if you require dynamic boat physics. In that case, [the more complex mesh-based buoyancy is required](https://www.gamedeveloper.com/programming/water-interaction-model-for-boats-in-video-games).

Personally I make use of both voxel and mesh buoyancy. Mesh-based buoyancy for boats, and voxel buoyancy for everything else.

In Unity, buoyancy should be applied during the `FixedUpdate`

which is the same update that physics is calculated. Applying buoyancy at a difference cadence (whether it be in `Update`

or some other step) can result in bugs or extra work for the physics engine. The general flow of your buoyancy update will likely resemble the following:

- Gather all buoyancy subdivisions and determine if they are above or below water.
- For each buoyancy subdivision,
- If it is above water, no action.
- If it is below water, calculate the buoyant force and apply it.


**Is Underwater**

One step that has been getting glossed over is checking if a point (whether a vertex or a voxel center) is underwater.

This is highly dependent on your particular project and how you have your water bodies implemented. Typically there are 3 types of water bodies:

- Infinite ocean plane (without waves)
- Infinite ocean plane (with waves)
- Complex water body shape (above sea-level lake, rivers, etc.)

If you use only (1) then your “is point underwater?” query can simply be `p.y < 0`

.

Personally, my project makes use of both (2) and (3) and so it has a generalized water body manager that allows for generic “is point underwater” queries. This manager uses a spatial partition to determine which water bodies, if any, the point may lie in and then checks against the current wave values.

If using waves it is vitally important that your CPU-side wave calculations are the exact same as those on the GPU-side if you are doing vertex shader based displacement. The visual rendering of the waves also needs to be as high fidelity as possible (whether using a high-poly base mesh and/or tesselation). This is because your wave queries will be using exact precision calculations whereas the rendered wave will be using stepped accuracy base on mesh density. This can lead to your object floating in mid-air if the water mesh is significantly lower resolution.

Alternatively if you can not use a high definition mesh (performance or stylistically limited), then that has to also be represented in your CPU-side queries and a interpolated value needs to be used to match the step size of the water mesh.

**Calculating Volume**

Only a single part of the buoyancy equation varies based on the object: \( V \).

As part of your buoyancy configuration you need to assign your object a mass (which in Unity is tied to the `Rigidbody`

) and a density. Again, this density is the key to everything and controls how slow/fast it sinks/floats. Density is defined as:

$$ \rho = {m \over V} $$

For the object we already know \( \rho \) and \( m \), and so we can rearrange to get \( V \):

$$ V = {m \over \rho } $$

And so our volumes can be calculated as:

```
TotalVolume = Mathf.Max(0.01f, Rigidbody.mass) / Density;
VoxelVolume = TotalVolume / Voxels.Count;
```


**Calculating Buoyancy**

Below is an excerpt from my own `RigidbodyBuoyancy`

class which serves as an example of how we calculate and apply the buoyancy.

```
private void ProcessBuoyancy(List<BuoyancyWaterData> waterDataSamples)
{
foreach (var waterSample in waterDataSamples)
{
if (!waterSample.IsInWater)
{
// Out of the water. Has no effect on buoyancy.
continue;
}
float depthScale = Mathf.Clamp01(waterSample.WaveHeight - waterSample.SamplePositionWS.y);
Vector3 archimedesForce = new Vector3(0.0f, waterSample.WaterBody.WaterDensity * VoxelVolume * -Physics.gravity.y, 0.0f);
Vector3 objectVelocity = Rigidbody.GetPointVelocity(waterSample.SamplePositionWS);
Vector3 localDampingForce = -objectVelocity * BuoyantDampingForce * Mathf.Max(0.01f, Rigidbody.mass);
Vector3 buoyantForce = localDampingForce + (depthScale * archimedesForce);
Rigidbody.AddForceAtPosition(buoyantForce, waterSample.SamplePositionWS);
}
}
```


`BuoyancyWaterData`

contains the results of a water query for a specific voxel and stores if the voxel is underwater, its depth, and its position (in both local and world-space). If the `waterSample`

is above the water then there is nothing to be done in regards to buoyancy.

If the sample is in the water,

- Calculate the
`archimedesForce`

which is our buoyancy function from the start. With the voxel-based representation we apply the entirety of the force upwards on the voxel. - Next, two different damping forces are calculated. These are not physically realistic, but they provide better results in Unity and help to prevent the object from launching out of the water like a rocket. A non-dummy could likely implement buoyancy without needing these, but again this ramble is written for dummies by a dummy.
`depthScale`

reduces the magnitude of the force as we get closer to the surface and helps to reduce jitter.`localDampingForce`

adjusts the force based on the current voxel velocity.

- Combine the
`archimedesForce`

and the damping forces to produce the final`buoyantForce`

. - Apply the
`buoyantForce`

to the voxel.

And that is it. Buoyancy really is quite simple, and to sum it up one last time:

- Subdivide your object based on either triangles or voxels.
- Check if the triangle or voxel is underwater.
- For each voxel that is underwater, calculate and apply the buoyant force.

If this dummy can do it, so can you!

For further reading/tutorials on the topic see these sources.