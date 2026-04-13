---
title: 'Game Physics: Implementing Support Function for Polyhedrons using Half Edges
  | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/02/game-physics-implementing-support-function-for-polyhedrons-using-half-edges/
author: Allen Chou
published: '2014-02-19'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

The half edge data structure is a nice data structure to represent polyhedron meshes. I will first introduce to you the half edge data structure; then, I will show you an example implementation of the half edge data structure; lastly, I will explain how we can implement an efficient [support function](http://allenchou.net/2013/12/game-physics-collision-detection-csos-support-functions/) for polyhedrons using a hill-climbing technique with the half edge data structure.

Please note that this entire post assumes convex polyhedrons.

### The Half Edge Data Structure

The half edge data structure is used to represent meshes using 3 lists: a list of vertices, a list of half edges (directed edges, distinguished from regular bi-directional edges), and a list of faces.

A vertex is a point in 3D. Each half edge points from one vertex to another; two half edges consisted of the same pair of vertices but pointing in opposite directions are __twins__. A face is a triangle. Vertices, edges, and faces are all __features__ of a mesh.

Note that a face does not necessarily have to be a triangle in a half edge data structure; it can be a polygon of any number of vertices. However, for simplicity’s sake, the example implementation shown in this post uses triangle faces.

The implementation I will show below is index-based instead of pointer-based in terms of reference-keeping, because this implementation supports dynamic addition and removal of vertices and faces, managing its internal memory usage. A __free list__ variable for a feature stores the index of a free feature, and each free feature has a __free link__ property that refers to the next free feature; basically, a free list is implemented as a singly linked list.

We define a face by a loop of 3 half edges, where the face is to the left of each half edge (CCW winding).


Each half edge contains the index of the face to its left, the index of the vertex it is pointing at, the index of the next half edge of the same face, the index of the previous half edge of the same face, and the index of its twin. Each vertex contains a position and the index of an outgoing half edge; it doesn’t matter which half edge it is, for we can recover the entire set of outgoing edges. Each face contains the index of an edge that the face is formed by; same as half edges, it doesn’t matter which edge it is, because we can always recover the entire loop of half edges forming the face.

The half edge data structure essentially contains __adjacency information__ of features. We can perform various adjacency queries on such structure, such as querying for all adjacent vertices of a vertex, or querying for the two adjacent faces of an edge. Hence, I use the name `AdjacencyInfo`

for the data structure.

Below is the interface for the `AdjacencyInfo`

structure.

struct AdjacencyInfo { // half edge struct Edge { int vert; // pointed to by half edge int face; // to the left of half edge int next; int prev; int twin; int freeLink; bool active; Edge(void) : vert(-1) , face(-1) , next(-1) , prev(-1) , twin(-1) , freeLink(-1) , active(false) { } }; struct Vert { Vec3 position; int edge; // a half edge pointing away int freeLink; bool active; Vert(void) : edge(-1) , freeLink(-1) , active(false) { } }; struct Face { int edge; // an incident half edge int freeLink; bool active; Face(void) : edge(-1) , freeLink(-1) , active(false) { } }; // type defs typedef std::vector<Vert> VertList; typedef std::vector<Edge> EdgeList; typedef std::vector<Face> FaceList; //constructure AdjacencyInfo(void) { Clear(); } // operations int AddVert(const Vec3 &position); void RemoveVert(int v); int AddFace(int v0, int v1, int v2); void RemoveFace(int f); void Clear(void); // utils int FindVertEdge(int v) const; // container for memory management VertList m_verts; EdgeList m_edges; FaceList m_faces; // free lists int m_freeVerts; int m_freeEdges; int m_freeFaces; // counters uint m_numVerts; uint m_numEdges; uint m_numFaces; // edge records typedef std::pair<int, int> VertPair; typedef std::map<VertPair, int> EdgeMap; EdgeMap m_edgeMap; };

First, let’s look at the function templates that allocate and free features. A feature’s `active`

property is set in these two function templates, indicating whether this feature is allocated from the container or not.

template <typename T, typename Container> int Allocate(int &freeList, Container &container) { int index = -1; if (freeList < 0) { // free list empty, just push index = static_cast<int>(container.size()); container.resize(index + 1); } else { index = freeList; // grab free feature T &feature = container[freeList]; // free list freeList = feature.freeLink; // remove feature from free list feature.freeLink = -1; } T &feature = container[index]; feature.active = true; return index; } template <typename T, typename Container> static void Free(int index, int &freeList, Container &container) { T &feature = container[index]; feature.freeLink = freeList; feature.active = false; freeList = index; }

Now, let’s look at the methods that adds a new vertex and removes a vertex from the mesh. Notice that the removal method destroys faces that are connected to the vertex.

int AdjacencyInfo::AddVert(const Vec3 &position) { const int v = Allocate<Vert>(m_freeVerts, m_verts); auto &vert = m_verts[v]; // write position vert.position = position; // initialize edge index vert.edge = -1; ++m_numVerts; return v; } void AdjacencyInfo::RemoveVert(int v) { auto &vert = m_verts[v]; // remove faces this vert connects to const int startEdge = vert.edge; if (startEdge >= 0) { int e = startEdge; do { auto &edge = m_edges[e]; RemoveFace(edge.face); e = m_edges[edge.prev].twin; } while (e != startEdge); } // dispose vert if (vert.edge >= 0) vert.edge = -1; // update free list Free<Vert>(v, m_freeVerts, m_verts); --m_numVerts; }

Next, let’s look at the methods that adds a new face and removes a face from the mesh. The face creation requires 3 indices of vertices forming the face. This process is a little bit more complicated, so I will explain the algorithm with the comments.

int AdjacencyInfo::AddFace(int v0, int v1, int v2) { const int faceVerts[3] = { v0, v1, v2 }; // allocate face const int f = Allocate<Face>(m_freeFaces, m_faces); auto &face = m_faces[f]; // create edges { // iterate face edges int faceEdgeIndices[3] = {-1, -1, -1}; for (uint i = 2, j = 0; j < 3; i = j++) { const uint v0 = faceVerts[i]; const uint v1 = faceVerts[j]; auto &vert0 = m_verts[v0]; auto &vert1 = m_verts[v1]; // check existence of half edge pair const auto edgeIter = m_edgeMap.find(VertPair(v0, v1)); const bool edgePairExists = edgeIter != m_edgeMap.end(); int e01 = -1; int e10 = -1; if (edgePairExists) { e01 = edgeIter->second; e10 = m_edges[e01].twin; } else { // allocate & init half edge pair e01 = Allocate<Edge>(m_freeEdges, m_edges); e10 = Allocate<Edge>(m_freeEdges, m_edges); // link twins m_edges[e01].twin = e10; m_edges[e10].twin = e01; // record edge existence m_edgeMap[VertPair(v0, v1)] = e01; m_edgeMap[VertPair(v1, v0)] = e10; m_numEdges += 2; m_numBoundaryEdges += 2; } // end of edge allocation auto &edge01 = m_edges[e01]; auto &edge10 = m_edges[e10]; // link vert to edges if (edge01.vert < 0) edge01.vert = v1; if (edge10.vert < 0) edge10.vert = v0; // link face to edge if (edge01.face < 0) { edge01.face = f; --m_numBoundaryEdges; } // link edge to vert if (vert0.edge < 0) vert0.edge = e01; // link edge to face if (face.edge < 0) face.edge = e01; // record face edges faceEdgeIndices[i] = e01; } // link face edges for (unsigned i = 2, j = 0; j < 3; i = j++) { const int eI = faceEdgeIndices[i]; const int eJ = faceEdgeIndices[j]; m_edges[eI].next = eJ; m_edges[eJ].prev = eI; } } // end of edge creation ++m_numFaces; return f; } int AdjacencyInfo::FindVertEdge(int v) const { // POSSIBLE OPTIMIZATION: // this is currently a linear operation for (auto &pair : m_edgeMap) { if (v == pair.first.first) return pair.second; } return -1; } void AdjacencyInfo::RemoveFace(int f) { // remove adjacent edges const int startEdge = m_faces[f].edge; int faceVertIndices[3] = {-1, -1, -1}; int faceEdgeIndices[3] = {-1, -1, -1}; int e = startEdge; int i = 0; do { auto &edge = m_edges[e]; const int t = edge.twin; const int n = edge.next; const int p = edge.prev; auto &twin = m_edges[t]; auto &next = m_edges[n]; auto &prev = m_edges[p]; faceVertIndices[i] = edge.vert; faceEdgeIndices[i] = e; ++i; // free both edges if twin face does not exist if (twin.face < 0) { m_edgeMap.erase(VertPair(edge.vert, prev.vert)); m_edgeMap.erase(VertPair(prev.vert, edge.vert)); edge.twin = -1; twin.twin = -1; Free<Edge>(e, m_freeEdges, m_edges); Free<Edge>(t, m_freeEdges, m_edges); m_numEdges -= 2; m_numBoundaryEdges -= 2; } ++m_numBoundaryEdges; e = n; } while (e != startEdge); // unlink everything from edges for (const int e : faceEdgeIndices) { // okay to access data members after fake "free" auto &edge = m_edges[e]; edge.next = -1; edge.prev = -1; edge.vert = -1; edge.face = -1; } // update vert edge for (const int v : faceVertIndices) { auto &vert = m_verts[v]; vert.edge = FindVertEdge(v); } // unlink edge from face auto &face = m_faces[f]; face.edge = -1; // finally, free face Free<Face>(f, m_freeFaces, m_faces); --m_numFaces; }

Lastly, the trivial clear method that removes all features:

void AdjacencyInfo::Clear(void) { m_verts.clear(); m_edges.clear(); m_faces.clear(); m_numVerts = 0; m_numEdges = 0; m_numFaces = 0; m_freeVerts = -1; m_freeEdges = -1; m_freeFaces = -1; m_edgeMap.clear(); }

### Adjacency Query

As mentioned before, we are ultimately going to use the half edge data structure to implement a support function for polyhedrons using a hill-climbing approach. Hill-climbing requires the ability to query adjacent vertices of a given vertex. Below is the general algorithm for performing an operation on all adjacent vertices of a vertex.

// loop through all edges leaving myVert int e = myVert->edge; int startEdge = e; const float oldBestDot = bestDot; do { auto &edge = edges[e]; // get adjacent vert pointed by edge const int vertIndex = edge.vert; auto vert = &verts[vertIndex]; // PERFORM OPERATION ON vert HERE // get next out-going edge e = edges[edge.twin].next; } while (startEdge != e);

### Hill-Climbing Support Function

If you’re implementing a polyhedron collider with traditional triangle lists, then you’ll probably end up using some sort of brute-force approach to implement its support function.

const Vec3 Support(const Mesh &mesh, const Vec3 &dir) { float bestDot = -FLT_MAX; Vec3 support; for (const auto &vert : mesh.Verts()) { const float tempDot = vert.Dot(dir); if (tempDot > bestDot) { bestDot = tempDot; support = vert; } } return support; }

If the polyhedron collider is stored as a half edge structure, then we can use a hill-climbing technique to implement the support function.

The concept is simple: We start with a random vertex (the first vertex in the vertex list will do) and compute its dot product with the support direction (support value). We then use the adjacency information to find all the vertices around the vertex, compute the support values of these vertices, move to the vertex that has the largest support value, and repeat this process until no adjacent vertex of the current vertex can give a better support value. The last vertex is our support point.

const Vec3 Support(const Mesh &mesh, const Vec3 &dir) { // grab adjacency information auto &adj = mesh.GetAdjacencyInfo(); auto &verts = adj.m_verts; auto &edges = adj.m_edges; // start from first point int bestVertIndex = 0; auto bestVert = &verts[bestVertIndex]; float bestDot = dir.Dot(bestVert->position); bool end = false; while (!end) { // loop through all edges leaving best vert int e = bestVert->edge; int startEdge = e; const float oldBestDot = bestDot; do { auto &edge = edges[e]; // get adjacent vert pointed by edge const int vertIndex = edge.vert; auto vert = &verts[vertIndex]; const float dot = dir.Dot(vert->position); if (dot >= bestDot + EPSILON) { // record new best vert bestVertIndex = bestVertIndex; bestVert = vert; bestDot = dot; } // get next out-going edge e = edges[edge.twin].next; } while (startEdge != e); // end if no new best vert is found end = (bestDot == oldBestDot); } return bestVert->position; }

### End of Half Edge Data Structure for Polyhedrons

Now that you understand the half edge data structure, you should be able to implement a support function for polyhedrons that performs better than the naive brute-force approach (with reasonably many vertices per polyhedron, that is).