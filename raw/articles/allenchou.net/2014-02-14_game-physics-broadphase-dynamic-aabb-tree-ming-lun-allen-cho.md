---
title: 'Game Physics: Broadphase – Dynamic AABB Tree | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/02/game-physics-broadphase-dynamic-aabb-tree/
author: Allen Chou
published: '2014-02-14'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

Dynamic AABB tree is a type of broadphase that is __borderless__, meaning that it does not impose a strict border limit as some other broadphases do, such as explicit grid and implicit grid.

It is very efficient in all aspects in terms of game physics, including ray casting, point picking, region query, and, most importantly, generating a list of collider pairs that are potentially colliding (which is the main purpose of having a broadphase).

In this post, I will explain how a dynamic AABB tree works and show you a sample implementation.

### The Structure

First, let’s look at the basic concept of a dynamic AABB tree. From its name, you can already guess that it has something to to with storing AABB-related information in a tree structure, and it is dynamic at run time.

Each collider has its own AABB, and they are stored inside a __binary tree__ as leaf nodes. Each internal node, a.k.a. branch node, holds its own AABB data that represents the __union__ of the AABB of both of its children.

Visual aids are always better than plain text. The picture below shows a spatial configurations of several colliders and a visual representation of a possible corresponding tree structure.

![thin AABB tree](../../assets/11988033c2946fef.png)



### Interface

