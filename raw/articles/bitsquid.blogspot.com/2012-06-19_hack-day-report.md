---
title: Hack Day Report
url: https://bitsquid.blogspot.com/2012/06/hack-day-report.html
author: Niklas
published: '2012-06-19'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Last Friday, we had our second *hack day* (aka *do-what-you-want day*, aka *google day*) at the office.

Different companies seem to take different approaches to hack days. At some places it just means that you can spend a certain percentage of your working week on your own projects. We wanted something that was a bit more focused and felt more like a special event, so we used the following approach:

People were encouraged to pick tasks that could be completed, or taken to a "proof-of-concept" level in a single day. The goal was that at the end of the day you should have something interesting to

*show/tell*your colleagues.It is ok to fail of course. Failure is often interesting. Trying crazy ideas with a significant risk of spectacular failure is part of the charm of a hack day.

A couple of days before the event, everbody presented their projects. The idea was to get everybody to start thinking about the topics, so that we could help each other with ideas and suggestions.

We ate breakfast together in the morning to start the discussions and get everybody in the spirit of the event. At the end of the day, we rounded off with a couple of beers.

We avoided Skype, email and meetings during the day, so that we could focus 100 % on the projects.

A couple of days after the events we had a small show & tell, where everybody could present what they had learned.


## Results

A number of interesting projects came out of this hack day:

Tobias and Mats created an improved highlighting system for indicating selected objects in the level editor. (Highlighting the OOBB works well for small objects, but for big things like landscapes and sub-levels, it is just confusing.)

Jim looked into a cross-platform solution for capturing screen shots and videos on target machines and transmitting them over the network.

Andreas created a Lua profiling tool, that can dynamically enable and disable profiling for any Lua function by hot-patching the code with profiler calls.

Finally, I rewrote the collision algorithm for our particle systems.


Being an egotistical bastard, I will focus on my own project.

Particle collision is one of those annoying things that it is difficult to find a good general solution to, for two reasons:

It ties together two completely different systems (particles and physics), creating an ugly coupling between them. Since the solution must have decent performance, the coupling must be done at a fairly low level, which makes it even worse.

Particles can have

*very*different collision requirements. Some effects need a massive amount of particles (e. g., sparks), but don't care that much about collision quality. As long as*most*of them bounce*somewhat*accurately, it is OK. Other effects may have just a single particle (e. g., a bullet casing). Performance doesn't matter at all, but if it doesn't bounce right you will surely notice. Handling both effects in the same system is a challenge. Having different systems for different effects is another kind of challenge.

My previous attempts at implementing particle collision have all been based on first cutting out a slice of the physics world around the particle effect and then trying to find a fast representation of the collision shapes in that world slice.

The problem with this approach is that there are a lot of variables to tweak and tune:

How big should the world slice be?

How much detail should there be in the simplified representation? More detail is slower, but gives better collision results.

What kind of representation should we use?

How should we handle dynamic/moving objects? How often should the world slice be updated?


I've tried a lot of different representations: a triangle soup, a collection of half-spheres, a height field, but none of them has given completely satisfactory results. Often, parameters that work for one effect at one location fail for a different effect at a different location. Both performance and behavior are hard to predict.

The main idea for the new approach came from a Naughty Dog presentation at GDC. Instead of trying to create a shared collision model for all particles, we give each particle *its own* collision model, and we store it inside the particle itself, together with the other particle data.

Of course, it would be expensive to store a complicated collision model inside every particle, so we use the simplest model possible: a plane. We can represent that by a normal and an offset from origin. So with this approach, the data for a particle might look something like this:

```
struct Particle {
Vector3 position;
Vector3 velocity;
Color8 color;
Vector3 collision_plane_normal;
float collision_plane_offset;
};
```

(Side note: Our particle data doesn't actually look like this, we use a "structure-of-arrays" approach rather than an "array-of-structures" and we don't have a fixed set of fields, each effect has its own set.)

Note that we don't bother with any flag for indicating whether there is plane or not. If there is no collision, we just put the collision plane far enough below the origin.

With this approach the collision test is super fast -- just a dot product and a compare. It is also really easy to parallelize the test or run it off-CPU, since it just uses local particle data and doesn't need to access any shared memory.

With this method we have divided the original collision problem into two simpler ones:

Collision test against a plane. (Trivial.)

Finding a suitable collision plane for each particle.


This means that if we want to, we can use different approaches for finding the collision planes for different effects. E.g., for static effects we could hard code the collision plane and avoid collision queries completely.

Generally, we can find a suitable collision plane for a particle by raycasting along its trajectory. If we didn't have any performance constraints, we could do a raycast for every particle every frame. That way we would always know what surface the particle would hit next, which means that we would get perfect collision behavior.

