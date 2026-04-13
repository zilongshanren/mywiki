---
title: Quaternion differentiation
url: https://fgiesen.wordpress.com/2012/08/24/quaternion-differentiation/
published: '2012-08-24'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Quaternion differentiation

I wanted to point someone to a short explanation of this today and noticed, with some surprise, that I couldn’t find something concise within 5 minutes of googling. So it seems worth writing up. I’m assuming you know what quaternions are and what they’re used for.

First, though, it seems important to point one thing out: Actually, there’s nothing special at all about either integration or differentiation of quaternion-valued functions. If you have a quaternion-valued function of one variable q(t), then

same as for any real- or complex-valued function.

So what, then, is this post about? Simple: unit quaternions are commonly used to represent rotations (or orientation of rigid bodies), and rigid-body dynamics require integration of orientation over time. Almost all sources I could find just magically pull a solution out of thin air, and those that give a derivation tend to make it way more complicated than necessary. So let’s just do this from first principles. I’m assuming you know that multiplying two unit quaternions quaternions q1q0 gives a unit quaternion representing the composition of the two rotations. Now say we want to describe the orientation q(t) of a rigid body rotating at constant angular velocity. Then we can write



where describes the rotation the body undergoes in one time step. Since we have constant angular velocity, we will have

, and more generally

for all nonnegative integer k by induction. So for even more general t we’d expect something like


.


Now, qω is a unit quaternion, which means it can be written in *polar form*

where θ is some angle and n is a unit vector denoting the axis of rotation. That part is usually mentioned in every quaternion tutorial. Embedding real 3-vectors as the corresponding pure imaginary quaternion, i.e. writing just for the quaternion

, is usually also mentioned somewhere. What usually isn’t mentioned is the crucial piece of information that the polar form of a quaternion, in fact, just the quaternion version of Euler’s formula: Any unit complex number

can be written as the complex exponential of a pure imaginary number

, and similarly any unit-length quaternion (and q

ω in particular) can be written as the exponential of a pure imaginary quaternion

which gives us a natural definition for

.


Now, what if we want to write a differential equation for the behavior of q(t) over time? Just compute the derivative of q(t) as you would for any other function of t. Using the chain and product rules we get:

Now t and θ are real numbers, so the exponential is of a real number times n; exp is defined as a power series, and for arbitrary c real we have

n commutes with powers of n, and real numbers commute with everything; therefore, n commutes with exp(cn) for arbitrary c, and thus

The vector θ**n** is in fact just the angular velocity ω, which yields the oft-cited but seldom-derived equation:

This is usually quoted completely without context. In particular, it’s not usually mentioned that q(t) describes the orientation of a body with constant angular velocity, and similar for the crucial link to the exponential function.

Hi,

It was with great satisfaction I found your deduction of the quarternion time derivate. I’ve been searching for this myself, but until now in vain.

However, I don’t understand when you say: “The vector θn is in fact just the angular velocity ω,..”

The angular velocity ω have the units radians/s, but the quantity θn have the unit radians as n is dimensionless.

Or have I missed something…

Regards,

Göran

In my derivation, t is just a real number; I’m not bothering with units throughout the post, which is what muddles things a bit.

If you want to patch it up and use dimensional quantities, you need to do it throughout:

The initial definition q(t) = q_omega^t * q_0 doesn’t work as-is; you need a fudge factor k [1/s] so you can use a power function here (we need to nail down after what amount of time we’ve turned by “one omega”). So you get

q(t) = q_omega^(k*t) * q_0

and for the differential equation, that gives us

q'(t) = k*(theta/2)*n * exp(k*t*(theta/2)*n) * q_0 = k*(theta/2)*n * q(t) = 1/2 * omega * q(t)

where omega = k*theta*n. k is still [1/s], theta is [rad] and n is a dimensionless vector.

Hope that helps. Sorry for the confusion.

Hi,

your explanation about this question regarding unit is already very clear. Thanks a lot for that.

But I’m still confused about the relationship. From my understanding, omega should be how much theta per second. Then it should be:

