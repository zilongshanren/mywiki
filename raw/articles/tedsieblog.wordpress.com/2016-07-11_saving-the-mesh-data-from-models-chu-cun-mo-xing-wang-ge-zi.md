---
title: Saving the Mesh Data from Models – 儲存模型網格資料
url: https://tedsieblog.wordpress.com/2016/07/11/saving-the-mesh-data-from-models/
author: Ted Sie
published: '2016-07-11'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

來分享一個提取模型網格資料的方法

在這篇文章用到下列技巧

**•** 製作外掛面板

**• **合併網格

**• **儲存資料

一開始先開啟一個新專案

並匯入一個含有 Skinned Mesh Renderer 的任意模型來當作提取範本

將匯入的模型拖拉至場景中

接著建立一個 SaveSkinMeshWizard.cs 腳本


開啟 SaveSkinMeshWizard.cs 腳本進行腳本撰寫

首先利用 ScriptableWizard 來產生外掛面板

using UnityEngine; using UnityEditor; public class SaveSkinMeshWizard : ScriptableWizard { //This line make the method to show in the Toolbar/SaveMesh/Open Save Mesh From SkinMeshRenderer [MenuItem("SaveMesh/Open Save Mesh From SkinMeshRenderer")] //Create the panel private static void CreateWizard() { ScriptableWizard.DisplayWizard<SaveSkinMeshWizard>( "Save Mesh From MeshFilter" ); } }

到這邊可以發現在面板中出現自定義的選項



可以發現到目前面板開啟後沒有任何輸入參數

所以在這邊我們加入一個 GameObject 參數

為面板新增一個複製物件選項

//Put the object which you want to clone it's mesh public GameObject cloneObject;

到目前為止若點選面板上的 Create 按鈕會出現以下訊息


所以我們需要在腳本中建立 OnWizardCreate 方法改善這個問題

//If we click the create button in the panel, this method will be executed. private void OnWizardCreate() { //User can choose the path of the mesh file string path = EditorUtility.SaveFilePanelInProject( "Save Mesh From MeshFilter", cloneObject.name + "_Mesh", "asset", "Specify where to save the mesh." ); //If user choose one path if( path.Length > 0 ) { //Get all meshes in the SkinnedMeshRenderer SkinnedMeshRenderer[] skinnedMeshRenderers = cloneObject.GetComponentsInChildren<SkinnedMeshRenderer>(); CombineInstance[] combine = new CombineInstance[skinnedMeshRenderers.Length]; //Combine all meshed in one mesh for( int cnt = 0; cnt < skinnedMeshRenderers.Length; cnt++ ) { combine[cnt].mesh = skinnedMeshRenderers[cnt].sharedMesh; combine[cnt].transform = skinnedMeshRenderers[cnt].transform.localToWorldMatrix; } //Create the new mesh Mesh mesh = new Mesh(); mesh.CombineMeshes( combine ); //Optimize the mesh MeshUtility.Optimize( mesh ); //Create the mesh file AssetDatabase.CreateAsset( mesh, path ); } }

完成後再次開啟面板並拖拉模型至 Clone Ocject 參數上

選擇儲存路徑後

按下存檔

就可以完成模型網格資料儲存的動作




最後附上完整程式碼

using UnityEngine; using UnityEditor; public class SaveSkinMeshWizard : ScriptableWizard { //This line make the method to show in the Toolbar/SaveMesh/Open Save Mesh From SkinMeshRenderer [MenuItem("SaveMesh/Open Save Mesh From SkinMeshRenderer")] //Create the panel private static void CreateWizard() { ScriptableWizard.DisplayWizard<SaveSkinMeshWizard>( "Save Mesh From MeshFilter" ); } //Put the object which you want to clone it's mesh public GameObject cloneObject; //If we click the create button in the panel, this method will be executed. private void OnWizardCreate() { //User can choose the path of the mesh file string path = EditorUtility.SaveFilePanelInProject( "Save Mesh From MeshFilter", cloneObject.name + "_Mesh", "asset", "Specify where to save the mesh." ); //If user choose one path if( path.Length > 0 ) { //Get all meshes in the SkinnedMeshRenderer SkinnedMeshRenderer[] skinnedMeshRenderers = cloneObject.GetComponentsInChildren<SkinnedMeshRenderer>(); CombineInstance[] combine = new CombineInstance[skinnedMeshRenderers.Length]; //Combine all meshed in one mesh for( int cnt = 0; cnt < skinnedMeshRenderers.Length; cnt++ ) { combine[cnt].mesh = skinnedMeshRenderers[cnt].sharedMesh; combine[cnt].transform = skinnedMeshRenderers[cnt].transform.localToWorldMatrix; } //Create the new mesh Mesh mesh = new Mesh(); mesh.CombineMeshes( combine ); //Optimize the mesh MeshUtility.Optimize( mesh ); //Create the mesh file AssetDatabase.CreateAsset( mesh, path ); } } }