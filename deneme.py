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
                width=1 + weight / 2
            )
    
    # HTML oluştur
    net.show("graph_visualization.html", notebook=False)
    
    # HTML dosyasını düzenle
    with open("graph_visualization.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    # CSS ve düğmeleri ekle
    style = """
    <style>
        #mynetwork {
            width: 85% !important;
            height: 750px !important;
            float: left !important;
        }
       #buttons {
    width: 15%; /* Sağ tarafta sabit genişlik */
    height: 100vh; /* Tam ekran yüksekliği */
    position: fixed; /* Sabit pozisyon */
    right: 0; /* Sağ tarafa hizalama */
    top: 0; /* Ekranın en üstünden başlama */
    background-color: #1a1a1a; /* Arka plan rengi */
    display: flex;
    flex-direction: column; /* Dikey hizalama */
    justify-content: space-evenly; /* Düğmeler arasında eşit boşluk */
    align-items: center; /* Düğmeleri yatayda ortala */
    padding: 10px;
    box-sizing: border-box;
    z-index: 9999; /* Üstte gösterim */
}

.menu-button {
    width: 90%; /* Düğmelerin genişliği */
    height: 12%; /* Her düğmenin yüksekliği (isteğe bağlı ayarlanabilir) */
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    display: flex;
    justify-content: center; /* Yazıyı ortala */
    align-items: center; /* Yazıyı ortala */
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
   let lastHighlightedNode = null;

    function handleClick(isterId) {
        if (isterId === 6) {
            findAuthorWithMostConnections();
        } else if (isterId === 5) {
            findConnectionsByOrcid();
        }
           else if (isterId === 7) {
            findLongestPathFromAuthor();
          }
          else {
            alert(`${isterId}. İster tıklandı`);
        }
    }

    function findLongestPathFromAuthor() {
    let startNodeId = prompt("Lütfen bir ORCID ID giriniz:");
    if (!startNodeId) {
        alert("Geçersiz ORCID ID!");
        return;
    }

    let foundNode = nodes.get(startNodeId);
    if (!foundNode) {
        alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
        return;
    }

    let visited = new Set();
    let longestPath = [];

    function dfs(nodeId, path) {
        visited.add(nodeId);
        path.push(nodeId);

        let neighbors = network.getConnectedNodes(nodeId);
        neighbors.forEach(neighbor => {
            if (!visited.has(neighbor)) {
                dfs(neighbor, path);
            }
        });

        // Eğer bu yol en uzunu ise güncelle
        if (path.length > longestPath.length) {
            longestPath = [...path];
        }

        path.pop(); // Geriye dön
        visited.delete(nodeId);
    }

    dfs(startNodeId, []);
    alert(`ORCID ID: ${startNodeId} için en uzun yol: ${longestPath.join(" → ")} (Uzunluk: ${longestPath.length})`);
}

    function findAuthorWithMostConnections() {
        let maxConnections = 0;
        let authorWithMostConnections = null;
        let authorNodeId = null;

        if (!nodes || !network) {
            alert("Düğümler veya ağ tanımlı değil!");
            return;
        }

        nodes.forEach(function(node) {
            let connectionCount = network.getConnectedNodes(node.id).length;
            if (connectionCount > maxConnections) {
                maxConnections = connectionCount;
                authorWithMostConnections = node.label;
                authorNodeId = node.id;
            }
        });

        if (authorNodeId) {
            highlightNode(authorNodeId);
            alert(`En fazla bağlantıya sahip yazar: ${authorWithMostConnections} (${maxConnections} bağlantı)`);
        }
    }

    function findConnectionsByOrcid() {
        let orcid = prompt("Lütfen bir ORCID ID giriniz:");
        if (!orcid) {
            alert("Geçersiz ORCID ID!");
            return;
        }

        let foundNode = nodes.get(orcid);
        if (!foundNode) {
            alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
            return;
        }

        let connectionCount = network.getConnectedNodes(orcid).length;
        highlightNode(orcid);
        alert(`ORCID ID: ${orcid} için toplam bağlantı sayısı: ${connectionCount}`);
    }

    function highlightNode(nodeId) {
        // Daha önce vurgulanmış bir düğüm varsa eski rengini geri getir
        if (lastHighlightedNode) {
            nodes.update([{ id: lastHighlightedNode, color: "#00ff00" }]);
        }

        // Yeni düğümü vurgula
        nodes.update([{ id: nodeId, color: "#ff0000" }]);
        lastHighlightedNode = nodeId;

        // Kamera o düğüme odaklansın
        network.focus(nodeId, {
            scale: 1.5,
            animation: {
                duration: 1000,
                easingFunction: "easeInOutQuad"
            }
        });
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
