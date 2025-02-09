# Project : Graph tree with author-article dataset
![image](https://github.com/user-attachments/assets/7fbfc794-20ab-459a-9ba3-84a372ee00c7)
![image](https://github.com/user-attachments/assets/91b4d486-3077-4722-8547-3e87fdabc01a)

# About this project :  
This project uses the subjects of graph structures, tree structure, graph algorithms. The authors in the excel dataset given to us and the authors they collaborated with, the articles they wrote were parsed appropriately and a graph structure was created.
This graph structure was visualized and links were created between the connected authors, if there were more connections, the connections were shown in a darker color. When the authors are clicked, the information about that author (ID, Articles, Number of Connections) and similar features are displayed. This information is in the Author Information table on the right. On the left, there is a table for the requirements requested in the document. The buttons in this table are clickable and when clicked, the algorithm of the request you pressed starts to work. Also, the author nodes have a physics engine and you can drag and pull them to the place you want.

This project was developed to model collaboration relationships between authors and to apply data structure and algorithm concepts through this model. In the project, authors and authors with whom these authors wrote articles are given in a ready dataset. A graph tree is obtained by establishing connections between these authors. There are 8 requests in the project. These requests are as follows.

## 1. Finding the shortest path between authors A and B and its graphical representation

The user will be asked for the IDs of authors A and B.
It will be checked whether there is a connected path between authors A and B. If there is a connection, the shortest path will be calculated according to the weights of the edges on the path. The calculated path will be shown graphically, a list of authors visited on the way from A to B will be created and the content of the queue will be shown step by step in this process.

## 2. Creating a queue according to node weights for author A and his/her collaborators

The number of articles written by each author will be defined as the node weight. The user will be asked for the ID of author A and all authors that author A and he/she collaborated with will be listed in a queue according to their node weights. Addition and removal operations to the queue will be shown live

## 3. Creating a BST (Binary Search Tree) from the authors in the queue

A binary search tree (BST) will be created from the authors in the queue created in the first step. The user will be asked for an author ID and after this author is removed from the tree, the final state of the tree will be shown graphically.

## 4. Calculating the shortest paths between author A and collaborating authors

The user will be asked for the ID of author A. A weighted graph will be created between author A, the authors he collaborates with and the authors they collaborate with. In this graph, the shortest paths to all nodes will be calculated and the table created in this process will be updated step by step

## 5. Calculating the number of authors that author A collaborates with

The user will be asked for the ID of author A and the total number of authors that this author collaborates with will be calculated and presented to the user

## 6. Determining the most collaborating author
The author who has collaborated the most among all authors in the database will be determined. The result will be presented to the user.
## 7. Finding the longest path that can be followed from the author ID received from the user

A writer ID will be requested from the user and the longest path that can be followed starting from this writer will be calculated. During this process, a node will be visited only once. The length will be determined by the number of nodes passed on the path and the result will be shown to the user

# Algorithms used

### 1. Dijkstra Algorithm
It was used to calculate the shortest path between two nodes on the graph. The nodes with the smallest distance were processed with a queue structure. This algorithm adopts a greedy approach and evaluates the best option available at each step. In other words, it processes the node with the shortest distance at each step and updates the distances of its neighbors. In this way, instead of examining all the paths on the graph one by one, only the most suitable paths are processed, thus ensuring efficiency.

### 2. DFS (Depth First Search)
It was implemented to find the longest path starting from a certain node. It scanned all the paths in depth by working with the LIFO principle.

### 3. Binary Search Tree (BST)
BST was used to store and process the shortest path results. Addition and removal operations to the queue were performed efficiently. In addition, inorder traversal was used to display the elements of the tree in an ordered manner. This ensured that the nodes in the data structure were accessed in an orderly manner.

# Libraries and tools used
Python: Development of algorithms and data processing.
Pandas: To extract and process data from Excel files.
Pyvis: To visualize graph structure.
Flask API: To provide interaction between HTML-based interface and Python.
HTML, CSS, JavaScript: Web interface design and user interactions.

# Developers 
### [Bedirhan Eren](https://github.com/bedirhaneren)
### [Ömer Attal](https://github.com/omerattal)

