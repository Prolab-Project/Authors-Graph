import pandas as pd
import sys

def parse_coauthors(coauthor_str):
    if pd.isna(coauthor_str):
        return []
    coauthor_str = coauthor_str.strip("[]")
    coauthor_list = [x.strip().strip("'").strip('"').lower() for x in coauthor_str.split(",")]
    return coauthor_list

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def addNode(self, author_ID, author_name):
        if author_ID not in self.nodes:
            self.nodes[author_ID] = {
                "name": author_name,
                "connections": []
            }

    def addEdges(self, author_ID_1, author_ID_2, weight=1):
        if author_ID_1 != author_ID_2:
            if author_ID_1 in self.nodes and author_ID_2 in self.nodes:
                edge = (min(author_ID_1, author_ID_2), max(author_ID_1, author_ID_2))
                if edge in self.edges:
                    self.edges[edge] += weight
                else:
                    self.edges[edge] = weight
                    self.nodes[author_ID_1]["connections"].append(author_ID_2)
                    self.nodes[author_ID_2]["connections"].append(author_ID_1)

    def writeTxt(self, output_file="graph_output.txt", terminal_limit=10):
        with open(output_file, "w", encoding="utf-8") as file:
            output = []

            output.append("Nodes:\n")
            for node_id, node_data in self.nodes.items():
                output.append(f"Author ID: {node_id}, Name: {node_data['name']}, Connections: {node_data['connections']}\n")

            output.append("\nEdge Weights:\n")
            for edge, weight in self.edges.items():
                output.append(f"Edge: {edge}, Weight: {weight}\n")

            print("Nodes (limited):")
            for i, line in enumerate(output):
                if i < terminal_limit:  
                    print(line.strip())
                file.write(line)

    def getNodes(self):
        return self.nodes     

    def get_outgoing_edges(self, node):
        """Bir düğümün komşularını döndürür."""
        if node in self.nodes:
            return self.nodes[node]["connections"]
        return []

    def value(self, from_node, to_node):
        """İki düğüm arasındaki kenar ağırlığını döndürür."""
        edge = (min(from_node, to_node), max(from_node, to_node))
        return self.edges.get(edge, float('inf')) 

def dijkstra(Graph, start_node): 
    unvisited_nodes = list(Graph.getNodes().keys())
    shortest_path = {}
    previous_nodes = {}
    max_value = sys.maxsize
    
    for node in unvisited_nodes: 
        shortest_path[node] = max_value
    shortest_path[start_node] = 0 
    
    while unvisited_nodes:
        current_min_node = None 
        for node in unvisited_nodes: 
            if current_min_node is None or shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        
        neighbors = Graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            temp_value = shortest_path[current_min_node] + Graph.value(current_min_node, neighbor)
            if temp_value < shortest_path[neighbor]:
                shortest_path[neighbor] = temp_value
                previous_nodes[neighbor] = current_min_node
        
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

def find_shortest_path(graph, start_id, end_id):
    previous_nodes, shortest_path = dijkstra(graph, start_id)
    path = []
    current_node = end_id

    while current_node != start_id:
        path.append(current_node)
        current_node = previous_nodes.get(current_node)
        if current_node is None:
            return None, float('inf')

    path.append(start_id)
    path.reverse()
    return path, shortest_path[end_id]

start_id = int(input("Enter the start ID "))
end_id = int(input("Enter the End ID "))

file_path = 'data/dataset.xlsx'
data = pd.read_excel(file_path)

unique_authors = data["author_name"].dropna().unique()
author_id_map = {author.lower(): idx + 1 for idx, author in enumerate(unique_authors)}

all_coauthors = set()
for coauthor_list in data["coauthors"].apply(parse_coauthors):
    all_coauthors.update(coauthor_list)

existing_authors = set(author_id_map.keys())
missing_coauthors = all_coauthors - existing_authors

next_id = max(author_id_map.values(), default=0) + 1
for coauthor in missing_coauthors:
    author_id_map[coauthor] = next_id
    next_id += 1

authorGraph = Graph()
for author_name, author_ID in author_id_map.items():
    authorGraph.addNode(author_ID, author_name)

data["author_id"] = data["author_name"].str.lower().map(author_id_map)
data["coauthors"] = data["coauthors"].apply(parse_coauthors)

for _, row in data.iterrows():
    coauthors = row["coauthors"]
    for coauthor in coauthors:
        authorGraph.addEdges(row["author_id"], author_id_map[coauthor])

# En kısa yol bulma ve yazdırma
path, distance = find_shortest_path(authorGraph, start_id, end_id)
if path is None:
    print(f"There is no path between {start_id} and {end_id} ")
else:
    print(f"Shortest path: {path}")
    print(f"Total distance: {distance}")

authorGraph.writeTxt(output_file="graph_output.txt")