Of course, we can't *actually* do that. Raycasts are comparatively expensive and we want to be able to support large numbers of particles.

To control the performance, I exposed a parameter that lets the effect designer control how many raycasts per frame an effect is a allowed to make. A typical value of 1.0 means that every frame, one particle in the effect is picked at random, a raycast is performed along that particles trajectory and its collision plane is updated with the result.

Note that with this solution, the work is always evenly distributed over the duration of the effect. That is a lot nicer than what you typically get with the "world slice" approach where there is a big chunk of work in the beginning when you cut out the world slice.

Astute readers will have noticed a fatal flaw with the design as it has been presented so far: it can't possibly work for very many particles. If we have an effect with 1 000 particles and do a raycast every frame, it will take 33 seconds before every particle has found its collision normal. By then, they will long since have fallen through the floor.

So, if we want to use this approach for large numbers of particles we must be able to somehow reuse the collision results. Typically, an effect will have bundles of particles traveling in approximately the same direction. When one such particle has done a raycast and found a collision, we want to be able to share the result with its neighbors somehow.

I wanted to find a solution to this without having to create a complicated collision representation, because that would bring back many of the problems I had with the "world slice" approach. Eventually, I decided that since what we want to do is to cache a collision query of the form:

`(position, direction) -> collision_plane`

The simplest possible thing would be to store the results in a hash. Hashes are nice, predictable data structures with well known performance characteristics.

To be able to hash on position and direction we must quantize them to integer values. We can quantize the position by dividing the world into cells of a certain width and height:

```
const float cell_side = 0.5f;
const float cell_height = 2.0f;
int ix = position.x / cell_side;
int iy = position.y / cell_side;
int iz = position.z / cell_height;
uint64 key = HASH_3(ix, iy, iz);
```

In this example, I use a higher resolution along the xy-axes than along the z-axes, because typically that is where the more interesting features are. `HASH_3()` is a macro that performs the first three rounds of the *murmur_hash* algorithm.

To quantize the direction we can use a similar approach. I decided to quantize the direction to just six different values, depending on along which principal axis the particle is mostly traveling:

```
unsigned id;
if (fabsf(dir.x) >= fabsf(dir.y) && fabsf(dir.x) >= fabsf(dir.z))
id = dir.x > 0 ? 0 : 1;
else if (fabsf(dir.y) >= fabsf(dir.z))
id = dir.y > 0 ? 2 : 3;
else
id = dir.z > 0 ? 4 : 5;
key = key ^ id;
```

Now that we have computed a quantized representation of *(position, direction)*, we can use that as lookup value into our hash, both for storing and fetching values:

```
struct CollisionPlane {
Vector3 normal;
float offset;
};
HashMap<uint64, CollisionPlane> _cache;
```

