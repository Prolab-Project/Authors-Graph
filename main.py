import pandas as pd

# Dosya okuma
data = pd.read_excel("data/dataset.xlsx")  

print(data.head())

class Graph:
    def __init__(self):
        self.nodes = {}

    def addNode(self, author_ID, author_name):
        if author_ID not in self.nodes:
            self.nodes[author_ID] = {
                "name": author_name,
                "connections": [] 
            }

    def addEdges(self, author_ID_1, author_ID_2):
        if author_ID_1 in self.nodes and author_ID_2 in self.nodes:
            if author_ID_2 not in self.nodes[author_ID_1]["connections"]:
                self.nodes[author_ID_1]["connections"].append(author_ID_2)
            if author_ID_1 not in self.nodes[author_ID_2]["connections"]:
                self.nodes[author_ID_2]["connections"].append(author_ID_1)

    def viewGraph(self, limit=10):
        count = 0
        for node_id, node_data in self.nodes.items():
            print(f"Author ID: {node_id}, Name: {node_data['name']}, Connections: {node_data['connections']}")
            count += 1
            if count >= limit:
                print("There are too many nodes...")
                break

    def writeTxt(self, output_file="graph_output.txt"): 
     with open(output_file, "w", encoding="utf-8") as file:  # encoding="utf-8" ekledik
        for node_id, node_data in self.nodes.items():
            file.write(f"Author ID: {node_id}, Name: {node_data['name']}, Connections: {node_data['connections']}\n")


authorGraph = Graph()

unique_authors = data["author_name"].dropna().unique()
author_id_map = {author.lower(): idx + 1 for idx, author in enumerate(unique_authors)}

for author_name, author_ID in author_id_map.items():
    authorGraph.addNode(author_ID, author_name)

data["author_id"] = data["author_name"].str.lower().map(author_id_map)

for _, row in data.iterrows():
    if pd.notna(row["coauthors"]):
        coauthors = [x.strip().lower() for x in row["coauthors"].split(",")]
        for coauthor in coauthors:
            if coauthor in author_id_map:
                authorGraph.addEdges(row["author_id"], author_id_map[coauthor])

authorGraph.viewGraph(limit=20)
authorGraph.writeTxt("graph_output.txt")
