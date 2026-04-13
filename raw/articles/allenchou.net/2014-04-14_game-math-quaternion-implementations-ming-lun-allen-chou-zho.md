---
title: 'Game Math: Quaternion Implementations | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/04/game-math-quaternion-implementations/
author: Allen Chou
published: '2014-04-14'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

I have covered the [basics of quaternions](http://allenchou.net/2014/04/game-math-quaternion-basics/). In this post, I will show some examples of quaternion implementations.

### The Interface

We want our quaternion class to handle basic arithmetics (addition, subtraction, and scalar multiplciation), as well as various operations (normalization, re-normalization, inversion, dot product, projection, quaternion product, vector rotation, and slerp).

class Quat { public: // this component layout is just conforming to my math // notation: [w, v] = [w, (x, y, z)] // the common layout is (x, y, z, w) float w, x, y, z; // constructors Quat(void); Quat(float w, float x, float y, float z); Quat(const Vec3 &axis, float angle); // arithmetics Quat &operator+=(const Quat &rhs); const Quat operator+(const Quat &rhs) const; Quat &operator-=(const Quat &rhs); const Quat operator-(const Quat &rhs) const; Quat &operator*= (float rhs); const Quat operator*(float rhs); // operations Quat &Normalize(void); const Quat Normalized(void) const; Quat &Renormalize(void); const Quat Renormalized(void) const; Quat &Invert(void); const Quat Inverted(void) const; float Dot(const Quat &rhs) const; Quat &Project(const Quat &onto); const Quat Projected(const Quat &onto) const; const Quat operator *(const Quat &rhs) const; const Vec3 &operator *(const Vec3 &rhs) const; }; const Quat operator*(float lhs, const Quat &rhs); const Quat Slerp(const Quat &q0, const Quat &q1, float t);

Note that all methods and functions work under the assumption that __all quaternions are unit quaternions__.

Now let’s look at the actual implementations.


### Constructors

The default constructor conveniently corresponds to no rotation at all (identity), hence zero rotation angle. Recall that for an orientation represented by an axis ![Rendered by QuickLaTeX.com \overrightarrow{n}](../../assets/58afda5173643155.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![Rendered by QuickLaTeX.com \[ q = [cos\frac{\theta}{2}, \overrightarrow{n} sin\frac{\theta}{2}] \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-073c21929ce71cdb3fe2892e4e59f843_l3.png)


So this is our default constructor:

Quat::Quat(void) : w(1.0f), x(0.0f), y(0.0f), z(0.0f) { }

And here’s the constructor that takes the components directly from the client code:

Quat::Quat(float w, float x, float y, float z) : w(w), x(x), y(y), z(z) { }

Finally, here’s the constructor that takes an orientation represented by an axis and an angle:

Quat::Quat(const Vec3 &axis, float angle) { w = cos(0.5f * angle); // assume axis vector is normalized float s = sin(0.5f * angle); x = axis.x * s; y = axis.y * s; z = axis.z * s; }

### Arithmetics

The arithmetics are very straightforward, so I will just let the code explain itself:

Quat &Quat::operator+=(const Quat &rhs) { w += rhs.w; x += rhs.x; y += rhs.y; z += rhs.z; return *this; } const Quat Quat::operator+(const Quat &rhs) const { return Quat(w + rhs.w, x + rhs.x, y + rhs.y, z + rhs.z); } Quat &Quat::operator-=(const Quat &rhs) { w -= rhs.w; x -= rhs.x; y -= rhs.y; z -= rhs.z; return *this; } const Quat Quat::operator-(const Quat &rhs) const { return Quat(w - rhs.w, x - rhs.x, y - rhs.y, z - rhs.z); } Quat &Quat::operator*=(const float rhs) { w *= rhs; x *= rhs; y *= rhs; z *= rhs; return *this; } const Quat Quat::operator*(const float rhs) const { return Quat(w * rhs, x * rhs, y * rhs, z * rhs); } const Quat operator*(float lhs, const Quat &rhs) { return rhs * lhs; }

### Normalization

To normalize a quaternion, we need to divide each component by the quaternion’s length.

Quat &Quat::Normalize(void) { float len_inv = 1.0 / sqrt(w * w + x * x + y * y + z * z); w *= len_inv; x *= len_inv; y *= len_inv; z *= len_inv; return *this; } const Quat Quat::Normalized(void) const { float len_inv = 1.0 / sqrt(w * w + x * x + y * y + z * z); return Quat(w * len_inv, x * len_inv, y * len_inv, z * len_inv); }

### Re-normalization

As mentioned in the [previous post](http://allenchou.net/2014/04/game-math-quaternion-basics/), we can utilize [polynomial approximation](http://allenchou.net/2014/02/game-math-fast-re-normalization-of-unit-vectors/) to make re-normalizing a quaternion that is already almost normalized faster than taking the square root of a floating-point number plus a floating-point division.

inline float FastSqrtInvAroundOne(float x) { const float a0 = 15.0f / 8.0f; const float a1 = -5.0f / 4.0f; const float a2 = 3.0f / 8.0f; return a0 + a1 * x + a2 * x * x; } Quat &Quat::Renormalize(const Vec3 &;v) { const float len_sq = w * w + x * x + y * y + z * z; const float len_inv = FastSqrtInvAroundOne(len_sq); w *= len_inv; x *= len_inv; y *= len_inv; z *= len_inv; return *this; } const Quat Quat::Renormalized(const Vec3 &v) const { const float len_sq = w * w + x * x + y * y + z * z; const float len_inv = FastSqrtInvAroundOne(len_sq); return Quat(w * len_inv, x * len_inv, y * len_inv, z * len_inv); }

### Inversion

Inverting a unit quaternion is just taking the conjugate of the quaternion:

Quat &Quat::Invert(void) { x = -x; y = -y; z = -z; return *this; } const Quat Quat::Inverted(void) const { return Quat(w, -x, -y, -z); }

### Dot Product

The dot product for quaternions is simple. It is literally treating quaternions as 4D vectors:

float Quat::Dot(const Quat &rhs) const { return w * rhs.w + x * rhs.x + y * rhs.y + z * rhs.z; }

### Projection

The “projection” of one quaternion onto another is also treated the say way you would for 4D vectors. This little tool will come in handy in later posts.

Quat &Quat::Project(const Quat &onto) { const float dot = Dot(onto); w = dot * onto.w; x = dot * onto.x; y = dot * onto.y; z = dot * onto.z; return *this; } const Quat Quat::Projected(const Quat &onto) const { const float dot = Dot(onto); return Quat(dot * onto.w, dot * onto.x, dot * onto.y, dot * onto.z); }

### Quaternion Product

Recall the formula for quaternion product:

![Rendered by QuickLaTeX.com \begin{flalign*} q_1 q_2 = [(w_1 w_2 - \overrightarrow{v_1} \cdot \overrightarrow{v_2}), \, (w_1 \overrightarrow{v_2} + w_2 \overrightarrow{v_1} + \overrightarrow{v_1} \times \overrightarrow{v2})] \\ \end{flalign*}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-a229d4b99f67390c8441ebe9b4a5d333_l3.png)


And here’s the implementation:

const Quat::Quat &operator *(const Quat &rhs) const { Quat q; const Vec3 vThis(x, y, z); q.w = w * rhs.w - vThis.Dot(rhs); const Vec3 newV = rhs.w * vThis + w * vRhs + vThis.Cross(vRhs); q.x = newV.x; q.y = newV.y; q.z = newV.z; return q; }

### Vector Rotation

Now recall that when we have a 3D vector ![Rendered by QuickLaTeX.com \overrightarrow{r}](../../assets/665cf8264d118337.png)

![Rendered by QuickLaTeX.com q](../../assets/6bacf3521f213f9b.png)


![Rendered by QuickLaTeX.com \[ [0, \overrightarrow{r}'] = q [0, \overrightarrow{r}] q^{-1}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1cf25c6b12addf9d19eedc85f6f3cfa2_l3.png)


where ![Rendered by QuickLaTeX.com \overrightarrow{r}'](../../assets/6e290a96dabf0e24.png)


Using this formula, we end up with the following implementation:

const Vec3 &Quat::operator *(const Vec3 &rhs) const { Quat result = (*this) * Quat(0.0f, rhs.x, rhs.y, rhs.z) * Inverted(); return Vec3(result.x, result.y, result.z); }

However, we can further optimize this operation by ignoring the result’s ![Rendered by QuickLaTeX.com w](../../assets/fdb8d80aa4044c76.png)


const Vec3 &Quat::operator *(const Vec3 &rhs) const { Vec3 v(x, y, z); return (2.0f * w * w - 1.0f) * rhs + 2.0f * v.Dot(rhs) * v + 2.0f * w * v.Cross(rhs); }

### Slerp

Finally, let’s look at slerp. Recall the slerp formula:

![Rendered by QuickLaTeX.com \[ Slerp(q_1, q_2, t) = \frac{sin((1 - t)\Omega)}{sin\Omega}q_1 + \frac{sin(t\Omega)}{sin\Omega}q_2, \, 0 \le t \le 1, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4a231d4f391da718761095c7f71b3370_l3.png)


And here’s our implementation:

const Quat Slerp(const Quat &q0, const Quat &q1, float t) { // the clamp takes care of floating-point errors const float omega = acos(Clamp(q0.Dot(q1), -1.0f, 1.0f)); const float sin_inv = 1.0f / sin(omega); return sin((1.0f - t) * omega) * sin_inv * q0 + sin(t * omega) * sin_inv * q1; }

You may opt to use a faster sine approximation, such as the polynomial approximation technique covered [here](http://allenchou.net/2014/02/game-math-faster-sine-cosine-with-polynomial-curves/).

### End of Quaternion Implementations

This is the end of the post. I have shown examples of quaternion implementations including basic arithmetics (addition, subtraction, and scalar multiplciation) and some important quaternion operations (normalization, re-normalization, inversion, dot product, projection, quaternion product, vector rotation, and slerp).