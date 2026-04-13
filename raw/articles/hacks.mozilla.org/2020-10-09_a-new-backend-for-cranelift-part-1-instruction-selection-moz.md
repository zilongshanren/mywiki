---
title: 'A New Backend for Cranelift, Part 1: Instruction Selection – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2020/10/a-new-backend-for-cranelift-part-1-instruction-selection/
author: Chris Fallin
published: '2020-10-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This post will describe my recent work on Cranelift as part of my day job at Mozilla. In this post, I will set some context and describe the instruction selection problem. In particular, I’ll talk about a revamp to the instruction selector and backend framework in general that we’ve been working on for the last nine months or so. This work has been co-developed with my brilliant colleagues Julian Seward and Benjamin Bouvier, with significant early input from Dan Gohman as well, and help from all of the wonderful Cranelift hackers.*

## Background: Cranelift

So what is Cranelift?

The project is a compiler framework written in [Rust](https://www.rust-lang.org/) that is designed especially (but not exclusively) for [just-in-time compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation). It’s a general-purpose compiler: its most popular use-case is to compile [WebAssembly](https://www.webassembly.org/), though several other frontends exist, for example, [cg_clif](https://github.com/bjorn3/rustc_codegen_cranelift), which adapts the Rust compiler itself to use Cranelift. Folks at Mozilla and several other places have been developing the compiler for a few years now. It is the default compiler backend for [wasmtime](https://github.com/bytecodealliance/wasmtime), a runtime for WebAssembly outside the browser, and is used in production in several other places as well.

We recently flipped the switch to turn on Cranelift-based WebAssembly support in nightly Firefox on [ARM64 (AArch64)](https://en.wikipedia.org/wiki/AArch64) machines, including most smartphones, and if all goes well, it will eventually go out in a stable Firefox release. Cranelift is developed under the umbrella of the [Bytecode Alliance](https://bytecodealliance.org/).

In the past nine months, we have built a new framework in Cranelift for the “machine backends”, or the parts of the compiler that support particular CPU instruction sets. We also added a new backend for AArch64, mentioned above, and filled out features as needed until Cranelift was ready for production use in Firefox. This blog post sets some context and describes the design process that went into the backend-framework revamp.

## Old Backend Design: Instruction Legalizations

To understand the work that we’ve done recently on Cranelift, we’ll need to zoom into the `cranelift_codegen`

crate above and talk about how it *used to* work. What is this “CLIF” input, and how does the compiler translate it to machine code that the CPU can execute?

Cranelift makes use of [CLIF](https://github.com/bytecodealliance/wasmtime/blob/main/cranelift/docs/ir.md), or the Cranelift IR (Intermediate Representation) Format, to represent the code that it is compiling. Every compiler that performs program optimizations uses some form of an [Intermediate Representation (IR)](https://en.wikipedia.org/wiki/Intermediate_representation): you can think of this like a virtual instruction set that can represent all the operations a program is allowed to do. The IR is typically simpler than real instruction sets, designed to use a small set of well-defined instructions so that the compiler can easily reason about what a program means.

The IR is also independent of the CPU architecture that the compiler eventually targets; this lets much of the compiler (such as the part that generates IR from the input programming language, and the parts that optimize the IR) be reused whenever the compiler is adapted to target a new CPU architecture. CLIF is in [Static Single Assignment (SSA)](https://en.wikipedia.org/wiki/Static_single_assignment_form) form, and uses a conventional [control-flow graph](https://en.wikipedia.org/wiki/Control-flow_graph) with basic blocks (though it previously allowed extended basic blocks, these have been phased out). Unlike many SSA IRs, it represents φ-nodes with block parameters rather than explicit φ-instructions.

Within `cranelift_codegen`

, before we revamped the backend design, the program remained in CLIF throughout compilation and up until the compiler emitted the final machine code. This might seem to contradict what we just said: how can the IR be machine-independent, but also be the final form from which we emit machine code?

The answer is that the old backends were built around the concept of “legalization” and “encodings”. At a high level, the idea is that every *Cranelift* instruction either corresponds to one *machine* instruction, or can be replaced by a sequence of other *Cranelift* instructions. Given such a mapping, we can refine the CLIF in steps, starting from arbitrary machine-independent instructions from earlier compiler stages, performing edits until the CLIF corresponds 1-to-1 with machine code. Let’s visualize this process:

A very simple example of a CLIF instruction that has a direct “encoding” to a machine instruction is `iadd`

, which just adds two integers. On essentially any modern architecture, this should map to a simple ALU instruction that adds two registers.

On the other hand, many CLIF instructions do not map cleanly. Some arithmetic instructions fall into this category: for example, there is a CLIF instruction to count the number of set bits in an integer’s binary representation (`popcount`

); not every CPU has a single instruction for this, so it might be expanded into a longer series of bit manipulations.

There are operations that are defined at a higher semantic level, as well, that will necessarily be lowered with expansions: for example, accesses to Wasm memories are lowered into operations that fetch the linear memory base and its size, bounds-check the Wasm address against the limit, compute the real address for the Wasm address, and perform the access.

To compile a function, then, we iterate over the CLIF and find instructions with no direct machine encodings; for each, we simply expand into the legalized sequence, and then recursively consider the instructions in that sequence. We loop until all instructions have machine encodings. At that point, we can emit the bytes corresponding to each instruction’s encoding.

## Growing Pains, and a New Backend Framework?

There are a number of advantages to the legacy Cranelift backend design, which performs expansion-based legalization with a single IR throughout. As one might expect, though, there are also a number of drawbacks. Let’s discuss a few of each.

### Single IR and Legalization: Pros

- By operating on a single IR all the way to machine-code emission, the same optimizations can be applied at multiple stages.
- If
*most*of the Cranelift instructions become one machine instruction, and few legalizations are necessary, then this scheme can be very fast: it becomes simply a single traversal to fill in “encodings”, which were represented by small indices into a table.

### Single IR and Legalization: Cons

- Expansion-based legalization may not always result in optimal code. There are sometimes
*single*machine instructions that implement the behavior of*multiple*CLIF instructions, i.e. a many-to-one mapping. In order to generate efficient code, we want to be able to make use of these instructions; expansion-based legalization cannot. - Expansion-based legalization rules must obey a partial order among instructions: if A expands into a sequence including B, then B cannot later expand into A. This could become a difficulty for the machine-backend author to keep straight.
- There are efficiency concerns with expansion-based legalization. At an algorithmic level, we prefer to avoid fixpoint loops (in this case, “continue expanding until no more expansions exist”) whenever possible. The runtime is bounded, but the bound is somewhat difficult to reason about, because it depends on the maximum depth of chained expansions.The data structures that enable in-place editing are also much slower than we would like. Typically, compilers store IR instructions in linked lists to allow for in-place editing. While this is asymptotically as fast as an array-based solution (we never need to perform random access), it is much less cache-friendly or
[ILP](https://en.wikipedia.org/wiki/Instruction-level_parallelism)-friendly on modern CPUs. We’d prefer instead to store arrays of instructions and perform single passes over them whenever possible. - Our particular implementation of the legalization scheme grew to be somewhat unwieldy over time (see, e.g., the GitHub issue
[#1141: Kill Recipes With Fire](https://github.com/bytecodealliance/wasmtime/issues/1141)). Adding a new instruction required learning about “recipes”, “encodings”, and “legalizations” as well as mere instructions and opcodes; a more conventional code-lowering approach would avoid much of this complexity. - A single-level IR has a fundamental tension: for analyses and optimizations to work well, an IR should have only one way to represent any particular operation. On the other hand, a machine-level representation should represent all of the relevant details of the target ISA. A single IR simply cannot serve both ends of this spectrum properly, and difficulties arose as CLIF strayed from either end.

For all of these reasons, as part of our revamp of Cranelift and a prerequisite to our new AArch64 backend, we built a new framework for machine backends and instruction selection. The framework allows machine backends to define their own instructions, separately from CLIF; rather than legalizing with expansions and running until a fixpoint, we define a single lowering pass; and everything is built around more efficient data-structures, carefully optimizing passes over data and avoiding linked lists entirely. We now describe this new design!

## A New IR: VCode

The main idea of the new Cranelift backend is to *add a machine-specific IR*, with several properties that are chosen specifically to represent machine-code well. We call this `VCode`

, which comes from “virtual-register code”, and the VCode contains `MachInst`

s, or machine instructions. The key design choices we made are:

- VCode is a linear sequence of instructions. There is control-flow information that allows traversal over basic blocks, but the data structures are not designed to easily allow inserting or removing instructions or reordering code. Instead, we lower into VCode with a single pass, generating instructions in their final (or near-final) order.
- VCode is
*not*SSA-based; instead, its instructions operate on registers. While lowering, we allocate virtual registers. After the VCode is generated, the register allocator computes appropriate register assignments and edits the instructions in-place, replacing virtual registers with real registers. (Both are packed into a 32-bit representation space, using the high bit to distinguish virtual from real.) Eschewing SSA at this level allows us to avoid the overhead of maintaining its invariants, and maps more closely to the real machine.

VCode instructions are simply stored in an array, and the basic blocks are recorded separately as ranges of array (instruction) indices. We designed this data structure for fast iteration, but not for editing.

Each instruction is mostly opaque from the point of view of the VCode container, with a few exceptions: every instruction exposes its (i) register references, and (ii) basic-block targets, if a branch. Register references are categorized into the usual “uses” and “defs” (reads and writes).

Note as well that the instructions can refer to *either* virtual registers (here denoted `v0`

..`vN`

) *or* real machine registers (here denoted `r0`

..`rN`

). This design choice allows the machine backend to make use of specific registers where required by particular instructions, or by the ABI (parameter-passing conventions).

Aside from registers and branch targets, an instruction contained in the VCode may contain whatever other information is necessary to emit machine code. Each machine backend defines its own type to store this information. For example, on AArch64, here are several of the instruction formats, simplified:

```
enum Inst {
/// An ALU operation with two register sources and a register destination.
AluRRR {
alu_op: ALUOp,
rd: Writable,
rn: Reg,
rm: Reg,
},
/// An ALU operation with a register source and an immediate-12 source, and a register
/// destination.
AluRRImm12 {
alu_op: ALUOp,
rd: Writable,
rn: Reg,
imm12: Imm12,
},
/// A two-way conditional branch. Contains two targets; at emission time, a conditional
/// branch instruction followed by an unconditional branch instruction is emitted, but
/// the emission buffer will usually collapse this to just one branch.
CondBr {
taken: BranchTarget,
not_taken: BranchTarget,
kind: CondBrKind,
},
// ...
```


These enum arms could be considered similar to “encodings” in the old backend, except that they are defined in a much more straightforward way, using type-safe and easy-to-use Rust data structures.

## Lowering from CLIF to VCode

We’ve now come to the most interesting design question: how do we lower from CLIF instructions, which are machine-independent, into VCode with the appropriate type of CPU instructions? In other words, what have we replaced the expansion-based legalization and encoding scheme with?

We perform a *single pass* over the CLIF instructions, and at each instruction, we invoke a function provided by the machine backend to lower the CLIF instruction into VCode instruction(s). The backend is given a “[lowering context](https://github.com/bytecodealliance/wasmtime/blob/cb306fd514f34e7dd818bb17658b93fba98e2567/cranelift/codegen/src/machinst/lower.rs#L58)” by which it can examine the instruction and the values that flow into it, performing “tree matching” as desired (see below). This naturally allows 1-to-1, 1-to-many, or many-to-1 translations. We incorporate a reference-counting scheme into this pass to ensure that instructions are only generated if their values are actually used; this is necessary to eliminate dead code when many-to-1 matches occur.

### Tree Matching

Recall that the old design allowed for 1-to-1 and 1-to-many mappings from CLIF instructions to machine instructions, but not many-to-1. This is particularly problematic when it comes to pattern-matching for things like addressing modes, where we want to recognize particular combinations of operations and choose a specific instruction that covers all of those operations at once.

Let’s start by defining a “tree” that is rooted at a particular CLIF instruction. For each argument to the instruction, we can look “up” the program to find its producer (def). Because CLIF is in SSA form, either the instruction argument is an ordinary value, which must have exactly one definition, or it is a block parameter (φ-node in conventional SSA formulations) that represents multiple possible definitions. We will say that if we reach a block parameter (φ-node), we simply end at a tree leaf – it is perfectly alright to pattern-match on a tree that is a *subset* of the true dataflow (we might get suboptimal code, but it will still be correct). For example, given the CLIF code:

```
block0(v0: i64, v1: i64):
brnz v0, block1(v0)
jump block1(v1)
block1(v2: i64):
v3 = iconst.i64 64
v4 = iadd.i64 v2, v3
v5 = iadd.i64 v4, v0
v6 = load.i64 v5
return v6
```


Let’s consider the load instruction: `v6 = load.i64 v5`

. A simple code generator could map this 1-to-1 to the CPU’s ordinary load instruction, using the register holding `v5`

as an address. This would certainly be correct. However, we might be able to do better: for example, on AArch64, the available addressing modes include a two-register sum `ldr x0, [x1, x2]`

or a register with a constant offset `ldr x0, [x1, #64]`

.

The “operand tree” might be drawn like this:

We stop at `v2`

and `v0`

because they are block parameters; we don’t know with certainty which instruction will produce these values. We can replace `v3`

with the constant `64`

. Given this view, the lowering process for the load instruction can fairly easily choose an addressing mode. (On AArch64, the code to make this choice is [here](https://github.com/bytecodealliance/wasmtime/blob/cb306fd514f34e7dd818bb17658b93fba98e2567/cranelift/codegen/src/isa/aarch64/lower.rs#L653); in this case it would choose the register + constant immediate form, generating a separate add instruction for `v0 + v2`

.)

Note that we do not actually explicitly construct an operand tree during lowering. Instead, the machine backend can query each instruction input, and the lowering framework will provide [a struct](https://github.com/bytecodealliance/wasmtime/blob/cb306fd514f34e7dd818bb17658b93fba98e2567/cranelift/codegen/src/machinst/lower.rs#L176) giving the producing instruction if known, the constant value if known, and the register that will hold the value if needed.

The backend may traverse up the tree (via the “producing instruction”) as many times as needed. If it cannot combine the operation of an instruction further up the tree into the root instruction, it can simply use the value in the register at that point instead; it is always safe (though possibly suboptimal) to generate machine instructions for only the root instruction.

### Lowering an Instruction

Given this matching strategy, then, how do we actually do the translation? Basically, the backend provides a function that is called once per CLIF instruction, at the “root” of the operand tree, and can produce as many machine instructions as it likes. This function is essentially just a large `match`

statement over the opcode of the root CLIF instruction, with the match-arms looking deeper as needed.

Here is a simplified version of the match-arm for an integer add operation lowered to AArch64 (the full version is [here](https://github.com/bytecodealliance/wasmtime/blob/cb306fd514f34e7dd818bb17658b93fba98e2567/cranelift/codegen/src/isa/aarch64/lower_inst.rs#L75)):

```
<span class="k">match</span> <span class="n">op</span> <span class="p">{</span>
<span class="c"> // ...</span>
<span class="nn"> Opcode</span><span class="p">::</span><span class="n">Iadd</span> <span class="k">=></span> <span class="p">{</span>
<span class="k"> let</span> <span class="n">rd</span> <span class="o">=</span> <span class="nf">get_output_reg</span><span class="p">(</span><span class="n">ctx</span><span class="p">,</span> <span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">]);</span>
<span class="k"> let</span> <span class="n">rn</span> <span class="o">=</span> <span class="nf">put_input_in_reg</span><span class="p">(</span><span class="n">ctx</span><span class="p">,</span> <span class="n">inputs</span><span class="p">[</span><span class="mi">0</span><span class="p">]);</span>
<span class="k"> let</span> <span class="n">rm</span> <span class="o">=</span> <span class="nf">put_input_in_rse_imm12</span><span class="p">(</span><span class="n">ctx</span><span class="p">,</span> <span class="n">inputs</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
<span class="k"> let</span> <span class="n">alu_op</span> <span class="o">=</span> <span class="nf">choose_32_64</span><span class="p">(</span><span class="n">ty</span><span class="p">,</span> <span class="nn">ALUOp</span><span class="p">::</span><span class="n">Add32</span><span class="p">,</span> <span class="nn">ALUOp</span><span class="p">::</span><span class="n">Add64</span><span class="p">);</span>
<span class="n"> ctx</span><span class="nf">.emit</span><span class="p">(</span><span class="nf">alu_inst_imm12</span><span class="p">(</span><span class="n">alu_op</span><span class="p">,</span> <span class="n">rd</span><span class="p">,</span> <span class="n">rn</span><span class="p">,</span> <span class="n">rm</span><span class="p">));</span>
<span class="p"> }</span>
<span class="c"> // ...</span>
<span class="p">}</span>
```


There is some magic that happens in several helper functions here. `put_input_in_reg()`

invokes the proper methods on the `ctx`

to look up the register that holds an input value. `put_input_in_rse_imm12()`

is more interesting: it returns a [ ResultRSEImm12](https://github.com/bytecodealliance/wasmtime/blob/cb306fd514f34e7dd818bb17658b93fba98e2567/cranelift/codegen/src/isa/aarch64/lower.rs#L63), which is a “register, shifted register, extended register, or 12-bit immediate”. This set of choices captures all of the options we have for the second argument of an add instruction on AArch64.

The helper looks at the node in the operand tree and attempts to match either a shift or zero/sign-extend operator, which can be incorporated directly into the add. It also checks whether the operand is a constant and if so, could fit into a 12-bit immediate field. If not, it falls back to simply using the register input. `alu_inst_imm12()`

then breaks down this enum and chooses the appropriate `Inst`

arm (`AluRRR`

, `AluRRRShift`

, `AluRRRExtend`

, or `AluRRImm12`

respectively).

And that’s it! No need for legalization and repeated code editing to match several operations and produce a machine instruction. We have found this way of writing lowering logic to be quite straightforward and easy to understand.

### Backward Pass with Use-Counts

Now that we can lower a single instruction, how do we lower a function body with many instructions? This is not quite as straightforward as looping over the instructions and invoking the match-over-opcode function described above (though that would actually work). In particular, we want to handle the many-to-1 case more efficiently. Consider what happens when the add-instruction logic above is able to incorporate, say, a left-shift operator into the add instruction.

The `add`

machine instruction would then use the *shift*’s input register, and completely ignore the shift’s output. If the shift operator has no other uses, we should avoid doing the computation entirely; otherwise, there was no point in merging the operation into the add.

We implement a sort of reference counting to solve this problem. In particular, we track whether any given SSA value is actually used, and we only generate code for a CLIF instruction if any of its results are used (or if it has a side-effect that must occur). This is a form of [dead-code elimination](https://en.wikipedia.org/wiki/Dead_code_elimination) but integrated into the single lowering pass.

We must see uses before defs for this to work. Thus, we iterate over the function body “backward”. Specifically, we iterate in [postorder](https://en.wikipedia.org/wiki/Depth-first_search#Vertex_orderings); this way, all instructions are seen before instructions that [dominate](https://en.wikipedia.org/wiki/Dominator_(graph_theory)) them, so given SSA form, we see uses before defs.

### Examples

Let’s see how this works in real life! Consider the following CLIF code:

```
function %f25(i32, i32) -> i32 {
block0(v0: i32, v1: i32):
v2 = iconst.i32 21
v3 = ishl.i32 v0, v2
v4 = isub.i32 v1, v3
return v4
}
```


We expect that the left-shift (`ishl`

) operation should be merged into the subtract operation on AArch64, using the reg-reg-shift form of ALU instruction, and indeed this happens (here I am showing the debug-dump format one can see with `RUST_LOG=debug`

when running `clif-util compile -d --target aarch64`

):

```
VCode {
Entry block: 0
Block 0:
(original IR block: block0)
(instruction range: 0 .. 6)
Inst 0: mov %v0J, x0
Inst 1: mov %v1J, x1
Inst 2: sub %v4Jw, %v1Jw, %v0Jw, LSL 21
Inst 3: mov %v5J, %v4J
Inst 4: mov x0, %v5J
Inst 5: ret
}
```


This then passes through the register allocator, has a prologue and epilogue attached (we cannot generate these until we know which registers are clobbered), has redundant moves elided, and becomes:

```
stp fp, lr, [sp, #-16]!
mov fp, sp
sub w0, w1, w0, LSL 21
mov sp, fp
ldp fp, lr, [sp], #16
ret
```


which is a perfectly valid function, correct and callable from C, on AArch64! (We could do better if we knew that this were a leaf function and avoided the stack-frame setup and teardown! Alas, many optimization opportunities remain.)

We’ve only scratched the surface of Cranelift’s design in this blog-post. Nevertheless, I hope this post has given a sense of the exciting work being done in compilers today!

*This post is an abridged version; see the full version for more more technical details.*

*Thanks to Julian Seward and Benjamin Bouvier for reviewing this post and suggesting several additions and corrections.*