# pyDATR
A simple reimplementation of the DATR language in Python 3

## 📌 Introduction
`pyDATR` is a minimalistic implementation of the [DATR](https://en.wikipedia.org/wiki/DATR) network notation language, originally developed and introduced by Roger Evans, Gerald Gazdar and Bill Keller. It is based on the standard specification [DATR RFC 2.0](https://web.archive.org/web/20110719101843/http://www.spectrum.uni-bielefeld.de/DATR/datr_rfc_2.0.ps) and inspired by [ZDATR](https://web.archive.org/web/20110719101756/http://www.spectrum.uni-bielefeld.de/DATR/index.html) and [pyDATR](https://pydatr.sourceforge.net/), while simplifying the code and expanding the scope of allowed symbols to modern standards.

`pyDATR` was mainly developed as a personal project for my thesis and has therefore not been tested thoroughly. However, it is fully functional except for a few details discussed in the **Important Remarks** section. Depending on personal demand, a more detailed documentation and sturdier implementation could follow in the future.

## 📄 Features
`pyDATR` closely follows the syntax of the original DATR specification, hence there will be no full tutorial in this section. Some of the features include:

* A DATR theory consists of ***nodes***, which further consist of ***sentences***. A theory can be queried with a node/path expression, which, if resolvable, returns only atom descriptors.
* Sentences are specified by a **path** (on the LHS) and one or more **descriptors** (on the RHS). A sentence can be either *extensional* or *definitional*. *Extensional* sentences contain only atom descriptors, while *definitional* sentences can include inheritance descriptors.
* Inheritance descriptors specify either a *path*, a *node*, or a *node/path pair*. In either case, the value of the descriptor is inherited from the specified *path*, *node*, or *node/path pair*, where the query is continued with the remaining, unresolved path.
* Inheritance can be *local* or *global*. Local inheritance starts from the node the query is currently at, while global inheritance starts the inheritance in the global context (by default the node where the query started).
* Paths are resolved from left to right, and DATR features **Definition by default**. This means that a path in a sentence matches any (queried) path that is at least as specific as itself (but also any rightward extension of it).

For a more detailed introduction to DATR, please read the [Paper by Evans and Gazdar](https://aclanthology.org/J96-2002/).

## ❔ Usage
TBA
This section covers the usage of pyDATR on a command line level.

## ❗ Important Remarks
TBA
This section covers important details and remarks about the pyDATR implementation.
