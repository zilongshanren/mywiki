---
title: 'cocos3d: Class List'
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/annotated/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[CC3ActionRangeLimit](/) | A [CC3ActionRangeLimit](/) holds another action, and serves to modify the normal zero-to-one range of update values to a smaller range that is presented to the contained action |
[CC3AngularVector](/) | Specifies a vector using angular coordinate axes |
[CC3Animate](/) | A CCActionInterval that animates a [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) |
[CC3ArrayNodeAnimation](/) | A concrete [CC3NodeAnimation](/) that holds animation data in simple arrays |
[CC3AttenuationCoefficients](/) | The coefficients of the equation for an attenuation function: (a + b*r + c*r*r), where r is the radial distance between a the source (light or camera) and the 3D location at which we want to calculate attenuation |
[CC3Billboard](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) | This [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) displays a 2D cocos2d CCNode as part of the 3D world |
[CC3BillboardBoundingBoxArea](/) | A [CC3NodeBoundingArea](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/), used exclusively with CC3Billboards, that uses the billboardBoundingRect property of the [CC3Billboard](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) as the bounding area, and checks the bounding area against a given bounding box (typically from the [CC3Layer](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_layer/)), using the doesIntersectBounds: method |
[CC3Bone](/) | [CC3Bone](/) is the building block of skeletons that control the deformation of a skin mesh |
[CC3BoundingBox](/) | Defines an axially-aligned-bounding-box (AABB), describing a 3D volume by specifying the minimum and maximum 3D corners |
[CC3BoxNode](/) | [CC3BoxNode](/) is a type of [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) that is specialized to display simple box or cube meshes |
[CC3BTreeNodeSequencer](/) | An [CC3BTreeNodeSequencer](/) is a type of [CC3NodeSequencer](/) that separates nodes into a B-tree structure of child sequencers |
[CC3BumpMapTextureUnit](/) | A texture unit configured for DOT3 bump-mapping |
[CC3Camera](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_camera/) | [CC3Camera](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_camera/) represents the camera viewing the 3D world |
[CC3ConfigurableTextureUnit](/) | A texture unit that provides complete flexibility to define the way the texture will be combined with the output of previous texture units |
[CC3DirectionalRotator](/) | This [CC3Rotator](/) subclass adds the ability to set rotation based on directional information |
[CC3DirectionMarkerNode](/) | [CC3DirectionMarkerNode](/) is a type of [CC3LineNode](/) specialized for drawing a line from the pivot point of its parent node to a point outside the bounding box of the parent node, in a particular direction |
[CC3DrawableVertexArray](/) | This abstract subclass of [CC3VertexArray](/) adds the functionality to draw the vertex data to the display through the GL engine |
[CC3EAGLView](/) | If your application supports BOTH multisampling AND node-picking from touch events, you should use this class instead of EAGLView |
[CC3ES1Renderer](/) | Specialized renderer that supports node-picking while multisampling antialiasing is active |
[CC3Fog](/) | [CC3Fog](/) controls fog in the 3D world |
[CC3Frustum](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_frustum/) | Represents a camera's frustum |
[CC3GLMatrix](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_g_l_matrix/) | A wrapper class for a 4x4 OpenGL matrix array |
[CC3Identifiable](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/) | This is a base subclass for any class that uses tags or names to identify individual instances |
[CC3Layer](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_layer/) | [CC3Layer](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_layer/) is a cocos2d CCLayer that supports full 3D rendering in combination with normal cocos2d 2D rendering |
[CC3Light](/) | [CC3Light](/) represents the light in the 3D world |
[CC3LightTracker](/) | [CC3LightTracker](/) is a specialized [CC3TargettingNode](/) that tracks a target and automatically updates its own globalLightLocation property from the globalLocation property of the target |
[CC3LineNode](/) | [CC3LineNode](/) is a type of [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) that is specialized to display lines |
[CC3LocalContentNode](/) | [CC3LocalContentNode](/) is an abstract class that forms the basis for nodes that have local content to draw |
[CC3LocalContentNodeAcceptor](/) | A type of [CC3LocalContentNodeEvaluator](/) that accepts all nodes with local content, and rejects all other nodes |
[CC3LocalContentNodeEvaluator](/) | A type of [CC3NodeEvaluator](/) that specializes in evaluating only CC3Nodes with local content |
[CC3Material](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_material/) | [CC3Material](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_material/) manages information about a material that is used to cover one or more meshes |
[CC3Mesh](/) | A [CC3Mesh](/) holds the 3D mesh for a [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) |
[CC3MeshModel](/) | Deprecated [CC3MeshModel](/) renamed to [CC3Mesh](/) |
[CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) | A [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) that draws a 3D mesh |
[CC3MeshNodeArraySequencer](/) | An [CC3MeshNodeArraySequencer](/) is a type of [CC3NodeArraySequencer](/) that only accepts mesh nodes, in addition to whatever other evaluation criteria is set by the evaluator property |
[CC3MeshNodeArraySequencerGroupMeshes](/) | An [CC3MeshNodeArraySequencerGroupTextures](/) is a type of [CC3MeshNodeArraySequencer](/) that groups together nodes that are using the same mesh |
[CC3MeshNodeArraySequencerGroupTextures](/) | An [CC3MeshNodeArraySequencerGroupTextures](/) is a type of [CC3MeshNodeArraySequencer](/) that groups together nodes that are using the same texture |
[CC3ModelSampleFactory](/) | [CC3ModelSampleFactory](/) is a convenience utility for creating sample 3D models for experimentation |
[CC3MortalPointParticle](/) | [CC3MortalPointParticle](/) is a type of [CC3PointParticle](/) that has a finite life |
[CC3MortalPointParticleEmitter](/) | [CC3MortalPointParticleEmitter](/) emits particles of type [CC3MortalPointParticle](/) |
[CC3MoveBy](/) | [CC3MoveBy](/) is a CCActionInterval that moves a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) by a specific translation amount |
[CC3MoveTo](/) | [CC3MoveTo](/) is a CCActionInterval that moves a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to a specific location |
[CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) | [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) and its subclasses form the basis of all 3D artifacts in the 3D world, including visible meshes, structures, cameras, lights, resources, and the 3D world itself |
[CC3NodeAcceptor](/) | A type of [CC3NodeEvaluator](/) that accepts all nodes by always returning YES from the evaluate: method |
[CC3NodeAnimation](/) | An instance of a subclass of [CC3NodeAnimation](/) manages the animation of nodes |
[CC3NodeArraySequencer](/) | An [CC3NodeArraySequencer](/) is a type of [CC3NodeSequencer](/) that arranges nodes into an array, and orders the nodes in the array by some criteria |
[CC3NodeArrayZOrderSequencer](/) | An [CC3NodeArrayZOrderSequencer](/) is a type of [CC3NodeArraySequencer](/) that sorts the contained nodes by their Z-order, which is a combination of the explicit Z-order property of each node, and a measure of the distance from the camera to the globalCenterOfGravity of the node's bounding volume |
[CC3NodeBoundingArea](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/) | A bounding volume that defines a 2D bounding area for a node, and checks that bounding area against a given 2D bounding box, which is typically the bounding box of the [CC3Layer](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_layer/), instead of the camera frustum |
[CC3NodeBoundingBoxVisitor](/) | Specialized transforming visitor that measures the bounding box of a node and all its descendants, by traversing each descendant node, ensuring each transformMatrix is up to date, and accumulating a bounding box that encompasses the local content of the startingNode and all of its descendants |
[CC3NodeBoundingBoxVolume](/) | A bounding volume that forms an axially aligned bounding box (AABB) around the node, in the node's local coordinate system |
[CC3NodeBoundingVolume](/) | Bounding volumes are used by CC3Nodes to determine whether a node interset the camera's frustum, or to determine boundaries for collision detection during physics simulation |
[CC3NodeDescriptor](/) | [CC3NodeDescriptor](/) is a type of [CC3Billboard](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) specialized for attaching a descriptive text label to another node |
[CC3NodeDrawingVisitor](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/) | [CC3NodeDrawingVisitor](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/) is a [CC3NodeVisitor](/) that is passed to a node when it is visited during drawing operations |
[CC3NodeEvaluator](/) | A [CC3NodeEvaluator](/) performs some type of accept/reject evaluation on a [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) instance |
[CC3NodePickingVisitor](/) | [CC3NodePickingVisitor](/) is a [CC3NodeDrawingVisitor](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/) that is passed to a node when it is visited during node picking operations using color-buffer based picking |
[CC3NodeRejector](/) | A type of [CC3NodeEvaluator](/) that rejects all nodes by always returning NO from the evaluate: method |
[CC3NodeSequencer](/) | A [CC3NodeSequencer](/) instance organizes nodes that are added to it |
[CC3NodeSequencerVisitor](/) | This visitor is used to visit CC3NodeSequencers to perform operations on nodes within the sequencers |
[CC3NodeSphericalBoundingVolume](/) | A bounding volume that forms a sphere around a single point |
[CC3NodeTighteningBoundingVolumeSequence](/) | A composite bounding volume that contains other bounding volumes |
[CC3NodeTransformingVisitor](/) | [CC3NodeTransformingVisitor](/) is a [CC3NodeVisitor](/) that is passed to a node when it is visited during transformation operations |
[CC3NodeUpdatingVisitor](/) | [CC3NodeUpdatingVisitor](/) is a [CC3NodeVisitor](/) that is passed to a node when it is visited during updating and transforming operations |
[CC3NodeVisitor](/) | A [CC3NodeVisitor](/) is a context object that is passed to a node when it is visited during a traversal of the node hierarchy |
[CC3OpaqueNodeAcceptor](/) | A type of [CC3LocalContentNodeEvaluator](/) that accepts only opaque nodes |
[CC3OpenGLES11ClientCapabilities](/) | [CC3OpenGLES11ClientCapabilities](/) manages trackers that read and remember OpenGL ES 1.1 client capabilities once, and restore that capability when the close method is invoked |
[CC3OpenGLES11Engine](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) | [CC3OpenGLES11Engine](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) manages the state of the OpenGL ES 1.1 |
[CC3OpenGLES11Fog](/) | [CC3OpenGLES11Fog](/) manages trackers for fog state |
[CC3OpenGLES11Hints](/) | [CC3OpenGLES11Hints](/) manages trackers for GL hints |
[CC3OpenGLES11Light](/) | [CC3OpenGLES11Light](/) manages trackers for an individual light |
[CC3OpenGLES11Lighting](/) | [CC3OpenGLES11Lighting](/) manages trackers for lighting state |
[CC3OpenGLES11Materials](/) | [CC3OpenGLES11Materials](/) manages trackers for materials state |
[CC3OpenGLES11Matrices](/) | [CC3OpenGLES11Matrices](/) manages trackers for matrix state |
[CC3OpenGLES11MatrixPalette](/) | [CC3OpenGLES11MatrixPalette](/) provides access to several commands that operate on one matrix the matrix palette |
[CC3OpenGLES11MatrixStack](/) | [CC3OpenGLES11MatrixStack](/) provides access to several commands that operate on one of the matrix stacks, none of which require state tracking |
[CC3OpenGLES11Platform](/) | [CC3OpenGLES11Platform](/) manages trackers that read and remember platform characteristics, capabilities and limits |
[CC3OpenGLES11ServerCapabilities](/) | [CC3OpenGLES11ServerCapabilities](/) manages trackers that read and remember OpenGL ES 1.1 server capabilities once, and restore that capability when the close method is invoked |
[CC3OpenGLES11State](/) | [CC3OpenGLES11State](/) manages trackers that read and remember OpenGL ES 1.1 state and restore that state when the close method is invoked |
[CC3OpenGLES11StateTracker](/) | This is the base class of all OpenGL ES 1.1 state trackers |
[CC3OpenGLES11StateTrackerActiveTexture](/) | [CC3OpenGLES11StateTrackerActiveTexture](/) tracks an enumerated GL state value for identifying the active texture |
[CC3OpenGLES11StateTrackerAlphaFunction](/) | [CC3OpenGLES11StateTrackerAlphaFunction](/) is a type of [CC3OpenGLES11StateTrackerComposite](/) that tracks the alpha test function and reference GL state values for materials |
[CC3OpenGLES11StateTrackerArrayBufferBinding](/) | [CC3OpenGLES11StateTrackerArrayBufferBinding](/) tracks binding and filling a vertex array |
[CC3OpenGLES11StateTrackerBoolean](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a boolean GL state value |
[CC3OpenGLES11StateTrackerCapability](/) | [CC3OpenGLES11StateTrackerCapability](/) tracks a boolean GL capability, indicating whether the capability is enabled or disabled |
[CC3OpenGLES11StateTrackerClientCapability](/) | [CC3OpenGLES11StateTrackerClientCapability](/) is a type of [CC3OpenGLES11StateTrackerCapability](/) that tracks a GL client capability |
[CC3OpenGLES11StateTrackerColor](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a color GL state value |
[CC3OpenGLES11StateTrackerColorFixedAndFloat](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a color GL state value, as either a float or fixed value |
[CC3OpenGLES11StateTrackerComposite](/) | A [CC3OpenGLES11StateTracker](/) that tracks a composite value |
[CC3OpenGLES11StateTrackerElementArrayBufferBinding](/) | [CC3OpenGLES11StateTrackerElementArrayBufferBinding](/) tracks binding and filling a vertex element (index) array |
[CC3OpenGLES11StateTrackerEnumeration](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks an enumerated GL state value |
[CC3OpenGLES11StateTrackerFloat](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a float GL state value |
[CC3OpenGLES11StateTrackerFogColor](/) | [CC3OpenGLES11StateTrackerFogColor](/) tracks a color GL state value for fog |
[CC3OpenGLES11StateTrackerFogEnumeration](/) | [CC3OpenGLES11StateTrackerFogEnumeration](/) tracks an enumeration GL state value for fog |
[CC3OpenGLES11StateTrackerFogFloat](/) | [CC3OpenGLES11StateTrackerFogFloat](/) tracks a float GL state value for fog |
[CC3OpenGLES11StateTrackerHintEnumeration](/) | [CC3OpenGLES11StateTrackerHintEnumeration](/) tracks an enumeration GL state value for a hint |
[CC3OpenGLES11StateTrackerInteger](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks an integer GL state value |
[CC3OpenGLES11StateTrackerLightColor](/) | [CC3OpenGLES11StateTrackerLightColor](/) tracks a color GL state value for an individual light |
[CC3OpenGLES11StateTrackerLightFloat](/) | [CC3OpenGLES11StateTrackerLightFloat](/) tracks a float GL state value for an individual light |
[CC3OpenGLES11StateTrackerLightVector](/) | [CC3OpenGLES11StateTrackerLightVector](/) tracks a 3D vector GL state value for an individual light |
[CC3OpenGLES11StateTrackerLightVector4](/) | [CC3OpenGLES11StateTrackerLightVector4](/) tracks a 4D vector GL state value for an individual light |
[CC3OpenGLES11StateTrackerManager](/) | An [CC3OpenGLES11StateTracker](/) that manages a number of other trackers |
[CC3OpenGLES11StateTrackerMaterialBlend](/) | [CC3OpenGLES11StateTrackerMaterialBlend](/) is a type of [CC3OpenGLES11StateTrackerComposite](/) that tracks the source and destination blending GL state values for materials |
[CC3OpenGLES11StateTrackerMaterialColor](/) | [CC3OpenGLES11StateTrackerMaterialColor](/) tracks a color GL state value for materials |
[CC3OpenGLES11StateTrackerMaterialFloat](/) | [CC3OpenGLES11StateTrackerMaterialFloat](/) tracks a float GL state value for materials |
[CC3OpenGLES11StateTrackerPlatformInteger](/) | [CC3OpenGLES11StateTrackerMaterialFloat](/) tracks a float GL state value for platform limits |
[CC3OpenGLES11StateTrackerPointer](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a pointer GL state value |
[CC3OpenGLES11StateTrackerPointParameterFloat](/) | [CC3OpenGLES11StateTrackerPointParameterFloat](/) tracks a float GL point parameter state value |
[CC3OpenGLES11StateTrackerPointParameterVector](/) | [CC3OpenGLES11StateTrackerPointParameterVector](/) tracks a 3D vector GL point parameter state value |
[CC3OpenGLES11StateTrackerPrimitive](/) | A type of [CC3OpenGLES11StateTracker](/) that tracks the state of a single primitive GL state value |
[CC3OpenGLES11StateTrackerServerCapability](/) | [CC3OpenGLES11StateTrackerServerCapability](/) is a type of [CC3OpenGLES11StateTrackerCapability](/) that tracks a GL server capability |
[CC3OpenGLES11StateTrackerTexEnvColor](/) | [CC3OpenGLES11StateTrackerTexEnvColor](/) tracks a color GL state value for the texture environment |
[CC3OpenGLES11StateTrackerTexEnvEnumeration](/) | [CC3OpenGLES11StateTrackerTexEnvEnumeration](/) tracks an enumerated GL state value for the texture environment |
[CC3OpenGLES11StateTrackerTexEnvPointSpriteCapability](/) | [CC3OpenGLES11StateTrackerTexEnvPointSpriteCapability](/) tracks a boolean GL capability for the point sprite texture environment |
[CC3OpenGLES11StateTrackerTextureBinding](/) | [CC3OpenGLES11StateTrackerTextureBinding](/) tracks an integer GL state value for texture binding |
[CC3OpenGLES11StateTrackerTextureClientCapability](/) | [CC3OpenGLES11StateTrackerTextureClientCapability](/) tracks a boolean GL capability for the point sprite texture environment |
[CC3OpenGLES11StateTrackerTextureServerCapability](/) | [CC3OpenGLES11StateTrackerTextureServerCapability](/) tracks a boolean GL capability for the point sprite texture environment |
[CC3OpenGLES11StateTrackerVector](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a 3D vector GL state value |
[CC3OpenGLES11StateTrackerVector4](/) | A [CC3OpenGLES11StateTrackerPrimitive](/) that tracks a 4D vector GL state value |
[CC3OpenGLES11StateTrackerVertexColorsPointer](/) | [CC3OpenGLES11StateTrackerVertexColorsPointer](/) tracks the parameters of the vertex colors pointer |
[CC3OpenGLES11StateTrackerVertexLocationsPointer](/) | [CC3OpenGLES11StateTrackerVertexLocationsPointer](/) tracks the parameters of the vertex locations pointer |
[CC3OpenGLES11StateTrackerVertexMatrixIndicesPointer](/) | [CC3OpenGLES11StateTrackerVertexLocationsPointer](/) tracks the parameters of the vertex matrix indices pointer |
[CC3OpenGLES11StateTrackerVertexNormalsPointer](/) | [CC3OpenGLES11StateTrackerVertexNormalsPointer](/) tracks the parameters of the vertex normals pointer |
[CC3OpenGLES11StateTrackerVertexPointer](/) | [CC3OpenGLES11StateTrackerVertexPointer](/) is a type of [CC3OpenGLES11StateTrackerComposite](/) that tracks the parameters of a vertex pointer |
[CC3OpenGLES11StateTrackerVertexPointSizesPointer](/) | [CC3OpenGLES11StateTrackerVertexPointSizesPointer](/) tracks the parameters of the vertex point sizes pointer |
[CC3OpenGLES11StateTrackerVertexTexCoordsPointer](/) | [CC3OpenGLES11StateTrackerVertexTexCoordsPointer](/) tracks the parameters of the vertex texture coordinates pointer |
[CC3OpenGLES11StateTrackerVertexWeightsPointer](/) | [CC3OpenGLES11StateTrackerVertexLocationsPointer](/) tracks the parameters of the vertex weights pointer |
[CC3OpenGLES11StateTrackerViewport](/) | [CC3OpenGLES11StateTrackerViewport](/) tracks the viewport GL state |
[CC3OpenGLES11StateTrackerWorldLightColor](/) | [CC3OpenGLES11StateTrackerWorldLightColor](/) tracks the color GL state value for the ambient world light |
[CC3OpenGLES11TextureMatrixStack](/) | [CC3OpenGLES11MatrixStack](/) provides access to several commands that operate on the texture matrix stacks, none of which require state tracking |
[CC3OpenGLES11Textures](/) | [CC3OpenGLES11Textures](/) manages trackers for texture and texture environment state |
[CC3OpenGLES11TextureUnit](/) | [CC3OpenGLES11Textures](/) manages trackers for texture and texture environment state |
[CC3OpenGLES11VertexArrays](/) | [CC3OpenGLES11VertexArrays](/) manages trackers for vertex arrays |
[CC3ParticleSystemBillboard](/) | A [CC3Billboard](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) node customized to display and manage a cocos2d 2D CCParticleSystem |
[CC3PerformanceStatistics](/) | Collects statistics about the updating and drawing performance of the 3D world |
[CC3PerformanceStatisticsHistogram](/) | Collects statistics about the updating and drawing performance of the 3D world, including a histogram for each of the raw updateRate and frameRate properties |
[CC3Plane](../../../../../api-ref/1.0/cocos3d/html/struct_c_c3_plane/) | The coefficients of the equation for a plane in 3D space (ax + by + cz + d = 0) |
[CC3PlaneNode](/) | [CC3PlaneNode](/) is a type of [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) that is specialized to display planes and simple rectanglular meshes |
[CC3PODBone](/) | A [CC3Bone](/) extracted from a POD file |
[CC3PODCamera](/) | A [CC3Camera](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_camera/) whose content originates from POD resource data |
[CC3PODLight](/) | A [CC3Light](/) whose content originates from POD resource data |
[CC3PODMaterial](/) | A [CC3Material](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_material/) whose content originates from POD resource data |
[CC3PODMesh](/) | A [CC3VertexArrayMesh](/) whose content originates from POD resource data |
[CC3PODMeshNode](/) | A [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) whose content originates from POD resource data |
[CC3PODNode](/) | A [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) extracted from a POD file |
[CC3PODNodeAnimation](/) | POD files can contain information to animate the nodes |
[CC3PODResource](/) | [CC3PODResource](/) is a [CC3Resource](/) that wraps a PVR POD data structure loaded from a file |
[CC3PODResourceNode](/) | A [CC3ResourceNode](/) that that wraps a [CC3PODResource](/) PVR POD resource |
[CC3PODSkinMesh](/) | A [CC3SkinMesh](/) extracted from a POD file |
[CC3PODSkinMeshNode](/) | A [CC3SkinMeshNode](/) extracted from a POD file |
[CC3PODSkinSection](/) | A [CC3SkinSection](/) extracted from a POD file |
[CC3PointParticle](/) | [CC3PointParticle](/) is an abstract class that represents a single particle emitted by a [CC3PointParticleEmitter](/) |
[CC3PointParticleEmitter](/) | A [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) that emits 3D point particles |
[CC3PointParticleHoseEmitter](/) | [CC3PointParticleHoseEmitter](/) emits [CC3UniformMotionParticle](/) particles in a stream, as if from the nozzle of a hose |
[CC3PointParticleMesh](/) | A mesh whose vertices are used to display point particles |
[CC3Ray](/) | Defines a ray or line in 3D space, by specifying a starting location and direction |
[CC3Resource](/) | [CC3Resource](/) is a wrapper class around a resource structure loaded from a data file containing 3D resources |
[CC3ResourceNode](/) | A [CC3ResourceNode](/) is a [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) that that wraps an instance of a subclass of [CC3Resource](/) in the resource property, extracts the nodes from that resource, and forms the root of the resulting node structural assembly |
[CC3RotateBy](/) | [CC3RotateBy](/) is a CCActionInterval that rotates a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) by a specific rotation amount |
[CC3RotateByAngle](/) | [CC3RotateByAngle](/) is a CCActionInterval that rotates a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) by a specific amount, by updating the rotationAngle propety |
[CC3RotateTo](/) | [CC3RotateTo](/) is a CCActionInterval that rotates a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to a specific orientation |
[CC3RotateToAngle](/) | [CC3RotateToAngle](/) is a CCActionInterval that rotates a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to a specific rotationAngle, by updating the rotationAngle propety |
[CC3RotateToLookAt](/) | [CC3RotateToLookAt](/) is a CCActionInterval that rotates a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to look at a specific location |
[CC3RotateToLookTowards](/) | [CC3RotateToLookTowards](/) is a CCActionInterval that rotates a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to look towards a specific direction |
[CC3Rotator](/) | CC3otator encapsulates the various mechanisms of rotating a node, and converts between them |
[CC3ScaleBy](/) | [CC3ScaleBy](/) is a CCActionInterval that scales a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) by a specific scale factor |
[CC3ScaleTo](/) | [CC3ScaleTo](/) is a CCActionInterval that scales a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to a specific scale |
[CC3SkeletonRestPoseBindingVisitor](/) | [CC3SkeletonRestPoseBindingVisitor](/) is a [CC3NodeVisitor](/) that is passed to an assembly of bone nodes (a skeleton) in order to establish the rest pose transforms for the bones in the skeleton |
[CC3SkinMesh](/) | [CC3SkinMesh](/) is a [CC3VertexArrayMesh](/) that, in addition to the familiar vertex data such as locations, normals and texture coordinates, adds vertex arrays for bone weights and bone matrix indices |
[CC3SkinMeshNode](/) | [CC3SkinMeshNode](/) is a [CC3MeshNode](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) specialized to use vertex skinning to draw the contents of its mesh |
[CC3SkinSection](/) | A [CC3SkinSection](/) defines a section of the skin mesh, and contains a collection of bones from the skeleton that influence the locations of the vertices in that section |
[CC3SoftBodyNode](/) | [CC3SoftBodyNode](/) is the primary structural component for a soft-body object that uses vertex skinning to manipulate and draw mesh vertices |
[CC3Sphere](/) | Defines a sphere |
[CC3TargettingNode](/) | This is a node class representing a 3D model node that can be pointed in a particular direction, or at another node |
[CC3Texture](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_texture/) | Each instance of [CC3Texture](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_texture/) wraps a cocos2d CCTexture2D instance, and manages applying that texture to the GL engine |
[CC3TexturedVertex](/) | Defines a simple vertex, containing location, normal, and texture coordinate data |
[CC3TextureUnit](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/) | [CC3TextureUnit](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/) is used by [CC3Texture](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_texture/) to configure the GL texture unit to which the texture is being applied |
[CC3TintAmbientTo](/) | A concrete subclass of [CC3TintTo](/) that changes the ambient color of the target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) |
[CC3TintDiffuseTo](/) | A concrete subclass of [CC3TintTo](/) that changes the diffuse color of the target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) |
[CC3TintEmissionTo](/) | A concrete subclass of [CC3TintTo](/) that changes the emission color of the target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) |
[CC3TintSpecularTo](/) | A concrete subclass of [CC3TintTo](/) that changes the specular color of the target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) |
[CC3TintTo](/) | [CC3TintTo](/) is an abstract CCActionInterval whose subclasses changes one of the color properties of a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to a particular color |
[CC3TouchedNodePicker](/) | A [CC3TouchedNodePicker](/) instance handles picking nodes from touch events in a [CC3World](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_world/) |
[CC3TransformBy](/) | [CC3TransformBy](/) is an abstract subclass of CCActionInterval that is the parent of subclasses that transform the location, rotation, or scale of a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) by some amount in some way |
[CC3TransformTo](/) | [CC3TransformTo](/) is an abstract subclass of CCActionInterval that is the parent of subclasses that transform the location, rotation, or scale of a target [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) to some end value in some way |
[CC3TranslucentNodeAcceptor](/) | A type of [CC3LocalContentNodeEvaluator](/) that accepts only translucent nodes |
[CC3UniformEvolutionParticle](/) | [CC3UniformEvolutionParticle](/) is a type of [CC3MortalPointParticle](/) that moves in a straight line in a single direction at a steady speed, and which can optionally have color and size that linearly move from an intitial color and size to a final color and size |
[CC3UniformMotionParticle](/) | [CC3UniformMotionParticle](/) is a type of [CC3MortalPointParticle](/) that moves in a straight line in a single direction at a steady speed |
[CC3VariegatedPointParticleHoseEmitter](/) | [CC3VariegatedPointParticleHoseEmitter](/) is a type of [CC3PointParticleHoseEmitter](/) whose particles can have a color and size that evolves during the lifetime of the particle |
[CC3Vector](../../../../../api-ref/1.0/cocos3d/html/struct_c_c3_vector/) | A vector in 3D space |
[CC3Vector4](../../../../../api-ref/1.0/cocos3d/html/struct_c_c3_vector4/) | A homogeneous vector in 4D graphics matrix space |
[CC3VertexArray](/) | [CC3VertexArray](/) manages the data associated with an aspect of a vertex |
[CC3VertexArrayMesh](/) | A [CC3VertexArrayMesh](/) is a mesh whose mesh data is kept in a set of CC3VertexArrays instances |
[CC3VertexArrayMeshModel](/) | Deprecated [CC3VertexArrayMeshModel](/) renamed to [CC3VertexArrayMesh](/) |
[CC3VertexColors](/) | A [CC3VertexArray](/) that manages the per-vertex color aspect of an array of vertices |
[CC3VertexIndices](/) | A [CC3VertexArray](/) that manages the drawing indices of an array of vertices |
[CC3VertexLocations](/) | A [CC3VertexArray](/) that manages the location aspect of an array of vertices |
[CC3VertexLocationsBoundingBoxVolume](/) | [CC3VertexLocationsBoundingBoxVolume](/) is a type of [CC3NodeBoundingBoxVolume](/) specialized for use with [CC3VertexArrayMesh](/) and [CC3VertexLocations](/) |
[CC3VertexLocationsBoundingVolume](/) | [CC3VertexLocationsBoundingVolume](/) is a type of [CC3NodeBoundingVolume](/) specialized for use with [CC3VertexArrayMesh](/) and [CC3VertexLocations](/) |
[CC3VertexLocationsSphericalBoundingVolume](/) | [CC3VertexLocationsSphericalBoundingVolume](/) is a type of [CC3NodeSphericalBoundingVolume](/) specialized for use with [CC3VertexArrayMesh](/) and [CC3VertexLocations](/) |
[CC3VertexMatrixIndices](/) | A [CC3VertexArray](/) that manages a collection of indices used by each vertex to point to a collection of distinct matrices during vertex skinning |
[CC3VertexNormals](/) | A [CC3VertexArray](/) that manages the normal aspect of an array of vertices |
[CC3VertexPointSizes](/) | A [CC3VertexArray](/) that manages the point sizes aspect of an array of point sprite vertices |
[CC3VertexRunLengthIndices](/) | An index array that manages the drawing indices of an array of vertices, treating the index array as a run-length encoded array of indexes |
[CC3VertexTextureCoordinates](/) | A [CC3VertexArray](/) that manages the texture coordinates aspect of an array of vertices |
[CC3VertexWeights](/) | A [CC3VertexArray](/) that manages a collection of weights used by each vertex during vertex skinning, which is the manipulation of a soft-body mesh under control of a skeleton of bone nodes |
[CC3Viewport](/) | GL viewport data |
[CC3ViewportManager](/) | [CC3ViewportManager](/) manages the GL viewport and device orientation for the 3D world, including handling coordinate system rotation based on the device orientation, and conversion of locations and points between the 3D and 2D coordinate systems |
[CC3WireframeBoundingBoxNode](/) | [CC3WireframeBoundingBoxNode](/) is a type of [CC3LineNode](/) specialized for drawing a wireframe bounding box around another node |
[CC3WireframeLocalContentBoundingBoxNode](/) | [CC3WireframeLocalContentBoundingBoxNode](/) is a [CC3WireframeBoundingBoxNode](/) that further specializes in drawing a bounding box around the local content of another node with local content |
[CC3World](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_world/) | [CC3World](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_world/) is a [CC3Node](../../../../../api-ref/1.0/cocos3d/html/interface_c_c3_node/) that manages a 3D scene |
[CCArray(CC3)](../../../../../api-ref/1.0/cocos3d/html/interface_c_c_array_07_c_c3_08/) | Extension category to support cocos3d functionality |
[CCDirector(CC3)](/) | Extension category to support cocos3d functionality |
[CCNode(CC3)](/) | Extension category to support cocos3d functionality |
[CCNode(CC3Billboard)](/) | CCNode extension to support embedding 2D CCNodes in the 3D world |
[CCNode(ControlledCCNodeProtocol)](/) | Methods added to the base CCNode to support structural node hierarchies containing controlled nodes |
[CCNodeController](../../../../../api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) | An instance of [CCNodeController](../../../../../api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) manages a single CCNode (typically a CCLayer) as changes occur to the device orientation (portrait, landscape, etc) |
[ControllableCCLayer](/) | A CCLayerColor that implements the [ControlledCCNodeProtocol](/) protocol, and therefore can be controlled by a [CCNodeController](../../../../../api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) to automatically rotate when the device orientation changes, and to permit this layer to be overlaid on the device camera if it exists, permitting "augmented reality" displays |
[<ControlledCCNodeProtocol>](/) | This protocol adds to a CCNode the ability to be managed by a [CCNodeController](../../../../../api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) so that the CCNode can react dynamically to changes in the device orientation (portrait, landscape, etc), as well as to allow the CCNode to act as an overlay for the device camera, permitting "augmented reality" displays |
[EAGLView(CC3Picking)](/) | This extension category adds support for node-picking while multisampling antialiasing is active, by defining the interface required by that support |
[NSObject(CC3)](/) | Extension category to support cocos3d functionality |
[UIColor(CC3)](/) | Extension category to support cocos3d functionality |