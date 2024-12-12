import pandas as pd

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

authorGraph = Graph()

data = pd.read_excel("data/dataset.xlsx")

unique_authors = data["author_name"].dropna().unique()
author_id_map = {author.lower(): idx + 1 for idx, author in enumerate(unique_authors)}

for author_name, author_ID in author_id_map.items():
    authorGraph.addNode(author_ID, author_name)

data["author_id"] = data["author_name"].str.lower().map(author_id_map)
data["coauthors"] = data["coauthors"].apply(parse_coauthors)

for _, row in data.iterrows():
    coauthors = row["coauthors"]
    for coauthor in coauthors:
        if coauthor in author_id_map:
            authorGraph.addEdges(row["author_id"], author_id_map[coauthor])

authorGraph.writeTxt("graph_output.txt", terminal_limit=10)
