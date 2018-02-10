# Kevin-Bacon
A demonstration of degrees of separation through the game "Six Degrees of Kevin Bacon". 

The program uses a weighted graph to determine the connectedness of the chosen actor to other actors in the "top250.txt" file. Each node represents an actor, while the number of edges from one to another represents the degrees of separation between them. For example, if actors A and B starred together in a movie, they have 1 degree of separation. If Actors B and C starred in a movie that did not involve actor A, then actors A and C have 2 degrees of separation. Statistics related to connectedness are calculated using traversal algorithms such as breadth first search and Dijkstra's algorithm.

More information on the game: https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon

To run on terminal: python3 kevinbacon.py
