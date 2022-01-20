# Breakthrough-CS-Public
Pre-Release of Computer Science

Special thanks to the following developers for their patches and contributions (in order of importance):

_Halludba 🙊
Beed 🍌,Woggy🦧

## USER INTERFACE

```
Enter L to load a game from a file, anything else to play a new game:> l

Current score: 8
Cards remaining in deck: 30

CURRENT LOCK
------------
Not met:       P a, F a, P a
Challenge met: K b
Not met:       P c, F b, P a
Challenge met: K a



SEQUENCE:

------------------
| K b | F c | K a |
------------------


HAND:

------------------------------
| P a | F a | P b | K a | P a |
------------------------------


(D)iscard inspect, (U)se card, (S)ave game:> u
```
## Game Save File format
The file is stored as the following:  
* Score  
  * Integer value 
* Locks and the Challenges that need to be met  
  * ToolType Kit 
* Is Locks met  
  * Bool
* Cards in hand  
  * ToolType Kit CardNum
* Card in sequence  
  * ToolType Kit CardNum
* Card in Discard  
  * ToolType Kit CardNum
* Card in Deck  
  * ToolType Kit CardNum
* 🙊🍌

## Links

https://en.wikibooks.org/wiki/A-level_Computing/AQA/Paper_1/Skeleton_program/2022

