---
title: Accelerating path tracing by using the BVH as multiresolution geometry
url: http://raytracey.blogspot.com/2018/07/accelerating-path-tracing-by-using-bvh.html
author: Sam Lapere
published: '2018-07-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Before continuing the tutorial series, let's have a look at a simple but effective way to speed up path tracing. The idea is quite simple: like an octree, a bounding volume hierarchy (BVH) can double as both a ray tracing acceleration structure and a way to represent the scene geometry at multiple levels of detail (multi-resolution geometry representation). Specifically the axis-aligned bounding boxes (AABB) of the BVH nodes at different depths in the tree serve as a more or less crude approximation of the geometry.



Low detail geometry enables much faster ray intersections and can be useful when light effects don't require full geometric accuracy, for example in the case of motion blur, glossy (blurry) reflections, soft shadows, ambient occlusion and global illumination with diffuse bounced lighting. Especially when geometry is not directly visible in the view frustum or in specular (mirror-like) reflections, using geometry proxies can provide a significant speedup (depending on the fault tolerance) at an almost imperceptible and negligible loss in quality.


Advantages of using the BVH itself as multi-resolution LOD geometry representation:


Advantages of using the BVH itself as multi-resolution LOD geometry representation:

- doesn't require an additional scene voxelisation step (the BVH itself provides the LOD): less memory hungry
- skips expensive triangle intersection when possible
- performs only ray/box intersections (as opposed to having a mix of ray/triangle and ray/box intersections) which is more efficient on the GPU (avoids thread divergence)
- BVH is stored in the GPU's cached texture memory (which is faster than global memory which should therefore store the triangles)
- BVH nodes can store extra attributes like smoothed normals, interpolated colours and on-the-fly generated GI

(Note: AFAIK low level access to the acceleration structure is not provided by API's like OptiX/RTX and DXR, this has to be written in CUDA, ISPC or OpenCL)

The renderer determines the appropriate level of detail based on the distance from the camera for primary rays or on the distance from the ray origin and the ray type for secondary rays (glossy/reflection, shadow, AO or GI rays). The following screenshots show the bounding boxes of the BVH nodes from depth 1 (depth 0 is the rootnode) up to depth 12:

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

![]() |

Normals are axis aligned, but can be precomputed per AABB vertex (and stored at low precision) by averaging the normals of the AABBs it contains, with the leafnodes averaging the normals of their triangles.


TODO upload code to github or alternaive non ms repo and post link, propose fixes to fill holes, present benchmark results (8x speedup), get more timtams

TODO upload code to github or alternaive non ms repo and post link, propose fixes to fill holes, present benchmark results (8x speedup), get more timtams

## 2 comments:

Hi,




very interesting materials on your blog,

is there a 101 tutorial for newbies about "octree" and "BVH"?

Thank you,

D.

Interesting idea, I wonder what the visual differences are compared to the current industry standard of LOD-ing using triangle meshes. I suppose it looks a lot like voxelized meshes, which are fine as a replacement for the further LODs.


Is this speedup an 8x improvement over just rendering the mesh normally with triangle intersections at the finest level?

Post a Comment