omega = k*theta

Why omega = k*theta*n? I think it doesn’t make sense that n is representing the direction of angular rate, because it should be ‘orthogonal’ between n and angular rate, shouldn’t it? Otherwise, what does n represent?

Hope to get your answer soon!

Regards,

Hongwei.

n is the normalized axis. theta is [radians], k is [1/s]. k*theta is radians per second but doesn’t specify the axis of rotation.

Hello! When checking the derivation of partial derivatives of a function of a quaternion for another mathematician at work, I found a fairly obscure flaw, this is not mentioned in your article above. Since the complex part is a unit vector, the obvious differentiation does not work, because it effectivily wiggles the individual parts without considering that wiggling one part would change all the other parts to keep the sum 1. Mathematically speaking, the individuial terms are not independent. To get the right result you must differentiate the imaginary parts of quaternion divided by the length of the unit vector i.e. R + Im/sqrt(x^2 + y^2 + z^2), this breaks the dependency between the terms.

I’m not sure what you mean. The imaginary part of the quaternions involved is *not* a unit vector.

A unit quaternion is one such that conj(q)*q = R^2 + x^2 + y^2 + z^2 (in your notation) = 1. I don’t see why you would normalize just the imaginary part of a quaternion, or what it’s intended to accomplish.

I’m simply talking about the quaternion-valued function q(t) = q_omega^t * q_0 here, which has the derivative (by time!) given above. Furthermore, for unit quaternions (which represent rotations), we have |q(t)| = |q_omega^t| * |q_0| = |q_omega|^t * |q_0| = 1^t * 1 = 1; so if q_omega and q_0 are both unit quaternions, the same will hold for any quaternion returned by q(t), without ever enforcing that constraint explicitly.

“Wiggling the individual parts” doesn’t make sense in this context; both q_omega and q_0 are constants, and while I’m looking at a quaternion-valued function, it’s a function of one real variable, t, which is the one I’m differentiating by. I don’t get to “wiggle” my quaternions off the curve described by q(t), which as I’ve described above is entirely made up of unit quaternions.

Hello!

You are my last hope. As u mentioned

q1=qw*q0 and so on. So my question would be, what is qw?

So to make it clear: I got an initail quaternion, and the angular velocities at 50Hz or so (doesnt matter) How can I update my orientation quaternion based on the w.x, w.y, and w.z (the 3 angulary velocity)?

q_w in polar form is given in the article, this is assuming you have a normalized axis (n) and an angle in radians per time step (theta).

The angular velocity vector w (well, omega really…) is the axis vector times the angular speed in radians per second.

If w=0, q_w is just the identity quaternion. Otherwise, use theta=len(w)*secs_per_timestep, n=normalize(w).

I am a bit confused. If talking about linear velocity, then we can write:

dp/dt = v

where p – position vector, v – linear velocity vector.

Then we can write:

p(t + Δt) = p(t) + v*Δt

One would expect the same principle work for quaternions. So, if we have

dq/dt = 0.5*ω*q

then we can write:

q(t + Δt) = q(t) + dq/dt * Δt = q(t) + 0.5*ω*q(t)*Δt

Can this scheme be used to integrate position in quaternion over time?

First-order, yes, and that is indeed the most common use for this.

However, position is linear; rotation fundamentally isn’t. If the forces acting on a particle sum to 0, “p(t + Δt) = p(t) + v*Δt” is exact. The same is not true for rotation. Even at constant angular velocity, there are higher-order terms in the Taylor series

q(t + Δt) = q(t) + dq/dt * Δt + d^2q/dt^2 * Δt^2 + …

and they are (in general) nonzero. The exact expression for constant angular velocity is already given in the article as part of the derivation:

q(t + Δt) = q_omega^(Δt) * q(t)

For comments on how to modify this when not working with unitless quantities, see my earlier comment.

This is exactly the missing piece I needed. I’ve been trying to get from angular velocity to quaternions and keep getting lost in a sea of trigonometry. Thanks!

Hi,

