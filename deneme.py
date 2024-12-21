import json
from pyvis.network import Network

def create_visualization(graph_data):
    """JSON dosyasından okunan graf verisini görselleştirir"""
    # Ağı oluştur
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#000000",
        font_color="white",
        directed=False
    )
    
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
    
    net.set_options(json.dumps(options))
    
    with open(graph_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    added_nodes = set()
    for node in data["nodes"]:
        node_id = node["orcid"]
        if node_id not in added_nodes:
            connection_count = len(node["connections"])
            color = "#00ff00" if node_id.startswith("0000-") else "#ff9999"
            size = 20 + min(connection_count, 100) * 0.2
            
            net.add_node(
                node_id,
                label=node["name"],
                title=f"ORCID: {node_id}\nİsim: {node['name']}\nBağlantı sayısı: {connection_count}",
                color=color,
                size=size,
                mass=1 + connection_count * 0.1
            )
            added_nodes.add(node_id)
    
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
    
    # Önce normal HTML'i oluştur
    net.show("graph_visualization.html", notebook=False)
    
    # Sonra HTML'i düzenle
    with open("graph_visualization.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    # Stil ve düğmeleri ekle
    style = """
    <style>
        #mynetwork {
            width: 85% !important;
            height: 750px !important;
            float: left !important;
        }
        #buttons {
            width: 15%;
            height: 750px;
            float: right;
            background-color: #1a1a1a;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 10px;
            box-sizing: border-box;
        }
        .menu-button {
            width: 100%;
            padding: 15px;
            margin: 5px 0;
            background-color: #0066cc;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
        }
        .menu-button:hover {
            background-color: #0052a3;
        }
    </style>
    """
    
    buttons = """
    <div id="buttons">
        <button class="menu-button" onclick="handleClick(1)">1. İster</button>
        <button class="menu-button" onclick="handleClick(2)">2. İster</button>
        <button class="menu-button" onclick="handleClick(3)">3. İster</button>
        <button class="menu-button" onclick="handleClick(4)">4. İster</button>
        <button class="menu-button" onclick="handleClick(5)">5. İster</button>
        <button class="menu-button" onclick="handleClick(6)">6. İster</button>
        <button class="menu-button" onclick="handleClick(7)">7. İster</button>
    </div>
    <script>
        function handleClick(isterId) {
            console.log(`${isterId}. İster tıklandı`);
            // İster işlevselliği buraya eklenecek
        }
    </script>
    """
    
    # HTML içeriğini güncelle
    html_content = html_content.replace('</head>', f'{style}</head>')
    html_content = html_content.replace('<body>', f'<body>{buttons}')
    
    # Güncellenmiş HTML'i kaydet
    with open("graph_visualization.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def main():
    try:
        create_visualization("graph_output.json")
        print("Görselleştirme graph_visualization.html dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"Görselleştirme hatası: {str(e)}")

if __name__ == "__main__":
    main()
