---
title: Picking and Hit-Testing in Metal
url: https://metalbyexample.com/picking-hit-testing/
published: '2018-11-07'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

In this article, we’ll see how to interact with our 3D scenes using a technique called *picking*. Picking helps us answer the question “What did the user just tap on?” More precisely, picking is the process of determining which object or objects in our scene are being indicated by an interaction like a mouse click or a touch on the screen. Picking is frequently used in 3D modeling and CAD programs to select objects for further manipulation, but many applications eventually require the user to interact with the scene, and picking is an essential tool for enabling such interactions.

Picking is mostly synonymous with [ hit-testing](https://en.wikipedia.org/wiki/Hit-testing), which is the more commonly-used term when discussing 2D graphical user interfaces. In fact, you may already be acquainted with

[UIKit’s model for hit-testing](https://developer.apple.com/documentation/uikit/uiview/1622469-hittest). For the purposes of this article, picking and hit-testing are identical.

You can view and download the sample code for this article [here](https://github.com/metal-by-example/metal-picking).

![A demonstration of selecting objects with picking](../../assets/422dd385825938d1.gif)


In order to understand how picking works, we need a solid understanding of coordinate spaces. This means we need to know how the vertices in our 3D models undergo transformation on their long journey to becoming pixels on the screen. Since this is so crucial to understanding how to actually do picking, let’s review the relevant coordinate spaces. If you feel comfortable with coordinate spaces, feel free to skip on down to the section titled [“Interaction”](https://metalbyexample.com#Interaction).

## A Brief Review of Coordinate Spaces

There are five coordinate spaces we need to understand: model space, world space, view space (also called camera space or eye space), clip space (closely related to normalized device coordinates), and screen space (also called window space, closely related to viewport space).

### Model Space to World Space

Recall that the vertices of a 3D model live in *model space*, meaning they are specified relative to the origin of the model. Since we often have more than one model in our scene, we provide each object with a model transformation, which transforms it from model space to *world space*, which is the global coordinate space in which all of our objects are positioned.

In a scene graph system such as SceneKit, the transform of the scene’s root node specifies world space. When nodes are added to a scene graph, their transformations combine in a hierarchy to position objects relative to one another. Under such a scheme, the model(-to-world) transformation of an object is the concatenation of the node’s transformation with the transformations of all of its ancestors in the scene graph, down to the root node.

### World Space to View Space

Now that we have all of our objects in a unified world space, we need to position them relative to the camera, which we do with the so-called *view transformation*. The view transformation is often computed as the inverse of the transformation matrix of the node the camera is attached to. Multiplying vertices in world space by the view transformation “positions” the portion of the scene that is visible “in front of” the virtual camera.

### View Space to Clip Space

The view transformation only partially describes the portion of the scene that is visible, however. It tells us where the camera *is*, but it doesn’t specify how wide or far it can *see*. Several additional parameters are required to specify the *view frustum*, which is the [pyramid-shaped volume](https://en.wikipedia.org/wiki/Frustum) that contains all of the visible objects in the scene. This frustum is defined by the camera position and orientation (i.e., the view transformation), as well as the camera’s field-of-view, aspect ratio, near plane distance, and far plane distance.

These parameters are used to compute the camera’s *projection transformation*. The purpose of the projection transformation is to move from view space to *clip space*, which is a hemi-cubical 1 shape bounded by the six planes that define the view frustum (i.e., the top, left, bottom, and right planes, truncated by the near plane and far plane).

### Clip Space to Screen Space

Up to this point, we’ve been discussing transformations that are entirely under our control as API users. In other words, we are responsible for calculating and combining the matrices associated with these transformations and applying them to vertices in the vertex function. Once vertices (in clip space) are returned from the vertex shader, the fixed-function *rasterizer* kicks in and performs additional transformations that are outside our control, but that are nevertheless important to understand.

Firstly, the x, y, and z components of every vertex are divided by the *w* component, which moves us from *homogeneous* clip space into Cartesian *normalized device coordinates*, where the x and y components of every vertex that lies inside the view frustum has a value between -1 and 1, and every z component has a value between 0 and 1.

These normalized device coordinates are scaled and biased (multiplied and shifted) so that they cover the viewport (window). The resulting coordinates are in *screen space*, with values ranging from 0 to the width of the viewport in x, and 0 to the height of the viewport in y.

## Interaction: Detecting Clicks and Touches

The interactions we will handle in the sample app are very simple: we only care when a mouse click occurs or when a touch begins. Once we have the location on the screen of one of these events, we’ll hand it off to our picking code to determine the selected objects.

On macOS, we want to listen for mouse-down events. We can override the following method on `NSViewController`

to be notified of such events. We use `NSView`

‘s `convert(:,from:)`

method to convert from the view’s coordinate space into the window’s coordinate space. Because AppKit’s convention uses the window’s lower-left corner as the origin, we need to flip these coordinates before passing them to our platform-independent handler.

override func mouseDown(with event: NSEvent) { var location = view.convert(event.locationInWindow, from: nil) location.y = view.bounds.height - location.y handleInteraction(at: location) }

On iOS, we listen for `touchesBegan`

and ask the first touch for its location in the view. Since UIKit’s upper-left origin agrees with Metal’s convention, we don’t need to perform a flip to get a pair of coordinates we can use:

override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) { if let location = touches.first?.location(in: view) { handleInteraction(at: location) } }

## There and Back Again: Inverting Transformations

The two methods above provide the 2D coordinates of a click or touch in the coordinate space of their containing window. This is the first step in working our way backwards to determine the object being interacted with.

Normally, we consider how to move from 3D coordinate spaces to the screen-space image we produce each frame, so working backwards can feel a little unfamiliar. One step is especially awkward, and that’s the process of moving from screen space to clip space, because it requires adding a dimension (moving from 2D to 3D). This is called *unprojection*. The process of unprojection actually requires us to turn a 2D point on the screen into a 3D *ray*, since our click or touch could correspond to any of the infinitely-many points along the line extending from the screen (at the near plane) into the scene. A ray consists of two parts: an *origin* and a *direction*. We’ll talk about how to construct the direction first, since the origin is the easier of the two.

### From Screen Space to Clip Space

First, we want to unproject the x, y position of the interaction point into a corresponding x, y pair on the near plane of clip space. We do this by scaling and biasing the coordinates by the width and height of the viewport (window), also flipping the Y axis so that it points up rather than down:

let clipX = (2 * Float(location.x)) / width - 1 let clipY = 1 - (2 * Float(location.y)) / height let clipCoords = float4(clipX, clipY, 0, 1)

### From Clip Space to View Space

Recall that we can ask our camera for a projection transformation that incorporates the various projection parameters and takes us from world space to clip space. In order to go in the opposite direction, we take the *inverse* of this matrix, which reverses all of its effects:

let projectionMatrix = camera.projectionMatrix(aspectRatio: aspectRatio) let inverseProjectionMatrix = projectionMatrix.inverse

Applying this inverted matrix to our clip space coordinates gives us the x, y pair of the *direction* of the ray we want in view space. We force its z component to -1 since the direction “out” of the screen in this space corresponds to the +Z axis, and we want our ray pointing “into” the screen. We also force its w component to 0, since it represents a vector, and we want it to transform as such in subsequent operations.

var eyeRayDir = inverseProjectionMatrix * clipCoords eyeRayDir.z = -1 eyeRayDir.w = 0

### From View Space to World Space

The final step we want to take with our ray direction is to move it into world space, where we’ll be performing the tests that tell us which object(s) our ray intersects.

Recall that the (world-to-)view transformation is the inverse of the transformation of the camera. Therefore, to go from view space to world space, we take the inverse of *that* matrix. Since the inverse of the inverse of an invertible matrix is the matrix itself, we can eliminate both inverses and just use the camera transformation matrix, but in the interest of clarity, we’ll show both inversions. Just remember that this is superfluous when optimizing your own picking routines:

let viewMatrix = cameraNode.worldTransform.inverse let inverseViewMatrix = viewMatrix.inverse

We can now apply the view-to-world transformation to our ray direction to get the world ray direction:

var worldRayDir = (inverseViewMatrix * eyeRayDir).xyz worldRayDir = normalize(worldRayDir)

Note that we normalize here, since the direction we’ve computed so far is almost certainly not unit-length. This isn’t strictly necessary: our intersection routines will work just fine with a non-unit-length ray direction, but I prefer to normalize, since the results of such routines are easier to interpret when the direction is normalized.

### Computing the Picking Ray Origin

We now know the world-space direction of our ray, but what about its origin? Well, we know that the virtual camera sits at (0, 0, 0) in view space, so why not start there and simply apply the view-to-world transformation?

let eyeRayOrigin = float4(x: 0, y: 0, z: 0, w: 1) let worldRayOrigin = (inverseViewMatrix * eyeRayOrigin).xyz

This works just fine. Note that we set the `w`

component to 1, since we want the origin to transform as a point rather than a vector. This is crucial, since the view matrix almost always has a translational component that would otherwise get lost if `w`

were 0.

### A Look Ahead

We’re almost there. We now have a world-space ray that we can test against the bounds of each object in our scene to determine which is being picked. I created a small `Ray`

struct that encapsulates an origin and direction and can be used by the hit-testing routines I added to my `Scene`

and `Node`

classes:

let ray = Ray(origin: worldRayOrigin, direction: worldRayDir) if let hit = scene.hitTest(ray) { //...something got hit; do something with it... }

In the next section, we’ll look at how to test a ray against the objects in a scene graph.

## Performing World-Space Intersection Tests

If we wanted absolutely precise hit-testing, we’d need to test the ray against every triangle in every object in our scene. This quickly gets expensive, especially when animating. Various acceleration schemes exist for narrowing down the objects to test against, but we’ll keep things simple in this example by providing each object with a *bounding volume*, specifically a sphere that is positioned at the object’s origin, and whose radius encompasses the entire object.

Since the objects in the sample app *are* spheres, we’ll get exact results, but real-world applications won’t have it so easy. You might want to use a different kind of bounding volume (such as an axis-aligned bounding box or oriented bounding box) if it’s called for.

### Ray-Sphere Intersection

I encapsulated the logic for testing for intersection between a ray and a sphere in a struct called `BoundingSphere`

. Here’s its interface:

struct BoundingSphere { var center: float3 var radius: Float func intersect(_ ray: Ray) -> Float? {...} }

The `intersect`

method returns the nearest intersecting ray *parameter*, if the ray and sphere do in fact intersect. The parameter is the value that, when multiplied by the ray’s direction and added to the ray’s origin, specifies the intersection point. I also created a struct called `HitResult`

that wraps a `Node`

, a `Ray`

, and an intersection parameter together, which allows you to ask for this point of intersection, which is sometimes useful:

struct HitResult { var node: Node var ray: Ray var parameter: Float var intersectionPoint: float3 { return ray.origin + parameter * ray.direction } }

The ray-sphere intersection routine was adapted from [this article](https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection), since I didn’t feel like rederiving it.

### Testing Against a Scene Graph

In order to test all of the objects in a scene graph for intersection, we write a recursive method that transforms the ray into the model space of each node, does the hit test, then recursively asks each of its child nodes to perform the same test. Note that we multiply by the *inverse* of the model-to-world transformation, since our ray was computed in world space. Note also that the transformations are cumulative, since the model-to-world transformation of an object in a scene graph is the product of its transformation combined with all of its ancestors’. I’ve elided the recursive step here for brevity, but you can see the full method in the sample code.

func hitTest(_ ray: Ray) -> HitResult? { let localRay = transform.inverse * ray var nearest: HitResult? if let parameter = boundingSphere.intersect(localRay) { nearest = HitResult(node: self, ray: ray, parameter: parameter) } // ...recursively test against child nodes, returning hits that are nearer... return nearest }

Once we have the result of the hit test, we can do whatever we like with the information: select an object for further manipulation, change its appearance in some way, or play some kind of animation. In the sample code, we toggle the object’s appearance between solid and wireframe, just to distinguish it visually, but there are no limits to the types of effects you might choose to build around this basic interaction.

## Conclusion

You can download the sample code [here](https://github.com/metal-by-example/metal-picking).

In this article, we dove deep on the theory of coordinate spaces in order to elucidate how to select objects in a 3D scene, which is the cornerstone of many types of interactions. I hope you were able to follow the ideas and the math, but if anything above requires further explanation, feel free to comment below. Thanks as always for reading.

-
I only recently learned that this shape is not actually a
[hemicube](https://en.wikipedia.org/wiki/Hemicube_(geometry)). It’s actually a[right rectangular prism](https://en.wikipedia.org/wiki/Cuboid), but that doesn’t roll off the tongue, nor does it precisely invoke the notion of “half of a cube,” so I’m sticking to the incorrect “hemicube” for now.[↩](https://metalbyexample.com#fnref-738-1)

Mr.EndlesswhyHello, it’s a very good article for my first ray test. when I touch a ball, I get the , but I want to project to a touch point again, I tried many times, I both failed to project the back to the touch point. (https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/mathematics-computing-2d-coordinates-of-3d-points)

Could you please help me? Thank you very much!

Warren MooreWell, it’s no wonder you had trouble converting backwards; I had a significant error in my logic!

First, here’s the code to “reproject” the hit point (in world space) to the viewport point (which is then fairly easy to convert into the space of your view or screen):

`let worldPoint = hit.intersectionPoint`

let eyePoint = viewMatrix * worldPoint

let clipPoint = projectionMatrix * eyePoint

let viewportX = (((clipPoint.x / clipPoint.w) + 1) / 2) * width

let viewportY = (((-clipPoint.y / clipPoint.w) + 1) / 2) * height

let viewportPoint = float2(viewportX, viewportY)

The problem arose from the fact that my intersection parameters were in inconsistent spaces: the intersection routine returned a model-space parameter, which was then treated as a world-space parameter for comparison purposes. I’ve fixed the code on Github and will update the article shortly.

Sorry for the error, and thanks for speaking up!

FattieYet another spectacular article, WM. Thanks!

I was wondering, you see how Apple have now encapsulated (say) the process of loading models in to a convenient Apple library that does all the work. I guess they have not yet done that for hit testing from the “camera” is that about right?

I suppose, as Apple does more and more of this work .. we can soon just forget about using Unity! 🙂

Thanks again, what about a new book for the Swift era!

Warren MooreRight; Metal and MetalKit provide utilities for GPU rendering and processing, but not much in the way of general utilities for games or UI. Higher-level frameworks like SceneKit and SpriteKit do, of course, but when using raw Metal, we have to build more of the infrastructure ourselves 🙂

I’d love to write another (Swift-centric) book on Metal, but I just haven’t found the time…

MJThank you very much for this great article. I have learned a lot from your gltf work and your book. can’t wait for a second edition.

I am trying to write the intersect function for a bounding box using MDLAxisAlignedBoundingBox. I can’t figure out what is wrong. I would be grateful if you can take a look at the following link

https://stackoverflow.com/questions/55435228/how-to-pick-a-bounding-box-using-mdl

Thanks in advance

MJThank you very much for this great article. can’t wait for the second edition of your book. I have been trying to write the intersect function for a bounding box as an extension MDLAxisAlignedBoundingBox (https://stackoverflow.com/questions/55435228/how-to-pick-a-bounding-box-using-mdl).

MJGreat article, Thanks for writing it. I have been trying to extend your idea for MDLAxisAlignedBoundingBox but without luck for the t0 factor. https://stackoverflow.com/questions/55435228/how-to-pick-a-bounding-box-using-mdl

Any idea where I went wrong.

Once again thanks for this and the GLTF code .

miguel saldanawhen i scale the sphere nodes, how do i update the boundingVolume to match the scaling of the node mesh?

Warren MooreThe fact that we take the inverse of the node’s model-to-world transform and perform hit-testing in model space accounts for any scaling in the node’s transform. Have you observed this not to be the case?

AlexExcuse me, how did you resolve an overlapping spheres each other during rotation of the scene?

AlexOh, sorry I’v founded it. It is just setting several flags. Metal is power tool.