The derivation was very helpful. This is when we have a function for a quaternion but what about differenciation when we have numbers instead of functions. Basically numerical differenciation of quaternions. I was wondering if you can suggest some ways to do it.

Thanks

You do it exactly the same way you would differentiate real or complex numbers: (q(t + h) – q(t)) / h.

thank you very much. it was very helpful :)

Hello!

By searching one cannot often find any practical formulae about quaternion space derivatives I’d like to point such formulae.

The best and simplest way to compute a quaternionic derivative is as follows. We represent a quaternion argument p = x+y⋅i+z⋅j+u⋅k (i,j,k are basic quaternion units; “⋅” is the quaternion multiplication) and a quaternion-differentiable (holomorphic) function of that argument ψ(p) = ψ_1(x,y,z,u)+ψ_2(x,y,z,u)⋅i+ψ_3(x,y,z,u)⋅j+ψ_4(x,y,z,u)⋅k in the Cayley–Dickson doubling form: p = a+b⋅j, where a´= x+y⋅i ; b = z+u⋅i and ψ(p)=ψ(a,b)=Φ_1(a,b)+Φ_(a,b)⋅j, where Φ_1(a,b)=ψ_1(a,b)+ψ_2(a,b)⋅i and Φ_2(a,b)=ψ_3(a,b)+ψ_4(a,b)⋅i. Each expression for ψ(p) is initially to be obtained from a complex function of the same kind by means of the direct replacement of a complex variable with a quaternion variable in the expression for the complex function. For example, ψ(p)=p^(-1). Just as a complex- holomorphic function satisfies Cauchy-Riemann’s equations in complex analysis, a quaternion- holomorphic function satisfies the following quaternionic generalization of Cauchy-Riemann’s equations:

(1) ∂Φ_1/∂a = ∂Φ_2*/∂b*, (2) ∂Φ_2/∂a = – ∂Φ_1*/∂b*

(3) ∂Φ_1/∂a = ∂Φ_2/∂b, (4) ∂Φ_2/∂a* = – ∂Φ_1/∂b*

after doing a = a* = x,

where the complex conjugation is denoted by * and the partial differentiation with respect to some variable s by ∂/∂s. For example, by ∂Φ_2*/∂b* is denoted the partial derivative of the complex conjugate of a function Φ_2 with respect to the complex conjugate of a variable b.

Firstly, we compute the partial derivatives of the functions Φ_1, Φ_2, Φ_1*, Φ_2* (with respect to the variables a, b, a*, b*); secondly, we put a = a* =x in the computed expressions of partial derivatives; and thirdly, we check whether equations (1) – (4) hold. One of the formulae to compute the first quaternionic derivative of the quaternion-holomorphic function is the following:

ψ(p)[1] = (∂Φ_1/∂a + ∂Φ_1/∂a*) + (∂Φ_2/∂a + ∂Φ_2/∂a*)⋅j .

Higher derivatives of quaternion-holomorphic functions can be computed analogically and they are holomorphic like the first derivative.

For details and examples I refer to http://vixra.org/abs/1609.0006

I really like this explanation, although there’s one thing I don’t fully understand. When calculating the derivative, how do you get (theta/2) * n to the left of the exponential? When I apply the chain rule it ends up to the right [if f = exp and g(x) = x * n * theta/2 then (f.g)'(t) = exp(t * n * theta/2) * n * theta/2], and because of non-commutativity of quaternions I don’t see how I can get to the desired result. Am I doing something wrong?

No, you’re right, that derivation incorrectly assumes commutativity as written and doesn’t actually work. :)

I’m about to fix this up in the post, but the short version is this: n commutes with powers n^k of n, and then you can use the definition of exp as a power series in n to show that n also commutes with exp(cn) with c=arbitrary real.

Hi,

Why you are not computing derivatives of n and θ as well? They do change in general rotation.

Because the problem statement assumes they’re constant, and I’m trying to cover the basic problems without introducing extraneous details!

This is still differential calculus, once you know the derivatives of the elementary functions you’re using, the rest is a matter of using the rules. If you need varying n or θ, you can use the chain and product rules yourself.