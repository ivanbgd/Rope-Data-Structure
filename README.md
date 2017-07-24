# Rope-Data-Structure

Implementation of a data structure that can store a string and efficiently cut a part
(a substring) of this string and insert it in a different position.
The current implementation only processes a given string.
It doesn't support inserting of new characters in the string. 

https://en.wikipedia.org/wiki/Rope_(data_structure)

Uses Splay tree to implement the Rope data structure.

Nodes don't have keys. They only have values. And the value is a lowercase English letter.
That means that one node contains and represents a single letter.
This data structure is about strings. The string represents (is) contents of a text document.
In a string, letters are in order, of course. The order is represented by their rank. That's why we use
order statistics to locate a node when searching for it (performing a "find" operation).
The rank can be seen as their index, and we'll use 0-based indexing.
The size of a node doesn't have anything to do with its rank. Also, when a node is splayed, its rank doesn't
change; only its size changes.
One has to think in terms of node rank, and not in terms of node key, as usual!
We could also add the field "rank" to Node objects.
But, that's not needed. In-order traversal gives all characters in order.

This is Python v2.7.

MIT License

Copyright (c) 2017 Ivan Lazarevic
