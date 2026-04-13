---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_contact_solver/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[List of all members.](/)

Public Member Functions
|
| **b2ContactSolver** ([b2ContactSolverDef](../../../../../api-ref/1.0/Box2D/html/structb2_contact_solver_def/) *def) |
void | **InitializeVelocityConstraints** () |
void | **WarmStart** () |
void | **SolveVelocityConstraints** () |
void | **StoreImpulses** () |
bool | **SolvePositionConstraints** () |
bool | **SolveTOIPositionConstraints** (int32 toiIndexA, int32 toiIndexB) |
Public Attributes
|
[b2TimeStep](../../../../../api-ref/1.0/Box2D/html/structb2_time_step/) | **m_step** |
[b2Position](../../../../../api-ref/1.0/Box2D/html/structb2_position/) * | **m_positions** |
[b2Velocity](../../../../../api-ref/1.0/Box2D/html/structb2_velocity/) * | **m_velocities** |
[b2StackAllocator](../../../../../api-ref/1.0/Box2D/html/classb2_stack_allocator/) * | **m_allocator** |
b2ContactPositionConstraint * | **m_positionConstraints** |
[b2ContactVelocityConstraint](../../../../../api-ref/1.0/Box2D/html/structb2_contact_velocity_constraint/) * | **m_velocityConstraints** |
[b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) ** | **m_contacts** |
int | **m_count** |


The documentation for this class was generated from the following file: