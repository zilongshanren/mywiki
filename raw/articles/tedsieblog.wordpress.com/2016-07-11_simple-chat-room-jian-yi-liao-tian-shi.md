---
title: Simple Chat Room – 簡易聊天室
url: https://tedsieblog.wordpress.com/2016/07/11/simple-chat-room/
author: Ted Sie
published: '2016-07-11'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

由於有人問到如何建立聊天室

所以利用 Unity 中內建的 Network 來簡易說明

首先新增一個 Server.cs

using UnityEngine; using System.Collections; public class Server : MonoBehaviour { //The number of allowed incoming connections public int connections = 4; //The port number we want to listen to public int port = 25000; void OnGUI() { //Network state switch (Network.peerType) { //Disconnected case NetworkPeerType.Disconnected: CreateServer(); break; //In server case NetworkPeerType.Server: OnServer(); break; } } //Create server button void CreateServer() { if (GUILayout.Button ("Create Server")) { //Initialize the server //Network.InitializeServer(int connections, int listenPort, bool useNat); Network.InitializeServer( connections, port, false ); } } //Wait for client and display the client information void OnServer() { GUILayout.Label ( "The Server is startting now, waiting for client connecting." ); int length = Network.connections.Length; for (int cnt = 0; cnt < length; cnt++) { GUILayout.Label( "-------------------------" ); GUILayout.Label( "Client " + cnt ); GUILayout.Label( "Client IP : " + Network.connections[cnt].ipAddress ); GUILayout.Label( "Client Port : " + Network.connections[cnt].port ); } } }

Server.cs 腳本主要是用來初始化伺服器

這裡所使用的方法都是 Unity API

這個腳本是用來初始化伺服器提供客戶端連線

接下來新增 Client.cs

using UnityEngine; using System.Collections; public class Client : MonoBehaviour { public string IP = "127.0.0.1"; //The port number we want to listen to public int port = 25000; //The total message private string message; //The send message private string sendMessage = ""; //The client name private string name = ""; void OnGUI() { switch (Network.peerType) { case NetworkPeerType.Disconnected: StartConnect(); break; case NetworkPeerType.Client: OnClient(); break; } } void StartConnect() { if (GUILayout.Button ("Connect to server")) { Network.Connect( IP, port ); } } void OnClient() { name = GUILayout.TextField( name, 10 ); sendMessage = GUILayout.TextField(sendMessage, 25); if (GUILayout.Button ("Send Message")) { //Network send function //networkView.RPC(string name, RPCMode mode, params object[] args); GetComponent<NetworkView>().RPC( "ReceiveMessage", RPCMode.All, name, sendMessage ); sendMessage = ""; } GUILayout.Label ( "Message : " ); GUILayout.Label ( message ); } //Network receive function [RPC] void ReceiveMessage(string n, string msg, NetworkMessageInfo info) { message += n + " : " + msg + "\n"; } }

用來傳遞訊息至其他客戶端

並且接受從其他客戶端傳來的訊息

接下來創建兩個新場景並分別命名為 Server 及 Client

分別將兩個腳本賦予場景中的 Main Camera

並新增 Component → Miscellaneous → Network View 至 Camera 上



接著分別輸出兩個場景檔




產生出 Server 及 Client 執行檔後

分別執行一次 Server、兩次 Client



按下 Create Server 按鈕後

至 Client 端按下 Connect to server 按鈕



若伺服端接收成功後

即可開始進行聊天功能測試

測試結果


此範例所用到的 Unity API 彙整

[NetworkPeerType](http://docs.unity3d.com/ScriptReference/NetworkPeerType.html)

[Network.InitializeServer](http://docs.unity3d.com/ScriptReference/Network.InitializeServer.html)

[Network.Connect](http://docs.unity3d.com/ScriptReference/Network.Connect.html)

[NetworkView.RPC](http://docs.unity3d.com/ScriptReference/NetworkView.RPC.html)

您好,請問有辦法在Unity中做到像Line那樣的聊天室嗎?

如果可以該怎麼做呢

最近在做小專題卡關很久了…

LikeLike

聊天室是一定可以做出來的

但你問的方向過大

所以無法很明確地回答你

不知道是卡在什麼地方呢

LikeLike

我想做的是在遊戲中加好友

然後跟個別好友有個別的聊天室

目前卡住的地方是不知怎麼讓特定的單一client端收到訊息

LikeLike

這要根據你的實現方式來討論

我這邊的實現方式已經是很舊的做法了

LikeLike