from flask import Flask, jsonify, request, render_template
import pandas as pd
import sys
import json 

def parse_coauthors(coauthor_str):
    if pd.isna(coauthor_str):
        return []
    coauthor_str = coauthor_str.strip("[]")
    coauthor_list = [x.strip().strip("'").strip('"').lower() for x in coauthor_str.split(",")]
    return coauthor_list

def clean_connections(graph):
    for orcid, node_data in graph.nodes.items():  # graph.getNodes() yerine graph.nodes
        if not orcid.startswith("generated"):
            author_name = node_data["name"]
            # Bağlantılar arasında yazarın ismiyle eşleşenleri temizle
            node_data["connections"] = [
                conn for conn in node_data["connections"]
                if graph.nodes[conn]["name"] != author_name
            ]
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def addNode(self, orcid, author_name):
        if orcid not in self.nodes:
            self.nodes[orcid] = {
                "name": author_name,
                "connections": [],
                "papers": []
            }

    def addPaper(self, orcid, paper_title):
        if orcid in self.nodes and paper_title not in self.nodes[orcid]["papers"]:
            self.nodes[orcid]["papers"].append(paper_title)

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

    def writeJsonManual(self, output_file="graph_output.json"):
    

     graph_data = {
        "nodes": [],
        "edges": []
     }

     # Düğümleri ekle
     for node_id, node_data in self.nodes.items():
        node_entry = {
            "orcid": node_id,
            "name": node_data["name"],
            "connections": [self.nodes[conn]["name"] for conn in node_data["connections"]]
        }
        # Eğer ORCID "generated" ile başlamıyorsa, makale başlıklarını ekle
        if not node_id.startswith("generated"):
            node_entry["papers"] = node_data["papers"]

        graph_data["nodes"].append(node_entry)

     # Kenarları ekle
     for edge, weight in self.edges.items():
        edge_entry = {
            "edge": list(edge),
            "weight": weight
        }
        graph_data["edges"].append(edge_entry)

     # JSON'u dosyaya yaz
     with open(output_file, "w", encoding="utf-8") as file:
        json.dump(graph_data, file, ensure_ascii=False, indent=4)

     print(f"Graph written to JSON file: {output_file}")

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

def create_priority_queue_manual(graph, start_id):
    """
    A yazarı ve işbirliği yaptığı yazarlar için düğüm ağırlıklarına göre kuyruk oluşturur.
    Ağırlık, her bir yazarın toplam işbirliği sayısını ifade eder.
    Kuyruk elle sıralanır (Python listesi kullanılarak).
    """
    if start_id not in graph.getNodes():
        print(f"No such ORCID {start_id} exists in the graph.")
        return []

    # Kuyruk: [(ağırlık, yazar_id)] şeklinde bir liste
    priority_queue = []
    visited = set()

    # A yazarını kuyruğa ekle
    start_connections = len(graph.getNodes()[start_id]["connections"])
    priority_queue.append((start_connections, start_id))
    visited.add(start_id)

    # A yazarı ile işbirliği yapanları kuyruğa ekle
    for neighbor in graph.get_outgoing_edges(start_id):
        if neighbor not in visited:
            neighbor_connections = len(graph.getNodes()[neighbor]["connections"])
            priority_queue.append((neighbor_connections, neighbor))
            visited.add(neighbor)

    # Kuyruğu ağırlıklara (ağırlık sayısına göre) göre büyükten küçüğe sırala
    for i in range(len(priority_queue)):
        for j in range(i + 1, len(priority_queue)):
            if priority_queue[i][0] < priority_queue[j][0]:  # Büyük ağırlık önce gelmeli
                priority_queue[i], priority_queue[j] = priority_queue[j], priority_queue[i]

    return priority_queue

