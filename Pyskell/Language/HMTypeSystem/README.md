# Hindley Milner Type System
> Python Implementation
>
> THIS FILE ON GITHUB DO NOT SUPPORT MATH-FORMULA DISPLAY, PLEASE USE MD-EDITOR ON PC.

So what is **Hindley Milner Type System**:

> It is an algorithm for inferring value types based on use.
>
> It literally formalizes the intuition that a type can be deduced by the functionality it supports.

By **formalize**, what can we achieve:

> $$\frac{A, A\rightarrow B}{B}$$

which means we can try to use some rules and algorithms to get some conclusions we want, without manually get the conclusion.

## Types and Expressions

### Variable

> Variables are valid expressions.

### Lambda (Abstraction)

If $e$ is any expression, $x$ is any variable, then $\lambda x.e$ is a valid expression.

> Example:
>
> $e = 2^x + x$ as an expression, and $x$ is a variable, then $\lambda x.e$ is a anonymous function.

### Application

If $f$ and $e$ are valid expressions, then $f(e)$ is also a valid expression.

### Let

If $x$ is a variable, $e_0$ and $e_1$ are valid expressions, then we can do replacement by notation $[e_0/x]e_1$ for replacing $x$ in $e_1$ with $e_0$.

## Some Statements about Types

Let $e$ be any expression, so $e$ is a variable that stands for any expression.

Then if $e$ is of any type, we can express "$e$ of type $t$" by notation $e: t$.

So $t$ is a variable stands for any type.

So we can introduce the **TypeVariable** from $t$.

<div style="page-break-after: always;"></div>

## Mono-type and Poly-type

### Mono-types

Monotypes always designate a particular type, in the sense that a monotype is equal only to itself and different from all others.

> Example: `Int == Int` and `Int != List`

We use $\tau$ for the notation of monotype.

### Poly-types

Polytypes (or type schemes) are types containing variables bound by one or more for-all quantifiers.

> Example: $id : \forall \alpha.\alpha \rightarrow \alpha$

## Formalizing Statements

- $\Gamma$: stands for a collection of statements we already know, or perhaps, the statements we're assuming.

- $\vdash$: denotes that something can be inferred.

  > Example: $\Gamma \vdash x:t$ says if we take all statements from $\Gamma$, we can infer that $x$ is of type $t$.

- $\in$: donates the membership in the statement collection.

## Algorithm

Let/Application/Abstraction/Variable's formalizing statements are easy, skip.

### Instantiation

$$\begin{equation}\frac{\vdash e : \sigma'\space\sigma' \sqsubseteq \sigma}{\Gamma\vdash e:\sigma}\end{equation}$$

> Example: $[Int]\rightarrow Int \sqsubseteq \forall t . [t]\rightarrow t \sqsubseteq [t] \rightarrow t$

### Generalization

$$\frac{\Gamma\vdash e:\sigma\space\alpha\notin free(\Gamma)}{\Gamma \vdash e:\forall \alpha.\sigma}$$

If $\alpha​$ is not free in $\Gamma​$, in another word $\alpha​$ is restricted inside $\Gamma​$, then $e :\forall \alpha . \sigma​$ can be inferred from the provided conditions.