---
title: Some Thoughts on Bunnyhill Interface Design | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/09/some-thoughts-on-bunnyhill-interface-design/
author: Allen Chou
published: '2011-09-25'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

I’ve gone through my first three weeks at [DigiPen](http://digipen.edu), and I finally have some time to cuddle with FlashDevelop once again.

I’ve decided to rewrite Bunnyhill from scratch. It’s been months since my last revision; lots of updates have been added to the latest Flash Player 11, and I’ve got some new ideas. So I think reworking Bunnyhill all over would be the best and fastest approach.

I’m keeping the scene graph structure, and I aim to simplify the initialization and set-up of a Bunnyhill canvas:

var canvas:Canvas = new Canvas ( stage, antiAliasLevel, useDepthAndStencilBuffers );


That’s it. The code above takes care of initializing the `Context3D`

initialization and setup; it also takes care of stage resize handling.

In addition to working with scene graph, I’ve decided to expose to users direct access to the graphics object.

var graphics:IGraphics = canvas.graphics;

In this way, users can have more low-level graphics control. Here’s the current `IGraphics`

interface design. I might add more stuff to it later. It essentially groups together the fundamental operations users need to work with graphics. I’ve split some original option parameters in some `Context3D`

methods into multiple methods, in order to make the interface more user-friendly.

public interface IGraphics { function get vertexShader():IVertexShader; function set vertexShader(value:IVertexShader):void; function get fragmentShader():IFragmentShader; function set fragmentShader(value:IFragmentShader):void; function createVertexBuffer():VertexBuffer; function createIndexBuffer():IndexBuffer; function createTexture(width:uint, height:uint):Texture; function createRenderBuffer ( width:uint, height:uint ):RenderBuffer; function setVertexBufferAt ( index:uint, vertexBuffer:VertexBuffer, format:String ):void; function setVertexShaderConstant ( startIndex:uint, data:Vector.<Number> ):void; function setFragmentShaderConstant ( startIndex:uint, data:Vector.<Number> ):void; function setTextureAt ( index:uint, texture:Texture ):void; function drawTriangles ( indexBuffer:IndexBuffer, startIndex:uint = 0, count:uint = 0 ):void; }

Now for the scene graph. There’s a root node on the canvas object to which users can assign a reference to the root node of a scene graph. The following scene graph is to draw two sprite sheets attached to a group node, which is the root node of the scene graph.

canvas.root = new Group ( mySpriteSheet1, mySpriteSheet2 );

That’s the basic idea. There are more special nodes I’m currently designing, including blend mode nodes, render buffer nodes, transform nodes, etc.

I hope I won’t get too busy with school work before finishing Bunnyhill.