def print_priority_queue_manual(priority_queue, graph):
    """
    Kuyruğu ekrana yazdırır.
    """
    print("\nPriority Queue (Yazarlar ve Ağırlıkları):")
    for weight, author_id in priority_queue:
        author_name = graph.getNodes()[author_id]["name"]
        print(f"Yazar: {author_name} (ORCID: {author_id}), İşbirliği Sayısı: {weight}")


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

# Her yazar için makale başlıklarını topla
author_papers = {}
for _, row in data.iterrows():
    if pd.notna(row["orcid"]) and pd.notna(row["paper_title"]):
        orcid = row["orcid"].lower()
        if orcid not in author_papers:
            author_papers[orcid] = []
        if row["paper_title"] not in author_papers[orcid]:  # Tekrarları önle
            author_papers[orcid].append(row["paper_title"])
unique_authors = data[["author_name", "orcid", "paper_title"]].dropna().drop_duplicates()
author_id_map = {row.orcid.lower(): row.author_name.lower() for _, row in unique_authors.iterrows()}

all_coauthors = set()
for coauthor_list in data["coauthors"].apply(parse_coauthors):
    all_coauthors.update(coauthor_list)

existing_authors = set(author_id_map.values())
missing_coauthors = all_coauthors - existing_authors

# Sabit bir ID oluşturmak için fonksiyon ve eksik yazarları işleme
def generate_deterministic_id(author_name):
    total = 0
    for i, char in enumerate(author_name):
        total += (i + 1) * ord(char)  # Her karakterin ASCII değerine pozisyonla ağırlık ver
    return f"generated-{total % 1000000}"  # Sabit bir uzunluk için modulo kullan

for coauthor in missing_coauthors:
    deterministic_id = generate_deterministic_id(coauthor)  # Sabit ID oluşturma
    author_id_map[deterministic_id] = coauthor

authorGraph = Graph()
for orcid, author_name in author_id_map.items():
    authorGraph.addNode(orcid, author_name)
    # Yazarın makalelerini ekle
    if orcid in author_papers:
        for paper in author_papers[orcid]:
            authorGraph.addPaper(orcid, paper)

data["author_orcid"] = data["orcid"].str.lower()
data["coauthors"] = data["coauthors"].apply(parse_coauthors)

for _, row in data.iterrows():
    coauthors = row["coauthors"]
    for coauthor in coauthors:
        coauthor_orcid = next((k for k, v in author_id_map.items() if v == coauthor), None)
        if coauthor_orcid:
            authorGraph.addEdges(row["author_orcid"], coauthor_orcid)

# Bağlantıları temizle
clean_connections(authorGraph)

# Temizlenmiş grafı JSON'a yaz
authorGraph.writeJsonManual("cleaned_graph_output.json")
print("Bağlantılardan yazarın kendi ismiyle eşleşenler temizlendi ve güncellenmiş JSON dosyasına yazıldı: cleaned_graph_output.json")


authorGraph.writeJsonManual("graph_output.json")
print("Graf JSON dosyasına yazdırıldı: graph_output.json")

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
    print(f"Count id number of connections is : {count_connection}")
    print(f"No such ORCID {start_id} exists in the graph.")

    # 2. İster: Kullanıcıdan yazar ID'si al ve kuyruk oluştur
author_id = input("dugum olusturmak icin ORCID id giriniz: ")
if author_id in authorGraph.getNodes():
    priority_queue = create_priority_queue_manual(authorGraph, author_id)
    print_priority_queue_manual(priority_queue, authorGraph)
else:
    print(f"No such ORCID {author_id} exists in the graph.")

# 2. İster: Kullanıcıdan yazar ID'si al ve kuyruk oluştur
author_id = input("dugum olusturmak icin ORCID id giriniz: ")
if author_id in authorGraph.getNodes():
    priority_queue = create_priority_queue_manual(authorGraph, author_id)
    print_priority_queue_manual(priority_queue, authorGraph)
else:
    print(f"No such ORCID {author_id} exists in the graph.")

