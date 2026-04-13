---
title: Amplify Shader Editor Beginner – 入門篇
url: https://tedsieblog.wordpress.com/2017/03/22/amplify-shader-editor-beginner/
author: Ted Sie
published: '2017-03-22'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

過往在編寫著色器效果時，都必須要透過大量的電腦圖學、數學計算、渲染流程…等知識來輔佐我們，也因為需要這麼多的事前準備，導致學習著色器的門檻相對較高，讓許多程式、非程式人員不敢輕易的轉動這扇門的把手。

而在前些日子中，偶然注意到 Unity 官方所推薦的這一套可視化著色器編輯器 Amplify Shader Editor。透過這套工具，可以使開發者輕易的跨越進入著色器領域的門檻，就算是非程式人員也可以透過 Amplify Shader Editor 來嘗試製作出屬於自己的酷炫效果。

透過這次的文章，希望可以幫助對著色器有興趣的開發者們，了解可視化著色器編輯器 Amplify Shader Editor 的運作方式、基礎使用方法及各項參數介紹。


文章來源：[Unity Taiwan](https://www.facebook.com/UnityTechTaiwan/)

插件來源：[Amplify Shader Editor](https://www.assetstore.unity3d.com/en/#!/content/68570)


#### Amplify Shader Editor 介紹

Amplify Shader Editor 提供了一個對 Unity 開發者相當友善的開發環境，可以與 Unity 編輯器和著色器完美的融合。透過這個工具，開發者能夠輕鬆實現 AAA 級質量的作品，並且能夠相當靈活地應用在任何 Unity 開發專案中，進而縮短製作團隊在美術呈現畫面上的開發時間。

![](../../assets/4ffc69502f4b0706.png)


透過這個工具，可以實現一些驚人的 AAA 級效果，例如：

![](../../assets/6091b5b028fcba35.gif)

*溶解效果（Dissolve Burn Fx）*

![](../../assets/8e33dac08aedbd5d.gif)

*三维映射（Triplanar Mapping）*

![](../../assets/1f80da933249ea95.gif)

*半透明（Translucency）*

![](../../assets/6dd1a9855a8045d1.gif)

*視差映射（Parallax Mapping）*

![](../../assets/baf1d12ca8a23cb4.gif)

*抖動（Dithering）*

![](../../assets/47bf2edcdc165add.gif)

*Fake Interior*

當然，Amplify Shader Editor 還包含了更多效果等你挖掘。

![](../../assets/461952f48ff26231.gif)



下面就讓我們依次介紹 Amplify Shader Editor 的使用過程與細節介紹，包含**安裝流程**、**基本操作**、**編輯器介面**、**材質模式與著色器模式**、**節點屬性介面**以及 **ASE 著色器 Hello World**。


#### 安裝流程

安裝 Amplify Shader Editor 的步驟相當簡單，只需要三個步驟就可以完成。

**步驟 1**

開啟 Unity 專案，雙擊 Amplify Shader Editor.unitypackage 將工具匯入專案中。

![](../../assets/b365713c5347ac06.png)


或是透過點擊 Assets > Import Package > Custom Package… ，並選擇 Amplify Shader Editor.unitypackage 進行匯入。

![](../../assets/8e998a84c93b6783.png)


**步驟 2**

匯入進度條完成後，在 Import Unity Package 畫面中選擇所有資源並點擊 Import 按鈕，將所有資源匯入專案。

![](../../assets/f9695e622187af63.png)


**步驟 3**

最後為了更好地理解，說明一下 Amplify Shader Editor 目錄結構：

![](../../assets/c2de5972193d02b7.png)


從專案目錄中可以發現，Amplify Shader Editor 事先提供了許多著色器範例，每個範例都包含了單獨的場景（Scene）做效果展示，開發者可以根據需求來直接使用。


#### 基本操作

**開啟 Amplify Shader Editor 編輯器介面**

依次點選 Window > Amplify Shader Editor > Open Canvas，或是雙擊 Amplify Shader Editor（以下簡稱 ASE）材質或著色器自動打開編輯器介面。

![](../../assets/1a06f54ce48b58cb.png)


**建立 Amplify Surface Shader（表面著色器）**

在 Project 面板選取資料夾後，依次點選 Assets > Create > Shader > Amplify Surface Shader，或是在 Project 面板中直接點擊滑鼠右鍵 Create > Shader > Amplify Surface Shader 進行建立。

![](../../assets/8f82a61988fce4ad.png)


**開啟 ASE 著色器編輯畫面**

雙擊 ASE 著色器就可以自動開啟編輯畫面。

![](../../assets/e2d366b2fd7f01f1.png)


或者可以在選擇 ASE 著色器的情況下，透過 Inspector 面板中的 Open in Shader Editor 按鈕開啟。

![](../../assets/d5c21a51699586cf.png)


**著色器文件命名**

可以直接在節點屬性（Node Properties）中的著色器名稱（Shader Name）進行修改，並可以使用正斜線（/）來新增著色器類別。

![](../../assets/e83897e4d54b7825.png)


PS：著色器檔案名稱是唯一的，必須在 Project 頁面中手動設置。但檔案與著色器可以使用不同名稱命名。

**ASE 著色器定位**

此區域在 ASE 編輯介面的左下角，顯示當前的著色器，點擊這個區域可以將 ASE Shader 在專案頁面中定位出來。邊緣的綠框提示當前開啟的著色器。

![](../../assets/8a89cd2d481bd916.png)


**查看 ASE 材質**

雙擊 ASE 材質就可以在編輯頁面中開啟。

![](../../assets/feacba9048629b9e.png)


**ASE 材質定位**

與定位 ASE 著色器相同，可以透過點擊右下角來定位出對應的 ASE 材質，且邊緣的提示框為藍色。

![](../../assets/aa613e1bf17f60ea.png)



#### 編輯器介面

**節點屬性介面（Node Properties）**

透過點擊編輯器中的各個節點，被選擇的節點會切換為橘色框狀態。該節點的屬性就會在節點屬性介面中顯示出來。若未選擇或選擇複數節點，則會顯示主節點的屬性。

![](../../assets/5077a846814f718e.png)

*著色器主節點的節點屬性*

![](../../assets/9bc0723e360ae442.png)

*發射器（Emission）的灰燼顏色（Ember Color Tint）節點的節點屬性*

另外，可以透過點擊節點屬性介面右上角的 “-” 按鈕來將介面最小化，點擊方塊按鈕將介面恢復。

![](../../assets/4bc3bcdd3ed86d7b.gif)


**編輯器頂端區域**

![](../../assets/8eba94832f7b97b5.png)

**保存按鈕**：保存/更新著色器數據。若是修改著色器名稱，需要點擊這個按鈕後才會正式生效。

![](../../assets/5f384d1662426ccb.png)

**自動保存按鈕**：開啟時自動保存著色器數據。

![](../../assets/fb9eb533eb10ae50.png)

**清除按鈕**：刪除所有無效節點。

![](../../assets/335b217832d88313.png)

**文字編輯按鈕**：使用文字編輯器開啟著色器文件。

![](../../assets/078d097adcb7e47e.png)

**回歸按鈕**：選中並定位主節點

![](../../assets/a0762b643c23f4f9.png)

**定位按鈕**：定位選中的節點。如果沒有選擇節點，將會定位出節點集合。

也可以透過雙擊滑鼠左鍵或鍵盤 F 鍵，來進行編輯器介面的自動縮放。

**節點選擇介面**

![](../../assets/4a61421e37cdf26c.png)


節點選擇介面位於編輯器右側，是一個可以搜尋節點類型的清單，可以找到所需要的節點類型，並直接拖放到編輯器中。和節點屬性介面一樣，可以透過點擊 “-” 按鈕來將介面最小化。

此外也可以在編輯器中點擊滑鼠右鍵，開啟節點選擇介面。

![](../../assets/af75c4509547e52d.png)


**使用快捷鍵建立節點**

編輯器中還有一個相當重要的功能，就是可以透過按住快捷鍵後單擊編輯器上的任意位置來建立新節點。在節點選擇介面中，一般會在節點名稱右邊的 [] 中顯示快捷鍵。例如：數字鍵 1 為浮點數（Float）節點，數字鍵 5 為顏色（Color）節點。

![](../../assets/ebe4665ad66f2b98.png)


**ASE 數據處理流程**

![](../../assets/8c5620261925c34b.jpeg)


在上圖中我們可以發現，ASE 的數據處理流程是由左至右的，輸入端口 > 數據處理 > 輸出端口。只有直接或間接連接到主節點的節點才會運作，並用於生成著色器代碼。若節點中包含了未連接的輸入端口，ASE 會在處理流程中使用內部數據，而這些內部數據可以透過節點屬性介面來進行編輯。

**可視化編輯重點**

![](../../assets/4f95c28b6cfd66f2.jpeg)


**選擇節點**：可以透過點擊滑鼠左鍵或透過左鍵拖動範圍來選取節點。此外，可以按住 Shift 鍵並點擊節點來做複選節點的動作。也可以使用 CTRL/CMD + A 來進行全選功能。要取消選取內容時，則可以透過點擊畫面的空白處來進行取消。選取節點並按住左鍵拖移則可以移動所選節點。

**刪除節點**：選取節點並點擊 Delete 鍵則可以將節點刪除。

**建立連接**：在端口點擊滑鼠左鍵並進行拖曳就可以將輸入端口與輸出端口進行連接。也可以點擊完整連接後拖曳到另一個端口形成新的連接。此外，將連接拖曳到畫布空白處則會自動彈出節點選擇介面，可以快速的選擇並建立需要的節點。

**刪除連接**：透過按住 Alt 鍵並點擊節點端口，或是將端口連接拖動到畫布空白處後點擊滑鼠左鍵，就可以刪除連接。連接高亮顯示時，表示連接有由左至右的完整數據流。

**端口**：輸出端口可以連接複數個輸入端口，但是輸入端口只能進行單一連接。此外，連接會自動與附近端口進行匹配，在操作上更為直覺。

**可視範圍**：按住滑鼠右鍵或中鍵可以移動整個畫布的可視範圍。若是選中的節點離開了可視範圍後，畫布將會自動滾動。另外還可以透過滑鼠滾輪放大或縮小可視範圍，會根據畫布上的節點進行縮放。

**兩側介面**：當 ASE 編輯介面的寬度小於 750 px 時，節點屬性介面和節點選擇介面會自動最小化。

#### 材質模式與著色器模式

![](../../assets/b593a65e87af3d0e.jpeg)


ASE 編輯介面包含兩種編輯模式，材質模式與著色器模式，主要取決於透過什麼方式讀取著色器文件。另外可以藉由畫布的外輪廓顏色來判斷編輯模式，藍色代表材質模式，綠色代表著色器模式。

![](../../assets/a2803eba34d6235a.jpeg)


在著色器中設置的數值通常稱為預設值（Default Value）。對任何預設值所做的修改都會自動影響最後的結果。當同時編輯材質和著色器時，需要記得注意哪些屬性有進行變動。

![](../../assets/d96d4181560d5275.jpeg)


材質預設值與著色器預設值不同，可以將材質理解成著色器實例，每個著色器實例的數據都是唯一的，但使用相同的預設值進行建立。材質參數只有在材質模式時才會顯示。在表示變量（顏色 Color、浮點數 Float、整數 Int、向量 Vector、矩陣 Matrix）的節點中有一個 Parameter Type 下拉選單，可以設置為 Property，以便在材質模式下組合出無限數量的變化。

![](../../assets/47be45a56a5435f8.jpeg)


如上圖所示，可以在相同的 ASE 著色器之間進行參數的複製與覆蓋。也可以透過 Open in Shader Editor 按鈕快速打開 Amplify Shader Editor 來編輯著色器與材質。

![](../../assets/1ce20b5ea1d7cf9a.jpeg)


除了使用 Open in Shader Editor 按鈕以外，還可以選擇 Open in Text Editor 按鈕，使用文字編輯器來修改著色器。


#### 節點屬性介面

其中大部分內容參考 Unity 著色器官方文件：

[https://docs.unity3d.com/Manual/SL-Reference.html](https://docs.unity3d.com/Manual/SL-Reference.html)

**主屬性（Main Properties）**

![](../../assets/eb6c1d7bfa74f12b.jpeg)


**著色器類型（Shader Type）**：顯示當前所使用的著色器類型。

**著色器名稱（Shader Name）**：可編輯文字框，用來定義著色器的名稱與路徑，使用正斜線（/）來區分其類別與名稱，例如 UserSamples/EnvironmentGradient。需要注意，著色器名稱與檔案名稱不同，檔案名稱需要額外設定。

**光照模型（Light Model）**：設定當前所使用的光照模型。ASE 提供了標準（Standard）、標準高光（Standard Specular）、Lambert 以及 Blinn Phong 光照模型。

**著色器模型（Shader Model）**：在編寫表面著色器或一般著色器時，HLSL 可以編譯成不同的著色器模型。越高的著色器模型可以完成更多功能，但可能會使著色器在一些較老舊的 GPU 或平台上無法使用。

**精度（Percision）**：定義著色器的計算精度，使用低精度類型可以獲得額外的效能提升，預設為 Float 精度。

**剔除模式（Cull Mode）**：定義著色器的剔除模式。提供了剔除正面（Front）、剔除背面（Back）以及剔除禁用（Off），預設為剔除背面模式。

**渲染路徑（Render Path）**：定義著色器所使用的渲染路徑模式。包含正向渲染（Forward）、延遲渲染（Defferred）以及全部渲染（All），預設為全部渲染模式。

**投射陰影（Cast Shadows）**：定義著色器是否支持投射陰影。

**接收陰影（Receive Shadows）**：定義著色器是否支持接受陰影。

**隊列索引（Queue Index）**：渲染順序偏移值。

**自定義編輯器（Custom Editor）**：允許開發者使用自定義的 ASE 編輯器。

**混合模式（Blend Mode）**

![](../../assets/01e98404a640376b.jpeg)


**混合模式（Blend Mode）**：自動調整混合模式參數，包含不透明（Opaque）、遮罩（Masked）、透明（Transparent）、Alpha Transparent 以及自定義（Custom）。

**渲染類型（Render Type）**：定義著色器的渲染類型，包含不透明（Opaque）、透明（Transparent）、透明剪裁（Transparent Cutout）、背景（Background）、覆蓋（Overlay）、不透明樹（Tree Opaque）、透明剪裁樹（Tree Transparent Cutout）、布告板樹（Tree Billboard）、草（Grass） 以及布告板草（Grass Billboard）。

**渲染順序（Render Queue）**：調整渲染順序，從數值越小的幾何體開始進行渲染。選項包含背景（Background）、幾何（Geometry）、Alpha 測試（Alpha Test）、透明（Trasparent）和覆蓋（Overlay）。

**遮罩剔除數值（Mask Clip Value）**：須與不透明度 alpha 比較，若不透明度小於遮罩剔除數值，則捨棄該像素。

**混合 RGB 和混合 Alpha（Blend RGB、Blend Alpha）**：當像素被寫入屏幕時，會透過何種方式混合。ASE 提供了自定義（Custom）、Alpha 混合（Alpha Blend）、預乘（Premultiplied）、加法（Additive）、Soft Additive、乘法（Multiplicative）和兩倍乘法（2x Multiplicative）模式。

**混合係數（Blend Factor）（Blend Src、Blend Dst）**：一般分為來源係數與目標係數，透過係數間的運算來得到最後結果，若是 BlendOp 使用邏輯運算，則會忽略混合係數。

![](../../assets/14539e53a440c335.png)


**混合操作 RGB 和混合操作 Alpha（Blend Op RGB、Blend Op Alpha）**：包含添加（Add）、子（Sub）、修改子（Rev Sub）、最小（Min）以及最大（Max）。

- 顏色遮罩（Color Mask）：設置顏色通道。

**模板緩衝（Stencil Buffer）**

![](../../assets/c3376b7283be68e0.jpeg)


模板緩衝器可以用來作為模板測試使用，用於保存或是拋棄像素。通常每個像素有 8 個位元，進行繪製時會調用該數值來進行模板測試，已決定是否在進入著色器前將像素計算捨棄。

**參考值（Reference）**：用來與模板緩衝區比較的數值，範圍是 0 ~ 255 整數。

**讀取遮罩值（Read Mask）**：讀取模板緩衝區時使用，默認值為 255，範圍是 0 ~ 255 整數。

**寫入遮罩值（Write Mask）**：寫入模板緩衝區時使用，默認值為 255，範圍是 0 ~ 255 整數。

**比較方法（Comparison）**：將參考值與模板緩衝區的當前內容進行比較的方法，包含大於（Greater）、大於等於（Greater or Equal）、小於（Less）、小於等於（Less or Equal）、等於（Equal）、不等於（Not Equal）、總是（Always）及從不（Never），預設為 Always。

**測試通過（Pass）**：當模板測試通過時所進行的處理，默認值為 keep。

**測試失敗（Fail）**：當模板測試失敗時所進行的處理，默認值為 keep。

**ZFail**：當模板測試通過但深度測試失敗時所進行的處理，默認為 keep。

**曲面細分（Tessellation）**

![](../../assets/c02e335647360734.jpeg)


**馮式曲面細分模式（Phong）**：修改曲面細分位置，使曲面細分稍微跟隨法線做網格生成，預設為 Off。

**類型（Type）**：曲面細分類型，包含基於位置（Distance-based）、固定（Fixed）、邊長（Edge Length）和 Edge Length Cull。

**曲面細分係數（Tess）**：範圍是 1 ~ 32。

**最小值（Min）**：最小細分距離。

**最大值（Max）**：最大細分距離。

**深度（Depth）**

![](../../assets/365d4cb936b56b16.jpeg)


**ZWrite 模式（ZWrite Mode）**：是否將此像素寫入深度緩衝區，預設為 On。若是繪製對象為不透明物件，則開啟此模式。若是繪製對象為透明物件，則關閉此模式。

**ZTest 模式（ZTest Mode）**：如何進行深度測試，包含小於（Less）、等於（Equal）、大於（Greater）、小於等於（LEqual）、大於等於（GEqual）、不等於（NotEqual）和隨時（Always），預設值為 LEqual。

**偏移（Offset）**：允許使用兩個參數來指定深度偏移，係數與單位。

**係數（Factor）**：相對於多邊形的 X 或 Y，縮放最大 Z 斜率。

**單位（Units）**：單位縮放最小可分辨深度緩衝區值。

**渲染平台（Rendering Platforms）**

定義支持平台，預設勾選全部平台。

![](../../assets/356887dbf5f4501e.jpeg)


**可用變量（Available Properties）**

顯示在節點屬性介面中設置為屬性（Property）的變量，可以透過拖動來調整它們的位置。

![](../../assets/1482d1c4b4277d5f.jpeg)



#### ASE 著色器 Hello World

**1. 建立 ASE 著色器**

依次點選 Create > Shader > Amplify Surface Shader 建立 ASE 著色器，重新命名為 MyShader。

**2. 建立 ASE 材質**

依次點選 Create > Material 建立 ASE 材質，重新命名為 MyMaterial。

**3. 開啟 ASE 著色器編輯模式**

點選 MyShader 後，在 Inspector 面板中點選 Open in Shader Editor 開啟 ASE 編輯器。將著色器名稱修改為 MyCollection/Shader1 並保存，最後將 MyShader 著色器與 MyMaterial 材質建立關聯。

![](../../assets/b3dac6736d099a86.jpeg)


**4. 修改光照模型**

將光照模型修改為 Standard Specular。

![](../../assets/b265286a725be164.jpeg)


**5. 新增 Lerp（線性插值）節點**

在畫布中點選滑鼠右鍵開啟節點選單，搜尋 Lerp 並點選新增 Lerp 節點，將 Lerp 輸出節點連接到主節點的 Albedo 輸入節點。

![](../../assets/ee6ffe4dffe4476b.jpeg)


**6. 新增 Color（顏色）節點**

搜尋並新增兩個 Color 節點。

![](../../assets/b764fc8f18b11d69.jpeg)


**7. 設定 Color 節點**

將兩個 Color 節點連接到 Lerp 節點輸入端口。並將 A 節點顏色設為灰色，B 節點顏色設為橘色。

![](../../assets/0dbd09c3472421df.jpeg)


**8. 建立不透明度 Float（浮點數）節點**

搜尋並建立 Float 節點，並命名為 Color Mix。將其連接到 Lerp 節點的 Alpha 輸入端口，最小值設定為 0，最大值設定為 1，並將參數類型設定為 Property。

![](../../assets/43406987fb2e33be.jpeg)


**9. 建立平滑、高光 Float 節點**

建立 Float 節點並重新命名為 Smoothness Level。將其連接到主節點的 Smoothnes（平滑）輸入端口，最小值設為 0，最大值設為 1，並將參數類型設定為 Property。

建立另一個 Float 節點並重新命名為 Specular Level。將其連接到主節點的 Speculer（高光）輸入端口，最小值設為 0，最大值設為 1，並將參數類型設定為 Property。

![](../../assets/abec2be0194745ba.jpeg)


**10. 設定法線貼圖**

最後我們需要找一張法線貼圖，將貼圖直接拖曳到畫布中並連接到主節點的 Normal（法線）輸入端口。因為這邊使用的法線貼圖具有金屬拉絲質感，所以可以看到著色器會呈現出金屬質感。

到這邊，我們成功的完成了第一個 ASE 著色器，不要忘記點擊更新按鈕來定期保存著色器數據，確保你的工作不會遺失。

![](../../assets/05bd6e3af7b045a1.jpeg)



#### 總結

透過這次的文章，可以幫助你了解 ASE 的操作流程以及參數說明，藉由這種可視化的編輯方式，可以大幅降低在編寫著色器時的入門門檻，讓無論是程式、美術以及企劃都能夠嘗試參與畫面呈現的修改與調整。而對於已經有著色器相關基礎的開發者，也可以透過這個工具來理解各種著色器的實作方式，透過文字編輯器來開啟 ASE 所生成的著色器並進行分析、優化效能，以節省著色器的開發時程。