Based on the base interface from the [broadphase overview post](http://allenchou.net/2013/12/game-physics-broadphase/), here’s the interface of our dynamic AABB tree.

class AABBTree : public Broadphase { public: AABBTree(void) : m_root(nullptr) , m_margin(0.2f) // 20cm { } virtual void Add(AABB *aabb); virtual void Remove(AABB *aabb); virtual void Update(void); virtual ColliderPairList &ComputePairs(void); virtual Collider *Pick(const Vec3 &point) const; virtual Query(const AABB &aabb, ColliderList &out) const; virtual RayCastResult RayCast(const Ray3 &ray) const; private: typedef std::vector<Node *> NodeList; void UpdateNodeHelper(Node *node, NodeList &invalidNodes); void InsertNode(Node *node, Node **parent); void RemoveNode(Node *node); void ComputePairsHelper(Node *n0, Node *n1); void ClearChildrenCrossFlagHelper(Node *node); void CrossChildren(Node *node); Node *m_root; ColliderPairList m_pairs; float m_margin; NodeList m_invalidNodes; };

And below is the implementation of the `Node`

structure.

The `Node::data`

property is a pointer to the actual AABB of a collider, and the purpose of the `Node::aabb`

property will be explained later.

struct Node { Node *parent; Node *children[2]; // these will be explained later bool childrenCrossed; AABB aabb; AABB *data; Node(void) : parent(nullptr) , data(nullptr) { children[0] = nullptr; children[1] = nullptr; } bool IsLeaf(void) const { return children[0] = nullptr; } // make this ndoe a branch void SetBranch(Node *n0, Node *n1) { n0->parent = this; n1->parent = this; children[0] = n0; children[1] = n1; } // make this node a leaf void SetLeaf(AABB *data) { // create two-way link this->data = data; data->userData = this; children[0] = nullptr; children[1] = nullptr; } void UpdateAABB(float margin) { if (IsLeaf()) { // make fat AABB const Vec3 marginVec(margin, margin, margin); aabb.minPoint = data->minPoint - marginVec; aabb.maxPoint = data->maxPoint + marginVec; } else // make union of child AABBs of child nodes aabb = children[0]->aabb.Union(children[1]->aabb); } Node *GetSibling(void) const { return this == parent->children[0] ? parent->children[1] : parent->children[0]; } };

### Balance

Similar to conventional binary trees, we would like to keep the AABB tree as __balanced__ as possible, for how balanced an AABB tree is affects its performance on various operations.

However, AABB trees has a different sense of balance compared to conventional binary trees. The balancing of an AABB tree is not based on the __depth__ of leaf nodes, but based on how __evenly__ two child nodes __divide__ their parent’s AABB.

### AABB Update

Many things will have moved within a time step, and thus their AABBs need to be updated. However, this means we will have to re-balance the tree after the AABBs are updated. The most naive way to do this is to re-construct the tree from scratch with the updated AABBs within each time step. It is a plausible solution if your scene is consisted of not too many colliders. But we would like our dynamic AABB tree to be more scalable, so here I’m going to employ the so-called “fat AABB” approach.

The idea is very simple: instead of making a node exactly correspond to the AABB it’s associated with, let’s make the node hold an extra piece of “fat AABB” data that is slightly fatter (larger) than the associated AABB, so the associated AABB is contained within the fat AABB. When the collider moves outside of the fat AABB within a time step, we remove the node from the tree, re-insert the node into the tree from the root, and then assign a new fat AABB to the node. The `AABBTree::m_margin`

property indicates how much fatter the fat AABB is to the original AABB; in the code above, I arbitrarily chose to use the value 0.2 meter (20 centimeters).

Thus, the `Node::aabb`

property stores a fat AABB of where the `Node::data`

property points to if the node is a leaf node, and it stores the union of the `Node::aabb`

properties of the node’s child nodes if the node is a branch node.

With fat AABBs, we only have to move around the nodes whose associated colliders are moving far enough between time steps.

void AABBTree::Update(const TimeStep &timeStep) { if (m_root) { if (m_root->IsLeaf()) m_root->UpdateAABB(m_margin); else { // grab all invalid nodes m_invalidNodes.clear(); UpdateNodeHelper(m_root, m_invalidNodes); // re-insert all invalid nodes for (Node *node: m_invalidNodes) { // grab parent link // (pointer to the pointer that points to parent) Node *parent = node->parent; Node *sibling = node->GetSibling(); Node **parentLink = parent->parent ? (parent == parent->parent->children[0] ? &parent->parent->children[0] : &parent->parent->children[1]) : &m_root; // replace parent with sibling sibling->parent = parent->parent ? parent->parent : nullptr; // root has null parent *parentLink = sibling; delete parent; // re-insert node node->UpdateAABB(m_margin); InsertNode(node, &m_root); } m_invalidNodes.clear(); } } void AABBTree::UpdateNodeHelper (Node *node, NodeList &invalidNodes) { if (node->IsLeaf()) { // check if fat AABB doesn't // contain the collider's AABB anymore if (!node->aabb.Contains(node->data->aabb)) invalidNodes.push_back(node); } else { UpdateNodeHelper(node->children[0], invalidNodes); UpdateNodeHelper(node->children[1], invalidNodes); } } }

### Node Insertion

When inserting a node to an AABB tree, the node is inserted at the root node and propagated down the tree until it reaches a leaf node; then, the leaf node is replaced by a new branch node, whose two children are the inserted node and the leaf node.

When we propagate an inserted node down a tree at a branch, we choose the child node to propagate to that gives the __least increase in volume__ of the branch’s AABB. This gives us a more balanced AABB tree. Of course, you can use other heuristics such as __closest AABB centroid__ when inserting nodes.

void AABBTree::Add(AABB *aabb) { if (m_root) { // not first node, insert node to tree Node *node = new Node(); node->SetLeaf(aabb); node->UpdateAABB(m_margin); InsertNode(node, &m_root); } else { // first node, make root m_root = new Node(); m_root->SetLeaf(aabb); m_root->UpdateAABB(m_margin); } } void AABBTree::InsertNode(Node *node, Node **parent) { Node *p = *parent; if (p->IsLeaf()) { // parent is leaf, simply split Node *newParent = new Node(); newParent->parent = p->parent; newParent->SetBranch(node, p); *parent = newParent; } else { // parent is branch, compute volume differences // between pre-insert and post-insert const AABB *aabb0 = p->children[0]->aabb; const AABB *aabb1 = p->children[1]->aabb; const float volumeDiff0 = aabb0->Union(node->aabb).Volume() - aabb0->Volume(); const float volumeDiff1 = aabb1->Union(node->aabb).Volume() - aabb1->Volume(); // insert to the child that gives less volume increase if (volumeDiff0 < volumeDiff1) InsertNode(node, &p->children[0]); else InsertNode(node, &p->children[1]); } // update parent AABB // (propagates back up the recursion stack) (*parent)->UpdateAABB(m_margin); }

### Node Removal

Node removal is more straight forward, so I will just show the code along with the comments.

void AABBTree::Remove(AABB *aabb) { Node *node = static_cast<Node *>(aabb->userData); // remove two-way link node->data = nullptr; aabb->userData = nullptr; RemoveNode(node); } void AABBTree::RemoveNode(Node *node) { // replace parent with sibling, remove parent node Node *parent = node->parent; if (parent) // node is not root { Node *sibling = node->GetSibling(); if (parent->parent) // if there's a grandparent { // update links sibling->parent = parent->parent; (parent == parent->parent->children[0] ? parent->parent->children[0] : parent->parent->children[1]) = sibling; } else // no grandparent { // make sibling root Node *sibling = node->GetSibling(); m_root = sibling; sibling->parent = nullptr; } delete node; delete parent; } else // node is root { m_root = nullptr; delete node; } }

### Computing Collider Pair List

Now that we have seen how to insert nodes, remove nodes, and update the tree, we can move onto what a broadphase is supposed to do: computing collider pair list, point picking, and ray casts.

The algorithm for computing the collider pair list needs a little bit more explanation. Here I decided to implement it recursively, because the code is more elegant this way. You can always re-implement it iteratively.

Basically, the recursive method `AABBTree::ComputePairsHelper`

takes two nodes as input, and based on the combination of the node types (2 leaf nodes, 1 leaf node plus 1 branch node, or 2 branch nodes), the method either tests for potential collider pair or invoke itself recursively with child nodes of the input nodes.

Here are all the 3 cases:

- 2 Leaf Nodes – We’ve reached the end of the tree, simply check the AABBs of the corresponding colliders and possibly add them to the pair list
- 1 Leaf Node plus 1 Branch Node – Cross check the child nodes of the branch node (make a recursive call with the child nodes), and make recursive calls with the leaf node against each child nodes of the branch node.
- 2 Branch Nodes – Make a recursive call on every combination of 2 nodes out of the 4 child nodes.

With the logic above alone, we can get duplicate pairs added to the list; thus, we use the `Node::childrenCrossed`

Boolean flag to check if the children of a branch node have already been “cross checked (passed into a recursive call)”. This little trick fixes the problem.

ColliderPairList &AABBTree::ComputePairs(void) { m_pairs.clear(); // early out if (!m_root || m_root->IsLeaf()) return m_pairs; // clear Node::childrenCrossed flags ClearChildrenCrossFlagHelper(m_root); // base recursive call ComputePairsHelper(m_root->children[0], m_root->children[1]); return m_pairs; } void AABBTree::ClearChildrenCrossFlagHelper(Node *node) { node->childrenCrossed = false; if (!node->IsLeaf()) { ClearChildrenCrossFlagHelper(node->children[0]); ClearChildrenCrossFlagHelper(node->children[1]); } } void AABBTree::CrossChildren(Node *node) { if (!node->childrenCrossed) { ComputePairsHelper(node->children[0], node->children[1]); node->childrenCrossed = true; } } void AABBTree::ComputePairsHelper(Node *n0, Node *n1) { if (n0->IsLeaf()) { // 2 leaves, check proxies instead of fat AABBs if (n1->IsLeaf()) { if (n0->data->Collides(*n1->data)) m_pairs.push_back(AllocatePair(n0->data->Collider(), n1->data->Collider())); } // 1 branch / 1 leaf, 2 cross checks else { CrossChildren(n1); ComputePairsHelper(n0, n1->children[0]); ComputePairsHelper(n0, n1->children[1]); } } else { // 1 branch / 1 leaf, 2 cross checks if (n1->IsLeaf()) { CrossChildren(n0); ComputePairsHelper(n0->children[0], n1); ComputePairsHelper(n0->children[1], n1); } // 2 branches, 4 cross checks else { CrossChildren(n0); CrossChildren(n1); ComputePairsHelper(n0->children[0], n1->children[0]); ComputePairsHelper(n0->children[0], n1->children[1]); ComputePairsHelper(n0->children[1], n1->children[0]); ComputePairsHelper(n0->children[1], n1->children[1]); } } // end of if (n0->IsLeaf()) }

### Point Picking

For point picking, we can just perform a iterative point-AABB check starting from the root node.

void AABBTree::Pick(const Vec3 &pos, PickResult &result) { std::queue<Node *> q; if (m_root) q.push(m_root); while (!q.empty()) { Node &node = *q.front(); q.pop(); if (node.IsLeaf()) { if (node.data->Collides(pos)) result.push_back(node.data->Collider()); } else { q.push(node.children[0]); q.push(node.children[1]); } } }

### Ray Casts

The logic flow for ray casting is very similar to point picking, except that there is an extra optimization step, where a node is instantly discarded if the ray intersection parameter `t`

is larger than our current smallest `t`

.

const RayCastResult AABBTree::RayCast (const Ray3 &ray, float maxDistance) { RayCastResult result; result.hit = false; result.t = 1.0f; std::queue<Node *> q; if (m_root) { q.push(m_root); } while (!q.empty()) { Node &node = *q.front(); q.pop(); AABB &colliderAABB = *node.data; AABB &aabb = node.IsLeaf() ? colliderAABB : node.aabb; float t; if (RayAABB(ray, aabb, maxDistance, t)) { // the node cannot possibly give closer results, skip if (result.hit && result.t < t) continue; if (node.IsLeaf()) { Collider &collider = *colliderAABB.Collider(); Vec3 n; float t; if (collider.RayCast(ray, maxDistance, t, n)) { if (result.hit) // compare hit { if (t < result.t) { result.collider = &collider; result.t = t; result.normal = n; result.intersection = ray.pos + t * maxDistance * ray.dir.Normalized(); } } else // first hit { result.hit = true; result.collider = &collider; result.t = t; result.ray = ray; result.normal = n; result.intersection = ray.pos + t * maxDistance * ray.dir.Normalized(); } } } else // is branch { q.push(node.children[0]); q.push(node.children[1]); } } } return result; }

### End of Dynamic AABB Tree

This concludes my example implementation of the dynamic AABB tree broadphase. If you followed my previous advice and already have an N-squared broadphase that can be easily swapped out, you can consider switching to dynamic AABB tree if the number of your rigid bodies is getting too large that the N-Squared broadphase starts dragging the performance of your game.

Hey I think I’ve found a different solution to the “crossed” problem. It seriously bugged me to have more data and time spent on this. I simply check if n0 and n1 are siblings. I wonder if that’s the trick Joshua was talking about, if not I’m very curious what it is.

Anyway thanks for that article 🙂

Pingback: Introductory Guide to AABB Tree Collision Detection | Azure From The Trenches

Nice post. Thanks.

One question about “AABBTree::Pick” method. Before adding the two children nodes to the queue, I guess you could make a collision test between Node::aabbox and the point for better performance, no ?

Yes. That’s a valid optimization. Thanks for pointing it out.

One other thing – you don’t really need to do the cross check flagging when looking for pairs. As long as you have a consistent rule for choosing which nodes to process, it will work.

For example, instead only add a pair when the leaf node n0 < n1 (or the other way around – it doesn't matter).

You can still end up with worst-case scenarios (all nodes on the right of the tree, say) pretty easily no matter what heuristic you use for deciding where to insert a node, since this completely depends on the order nodes are added. The heuristic’s job is to try to cluster spatially-similar nodes in the same area of the tree, and ideally keep the nodes as small as possible but it’s doing this based on very limited information.

You really need to rebalance the tree (either during insertion or after a bulk add or remove) to keep the performance up. If you add a line of aabbs sequentially, you’ll probably generate the worst-case scenario.

One option for balancing the tree is to do what AVL trees do, and rotate nodes when an imbalance is discovered. It’s not perfect since it allows local imbalances in tree height up to 1 level, which can lead to global imbalances of more than that, but it does do a pretty good job and is fairly quick. I found that I could pull out some of the code used for swapping children during insertion and this made the rebalancing pretty easy to implement.

It has come to my attention that your ComputePairsHelper function fails to actually prune the objects as you only test the Aabb’s when they are leaf nodes. Because of this you are always iterating over all pairs in the tree and not getting any performance gains.

Also, there’s a neat trick to avoid having to set bits for the cross check. Message me sometime and I can go over it for you.

Thanks, Josh. Will do.

Thanks a lot for this tutorial, you helped me a lot understanding AABB Trees.

thanks , i got it 🙂

Hi allen, nice article! thank you.

I can not understand what is going on in CrossChildren(), why do you recall ComputePairsHelper() inside of it?

Shouldn’t it be like ClearChildrenCrossFlagHelper() method?

The ComputeParisHelper() call in CrossChildren() is the base recursion call, and the ComputePairsHelper() calls itself to recurse over the entire AABB tree.

Can you clarify what you mean by “be like ClearChildrenCrossFlagHelper() method”?

Nice post! Thank you!

One comment: in ComputePairsHelper, do you not need to run CrossChildren on n0 and n1 (if they are not leaves), in the case where n0->aabb and n1->aabb do not intersect? Refering to your illustrated A-B-C example above, A may very well collide with B, even though C’s aabb does not intersect the aabb containing A and B.

Ah. You’re right. Thanks for pointing that out. The code is now fixed.

Thank you for your post on Dynamic AABB Tree. To understand the concept is one thing but to know how to implement it is an entirely different thing. Very much appreciated for the implementation example. I just started to learn about Collision Detection and I’m interested in Dynamic AABB Tree.

Here in your example I’m just wondering why you need a two-way link in your SetLeaf()-Method, specifically the line “data->userData = this”? Does it mean that every AABB needs to hold a Node* member? What is its purpose? I can’t seem to grasp it. Especially since you don’t use “userData” anywhere else beside in the Remove()-Method.

Thank you very much.

Exactly. The user data is used to look up corresponding node of an AABB to be removed. The Remove method takes a pointer to an AABB, and it needs to know the corresponding node so it knows what to pass to the RemoveNode method.

Note that this is just an example implementation. There are definitely other ways to achieve this.

You refer to a “proxy” member on the Node class, but there isn’t one there. What is this supposed to be? (A Proxy3D? what is this supposed to hold?).

I’m sorry. By “proxy” I meant the collider’s AABB (not the node’s fat AABB). I copied it over from my school project, which I forgot to modify/simplify for the purpose for this post. I already fixed it. Thanks for pointing it out.

Have you run performance tests on this? All those pointer follows are very scary.

These days I strongly prefer a simple bucketing or spatial-hashing technique, with cells 10-20x the size of average rigid bodies. Bucket objects in a first pass (of course a body may be in multiple cells) and then run a simple n^2 check on the contents of each bucket. If you keep your buckets around you can use them for ray or shape casts as well.

The simplicity of this type of broadphase makes it easy to optimize and there’s a nice opportunity to go wide on the per-bucket n^2 checks.

The typical game scenario has a giant static background (which should always be special-cased out) and small bodies typically grouped in “clusters” with a fair bit of space between them. I like to focus on trying to identify the clusters and not spend so much effort on saving time within them – they’re likely to be all hooked up by either contact or ragdoll constraints anyway.

I’ve only experimented with the N^2 broadphase and dynamic AABB tree broadphase so far, so I’m not sure how my implementation of dynamic AABB tree performs compared to other broadphases beside N^2.

I will definitely experiment with spatial-hashing broadphases later. Thanks for the advice.

I am only starting with physics, but for my current implementation I’ve used simple brute force – object picking. For larger scenes your AABB would be much better.

Do you have any demo for the topic?

Another question: is AABB better that three based on Bounding spheres? and what about Object Aligned Bounding Boxes?

Sorry. I don’t have a working demo at the moment. The code segments are from my school project that I am not allowed to fully disclose.

In terms of game physics broadphase, I think AABB trees are better than bounding sphere trees and OBB trees, because collision tests of AABBs are more efficient than OBBs and AABB trees can be much more tightly packed than bounding sphere trees.