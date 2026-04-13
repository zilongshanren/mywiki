---
title: MaterialPropertyDrawer in Shader – GUI without creating shaderGUI
url: https://cmwdexint.com/2017/05/06/materialpropertydrawer-in-shader-gui-without-creating-shadergui/
author: Ming Wai Chan
published: '2017-05-06'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

![16999105_467532653370479_4085466863356780898_n](../../assets/23b72ac701e67b24.jpg)



[https://docs.unity3d.com/ScriptReference/MaterialPropertyDrawer.html](https://docs.unity3d.com/ScriptReference/MaterialPropertyDrawer.html)

Shader "MaterialPropertyDrawer"
{
Properties
{
_MainTex("Texture", 2D) = "white" {}
[HideInInspector] _MainTex2("Hide Texture", 2D) = "white" {}
[NoScaleOffset] _MainTex3("No Scale/Offset Texture", 2D) = "white" {}
[PerRendererData] _MainTex4("PerRenderer Texture", 2D) = "white" {}
[Normal] _MainTex5("Normal Texture", 2D) = "white" {}
_Color("Color", Color) = (1,0,0,1)
[HDR] _HDRColor("HDR Color", Color) = (1,0,0,1)
_Vector("Vector", Vector) = (0,0,0,0)
//Can't go below zero
[Gamma] _GVector("Gamma Vector", Vector) = (0,0,0,0)
// Header creates a header text before the shader property.
[Header(A group of things)]
// Will set "_INVERT_ON" shader keyword when set
[Toggle] _Invert("Auto keyword toggle", Float) = 0
// Will set "ENABLE_FANCY" shader keyword when set.
[Toggle(ENABLE_FANCY)] _Fancy("Keyword toggle", Float) = 0
// Will show when ENABLE_FANCY is true //Feature request
//[ShowIf(ENABLE_FANCY)] _ShowIf("Show If", Float) = 0
// Blend mode values
[Enum(UnityEngine.Rendering.BlendMode)] _Blend("Blend mode Enum", Float) = 1
// A subset of blend mode values, just "One" (value 1) and "SrcAlpha" (value 5).
[Enum(One,1,SrcAlpha,5)] _Blend2("Blend mode subset", Float) = 1
// Each option will set _OVERLAY_NONE, _OVERLAY_ADD, _OVERLAY_MULTIPLY shader keywords.
[KeywordEnum(None, Add, Multiply)] _Overlay("Keyword Enum", Float) = 0
// ...later on in CGPROGRAM code:
//#pragma multi_compile _OVERLAY_NONE, _OVERLAY_ADD, _OVERLAY_MULTIPLY
// ...
// A slider with 3.0 response curve
[PowerSlider(3.0)] _Shininess("Power Slider", Range(0.01, 1)) = 0.08
// An integer slider for specified range (0 to 255)
[IntRange] _Alpha("Int Range", Range(0, 255)) = 100
// Default small amount of space.
[Space] _Prop1("Small amount of space", Float) = 0
// Large amount of space.
[Space(50)] _Prop2("Large amount of space", Float) = 0
}