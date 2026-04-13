---
title: UGUI Event Listener – UGUI 事件接收器
url: https://tedsieblog.wordpress.com/2016/07/11/ugui-event-listener/
author: Ted Sie
published: '2016-07-11'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

由於有人問到了 uGUI 的觸發事件如何使用

所以就參考了網路上的資料

以 NGUI 的 UIEventListener 為底所實作出來的 uGUI 事件接收器

腳本如下

using UnityEngine; using UnityEngine.EventSystems; public class EventListener : EventTrigger { public delegate void VoidDelegate (GameObject go); public VoidDelegate onClick; public VoidDelegate onDown; public VoidDelegate onEnter; public VoidDelegate onExit; public VoidDelegate onUp; static public EventListener Get (GameObject go) { EventListener listener = go.GetComponent<EventListener>(); if (listener == null) listener = go.AddComponent<EventListener>(); return listener; } public override void OnPointerClick(PointerEventData eventData) { if(onClick != null) onClick(gameObject); } public override void OnPointerDown(PointerEventData eventData) { if(onDown != null) onDown(gameObject); } public override void OnPointerEnter(PointerEventData eventData) { if(onEnter != null) onEnter(gameObject); } public override void OnPointerExit(PointerEventData eventData) { if(onExit != null) onExit(gameObject); } public override void OnPointerUp(PointerEventData eventData) { if(onUp != null) onUp(gameObject); } }


使用方式：

using UnityEngine; using System.Collections; public class TestEventListener : MonoBehaviour { void Awake() { EventListener.Get(gameObject).onClick = OnClick; EventListener.Get(gameObject).onDown = OnDown; EventListener.Get(gameObject).onEnter = OnEnter; EventListener.Get(gameObject).onExit = OnExit; EventListener.Get(gameObject).onUp = OnUp; } private void OnClick(GameObject button) { Debug.Log(button.name + " click"); } private void OnDown(GameObject button) { Debug.Log(button.name + " down"); } private void OnEnter(GameObject button) { Debug.Log(button.name + " enter"); } private void OnExit(GameObject button) { Debug.Log(button.name + " exit"); } private void OnUp(GameObject button) { Debug.Log(button.name + " up"); } }


將 TestEventListener 附加到 uGUI 元件上即可使用

在 NGUI 中需要另外附加 Collider 來作為媒介

而在 uGUI 中並不需要額外的 Collider


資料來源