(Side note: Unless I'm worried about hash function collisions, I prefer to hash my keys *before* I insert them in the *HashMap* and just use a `HashMap<uint64,T>` instead of `HashMap<MyComplicatedKeyStruct,T>`. That way the hash map uses less memory and lookups can be done with a simple modulo operation.)

Whenever I do a particle raycast I store the result in the cache. When particles are spawned they lookup their collision plane in the cache. Particles also query the cache every time they bounce, since that typically means they will be traveling in a new direction.

I have a maximum size that the cache is allowed to use. When the cache reaches the maximum size, older entries are thrown out.

## Results

The system gives high quality results for effects with few particles (because you get lots of raycasts per particle) and is still able to handle massive amounts of particles. The performance load is evenly distributed and it doesn't need any special cases for dynamic objects.

There are some drawbacks. The cache requires some tweaking. Since it can only store one collision plane for each quantization cell it will miss important features if the cells are too big. On the other hand, if the cells are too small, we need lots of entries in the cache to represent the world, which means more memory and slower lookups.

Since we only have one collision normal per particle, there are some things that the particles just can't do. For example, they can never come to rest at the bottom of a V-shape, because they will always only be colliding with one of the planes in the V. Overall, they will behave pretty badly in corners, where several collision planes with different normals meet. Some of these issues could be fixed by storing more than one collision plane in the particle, but I don't think it is worth it. I prefer the simpler approach and having particles that in some tricky situations can fall through the ground.

Compared to the old collision code, the new code is simpler, runs faster and looks better.

All in all, I would say that the hack day was a success. We had great fun and produced some useful stuff. We will definitely do more days like this in the future. Not too often though. I think it is important that these days feel like a special treat. If they become too mundane, something important is lost. Once a month or so, would be ideal, I think.

Have you considered removing the velocity component of the position (by projecting) before hashing? Two particles traveling along the same ray (but one is older) will have the same collision plane.


ReplyDeleteI guess this doesn't work exactly if the particles aren't traveling in straight lines - the older particle may have gone around an obstacle the younger one should hit :(

If you look at how the velocity is quantized you will see that I only take the direction of the velocity into account, not the speed. So I am already doing this.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThat's not quite what I meant. I was recommending putting two particles into the same hash bucket if they're moving along the same line - collapsing their positions together.




ReplyDeleteEg. particle A at p=(10, 10, 10) and v=(1, 0, 0)

and particle B at p=(20, 10, 10) and v=(1, 0, 0)

should have the same hash, because eventually A will reach B's current position.

Something like this before hashing:

p -= (p dot norm(v)) * norm(v)

Again, it only really works if the particles are only colliding with a convex set of planes, or moving in straight lines, or something like that. If there's a plane separating A from B, A won't see it.

Thanks for sharing the fun project :)




ReplyDelete>>With this approach the collision test is super fast -

>>- just a dot product and a compare.

No, the collision test has been moved to the ray test function.

The plane stored in each particle is basically the cached result of the collision detection/ray test. The smart part is using caching/hashing to avoid expensive ray tests.

So what geometry do you perform your ray test?

Do you use the physics engine data or graphics artwork or some "approximate geometry around the particle" ?

Yes, it is essentially a lossy/approximate cache hierarchy for collision tests. The lowest level is the plane stored in the particle. The next level is the hash.



ReplyDeleteI use the physics engine (PhysX) to perform the ray tests.

You could add more layers to the cache and have some approximate world slice thing above the hash, before you reach the "real physics". But I'm not sure if having more cache layers gives you anything that is worth the added complexity.

@Ian I see... regarding the particles as infinite lines you can define them with just a direction and a 2D offset in the plane normal to the line. You could use that for the hash key and get rid of one dimension.


ReplyDeleteThe problem is how to get that to work with quantization. With your approach, the further a particle is from origo, the more accurately you need to represent the direction in order to be able to "reconstruct" its full 3D position with any accuracy. (At large distances, even slight angle differences will cause the rays to diverge and hit very different parts of the geometry.)

I'm interested in the highlighting system that Tobias and Mats have come up with. Could they (or you) elaborate on that?


ReplyDeleteI imagine it has something to do with tinting the objects instead of drawing the bounding boxes, but I'd be interested in which situations they prefer bounding boxes and in which they prefer tinting.

Thanks!

@Malte The initial idea arose because sometimes a unit is composed of non-continuous geometry, or geometry with large holes in it. For example, imagine you're looking through a selected archway unit. The camera can't see the outside of the bounding box if it is inside the archway. Because of this situation, simply drawing the bounding box is not enough.




ReplyDeleteSince there are typically objects that would suffer from being drawn in a tinted fashion, such as navigation meshes, trigger volumes or other "editor-visible" geometry, we decided to show selection state using a colored wireframe overlay instead. This allows mesh selections to blend nicely with objects that use our standard line drawer. I.e. we can alter the line colors when drawing a selected trigger volume and have it look like the wireframe overlay on our mesh objects.

Tobias suggested we implement this wireframe overlay as a separate shader pass, since that would both be fast and yield correct results for skinned meshes, etc. The modifications we made to the engine were quite minor, and slotted nicely into our data-driven renderer. We basically added the option to define shader pass flags, and create passes in the shaders that could be enabled or disabled based on the state of those flags. We then proceeded to add a "wireframe" pass to the base shaders, which we enable when a mesh is selected.

To be honest, we didn't manage to fully implement the new selection style in that single hack day, but we hope to revisit it soon! In the meantime, the shader pass flags feature have yielded a substantial performance boost for dynamic light sources in an Android project using the engine. It is also used by other game projects to signal state changes such as poisoned or boosted characters, and in-game selection state. I think it is an interesting example of the indirect benefits a hack day can yield.

Nice Information! I personally really appreciate your article. This is a great website. I will make sure that I stop back again. These are some really great tips! Another important note is to make sure you give completely specific instructions to your cleaning staffs.



ReplyDeleteThanks, รอย ฮอดจ์สัน

https://fun88club.net/

https://zaza000.hatenablog.com/

https://188betgroup.com/

Your article is great. Come in, read my stuff, click. >> fun88club

ReplyDeletezaza000

188betgroup

บาคาร่า ออนไลน์




ReplyDeleteFun Casino in Bognor High Street at Cassino Amusements

Cassino is the place to have fun, enjoy the excitement of casino gaming in a relaxed, family-friendly environment. With Casino in Bangor High Street, you’ll be spoiled for choice. Our state-of-the-art facilities are guaranteed to put a smile on your face, with a wide selection of slot and gaming machines to cater to everyone.

You’ve done an excellent job breaking down a complex issue. I now feel much more confident about this topic.

ReplyDelete