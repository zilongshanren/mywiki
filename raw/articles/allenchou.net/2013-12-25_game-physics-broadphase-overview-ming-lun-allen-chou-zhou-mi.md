---
title: 'Game Physics: Broadphase – Overview | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-broadphase/
author: Allen Chou
published: '2013-12-25'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

As mentioned in this [introductory post](http://allenchou.net/2013/12/game-physics-introduction/), a broadphase is the algorithm of choice to efficiently decide whether it is possible for two colliders to collide, without using the actual collision detection algorithm that is more expensive.

Typically, a broadphase keeps track of bounding volumes, usually AABBs, of all colliders. The broadphase produces a list of collider pairs whose AABBs are colliding. These collider pairs are then passed on to the collision detection algorithm to decide whether they actually collide.


Additionally, some physics engine supports point picking, region query, and ray casts. Usually, the physics engine would rely on the broadphase to perform these tasks, because the broadphase has a good approximations of the whereabouts of colliders. Note that in the implementation presented here, picking and ray casts performed by the broadphase give exact results, unlike the collision pair list computation which is a conservative approximation.

When building a physics engine, start with the most trivial N-Squared Broadphase. However, make it so that it is easy to swap it out with other broadphases later. It is very easy and fast to get an N-Squared Broadphase up and running, so that you can focus on other aspects of the physics engine without being bogged down by broadphase specifics.

In this post, we will look at a possible interface of broadphase and an implementation example of the N-Squared Broadphase (clarity is preferred over efficiency in the example). More sophisticated broadphases will be covered in later posts, as they deserve their own posts.

### Interface

As mentioned before, a typical broadphase generates a list of collider pairs that can possibly be colliding, and sometimes a point pick and ray cast methods.

typedef std::pair<Collider *, Collider *> ColliderPair; typedef std::list<ColliderPair> ColliderPairList; class Broadphase { public: // adds a new AABB to the broadphase virtual void Add(AABB *aabb) = 0; // updates broadphase to react to changes to AABB virtual void Update(void) = 0; // returns a list of possibly colliding colliders virtual const ColliderPairList &ComputePairs(void) = 0; // returns a collider that collides with a point // returns null if no such collider exists virtual Collider *Pick(const Vec3 &point) const = 0; // returns a list of colliders whose AABBs collide // with a query AABB typedef std::vector<Collider *> ColliderList; virtual void Query(const AABB &aabb, ColliderList &output) const = 0; // result contains the first collider the ray hits // result contains null if no collider is hit virtual RayCastResult RayCast(const Ray3 &ray) const = 0; };

The `Ray3`

structure is simply a collection of two vectors, a position and a direction (the direction vector is assumed to be normalized).

struct Ray3 { Vec3 pos; Vec3 dir; };

And the `RayCastResult`

structure holds a flag indicating the success of ray cast, a pointer to the collider that the ray hits, the hit position, and surface normal at the hit position.

struct RayCastResult { bool hit; Collider *collider; Vec3 position; Vec3 normal; };

### N-Squared Broadphase

Let’s look at the N-Squared Brodphase class. It basically implements all virtual functions defined in the broadphase interface, and it internally keeps a vector of AABBs for n-squared comparisons. The N-Squared Broadphase is so brute-force that the `Update`

method doesn’t even do anything special.

class NSquared : public Broadphase { public: virtual void Add(AABB *aabb) { m_aabbs.push_back(aabb); } virtual void Update(void) { // do nothing } virtual ColliderPairList &ComputePairs(void); virtual Collider *Pick(const Vec3 &point) const; virtual Query(const AABB &aabb, ColliderList &out) const; virtual RayCastResult RayCast(const Ray3 &ray) const; private: AABBList m_aabbs; ColliderPairList m_pairs; };

#### Computing Collider Pair List

The `NSquared::ComputePairs`

method does what the name of the N-Squared Broadphase suggests: generating a list of possibly colliding colliders using a brute-force double loop.

const ColliderPairList3D &NSquared3D::ComputePairs(void) { m_pairs.clear(); // outer loop auto end = m_aabbs.end(); for (auto i = m_aabbs.begin(); i != end; ++i) { // inner loop auto jStart = i; for (auto j = ++jStart; j != end; ++j) { AABB *aabbA = *i; AABB *aabbB = *j; Collider *colliderA = aabbA->Collider(); Collider *colliderB = aabbB->Collider(); RigidBody *bodyA = colliderA->Body(); RigidBody *bodyB = colliderB->Body(); // skip same-body collision if (bodyA == bodyB) continue; // add collider pair if (aabbA->Collides(aabbB)) m_pairs.push_back( std::make_pair(aabbA->collider, aabbB->collider)); } // end of inner loop } // end of outer loop return m_pairs; }

#### Point Picking

The picking is quite trivial as well. It simply involves looping through all AABBs and return the first corrsponding collider that collides with the specified pick point, if any can be found. Note that there ‘s one level of abstraction here: the `Collider::Contains`

method depends on the actual underlying geometry of the collider. It can be a box, sphere, or anything. The implementations of the picking of specific shapes are not the focus of this post.

Collider *NSquared3D::Pick(const Vec3 &point) { for (auto &aabb : m_aabbs) if (aabb->Contains(position)) return aabb->Collider(); // no collider found return nullptr; }

#### Region Query

The logic of region query is almost identical to point picking: loop through all the AABBs of colliders, and add an AABB to the output list if it collides with the query region (passed in as an AABB).

void NSquared3D::Query(const AABB &aabb, ColliderList &out) { for (auto &colliderAABB: m_aabbs) if (colliderAABB->Collides(aabb)) out.push_back(colliderAABB->Collider()); }

#### Ray Casts

For ray casts, we are going to use brute force to test the ray against every AABB and, if the AABB is hit by the ray, the AABB’s corresponding collider. If we have a non-empty set of colliders hit by the ray, we then pick the ray cast result that is closest to the ray’s position. Implementations of ray-AABB and ray-collider tests are not the focus of this post and are thus abstracted.

RayCastResult NSquared3D::RayCast(const Ray3 &ray) { typedef std::vector<Collider *> CandidateList; // test AABBs for candidates CandidateList candidateList; candidateList.reserve(m_aabbs.size()); for (AABB &aabb : m_aabbs) if (aabb->TestRay(ray)) candidateList.push_back(aabb->Collider); // struct for storing ray-collider test results struct ResultEntry { Collider3D *collider; float t; Vec3 normal; bool operator<(const ResultEntry &rhs) const { // smaller t = closer return t > rhs.t; } }; typedef std::vector<ResultEntry> ResultList; // test actual colliders ResultList resultList; resultList.reserve(candidateList.size()); for (Collider *collider : candidateList) { // hit point = ray.pos + t * ray.dir float t; Vec3 normal; if (collider->TestRay(ray, t, n)) { ResultEntry entry = { collider, t, normal }; resultList.push_back(entry); } } // sort the result list std::sort(resultList.begin(), resultList.end()); RayCastResult result; if (!resultList.empty()) { // the first result entry is the closest one ResultEntry &entry = resultList.front(); result.hit = true; result.collider = entry.collider; result.t = entry.t; result.normal = entry.normal; result.intersection = ray.pos + entry.t * ray.dir; } else result.hit = false; return result; }

### End of Broadphase Overview & N-Squared Implementation Example

This concludes the overview of broadphase and an implementation example of the N-Squared Broadphase. I will very likely move on to other topics before writing about other broadphases.

Hi, thanks for the article. I have a question about why do you keep the colliders in a list in the broadphase? why not fetch them form the World or whatever class ure using? Because in this case, how do you get the updated positions? I know ure keeping references to the colliders, but u need the world position and not the object position to detect collisions.

Hi. I’m afraid I don’t fully understand your question. Can you elaborate on what you meant by “fetching them from the world” and where you would put this logic? Can you also clarify what you meant by “getting the updated positions”?

Did you mean to ask how the colliders can be compared without access to the world, since the colliders store coordinates in local space and not world space? If that’s what you meant to ask (I’m going out on a limb here), every time the world is updated, information needed to perform broadphase and collision detection in world space can be computed and cached in each collider. This way, such world space computations only need to happen once per collider per physics step.

Sorry for being so lame as I am doing this for the first time based on what you have mentioned.

OK I am now stuck at what to do next? What I intend to do is make my box collide with a plane. I have the box which falls down fine. So now do I need to generate a collider of the plane and then pass its pointer to each rigidbody? or do I need to instruct each rigibody to contain the plane as its collidor? I understand how the upper code works but I am having a lot of difficulty putting all this in a demo app? And couldn’t I just calculate the AABB of my plane/box and pass that as a collidor?

If its fine with you, could you please help me out with this? I can email my code if that helps?

My approach is constructing each rigid body as a collection of colliders.

What you’ll need next is collision detection and resolution (which you can learn by reading the following articles). For collision detection between a box and a plane, you can either write a special-case algorithm or use the general GJK algorithm; it’s all up to you (I just use GJK for everything except for sphere-sphere and sphere-box collisions because I’m lazy).

Hi Allen,

A couple of problems here .

1) The NSquared member m_pairs should be a vector IIUC

should be

2) The Pick function should just return the Collider.It should not call the Contains function again (which returns a boolean result). That is, this function

should be this

3) This line in ComputePairs

should be this

Thanks for pointing out the typos. Fixed.