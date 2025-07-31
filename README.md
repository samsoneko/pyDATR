# pyDATR
A simple reimplementation of the DATR language in Python 3.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203.12.6-1f425f.svg?logo=python)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## 📌 Introduction
`pyDATR` is a minimalistic implementation of the [DATR](https://en.wikipedia.org/wiki/DATR) network notation language, originally developed and introduced by Roger Evans, Gerald Gazdar and Bill Keller. It is based on the standard specification [DATR RFC 2.0](https://web.archive.org/web/20110719101843/http://www.spectrum.uni-bielefeld.de/DATR/datr_rfc_2.0.ps) and inspired by [ZDATR v1.1](https://web.archive.org/web/20110719101756/http://www.spectrum.uni-bielefeld.de/DATR/index.html) and [pyDATR 0.2](https://pydatr.sourceforge.net/), while simplifying the code and expanding the scope of allowed symbols to modern standards.

`pyDATR` was mainly developed as a personal project for my thesis and has therefore not been tested thoroughly. However, it is fully functional except for a few details discussed in the **Important Remarks** section. Depending on personal demand, a more detailed documentation and sturdier implementation could follow in the future.

## 📄 Features
`pyDATR` closely follows the syntax of the original DATR specification, hence there will be no full tutorial in this section. Some of the features include:

* A DATR theory consists of ***nodes***, which further consist of ***sentences***. A theory can be queried with a node/path expression, which, if resolvable, returns only atom descriptors.
* Sentences are specified by a **path** (on the LHS) and one or more **descriptors** (on the RHS). A sentence can be either *extensional* or *definitional*. *Extensional* sentences contain only atom descriptors, while *definitional* sentences can include inheritance descriptors.
* Inheritance descriptors specify either a *path*, a *node*, or a *node/path pair*. In either case, the value of the descriptor is inherited from the specified *path*, *node*, or *node/path pair*, where the query is continued with the remaining, unresolved path.
* Inheritance can be *local* or *global*. Local inheritance starts from the node the query is currently at, while global inheritance starts the inheritance in the global context (by default the node where the query started).
* Paths are resolved from left to right, and DATR features **Definition by default**. This means that a path in a sentence matches any (queried) path that is at least as specific as itself (but also any rightward extension of it).

For a more detailed introduction to DATR, please read the [Paper by Evans and Gazdar](https://aclanthology.org/J96-2002/).

---

Compiling and querying a DATR theory using pyDATR happens in 4 steps:
### 1. Tokenizing the theory
In this step, the entire input file is tokenzied using `ply.lex`. While the naming rules for nodes, atoms and variables remain (Nodes start with a capital letter, paths with a lowercase letter and variables with a $) the allowed scope of symbols has been raised to any symbols not reserved for DATR syntax. If the syntax of the input file does not match the DATR specification, a respective error is thrown and the tokenizer terminates.
### 2. Parsing the theory
In this step, the tokenized input is further parsed using `ply.yacc`. The grammar used for this is modeled after the grammar rules used by [ZDATR v1.1](https://web.archive.org/web/20110719101756/http://www.spectrum.uni-bielefeld.de/DATR/index.html), while being adjusted to better match the full DATR specification. If the syntax of the input file does not match the DATR specification, a respective error is thrown and the parser terminates. 
### 3. Converting the theory to a python object representation
In this step, the parsed input is converted into python objects. The resulting structure is as follows:
1. A theory "parent" object holds all necessary information for the entire DATR theory.
2. The theory object contains a list of child node objects as well as a list of variable objects.
3. Each node object contains a list of sentence objects.
4. Each variable object contains a list of atoms or other variable references.
5. Each sentence object contains a list for the LHS and a list for the RHS. The LHS may consist of atoms or variable references, while the RHS may consist of atoms, variable references or pointers (indicating inheritance).
6. Atoms, both in paths as well as in the RHS, are represented by simple strings.

In this step, a few checks are executed to test whether the parsed theory contains any logical errors. For example, duplicate node and variable names result in an error and a termination of the program.
### 4. (Querying the theory)
The theory can be queried using the same syntax as the original DATR. A query consists of a node and a path specification, for example `Node1:<path1 path2>`. The query is successful if it is resolvable to only atoms, in which case the list of atoms is returned. If the query is not resolvable to atoms or a different problem occurs (for example a variable or path not resolvable), a respective error is thrown and the program terminates. This is also the case if the query does not match the syntactic rules of DATR.

## ⚙️ Structure
All files relevant for the project are listed below:

* `src/`
    * `error.py` -> Contains custom errors for the pyDATR implementation.
    * `lexer.py` -> Implements the lexical analyzer for pyDATR (Tokenization).
    * `parser.py` -> Implements the parser for pyDATR (Parsing / Compiling).
    * `theory.py` -> Provides all code for loading and representing a DATR theory as objects, as well as all code for handling queries.
* `datr_cli.py` -> The CLI for compiling and interacting with a theory.

## ❔ Usage
While every step of `pyDATR` can be called separately, a straightforward way to interact with the program is the `datr_cli.py` file.
When executing it on the command line, the first argument specifies the input file.
For example, executing `python datr_cli.py example.dtr` would compile the theory from `example.dtr`.
Afterwards, a query like `Node1:<path1 path2>` can be given to the program via the console, which returns the resolved atoms.

## ❗ Important Remarks
This section covers important details and remarks about the pyDATR implementation. Some of them regard the limits of the current implementation, others regard possible deviations from the original DATR specification.

### Logic errors not recognized by pyDATR
Currently, a few checks are executed to make sure that a compiled theory is logically sound. For example, duplicate node and variable names result in an error and a termination of the program. However, not all possible logical oversights are covered. There is currently no check for duplicate sentences, hence identical paths in two or more different sentences. This as well as similar mistakes could lead to a crash of the program or an incorrect response. While further improvements to the code are planned, not every logical error is detectable without serious expense, which conflicts with the minimal approach of pyDATR. For instance, a group of nodes inheriting from each other in a circle could lead to problems, but would be hard to detect. For this reason, some responsibility has to be given to the user: If a theory was thoroughly checked before and is logically sound, it can be compiled and queried without problems.

### Infinite loops / recursion
As mentioned in the previous section, nodes inheriting from each other in circles can cause problems. More specific: infinite loops. This is hard to filter out during compilation, and while immediately obvious during querying, there is currently no check to prevent it. If the program is stuck in an infinite loop, it terminates itself shortly after due to pythons recursion limit. While this can't be described as properly handling the error, it is currently sufficient to be left as is, expecially as infinite recursion will not be present in logically sound theories.

### Limits to variable definitions.
While pyDATR support variables and even variables "inheriting" from other variables, it currently does not support excluding values like the original DATR does.
This means that declarations like `#vars $var1 : atom1 atom2.` and even `#vars $var1 : atom1 $var2.` are fine (as long as `$var2` is also declared), but declarations such as `#vars $var1 : $var2 - atom1.` (excluding `atom1` using `-`) are not allowed. While this may be added in the future, there are no concrete plans to do so. The original paper also leaves some ambiguity when it comes to this feature: The symbol `-` is used to indicate exclusion, but it is not defined as a reserved symbol. This is inconsistent with the syntactic definition of DATR, which "distinguishes four classes of lexical token: nodes, atoms, variables, and reserved symbols." [Evans and Gazdar, 1996, Section 3.1.1](https://aclanthology.org/J96-2002/), as `-` is neither of the four.
