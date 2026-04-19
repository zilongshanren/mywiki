---
tags: [game-engines, playcanvas, javascript, esm, 脚本系统, 模块化]
date: 2026-04-19
sources: 1
---

# PlayCanvas ESM Scripts：从全局脚本到标准模块

**PlayCanvas 的脚本系统在 2025 年完成了第二次换代**：从 2016 年推出的 Classic Scripts（基于 `pc.createScript` 注册到全局、通过 hidden global 组织代码）换成基于 **ECMAScript Modules**（`.mjs` + `import/export` + class）的 **ESM Scripts**。官方把 ESM 定为**新项目的推荐写法**，但保留与 Classic 的双向兼容——老项目不强制迁移，同项目里两种脚本可以并存。这是一个信号性很强的工程决策：一个 10 年历史的 web 引擎终于把它的脚本编写规约对齐到现代 JS 生态主流。

## 为什么推倒重来

Classic Scripts 的几个结构性痛点，在 2016 年都是"时代局限"：

- **隐藏全局**：每个 script 文件其实是在一个框起来的全局里跑，`pc.createScript('name', ...)` 注册后通过名字查找；IDE 没法从静态代码推导出哪个 script 在哪里被用，**auto-complete 和跳转都靠蒙**。
- **加载顺序**：没有显式依赖图，运行期要靠 project settings 里手动排 script order，错了就跑出 undefined。
- **跨项目复用**：script 代码没法用 npm 或 `import` 分发，复制粘贴成常态。
- **绑不住类型**：虽然可以手工写 `.d.ts`，但脚本自身是"name + attributes 对象"的软结构，类型系统看不懂。

ESM 直接解了这些：

- `import` / `export` 是显式依赖图，打包器能做静态分析，未来支持 tree-shaking。
- 每个 script 是一个**有自己作用域的 class**，没有全局污染。
- Editor 从 `scriptName` 静态字段就能拿到 script 身份；`@attribute` 注释驱动属性 UI 的暴露。
- **Import maps** 支持别名和从 CDN 拉第三方库，这让 web-native 的依赖管理回到 JS 生态主流路径。

## 新写法的形状

最小样板：

```js
import { Script } from 'playcanvas';

export class Rotator extends Script {
    static scriptName = 'rotator';

    /**
     * @attribute
     * @range [0, 10]
     */
    speed = 5;

    update(dt) {
        this.entity.rotateLocal(0, this.speed * dt, 0);
    }
}
```

关键差异：

- 文件是 `.mjs`，原生 ESM。
- 类继承 `Script`，生命周期方法（`update` / `initialize` / …）是 class method 而不是 prototype 上的松散函数。
- **属性通过字段 + 注释声明**——`speed = 5` 带 `@attribute` 注释就能在 Editor 里暴露成滑块，`@range [0, 10]` 就是范围提示。和 Classic 里写 `attributes.add('speed', { type: 'number', ... })` 相比，类型和默认值从源码里直接读。
- `static scriptName` 是 Editor 用来把 JS class 和 Editor 里的 script 组件绑定的 key。

## 工程上的取舍

### 向后兼容优先

PlayCanvas 的 Editor 里 Classic 脚本的已有项目数量巨大。团队没走"砍旧立新"的路，而是保留 Classic 不动、把 ESM 作为并行路径：`.js` 还是 Classic，`.mjs` 进入 ESM 轨道，**同一个项目里两种可以混用**。对于一个商用 web 引擎，这几乎是唯一可行选项——强制迁移会打散社区。

### 工具链收益

ESM 的实际价值在 Editor 和外部 IDE 的体验上：

- **Auto-complete 真的能用了**：TS 可以追到 class 定义，不再依赖运行期注册。
- **Inline docs 跟得上**：JSDoc 直接挂在类和字段上，Editor 和 VSCode 都能读。
- **跨项目复用**：写个 `utils/math.mjs` 可以被多个 scene 里的 script `import`，也可以 publish 到 npm 让别的项目吃。

### 和其他 PlayCanvas 入口的对位

PlayCanvas 现在有三条并行的开发入口：

- **Classic / ESM Scripts** —— 命令式、在 Editor 里挂载到 Entity。
- **Engine** —— 纯代码项目，脚本组织完全自由。
- **[[playcanvas-react-declarative|@playcanvas/react]]** —— 声明式 JSX 包装。

ESM Scripts 是 Editor 路径的现代化，不是另起炉灶的"React 第四路"——它就是把 Editor 里那张 script 列表的每一行变得更规范、更可工具化。

## 相关

- [[playcanvas-react-declarative]]
- [[playcanvas-engine-2-breaking-changes]]
- [[mark-lundin]]
- [[ecs]]

## Sources

- [[sources/playcanvas-esm-scripts]]
