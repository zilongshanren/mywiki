---
tags: [rotation, euler-angles, quaternion, animation, gimbal-lock]
date: 2026-04-19
sources: 1
---

# 万向锁与欧拉角插值

"Gimbal lock"（万向锁）这个从机械陀螺仪继承来的名字在计算机图形里其实有误导性——引擎里没有任何东西被"锁住"，对象可以自由旋转到任何姿态。[[niklas-frykholm]] 在 2013 年那篇 *What is gimbal lock and why do we still have to worry about it?* 里把问题还原到本质：欧拉角（指定轴序后的三个角度，如 XYZ、XZX 共十二种排列）确实能表达任意姿态，但**表示不唯一**，且在某些位置（典型是中间角 = 90°、两个旋转轴重合时）出现坐标奇异——现实中只差一点点的两个姿态，对应的欧拉角却相距 180°。

问题因此不是"表达不了"，而是**关键帧插值**。如果在两个相邻关键帧之间某个欧拉分量翻了 180°，线性插值就会让物体在视口里做一次多余的翻滚。

常见做法——换成四元数插值——只在**内部计算**这一层解决问题：只要在插值前把欧拉角转成 [[quaternion-slerp-nlerp|四元数]] 做 slerp/nlerp，gimbal lock 带来的翻滚就不会出现。注意四元数 slerp 总走最短路径，因此单帧旋转超过 180° 的"多圈旋转"无法原样保留，需要按目标帧率重采样关键帧，再生成新的四元数关键帧。

然而，**动画师的 UI 需求**让欧拉角逃不掉。动画师希望看到三条可编辑的曲线并用切线控制形状——四元数的 xyz 分量画成曲线对动画师没有语义。于是 Stingray 的 cutscene 系统在数据模型上必须保留欧拉角，并提供标配的规避手段：切换轴序（XYZ ↔ XZX ↔ …）、往返四元数做"Euler filter"把 ±180° 的跳变拍回去。换言之，gimbal lock 是一个被欧拉角+曲线编辑器这个**组合**逼出来的永久负担，只要动画师还在曲线里拖控制点，引擎就要继续背它。

和这个主题相关的更深的基础见 [[3d-rotation-math]] 与 [[exponential-map-rotations]]（后者是一种能画曲线又没有奇异的替代方案，但同样不是动画师熟悉的 UI）。

## Sources

- [[sources/bitsquid-gimbal-lock]]
