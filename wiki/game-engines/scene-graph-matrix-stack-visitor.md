---
tags: [scene-graph, visitor-pattern, matrix-stack, 场景图, 变换, 引擎架构]
date: 2026-04-14
sources: 1
---

# 场景图：矩阵栈与访问者模式

构建场景图（scene graph）时有一个看似很自然的做法：每个节点自己持有一份 **全局变换**（global transform），父节点的 `update` 把这份全局变换递归地刷新给子节点。[[allen-chou|Allen Chou]] 早期写 2.5D billboard 引擎 ZedBox 时就是这么干的——效果能跑，但很快变得难维护，而且根本不适用于真正的 **scene graph**：当一个子节点允许有多个父节点时，"每个节点一份全局变换"的假设就崩了，因为同一节点在不同路径下的全局变换根本不同。

## 把全局变换从节点里搬出去

破局的思路出奇简单：**全局变换不属于节点，它属于遍历过程**。节点只需要维护自己的 **local transform**，遍历时再临时组合出全局变换。一旦把状态从节点里剥离，多父节点、实例化复用都不再是问题。

## 矩阵栈

[[coordinate-spaces|坐标空间]]的层级组合天然符合栈结构：下压一层就是"进入子坐标系"，弹出就是"回到父坐标系"。一个最小的矩阵栈接口只有三个操作：

```
interface IMatrixStack {
    get top(): Matrix;
    push(m: Matrix): void;
    pop(): Matrix;
}
```

配合场景图的深度优先遍历，就是经典的"进入节点时 push、离开节点时 pop"模式。栈顶在任何时刻都代表"从根到当前节点的累积变换"，等价于 [[mvp-transform|MVP]] 里的 Model 矩阵那一截。

## 访问者模式把栈"带下去"

问题是：这个矩阵栈该放哪？如果挂在节点上，那又回到了"节点持有全局状态"的老路。Allen Chou 在和 [Minko 3D 引擎](http://aerys.in/minko) 作者 Jean-Marc Le Roux 聊过之后，意识到答案是 **访问者模式（Visitor Pattern）**：矩阵栈被一个 visitor 对象持有，遍历的时候 visitor 去"拜访"每个节点，节点在被访问的瞬间才有机会读 `visitor.matrixStack.top()` 并计算自己的全局变换。

```
class ContainerNode implements INode {
    visit(visitor: IVisitor): void {
        // 进入子坐标系
        visitor.matrixStack.push(visitor.matrixStack.top() * localTransform);
        for (const child of children) child.visit(visitor);
        // 回到父坐标系
        visitor.matrixStack.pop();
    }
}
```

叶节点则简单地读栈顶：

```
visit(visitor: IVisitor): void {
    const globalTransform = visitor.matrixStack.top() * localTransform;
    // 用 globalTransform 渲染当前叶节点
}
```

## 为什么这个重构很值

- **正确性**：同一个节点挂在不同父亲下、在同一帧里参与多次遍历，各自拿到的全局变换是独立的。节点本身不再持有会被"污染"的状态。
- **可维护性**：渲染、拾取（picking）、包围盒重算、动画采样都可以实现为**不同的 visitor**，共享同一棵场景图，而节点类保持精简。这正是访问者模式的经典受益场景：操作族和数据结构独立演化。
- **与图形 API 的默契**：早期固定管线的 OpenGL 就内置了矩阵栈（`glPushMatrix` / `glPopMatrix`），这个模式本质上是把同一思路拿到 CPU 端做场景层次管理。

## 相关
- [[mvp-transform]]
- [[coordinate-spaces]]
- [[rendering-pipeline]]
- [[composite-command-pattern]] —— 同样是"把操作族抽出来独立演化"的思路
- [[allen-chou]]
- [[scene-graph-unnecessary-in-engine]] —— 反面观点：[[angelo-pesce|Pesce]] 认为引擎根本不应该以通用场景图为核心

## Sources

- [[sources/allenchou-matrix-stack-visitor]]
