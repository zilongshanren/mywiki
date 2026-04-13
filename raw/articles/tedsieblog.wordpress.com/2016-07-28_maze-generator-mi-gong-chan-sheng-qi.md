---
title: Maze Generator – 迷宮產生器
url: https://tedsieblog.wordpress.com/2016/07/28/maze-generator/
author: Ted Sie
published: '2016-07-28'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

嘗試了在 Roguelike 遊戲中會看到的隨機迷宮生成

在每次玩家進入地城時會產生出不一樣的迷宮

使遊戲的變化性提升


# Preparing

##### GameObjectUtils.cs

using UnityEngine; namespace TEDCore.Utils { public static class GameObjectUtils { public static GameObject FindChild(this GameObject root, string name) { GameObject tempObject = null; Transform transformCache = root.transform; int childCount = root.transform.childCount; int cnt = 0; for(cnt = 0; cnt < childCount; cnt++) { tempObject = transformCache.GetChild(cnt).gameObject; if(name == tempObject.name) { return tempObject; } } for(cnt = 0; cnt < childCount; cnt++) { tempObject = transformCache.GetChild(cnt).gameObject; if(tempObject.transform.childCount > 0) { tempObject = tempObject.FindChild(name); if(null != tempObject) { return tempObject; } } } return null; } } }

Line 7

利用了擴充方法 [this](https://msdn.microsoft.com/zh-tw/library/bb383977.aspx)

主要是用來更方便的尋找 GameObject 物件下的同名物件

會在後續的腳本中使用到

首先先建立好會使用到的基本物件 EmptyCellPrefab 及 CellPrefab

![EmptyCellPrefab](../../assets/9f82ecef2b0ed720.png)


![CellPrefab](../../assets/cf3e0abe9d38f82e.png)


EmptyCellPrefab：為迷宮背景的預置物件

CellPrefab：為各個單位的預置物件

# Base Scripts

##### BaseCell.cs

用來產生新的迷宮單位

並將單位配置到迷宮中

using UnityEngine; public class BaseCell { public const string PREFAB_NAME = "CellPrefab"; public Vector2 Center { get { return m_center; } } public GameObject Root { get { return m_root; } } private Vector2 m_center; private GameObject m_root; private BaseMaze m_maze; public BaseCell(int w, int h, MazeGenerator mazeGenerator) { m_center = new Vector2 (w, h); m_root = GameObject.Instantiate (Resources.Load(PREFAB_NAME) as GameObject); m_root.name = string.Format("Cell {0},{1}", m_center.x, m_center.y); m_root.transform.position = new Vector3 (m_center.x, m_center.y, -0.1f); m_maze = mazeGenerator.maze; m_maze.SetCell(w, h, this); } }

Line 14：建構函式，在相對的行列產生基本單位

##### BaseMaze.cs

儲存、管理迷宮單位

using UnityEngine; using System.Collections; public class BaseMaze : MonoBehaviour { public int Width { get { return m_width; } } public int Height { get { return m_height; } } public GameObject emptyCellPrefab; public Transform emptyCellRoot; public Transform cellRoot; private int m_width; private int m_height; private BaseCell[,] m_maze; private GameObject[,] m_emptyMaze; public void InitializeMaze(int width, int height) { DestroyMaze(); m_width = width; m_height = height; m_maze = new BaseCell[m_width, m_height]; m_emptyMaze = new GameObject[m_width, m_height]; for(int w = 0; w < m_width; w++) { for(int h = 0; h < m_height; h++) { m_emptyMaze[w, h] = Instantiate(emptyCellPrefab); m_emptyMaze[w, h].transform.position = new Vector3(w, h); m_emptyMaze[w, h].transform.SetParent(emptyCellRoot); } } } public BaseCell GetCell(int width, int height) { if(width < 0 || width >= m_width || height < 0 || height >= m_height) return null; return m_maze[width, height]; } public void SetCell(int width, int height, BaseCell cell) { if(width < 0 || width >= m_width || height < 0 || height >= m_height) return; m_maze[width, height] = cell; m_maze[width, height].Root.transform.SetParent(cellRoot); } private void DestroyMaze() { if (null == m_maze) return; BaseCell cell = null; GameObject cellObject = null; for(int h = 0; h < m_height; h++) { for(int w = 0; w < m_width; w++) { cell = GetCell(w, h); if(null != cell) { Destroy(m_maze[w, h].Root); } cellObject = m_emptyMaze[w, h]; if(null != cellObject) { Destroy(cellObject); } } } m_maze = null; m_emptyMaze = null; } public bool HasCell(int width, int height) { return null != GetCell(width, height); } }

Line 18：迷宮初始化

Line 39：取得該行列迷宮單位

Line 49：設定該行列迷宮單位

Line 60：刪除迷宮

Line 91：判斷該行列是否已有迷宮單位

##### MazeGenerator.cs

迷宮管理器

負責管理迷宮的生成

以及鏡頭控制

using UnityEngine; using System; using System.Collections; using System.Collections.Generic; public class MazeGenerator : MonoBehaviour { public BaseMaze maze; public int width = 10; public int height = 10; public int roomTestCount = 10; public bool playAnimation = true; void Awake() { GenerateMaze(); } private void SetupCamera() { Camera.main.transform.position = new Vector3 (width - 1, height - 1, -20) / 2; if(Screen.width > Screen.height) { float ratio = (float)Screen.width / Screen.height; if((float)width / height > ratio) Camera.main.orthographicSize = (float)width / 2 + 1; else Camera.main.orthographicSize = (float)height / 2 + 1; } else { float ratio = (float)Screen.height / Screen.width; if((float)height / width > ratio) Camera.main.orthographicSize = (float)height / 2 + 1; else Camera.main.orthographicSize = (float)width / 2 + 1; } } private void InitializeMaze() { SetupCamera (); maze.InitializeMaze(width, height); } public void GenerateMaze() { InitializeMaze (); StartCoroutine(StartGenerateMaze()); } private IEnumerator StartGenerateMaze() { BaseCell cellCache = null; for(int w = 0; w < width; w++) { for(int h = 0; h < height; h++) { if(playAnimation) yield return new WaitForSeconds(0.05f); new BaseCell(w, h, this); } } } }

Line 19：攝影機設置

Line 44：迷宮初始化接口

Line 51：迷宮產生接口

Line 58：迷宮產生

接著在場景中完成基本配置

![Preparing](../../assets/be856c58bba839a5.png)


##### Base Scripts 執行結果

![PreparingGif](../../assets/5b7810bc2b45d402.gif)


# Implement MazeUtils

##### MazeUtils.cs

用來處理在這個專案中會使用的到列舉

以及與列舉相關的靜態方法

using UnityEngine; namespace Maze.Utils { public enum Direction { None, Up, Down, Left, Right, } public enum NeighbourType { Wall, Visited, None, } public static class MazeUtils { public static Vector2 DirectionToVector2(Direction direction) { Vector2 result = Vector2.zero; switch(direction) { case Direction.Up: result = Vector2.up; break; case Direction.Down: result = Vector2.down; break; case Direction.Left: result = Vector2.left; break; case Direction.Right: result = Vector2.right; break; } return result; } public static Direction GetOppositeDirection(Direction direction) { Direction result = Direction.None; switch(direction) { case Direction.Up: result = Direction.Down; break; case Direction.Down: result = Direction.Up; break; case Direction.Left: result = Direction.Right; break; case Direction.Right: result = Direction.Left; break; } return result; } } }

Line 5：方向列舉定義

Line 14：鄰邊單位狀態列舉定義

Line 23：將 Direction 轉換為 Vector2

Line 47：取得反方向 Direction 列舉

# Implement BaseCell

在上一步驟中

我們完成了事前的準備

接下來要開始著手實作 BaseCell 中所需要使用的到方法

##### BaseCell.cs

using UnityEngine; using System; using System.Collections.Generic; using TEDCore.Utils; using Maze.Utils; public class BaseCell { public const string PREFAB_NAME = "CellPrefab"; public Vector2 Center { get { return m_center; } } public GameObject Root { get { return m_root; } } private Vector2 m_center; private GameObject m_root; private BaseMaze m_maze; private Dictionary<Direction, NeighbourType> m_neighbours; private Dictionary<Direction, GameObject> m_walls; public BaseCell(int w, int h, MazeGenerator mazeGenerator) { m_center = new Vector2 (w, h); m_root = GameObject.Instantiate (Resources.Load(PREFAB_NAME) as GameObject); m_root.name = string.Format("Cell {0},{1}", m_center.x, m_center.y); m_root.transform.position = new Vector3 (m_center.x, m_center.y, -0.1f); m_maze = mazeGenerator.maze; m_maze.SetCell(w, h, this); SetupWalls (Direction.None); SetupNeighbours (); } public BaseCell(BaseCell previousCell, Direction direction, MazeGenerator mazeGenerator) { m_center = previousCell.Center + MazeUtils.DirectionToVector2(direction); m_root = GameObject.Instantiate (Resources.Load(PREFAB_NAME) as GameObject); m_root.name = string.Format("Cell {0},{1}", m_center.x, m_center.y); m_root.transform.position = new Vector3 (m_center.x, m_center.y, -0.1f); m_maze = mazeGenerator.maze; m_maze.SetCell((int)m_center.x, (int)m_center.y, this); SetupWalls (direction); SetupNeighbours (); } private void SetupWalls(Direction initialDirection) { m_walls = new Dictionary<Direction, GameObject> (); for(int cnt = 1; cnt < Enum.GetNames(typeof(Direction)).Length; cnt++) { GameObject wall = m_root.FindChild("Wall" + ((Direction)cnt).ToString()); m_walls.Add((Direction)cnt, wall); if(initialDirection != Direction.None) { if((Direction)cnt == MazeUtils.GetOppositeDirection(initialDirection)) { DisableWalls((Direction)cnt); } } } } public void DisableWalls(Direction direction) { m_walls [direction].SetActive (false); } private void SetupNeighbours() { m_neighbours = new Dictionary<Direction, NeighbourType> (); for(int cnt = 1; cnt < Enum.GetNames(typeof(Direction)).Length; cnt++) { m_neighbours.Add((Direction)cnt, NeighbourType.None); } if (m_center.y + 1 == m_maze.Height) m_neighbours[Direction.Up] = NeighbourType.Wall; if (m_center.y - 1 < 0) m_neighbours[Direction.Down] = NeighbourType.Wall; if (m_center.x - 1 < 0) m_neighbours[Direction.Left] = NeighbourType.Wall; if (m_center.x + 1 == m_maze.Width) m_neighbours[Direction.Right] = NeighbourType.Wall; UpdateNeighbours (); } private void UpdateNeighbours() { for(int cnt = 1; cnt < Enum.GetNames(typeof(Direction)).Length; cnt++) { Vector2 direction = m_center + MazeUtils.DirectionToVector2 ((Direction)cnt); if(direction.x < 0 || direction.x == m_maze.Width || direction.y < 0 || direction.y == m_maze.Height) continue; if(m_maze.HasCell((int)direction.x, (int)direction.y)) { m_neighbours[(Direction)cnt] = NeighbourType.Visited; } } } public Direction GetRandomDirection() { UpdateNeighbours (); List<int> directions = new List<int> (); bool noNeighbour = true; for(int cnt = 1; cnt < Enum.GetNames(typeof(Direction)).Length; cnt++) { if(m_neighbours[(Direction)cnt] == NeighbourType.None) { noNeighbour = false; directions.Add(cnt); } } if (noNeighbour) return Direction.None; int randomNum = UnityEngine.Random.Range (0, directions.Count); Direction randomDirection = (Direction)directions[randomNum]; DisableWalls (randomDirection); return randomDirection; } }

Line 36：建構函式，透過輸入的 BaseCell 在相應方向上產生另一個基本單位

Line 52：初始化提取牆壁物件

Line 71：關閉牆壁物件

Line 77：初始化設定鄰邊單位狀態為 NeighbourType.Wall

Line 101：更新鄰邊單位狀態為 NeighbourType.Wall

Line 118：隨機獲取尚未遍歷過的鄰邊方向

# Backtracking Algorithm

#### Backtracking Algorithm Pseudocode

完成了 BaseCell 中所需要用到的方法後

接下來要開始進入如何產生迷宮的部分

在一開始先來看一下最暴力 Backtracking Algorithm 回溯演算法

利用 [Stack](https://msdn.microsoft.com/en-us/library/system.collections.stack(v=vs.110).aspx) 先進後出的結構

不斷的遍歷所有 BaseCell

直到所有 BaseCell 的鄰邊都不為空

Add the initialBaseCelltoCellStackwhileCellStackis not empty peek theBaseCellcfromCellStackifchas an empty neighbor choose a random neighbor create the newBaseCelland add it toCellStackelse popcfromCellStack

#### Implement Backtracking Algorithm

完成了回溯法的虛擬程式碼後

我們就可以來著手實作

先定義好每種演算法的基礎類別

##### AlgorithmBase.cs

using System.Collections; public class AlgorithmBase { public bool IsGenerating { get { return m_isGenerating; } } protected MazeGenerator m_mazeGenerator; protected bool m_isGenerating = false; public AlgorithmBase(MazeGenerator mazeGenerator) { m_mazeGenerator = mazeGenerator; } public virtual IEnumerator Update (bool playAnimation) { return null; } }

#### Implement Backtracking Algorithm

##### BacktrackingAlgorithm.cs

using System.Collections; using System.Collections.Generic; using Maze.Utils; public class BacktrackingAlgorithm : AlgorithmBase { private Stack<BaseCell> m_cellStack; public BacktrackingAlgorithm(MazeGenerator mazeGenerator) : base(mazeGenerator) { } public override IEnumerator Update(bool playAnimation) { m_isGenerating = true; m_cellStack = new Stack<BaseCell> (); if(playAnimation) yield return null; m_cellStack.Push (new BaseCell(0, 0, m_mazeGenerator)); BaseCell cellCache = null; Direction directionCache = Direction.None; while(m_cellStack.Count != 0) { cellCache = m_cellStack.Peek(); directionCache = cellCache.GetRandomDirection(); if(directionCache != Direction.None) { if(playAnimation) yield return null; m_cellStack.Push(new BaseCell(cellCache, directionCache, m_mazeGenerator)); } else { m_cellStack.Pop(); } } m_isGenerating = false; } }

#### Result of Backtracking Algorithm

完成了 Backtracking Algorithm 後

我們必須對 MazeGenerator 做一些調整

來看到演算法的結果

##### MazeGenerator.cs

using UnityEngine; using System; using System.Collections; using System.Collections.Generic; public class MazeGenerator : MonoBehaviour { public BaseMaze maze; public int width = 10; public int height = 10; public int roomTestCount = 10; public bool playAnimation = true; public AlgorithmBase algorithm; void Awake() { algorithm = new BacktrackingAlgorithm(this); GenerateMaze(); } private void SetupCamera() { Camera.main.transform.position = new Vector3 (width - 1, height - 1, -20) / 2; if(Screen.width > Screen.height) { float ratio = (float)Screen.width / Screen.height; if((float)width / height > ratio) Camera.main.orthographicSize = (float)width / 2 + 1; else Camera.main.orthographicSize = (float)height / 2 + 1; } else { float ratio = (float)Screen.height / Screen.width; if((float)height / width > ratio) Camera.main.orthographicSize = (float)height / 2 + 1; else Camera.main.orthographicSize = (float)width / 2 + 1; } } private void InitializeMaze() { SetupCamera (); maze.InitializeMaze(width, height); } private bool IsGenerating() { if (null != algorithm && algorithm.IsGenerating) { return true; } return false; } public void GenerateMaze() { if(IsGenerating()) { return; } StopGenerateMaze (); InitializeMaze (); StartGenerateMaze (); } private void StartGenerateMaze() { StartCoroutine(algorithm.Update(playAnimation)); } private void StopGenerateMaze() { StopCoroutine(algorithm.Update(playAnimation)); } }

#### Backtracking Algorithm 執行結果

![BacktrackingAlgorithm](../../assets/5b45adb9bee9ea7e.gif)


# Backjumping Algorithm

#### Backjumping Algorithm Pseudocode

現在來試著套入 Backjumping Algorithm

與 Backtracking 最大的差異是在陣列的結構

Backtracking 中，在 Cell 周圍都不為空時，會提取陣列中的最後一個物件

Backjumping 中，則會提取陣列的第一個物件

Add the initialBaseCelltoCellListwhileCellListis not empty get the lastBaseCellcfromCellListifchas an empty neighbor choose a random neighbor create the newBaseCelland add it toCellListelse removecfromCellListmove the firstBaseCellto the last inCellList

#### Implement Backjumping Algorithm

##### BackjumpingAlgorithm.cs

using System.Collections; using System.Collections.Generic; using Maze.Utils; public class BackjumpingAlgorithm : AlgorithmBase { private List<BaseCell> m_cellList; public BackjumpingAlgorithm(MazeGenerator mazeGenerator) : base(mazeGenerator) { } public override IEnumerator Update(bool playAnimation) { m_isGenerating = true; m_cellList = new List<BaseCell> (); if(playAnimation) yield return null; m_cellList.Add (new BaseCell(0, 0, m_mazeGenerator)); BaseCell cellCache = null; Direction directionCache = Direction.None; while(m_cellList.Count != 0) { cellCache = m_cellList[m_cellList.Count - 1]; directionCache = cellCache.GetRandomDirection(); if(directionCache != Direction.None) { if(playAnimation) yield return null; m_cellList.Add(new BaseCell(cellCache, directionCache, m_mazeGenerator)); } else { m_cellList.RemoveAt(m_cellList.Count - 1); if(m_cellList.Count >= 2) { BaseCell firstCell = m_cellList[0]; m_cellList.RemoveAt(0); m_cellList.Add(firstCell); } } } m_isGenerating = false; } }

#### Implement Backjumping 執行結果

![BackjumpingAlgorithm](../../assets/1ea5e17b08976c12.gif)


# Prims Algorithm

#### Prims Algorithm Pseudocode

Prims 的最大差別是在每次提取時隨機提取陣列中的物件

Add the initialBaseCelltoCellListwhileCellListis not empty get the randomBaseCellcfromCellListifchas an empty neighbor choose a random neighbor create the newBaseCelland add it toCellListelse removecfromCellList

#### Implement Prims Algorithm

##### PrimsAlgorithm.cs

using System.Collections; using System.Collections.Generic; using Maze.Utils; public class PrimsAlgorithm : AlgorithmBase { private List<BaseCell> m_cellList; public PrimsAlgorithm(MazeGenerator mazeGenerator) : base(mazeGenerator) { } public override IEnumerator Update(bool playAnimation) { m_isGenerating = true; m_cellList = new List<BaseCell> (); if(playAnimation) yield return null; m_cellList.Add (new BaseCell(0, 0, m_mazeGenerator)); BaseCell cellCache = null; Direction directionCache = Direction.None; int randomCache = 0; while(m_cellList.Count != 0) { randomCache = UnityEngine.Random.Range(0, m_cellList.Count); cellCache = m_cellList[randomCache]; directionCache = cellCache.GetRandomDirection(); if(directionCache != Direction.None) { if(playAnimation) yield return null; m_cellList.Add(new BaseCell(cellCache, directionCache, m_mazeGenerator)); } else { m_cellList.RemoveAt(randomCache); } } m_isGenerating = false; } }

#### Prims Algorithm 執行結果

![PrimsAlgorithm](../../assets/25c7e4fca9fbb06a.gif)


# Algorithm Callback

為了增加迷宮的可玩性

需要先在 Algorithm 中加入 callback

用來在迷宮產生完畢後，執行其他功能

##### AlgorithmBase.cs

using System; using System.Collections; public class AlgorithmBase { public bool IsGenerating { get { return m_isGenerating; } } protected MazeGenerator m_mazeGenerator; protected bool m_isGenerating = false; public AlgorithmBase(MazeGenerator mazeGenerator) { m_mazeGenerator = mazeGenerator; } public virtual IEnumerator Update (bool playAnimation, Action onComplete = null) { return null; } }

##### BacktrackingAlgorithm.cs

using System; using System.Collections; using System.Collections.Generic; using Maze.Utils; public class BacktrackingAlgorithm : AlgorithmBase { private Stack<BaseCell> m_cellStack; public BacktrackingAlgorithm(MazeGenerator mazeGenerator) : base(mazeGenerator) { } public override IEnumerator Update(bool playAnimation, Action onComplete = null) { m_isGenerating = true; m_cellStack = new Stack<BaseCell> (); if(playAnimation) yield return null; m_cellStack.Push (new BaseCell(0, 0, m_mazeGenerator)); BaseCell cellCache = null; Direction directionCache = Direction.None; while(m_cellStack.Count != 0) { cellCache = m_cellStack.Peek(); directionCache = cellCache.GetRandomDirection(); if(directionCache != Direction.None) { if(playAnimation) yield return null; m_cellStack.Push(new BaseCell(cellCache, directionCache, m_mazeGenerator)); } else { m_cellStack.Pop(); } } m_isGenerating = false; if(null != onComplete) { onComplete(); } } }

##### BackjumpingAlgorithm.cs

using System; using System.Collections; using System.Collections.Generic; using Maze.Utils; public class BackjumpingAlgorithm : AlgorithmBase { private List<BaseCell> m_cellList; public BackjumpingAlgorithm(MazeGenerator mazeGenerator) : base(mazeGenerator) { } public override IEnumerator Update(bool playAnimation, Action onComplete = null) { m_isGenerating = true; m_cellList = new List<BaseCell> (); if(playAnimation) yield return null; m_cellList.Add (new BaseCell(0, 0, m_mazeGenerator)); BaseCell cellCache = null; Direction directionCache = Direction.None; while(m_cellList.Count != 0) { cellCache = m_cellList[m_cellList.Count - 1]; directionCache = cellCache.GetRandomDirection(); if(directionCache != Direction.None) { if(playAnimation) yield return null; m_cellList.Add(new BaseCell(cellCache, directionCache, m_mazeGenerator)); } else { m_cellList.RemoveAt(m_cellList.Count - 1); if(m_cellList.Count >= 2) { BaseCell firstCell = m_cellList[0]; m_cellList.RemoveAt(0); m_cellList.Add(firstCell); } } } m_isGenerating = false; if(null != onComplete) { onComplete(); } } }

##### PrimsAlgorithm.cs

using System; using System.Collections; using System.Collections.Generic; using Maze.Utils; public class PrimsAlgorithm : AlgorithmBase { private List<BaseCell> m_cellList; public PrimsAlgorithm(MazeGenerator mazeGenerator) : base(mazeGenerator) { } public override IEnumerator Update(bool playAnimation, Action onComplete = null) { m_isGenerating = true; m_cellList = new List<BaseCell> (); if(playAnimation) yield return null; m_cellList.Add (new BaseCell(0, 0, m_mazeGenerator)); BaseCell cellCache = null; Direction directionCache = Direction.None; int randomCache = 0; while(m_cellList.Count != 0) { randomCache = UnityEngine.Random.Range(0, m_cellList.Count); cellCache = m_cellList[randomCache]; directionCache = cellCache.GetRandomDirection(); if(directionCache != Direction.None) { if(playAnimation) yield return null; m_cellList.Add(new BaseCell(cellCache, directionCache, m_mazeGenerator)); } else { m_cellList.RemoveAt(randomCache); } } m_isGenerating = false; if(null != onComplete) { onComplete(); } } }

# Room Generator

完成了三種演算方式的 Callback 後

目前迷宮的道路都已經可以自動產生出來了

但是往往在地城類遊戲中

都會有各種房間的配置來提升遊戲可玩性

首先建立房間的基本配置

包含：房間中心、房間長寬

##### BaseRoom.cs

using UnityEngine; public class BaseRoom { public int PivotW { get { return m_pivotW; } } public int PivotH { get { return m_pivotH; } } public int RoomWidth { get { return m_roomWidth; } } public int RoomHeight { get { return m_roomHeight; } } private int m_pivotW; private int m_pivotH; private int m_roomWidth; private int m_roomHeight; public BaseRoom(int width, int height) { m_pivotW = Random.Range (1, width - 2); m_pivotH = Random.Range (1, height - 2); m_roomWidth = Random.Range (2, Mathf.Min(width - m_pivotW, 20)); m_roomHeight = Random.Range (2, Mathf.Min(height - m_pivotH, 20)); if((float)m_roomHeight / m_roomWidth > 1.5f) { m_roomHeight = (int)(m_roomWidth * Random.Range(1.0f, 1.5f)); } else if((float)m_roomWidth / m_roomHeight > 1.5f) { m_roomWidth = (int)(m_roomHeight * Random.Range(1.0f, 1.5f)); } } }

# Implement Room Generator

##### RoomGenerator.cs

uusing UnityEngine; using System.Collections.Generic; public class RoomGenerator { private MazeGenerator m_mazeGenerator; private int m_testCount; private List<BaseRoom> m_rooms; public RoomGenerator(MazeGenerator mazeGenerator, int testCount = 1) { m_mazeGenerator = mazeGenerator; m_testCount = testCount; } public void Generate() { m_rooms = new List<BaseRoom> (); for(int cnt = 0; cnt < m_testCount; cnt++) { BaseRoom baseRoom = new BaseRoom(m_mazeGenerator.width, m_mazeGenerator.height); if(CanCreateRoom(baseRoom)) { CreateRoom(baseRoom); } } } private bool CanCreateRoom(BaseRoom baseRoom) { if (m_mazeGenerator.maze.HasCell(baseRoom.PivotW, baseRoom.PivotH) || m_mazeGenerator.maze.HasCell(baseRoom.PivotW, baseRoom.PivotH + baseRoom.RoomHeight - 1) || m_mazeGenerator.maze.HasCell(baseRoom.PivotW + baseRoom.RoomWidth - 1, baseRoom.PivotH) || m_mazeGenerator.maze.HasCell(baseRoom.PivotW + baseRoom.RoomWidth - 1, baseRoom.PivotH + baseRoom.RoomHeight - 1)) return false; for(int h = baseRoom.PivotH - 1; h < baseRoom.PivotH + baseRoom.RoomHeight + 1; h++) { for(int w = baseRoom.PivotW - 1; w < baseRoom.PivotW + baseRoom.RoomWidth + 1; w++) { if(w == m_mazeGenerator.maze.Width || h == m_mazeGenerator.maze.Width || w < 0 || h < 0) return false; if(m_mazeGenerator.maze.HasCell(w, h)) return false; } } return true; } private void CreateRoom(BaseRoom baseRoom) { m_rooms.Add(baseRoom); BaseCell baseCell = null; float randomR = Random.Range(0, 255f) / 255; float randomG = Random.Range(0, 255f) / 255; float randomB = Random.Range(0, 255f) / 255; for(int h = baseRoom.PivotH; h < baseRoom.PivotH + baseRoom.RoomHeight; h++) { for(int w = baseRoom.PivotW; w < baseRoom.PivotW + baseRoom.RoomWidth; w++) { baseCell = new BaseCell (w, h, m_mazeGenerator); baseCell.SetColor(new Color(randomR, randomG, randomB)); #region corner if(w == baseRoom.PivotW && h == baseRoom.PivotH) { baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(w == baseRoom.PivotW && h == baseRoom.PivotH + baseRoom.RoomHeight - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(w == baseRoom.PivotW + baseRoom.RoomWidth - 1 && h == baseRoom.PivotH) { baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Left); continue; } if(w == baseRoom.PivotW + baseRoom.RoomWidth - 1 && h == baseRoom.PivotH + baseRoom.RoomHeight - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Left); continue; } #endregion #region edge if(h == baseRoom.PivotH) { baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(h == baseRoom.PivotH + baseRoom.RoomHeight - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(w == baseRoom.PivotW) { baseCell.DisableWalls (Maze.Utils.Direction.Right); baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Down); continue; } if(w == baseRoom.PivotW + baseRoom.RoomWidth - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Down); continue; } #endregion baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Right); } } } public void CreateDoors() { for(int cnt = 0; cnt < m_rooms.Count; cnt++) { CreateDoor(m_rooms[cnt]); } } private void CreateDoor(BaseRoom baseRoom) { int randomDirection = Random.Range (0, 4); int randomW = 0; int randomH = 0; switch(randomDirection) { case 0: randomW = Random.Range(baseRoom.PivotW, baseRoom.PivotW + baseRoom.RoomWidth); randomH = baseRoom.PivotH + baseRoom.RoomHeight - 1; m_mazeGenerator.maze.GetCell(randomW, randomH).DisableWalls(Maze.Utils.Direction.Up); m_mazeGenerator.maze.GetCell(randomW, randomH + 1).DisableWalls(Maze.Utils.Direction.Down); break; case 1: randomW = Random.Range(baseRoom.PivotW, baseRoom.PivotW + baseRoom.RoomWidth); randomH = baseRoom.PivotH; m_mazeGenerator.maze.GetCell(randomW, randomH).DisableWalls(Maze.Utils.Direction.Down); m_mazeGenerator.maze.GetCell(randomW, randomH - 1).DisableWalls(Maze.Utils.Direction.Up); break; case 2: randomW = baseRoom.PivotW; randomH = Random.Range(baseRoom.PivotH, baseRoom.PivotH + baseRoom.RoomHeight); m_mazeGenerator.maze.GetCell(randomW, randomH).DisableWalls(Maze.Utils.Direction.Left); m_mazeGenerator.maze.GetCell(randomW - 1, randomH).DisableWalls(Maze.Utils.Direction.Right); break; case 3: randomW = baseRoom.PivotW + baseRoom.RoomWidth - 1; randomH = Random.Range(baseRoom.PivotH, baseRoom.PivotH + baseRoom.RoomHeight); m_mazeGenerator.maze.GetCell(randomW, randomH).DisableWalls(Maze.Utils.Direction.Right); m_mazeGenerator.maze.GetCell(randomW + 1, randomH).DisableWalls(Maze.Utils.Direction.Left); break; } } }

Line 10：建構函式，在這邊對 RoomGenerator 進行初始化配置

Line 16：房間產生接口

Line 30：檢查該 BaseRoom 能不能產生

Line 54：產生房間，並更新房間牆壁顯示

Line 143：遍歷房間資料

Line 152：產生房間出入口

# Adjust MazeGenerator

最後在 MazeGenerator 中加入 RoomGenerator 方法

##### MazeGenerator.cs

using UnityEngine; using System; using System.Collections; using System.Collections.Generic; public class MazeGenerator : MonoBehaviour { public BaseMaze maze; public int width = 10; public int height = 10; public int roomTestCount = 10; public bool playAnimation = true; public AlgorithmBase algorithm; private RoomGenerator m_roomGenerator; void Awake() { algorithm = new BacktrackingAlgorithm(this); GenerateRoomAndMaze(); } private void SetupCamera() { Camera.main.transform.position = new Vector3 (width - 1, height - 1, -20) / 2; if(Screen.width > Screen.height) { float ratio = (float)Screen.width / Screen.height; if((float)width / height > ratio) Camera.main.orthographicSize = (float)width / 2 + 1; else Camera.main.orthographicSize = (float)height / 2 + 1; } else { float ratio = (float)Screen.height / Screen.width; if((float)height / width > ratio) Camera.main.orthographicSize = (float)height / 2 + 1; else Camera.main.orthographicSize = (float)width / 2 + 1; } } private void InitializeMaze() { SetupCamera (); maze.InitializeMaze(width, height); } private bool IsGenerating() { if (null != algorithm && algorithm.IsGenerating) { return true; } return false; } public void GenerateMaze() { if(IsGenerating()) { return; } StopGenerateMaze (); InitializeMaze (); StartGenerateMaze (); } public void GenerateRoom() { if(IsGenerating()) { return; } InitializeMaze (); StartCreateRoom(); } public void GenerateRoomAndMaze() { if(IsGenerating()) { return; } StopGenerateMaze(); InitializeMaze(); StartCreateRoom(); StartGenerateMaze(m_roomGenerator.CreateDoors); } private void StartCreateRoom() { m_roomGenerator = new RoomGenerator(this, roomTestCount); m_roomGenerator.Generate (); } private void StartGenerateMaze(Action callback = null) { StartCoroutine(algorithm.Update(playAnimation, callback)); } private void StopGenerateMaze() { StopCoroutine(algorithm.Update(playAnimation)); } }

Room And Maze Generate 執行結果

![RoomAndMazeNormal](../../assets/74652ad64622ddef.gif)


#### Room Color Changed

為了增加畫面的變化性

再生成房間的同時加入顏色增加房間的辨識度

在 BaseCell.cs 中加入

public void SetColor(Color color) { m_root.FindChild("Center").GetComponent<MeshRenderer>().material.color = color; }

修改 RoomGenerator.CreateRoom

private void CreateRoom(BaseRoom baseRoom) { m_rooms.Add(baseRoom); BaseCell baseCell = null; float randomR = Random.Range(0, 255f) / 255; float randomG = Random.Range(0, 255f) / 255; float randomB = Random.Range(0, 255f) / 255; for(int h = baseRoom.PivotH; h < baseRoom.PivotH + baseRoom.RoomHeight; h++) { for(int w = baseRoom.PivotW; w < baseRoom.PivotW + baseRoom.RoomWidth; w++) { baseCell = new BaseCell (w, h, m_mazeGenerator); baseCell.SetColor(new Color(randomR, randomG, randomB)); #region corner if(w == baseRoom.PivotW && h == baseRoom.PivotH) { baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(w == baseRoom.PivotW && h == baseRoom.PivotH + baseRoom.RoomHeight - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(w == baseRoom.PivotW + baseRoom.RoomWidth - 1 && h == baseRoom.PivotH) { baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Left); continue; } if(w == baseRoom.PivotW + baseRoom.RoomWidth - 1 && h == baseRoom.PivotH + baseRoom.RoomHeight - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Left); continue; } #endregion #region edge if(h == baseRoom.PivotH) { baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(h == baseRoom.PivotH + baseRoom.RoomHeight - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Right); continue; } if(w == baseRoom.PivotW) { baseCell.DisableWalls (Maze.Utils.Direction.Right); baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Down); continue; } if(w == baseRoom.PivotW + baseRoom.RoomWidth - 1) { baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Down); continue; } #endregion baseCell.DisableWalls (Maze.Utils.Direction.Up); baseCell.DisableWalls (Maze.Utils.Direction.Down); baseCell.DisableWalls (Maze.Utils.Direction.Left); baseCell.DisableWalls (Maze.Utils.Direction.Right); } } }

#### 執行結果

![RoomAndMazeColor](../../assets/542d9e19a4583d7c.gif)


# 加入簡易編輯器執行結果

![FinalMazeEditor](../../assets/c3f00a194abbc7bd.png)


![FinalMazeNormal](../../assets/692f21b7f76e8493.png)


參考資料

[Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

[Backtracking](https://en.wikipedia.org/wiki/Backtracking)

[Backjumping](https://en.wikipedia.org/wiki/Backjumping)

[房间和迷宫：一个地牢生成算法](http://indienova.com/indie-game-development/rooms-and-mazes-a-procedural-dungeon-generator/)

專案 Source Code

[GitHub Source Code](https://github.com/ted10401/MazeGenerator)

感謝分享好東西～ 不過網頁顯示 “” 的編碼怪怪的～ 導致程式碼看起來有點吃力，哈哈。。 🙂

LikeLike

感謝提醒，也許是網頁的編碼出了問題，現在已經修正了！

LikeLike

Hi Ted，

我最近也在處理迷宮生成方面的事情，很幸運能看到這篇文章，有不少幫助

不過對於連接房間的部分我有點小小的疑惑

上面生成門的部分，看起來是隨機選一邊然後開一個洞

如果是這樣的話會不會發生以下問題呢？

1. 兩個緊靠的房間互相連接，但卻未向外連接

http://imgur.com/v3rOoxx

2. 兩個房間卡出一個獨立的走道，它們卻又剛好沒有開向那邊的門

http://imgur.com/hhCPI7P

LikeLike

是有可能會有這問題的喔

可以試著透過修改房間產生的條件

來達到避免以上邏輯問題發生

LikeLike