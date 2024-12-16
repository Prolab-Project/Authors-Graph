from flask import Flask, jsonify, request, render_template
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

    def addNode(self, orcid, author_name):
        if orcid not in self.nodes:
            self.nodes[orcid] = {
                "name": author_name,
                "connections": []
            }

    def addEdges(self, orcid_1, orcid_2, weight=1):
        if orcid_1 != orcid_2:
            if orcid_1 in self.nodes and orcid_2 in self.nodes:
                edge = (min(orcid_1, orcid_2), max(orcid_1, orcid_2))
                if edge in self.edges:
                    self.edges[edge] += weight
                else:
                    self.edges[edge] = weight
                    self.nodes[orcid_1]["connections"].append(orcid_2)
                    self.nodes[orcid_2]["connections"].append(orcid_1)

    def writeTxt(self, output_file="graph_output.txt", terminal_limit=10):
        with open(output_file, "w", encoding="utf-8") as file:
            output = []

            output.append("Nodes:\n")
            for node_id, node_data in self.nodes.items():
                connections = [
                    self.nodes[conn]["name"] if conn not in self.nodes else conn
                    for conn in node_data['connections']
                ]
                output.append(f"ORCID: {node_id}, Name: {node_data['name']}, Connections: {connections}\n")

            output.append("\nEdge Weights:\n")
            for edge, weight in self.edges.items():
                output.append(f"Edge: {edge}, Weight: {weight}\n")

            print("Nodes (limited):")
            for i, line in enumerate(output):
              #  if i < terminal_limit:
                  #  print(line.strip())
                file.write(line)

    def getNodes(self):
        return self.nodes

    def get_outgoing_edges(self, node):
        if node in self.nodes:
            return self.nodes[node]["connections"]
        return []

    def value(self, from_node, to_node):
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

def find_max_connection(graph):
    max_connections = 0 
    most_connected_author = None 

    for orcid , node_data in graph.getNodes().items() : 
        connection_count = len (node_data["connections"]) 
        if connection_count > max_connections : 
            max_connections = connection_count 
            most_connected_author = orcid 
    return most_connected_author, max_connections         

def find_connection_count(graph, countId) :
    for orcid , node_data in graph.getNodes().items() : 
        if orcid == countId : 
            count_connection = len (node_data["connections"])
            return count_connection
    return None      

def find_longest_path(graph, start_node):
    visited = set()  
    longest_path = []  

    def dfs(current_node, path):
        nonlocal longest_path
        visited.add(current_node)
        path.append(current_node)

        # Eğer yol, mevcut en uzun yoldan uzunsa, güncelle
        if len(path) > len(longest_path):
            longest_path = path[:]

        # Komşuları gez
        for neighbor in graph.get_outgoing_edges(current_node):
            if neighbor not in visited:
                dfs(neighbor, path)

        # Geri dönmeden önce düğümü path'ten çıkar
        path.pop()
        visited.remove(current_node)

    dfs(start_node, [])
    return longest_path

file_path = 'data/dataset.xlsx'
data = pd.read_excel(file_path)

unique_authors = data[["author_name", "orcid"]].dropna().drop_duplicates()
author_id_map = {row.orcid: row.author_name.lower() for _, row in unique_authors.iterrows()}

all_coauthors = set()
for coauthor_list in data["coauthors"].apply(parse_coauthors):
    all_coauthors.update(coauthor_list)

existing_authors = set(author_id_map.values())
missing_coauthors = all_coauthors - existing_authors

next_id = len(author_id_map) + 1
for coauthor in missing_coauthors:
    author_id_map[f"generated-{next_id}"] = coauthor
    next_id += 1

authorGraph = Graph()
for orcid, author_name in author_id_map.items():
    authorGraph.addNode(orcid, author_name)

data["author_orcid"] = data["orcid"].str.lower()
data["coauthors"] = data["coauthors"].apply(parse_coauthors)

for _, row in data.iterrows():
    coauthors = row["coauthors"]
    for coauthor in coauthors:
        coauthor_orcid = next((k for k, v in author_id_map.items() if v == coauthor), None)
        if coauthor_orcid:
            authorGraph.addEdges(row["author_orcid"], coauthor_orcid)

authorGraph.writeTxt("graph_output.txt", terminal_limit=10)
print("Graf txt dosyasına yazdırıldı: graph_output.txt")

start_orcid = input("Enter the start ORCID: ")
end_orcid = input("Enter the end ORCID: ")

path, distance = find_shortest_path(authorGraph, start_orcid, end_orcid)
if path is None:
    print(f"\n\nThere is no path between {start_orcid} and {end_orcid}")
else:
    print(f"\n\nShortest path: {path}")
    print(f"\nTotal distance: {distance}")
    
most_connected_author, max_connections = find_max_connection(authorGraph)
author_name = authorGraph.getNodes()[most_connected_author]["name"]

print(f"Most connected author: {author_name} (ORCID: {most_connected_author})")
print(f"Number of connections: {max_connections}")

countId = input("Type the ID for which you want to calculate the number of connections :")
count_connection = find_connection_count(authorGraph,countId)
if count_connection is None : 
    print ("Count id has no connections")

    print(f"Count id number of connections is : {count_connection}")

    start_id = input("Enter the ORCID to find the longest path: ")

if start_id in authorGraph.getNodes():
    longest_path = find_longest_path(authorGraph, start_id)
    print(f"\nLongest path from {start_id}: {longest_path}")
    print(f"Number of nodes in the longest path: {len(longest_path)}")
else:
    print(f"No such ORCID {start_id} exists in the graph.")
