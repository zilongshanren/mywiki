---
title: In-game vertex painting with Unreal Engine (Wash Car Effect)
url: https://alfredbaudisch.com/experiment-logs/in-game-vertex-painting-with-unreal-engine-wash-car-effect/
published: '2022-07-30'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

As stated in the [experiment page](https://alfredbaudisch.com/experiments/gamedev/runtime-in-game-vertex-painting-to-simulate-dirt-removal/), the intention here is to add and remove dirt to meshes dynamically during runtime.

**Unfortunately, with this implementation, I did not manage to make it work with packaged projects**, due to `StaticMeshComponent->CachePaintedDataIfNecessary();`

which works only in the Editor and PIE.

I'm posting this experiment Log as it can be useful for those looking for runtime Vertex Painting with UE4 and UE5 (and as a future note to myself, in case I need it again).

In any case, I am not going to use this implementation and this approach, I decided to move forward with splat maps and realtime texture painting with Render Targets.

## Mesh and Material setup

- In any mesh, paint in any of the vertex color RGB channels (or in all of them for different effects) where you want to have dirt (or any kind of texture)
- In the material, you LERP between the different textures with the main texture of the mesh, where the amount/alpha are the vertex colors

## Painting in the editor

The vertices can be painted both in an external 3D package (Blender, etc) or inside Unreal.

Basic material to see vertex colors:

![](../../assets/4ba37f5f4c211730.png)


## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## Implementation

- Create a new Actor Component C++ class.
- In
`InitialiseInstancedOverrideVertexColorBuffer`

it's possible to count the amount of dirt and cleaned vertices, in order to track progress of the dirtiness/cleanness of the mesh, I left the`TODO`

placeholders there.

### C++ Header

```
// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "VertexPaintableComponent.generated.h"
/*
* Inspirations and sources:
* - http://www.orfeasel.com/vertex-painting-at-runtime/
* - https://github.com/alanedwardes/UE4VertexColorSpread
* - https://www.raywenderlich.com/6817-dynamic-mesh-painting-in-unreal-engine-4
* - http://unrealpaths.blogspot.com/2016/06/vertex-painting-on-meshes.html
* - https://www.youtube.com/watch?v=lkxZ1DMRQPg
*/
/**
Channel used for spreading vertex colors.
*/
UENUM()
namespace AVertexColorSpreadChannel
{
enum Channel
{
Red,
Green,
Blue,
Alpha,
};
}
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class GAME_API UVertexPaintableComponent : public UActorComponent
{
GENERATED_BODY()
public:
// Sets default values for this component's properties
UVertexPaintableComponent();
UFUNCTION(BlueprintCallable, Category=VertexPainting)
void PaintVertexAtLocation(FVector HitLocation, float PaintLerpProgress = 1.0f);
UPROPERTY(BlueprintReadWrite, EditAnywhere, Category=VertexPainting)
FColor TargetBaseColor = FColor::White;
protected:
// Called when the game starts
virtual void BeginPlay() override;
/**
Create LOD info entries, and ensure the override vertex color buffer exists.
*/
void InitialiseLODInfoAndBuffers();
/**
Create a new override vertex color buffer.
*/
void InitialiseInstancedOverrideVertexColorBuffer(FStaticMeshComponentLODInfo* InstanceMeshLODInfo,
FStaticMeshLODResources& LODModel);
/**
Get the intensity of the selected channel (see Channel)
*/
int32 GetNearestVertIndex(FVector Position, FStaticMeshLODResources& LODModel);
/**
Get the intensity of the selected channel (see Channel)
*/
uint8 GetIntensity(FColor Color);
/**
Set the intensity of the selected channel to the given value (see Channel)
*/
void SetIntensity(FColor *Color, uint8 Intensity);
UPROPERTY(BlueprintReadOnly)
UStaticMeshComponent* StaticMeshComponent;
};
```


### C++ Implementation

```
// Fill out your copyright notice in the Description page of Project Settings.
#include "VertexPaintableComponent.h"
#include "StaticMeshResources.h"
// Sets default values for this component's properties
UVertexPaintableComponent::UVertexPaintableComponent()
{
// Set this component to be initialized when the game starts, and to be ticked every frame. You can turn these features
// off to improve performance if you don't need them.
PrimaryComponentTick.bCanEverTick = true;
}
// Called when the game starts
void UVertexPaintableComponent::BeginPlay()
{
Super::BeginPlay();
StaticMeshComponent = GetOwner()->FindComponentByClass<UStaticMeshComponent>();
if(StaticMeshComponent != nullptr && IsValid(StaticMeshComponent))
{
InitialiseLODInfoAndBuffers();
}
}
void UVertexPaintableComponent::PaintVertexAtLocation(FVector HitLocation, float PaintLerpProgress)
{
// Init the buffers and LOD data
InitialiseLODInfoAndBuffers();
FStaticMeshComponentLODInfo* InstanceMeshLODInfo = &StaticMeshComponent->LODData[0];
FStaticMeshLODResources& LODModel = StaticMeshComponent->GetStaticMesh()->GetRenderData()->LODResources[0];
float BrushSize = 150.0f;
auto LocalToWorld = StaticMeshComponent->GetComponentToWorld().ToMatrixWithScale();
for (auto i = 0; i < LODModel.GetNumVertices(); i++)
{
auto LocalVertexPosition = LODModel.VertexBuffers.PositionVertexBuffer.VertexPosition(i);
auto WorldVertexPosition = LocalToWorld.TransformPosition(UE::Math::TVector4<double>(LocalVertexPosition.X, LocalVertexPosition.Y, LocalVertexPosition.Z, 1.0f));
auto Distance = FVector::DistSquared(WorldVertexPosition, HitLocation);
if (Distance <= BrushSize)
{
FLinearColor from = FLinearColor(InstanceMeshLODInfo->OverrideVertexColors->VertexColor(i));
FLinearColor to = FLinearColor(TargetBaseColor);
FColor ¤tColor = InstanceMeshLODInfo->OverrideVertexColors->VertexColor(i);
currentColor = FLinearColor::LerpUsingHSV(from, to, PaintLerpProgress).ToFColor(false);
}
}
// Notify the render thread about the buffer change
BeginUpdateResourceRHI(InstanceMeshLODInfo->OverrideVertexColors);
StaticMeshComponent->MarkRenderStateDirty();
#if WITH_EDITORONLY_DATA
StaticMeshComponent->CachePaintedDataIfNecessary();
#endif
}
int32 UVertexPaintableComponent::GetNearestVertIndex(FVector Position, FStaticMeshLODResources& LODModel)
{
auto ShortestDistance = 0;
auto NearestVertexIndex = -1;
auto LocalToWorld = StaticMeshComponent->GetComponentToWorld().ToMatrixWithScale();
for (auto i = 0; i < LODModel.GetNumVertices(); i++)
{
auto LocalVertexPosition = LODModel.VertexBuffers.PositionVertexBuffer.VertexPosition(i);
auto WorldVertexPosition = LocalToWorld.TransformPosition(UE::Math::TVector4<double>(LocalVertexPosition.X, LocalVertexPosition.Y, LocalVertexPosition.Z, 1.0f));
auto Distance = FVector::DistSquared(WorldVertexPosition, Position);
if (Distance < ShortestDistance || ShortestDistance < 0)
{
ShortestDistance = Distance;
NearestVertexIndex = i;
}
}
return NearestVertexIndex;
}
void UVertexPaintableComponent::InitialiseLODInfoAndBuffers()
{
if (StaticMeshComponent->LODData.Num() == 0)
{
StaticMeshComponent->SetLODDataCount(1, StaticMeshComponent->LODData.Num());
}
FStaticMeshLODResources& LODModel = StaticMeshComponent->GetStaticMesh()->GetRenderData()->LODResources[0];
FStaticMeshComponentLODInfo* InstanceMeshLODInfo = &StaticMeshComponent->LODData[0];
if (InstanceMeshLODInfo->OverrideVertexColors == nullptr)
{
InitialiseInstancedOverrideVertexColorBuffer(InstanceMeshLODInfo, LODModel);
}
}
void UVertexPaintableComponent::InitialiseInstancedOverrideVertexColorBuffer(FStaticMeshComponentLODInfo* InstanceMeshLODInfo, FStaticMeshLODResources& LODModel)
{
// Check that we don't already have an overridden vertex color buffer
check(InstanceMeshLODInfo->OverrideVertexColors == nullptr);
// Create a new buffer
InstanceMeshLODInfo->OverrideVertexColors = new FColorVertexBuffer;
if ((int32)LODModel.VertexBuffers.ColorVertexBuffer.GetNumVertices() >= LODModel.GetNumVertices())
{
// If the mesh already has vertex colours, initialise OverrideVertexColors from them
InstanceMeshLODInfo->OverrideVertexColors->InitFromColorArray(&LODModel.VertexBuffers.ColorVertexBuffer.VertexColor(0), LODModel.GetNumVertices());
}
else
{
// If it doesn't, set all overridden vert colours to black
InstanceMeshLODInfo->OverrideVertexColors->InitFromSingleColor(TargetBaseColor, LODModel.GetNumVertices());
}
for (auto i = 0; i < LODModel.GetNumVertices(); i++)
{
if(InstanceMeshLODInfo->OverrideVertexColors->VertexColor(i) != TargetBaseColor)
{
// TODO: add vertex idx to the dirt list
// TODO: save amount of dirt vertexes, to keep track of % cleaned/dirt
}
}
BeginInitResource(InstanceMeshLODInfo->OverrideVertexColors);
}
```


### Add Component

Add the newly created `VertexPaintableComponent`

to any mesh supposed to be paintable during runtime.

### Performing the Vertex Painting Action

Perform a line trace with the character and then call `Paint Vertex at Location`

from the Hit's `VertexPaintableComponent`

component (if found).

Copy the Blueprints from here: [https://blueprintue.com/blueprint/fky3jco9/](https://blueprintue.com/blueprint/fky3jco9/)