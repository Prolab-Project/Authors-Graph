import json
from pyvis.network import Network

def create_visualization(graph_data):
    """JSON dosyasından okunan graf verisini görselleştirir"""
    # Fizik ayarları
    options = {
        "physics": {
            "stabilization": {
                "enabled": True,
                "iterations": 1000
            },
            "barnesHut": {
                "gravitationalConstant": -2000,
                "springConstant": 0.01,
                "damping": 0.5
            }
        }
    }
    
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#000000",
        font_color="white",
        directed=False
    )
    
    # Fizik ayarlarını doğru şekilde uygula
    net.set_options(json.dumps(options))
    
    # JSON dosyasını oku
    with open(graph_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Düğümleri ekle
    added_nodes = set()
    for node in data["nodes"]:
        node_id = node["orcid"]
        if node_id not in added_nodes:
            # Düğüm özelliklerini belirle
            connection_count = len(node["connections"])
            color = "#00ff00" if node_id.startswith("0000-") else "#ff9999"
            size = 20 + min(connection_count, 100) * 0.2  # Daha yumuşak bir ölçeklendirme
            
            # Düğümü ekle
            net.add_node(
                node_id,
                label=node["name"],
                title=f"ORCID: {node_id}\nİsim: {node['name']}\nBağlantı sayısı: {connection_count}",
                color=color,
                size=size,
                mass=1 + connection_count * 0.1  # Büyük düğümlere daha fazla kütle ekle
            )
            added_nodes.add(node_id)
    
    # Kenarları ekle
    for edge in data["edges"]:
        source, target = edge["edge"]
        weight = edge["weight"]
        
        if source in added_nodes and target in added_nodes:
            net.add_edge(
                source,
                target,
                value=weight,
                title=f"Bağlantı sayısı: {weight}",
                width=1 + weight/2
            )
    
    return net

def main():
    try:
        # Görselleştirme oluştur
        net = create_visualization("graph_output.json")
        
        # HTML dosyasına kaydet
        net.show("graph_visualization.html", notebook=False)
        print("Görselleştirme graph_visualization.html dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"Görselleştirme hatası: {str(e)}")

if __name__ == "__main__":
    main()
