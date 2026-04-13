---
title: Matrix Stack and the Visitor Pattern | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/02/matrix-stack-and-the-visitor-pattern/
author: Allen Chou
published: '2011-02-11'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

**Scene Graphs and Scene Trees**

When building a scene graph framework, such as the display list in ActionScript 3.0, two types of nodes are involved: internal nodes and leaf nodes. The transformation properties (x, y, rotation, etc.) are passed down from parents to children; that is, if the parent’s local coordinate is (10, 10), and a child’s local coordinate is (5, 5), then the global coordinate of the child is (15, 15).

[ZedBox](https://allenchou.net/code.google.com/p/zedbox/), my 2.5D billboard engine, internally manages objects in scene tree structure (a more specific type of scene graph where each child can only have one parent), just like the display list structure in ActoinScript 3.0. Each node holds a reference to an object containing its global transformation. When the scene tree is traversed in the render routine, the global transformation of each node is updated by its parents; in other words, the global transformation of each node is updated recursively from the root down.

Back then, this seemed to be a very reasonable approach to me. Later, however, I found out that this approach eventually made my code very messy and hard to maintain. Also, this approach does not apply to scene graphs; since in a graph each node can have more than one parents, it’s not right to have each node to hold reference to a single global transformation of its own. After a having a little chat with [Jean-Marc Le Roux](http://blogs.aerys.in/jeanmarc-leroux/) (the author of [Minko](http://aerys.in/minko) 3D engine), I got to know that he used the [Visitor Pattern](http://en.wikipedia.org/wiki/Visitor_pattern) in Minko to traverse the nodes managed in scene graph structure. Suddenly, it had struck me that this pattern is the key to calculate global transformation of the nodes in a scene graph. Instead of storing the global transformation of each node in the node itself, each node can have a chance to access the visitor when the visitor visits the node, where the visitor holds a reference to a matrix stack.

**Matrix Stack**

A matrix stack is essentially, well, a stack that contains matrices (here a matrix represents spatial transformation). The interface of a matrix stack may look like this.

interface IMatrixStack { //returns a reference of the top matrix function get top():Matrix; //pushes a matrix to the stack function push(matrix:Matrix):void; //returns the top matrix popped from the stack function pop():Matrix; }

The following code pushes a matrix A to the stack, and then pushes the product of matrix A and matrix B to the stack. Of course, there is no multiplication operation overriding in ActionScript 3.0. I used the multiplication operator just to make the code look clean.

matrixStack.push(A); matrixStack.push( matrixStack.top() * B );

**Visitor Pattern**

Using the Visitor Pattern, the scene graph is traversed by allowing a visitor to “visit” each node, holding information passed from a node to another. The visitor in scene graph contains a matrix stack, whose top matrix is the global transformation of a node’s parent.

This is the interface of a node.

interface INode { function get localTransform():Matrix; function visitor(visitor:IVisitor):void; }

And this is the interface of a visitor.

interface IVisitor { function get matrixStack():IMatrixStack }

Below is a possible implementation of a container (internal) node class.

class ContainerNode implements INode { private var _localTransform:Matrix = new Matrix(); public function get localTransform():Matrix { return _localTransform; } private var _nodes:Vector.<INode> = new Vector.<INode>(); public function add(child:INode):void { if (_nodes.indexOf(child) < 0) { _nodes.push(child); } } public function remove(child:INode):void { var index:int; if (index = _nodes.indexOf(child) >= 0) { _nodes.splice(index, 1); } } public function visit(visitor:IVisitor):void { //push the global transform of the group to the stack visitor.matrixStack.push( visitor.matrixStack.top() * localTransform ); //make the visitor visit the children for each (var child:INode in _children) { child.visit(visitor); } //pop the global transform of the group from the stack visitor.matrixStack.pop(); } }

So, in a child node, the following code calculates the global transformation of the node itself.

function visit(visitor:IVisitor):void { var globalTransform:Matrix = visitor.matrixStack.top() * localTransform; //do something with the global transform }

This is pretty much my current approach to manage scene graphs in [Pyronova](http://code.google.com/p/pyronova/), my bitmap rendering engine, and Bunnyhill, my 2D rendering engine based on [Molehill](http://labs.adobe.com/technologies/flash/molehill/), the upcoming ActionScript 3.0 API that supports GPU acceleration.