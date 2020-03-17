# minimalism
Implementation of A Formalization of Minimalist Syntax (Collins &amp; Stabler, 2016)

## 2 - Preliminary Definitions
### Definition 1 - Universal Grammar
structures\definitions\class UniversalGrammar

### Definition 2 - Lexical Item
structures\syntactic_objects\class LexicalItem

### Definition 3 - Lexicon
structures\lexicon\class Lexicon

### Definition 4 - I-Language
structures\definitions\class ILanguage

### Definition 5 - Lexical Item Token
structures\syntactic_objects\class LexicalItemToken

### Definition 6 - Lexical Array
structures\definitions\class LexicalArray

### Definition 7 - Syntactic Object
structures\syntactic_objects\class SyntacticObject

### Definition 8 - Immediate Containment (SO)
structures\syntactic_objects\class SyntacticObject.immediately_contains

### Definition 9 - Containment (SO)
structures\syntactic_objects\class SyntacticObject.contains

## 3 - Workspaces, Select, Merge

### Definition 10a - Stage
structures\definitions\class Stage

### Definition 10b - Workspace of a Stage
structures\definitions\class Workspace

### Definition 11 - Root
structures\definitions\class Workspace.is_root

### Definition 12 - Select (Stage)
structures\definitions\class Stage.select_stage

### Definition 13 - Merge
structures\definitions\class Stage.merge_stage
structures\definitions\class Workspace.merge_workspace

### Definition 14 - Derivation
derivations\derivation\class Derivation(object)
(incomplete)

### Definition 15 - Derivable (SO from Lexicon)
structures\syntactic_objects\class SyntacticObject.is_derivable
(not implemented)

## 4 - Occurrences

### Definition 16 - Position/Path
structures\syntactic_objects\class SyntacticObject.paths

### Definition 17 - Occurrence
structures\syntactic_objects\class SyntacticObject.does_occur
structures\syntactic_objects\class SyntacticObject.occurrence
(not implemented)

### Definition 18 - Immediate Containment
structures\syntactic_objects\class SyntacticObject.immediately_contains

### Definition 19 - Sisterhood
structures\syntactic_objects\class SyntacticObject.are_sisters
(untested)

### Definition 20 - Sisterhood_Occurrences
(not implemented)

### Definition 21a - C-Command (syntactic objects)
structures\syntactic_objects\class SyntacticObject.c_commands

### Definition 21b - Asymmetric C-Command (syntactic objects)
structures\syntactic_objects\class SyntacticObject.asymmetric_c_command

### Definition 22 - C-Command (Paths)
(not implemented)

## 5 - Syntactic Objects Built from Chains
Won't be implemented, in accordance with the logic of the paper

## 6 - General Properties of Derivations

### Definition 23 - Derivable (Workspace)
(not implemented)

### Definition 24 - Binary Branching (T/F)
not implemented
Theorem 5: Every derivable syntactic object is binary branching

## 7 - Labels

### Definition 25 - Trigger Feature
Features\Class Trigger_Feature(Syn_Feature)

### Definition 26 - Triggers
structures\syntactic_objects\SyntacticObjectSet.triggers

### Definition 27 - (Triggered) Merge
structures\syntactic_objects\SyntacticObjectSet.merge

### Definition 28 - Label
structures\

### Definition 29 - Maximal Projection
structures\

### Definition 30 - Minimal Projection
structures\

### Definition 31 - Immediate Projection
structures\

### Definition 32 - Complement
structures\

### Definition 33 - Specifier
structures\

## 8 - Transfer

### Definition 34
structures\

### Definition 35 - Strong Phase
structures\

### Definition 36
structures\

### Definition 37 (replacing Definition 7) - Syntactic Object
structures\

### Definition 38 - Derivation
structures\

## 9 - Transfer_LF

### Definition 39 - Transfer_LF
structures\

## 10 - Transfer_PF

### Definition 40 - Final
structures\

### Definition 41 - Transfer_PF
structures\

## 13 - Convergence

### Definition 42 - Convergence_CI
structures\

### Definition 43 - Convergence_SM
structures\

### Definition 44 - Convergence
structures\

