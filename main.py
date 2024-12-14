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
                output.append(f"ORCID: {node_id}, Name: {node_data['name']}, Connections: {node_data['connections']}\n")

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

start_id = input("Enter the start ORCID: ")
end_id = input("Enter the end ORCID: ")

file_path = 'data/dataset.xlsx'
data = pd.read_excel(file_path)

authorGraph = Graph()
for _, row in data.iterrows():
    author_name = row["author_name"]
    orcid = row["orcid"]
    coauthors = parse_coauthors(row["coauthors"])

    authorGraph.addNode(orcid, author_name)
    for coauthor_orcid in coauthors:
        authorGraph.addEdges(orcid, coauthor_orcid)

path, distance = find_shortest_path(authorGraph, start_id, end_id)
if path is None:
    print(f"There is no path between {start_id} and {end_id}")
else:
    print(f"Shortest path: {path}")
    print(f"Total distance: {distance}")

authorGraph.writeTxt(output_file="graph_output.txt")
