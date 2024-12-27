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
    
    options = {
        "physics": {
            "enabled": True,  # Fizik motorunu etkinleştir
            "stabilization": {
                "enabled": True,
                "iterations": 150  # Stabilizasyon iterasyon sayısı
            },
            "barnesHut": {
                "gravitationalConstant": -3000,  # Çekim kuvveti
                "centralGravity": 0.4,  # Merkezi çekim
                "springLength": 10,  # Yay uzunluğu
                "springConstant": 0.1,  # Yay sertliği
                "damping": 0.2  # Sönümleme oranı
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
            
            # Papers bilgisini al ve düzenle
            papers = node.get("papers", [])
            papers_html = "<br>".join(papers) if papers else "Yok"

            # Düğüm için tooltip bilgisi
            title = f"""
                <b>ORCID:</b> {node_id}<br>
                <b>İsim:</b> {node['name']}<br>
                <b>Bağlantı Sayısı:</b> {connection_count}<br>
                <b>Makaleler:</b><br>{papers_html}
            """

            net.add_node(
                node_id,
                label=node["name"],
                title=title,
                color=color,
                size=size,
                mass=1 + connection_count * 0.1,
                value=connection_count
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
        body {
        background-color: #000000; /* Tüm sayfa arka planını siyah yap */
        margin: 0; /* Kenarlardaki boşlukları sıfırla */
        padding: 0;
        overflow: hidden; /* Taşan içeriği gizle */
    }

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

    #info-panel {
        width: 15%;
        height: 100vh;
        position: fixed;
        left: 0;
        top: 0;
        background-color: #1a1a1a;
        color: white;
        padding: 20px;
        box-sizing: border-box;
        overflow-y: auto;
        z-index: 9999;
        resize: horizontal;
        overflow: auto;
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

    #info-content {
        font-size: 14px;
        line-height: 1.5;
        color: white; /* Yazı rengini beyaz yap */
        background-color: transparent;
    }

    #info-content table, #info-content th, #info-content td {
        color: white; /* Tablo yazı rengini beyaz yap */
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

        <style>
            #mynetwork {
                width: 85% !important;
                height: 750px !important;
                float: right !important;
            }
            #info-panel {
                width: 15%;
                height: 100vh;
                position: fixed;
                left: 0;
                top: 0;
                background-color: #1a1a1a;
                color: white;
                padding: 20px;
                box-sizing: border-box;
                overflow-y: auto;
                z-index: 9999;
            }
            #info-content {
                font-size: 14px;
                line-height: 1.5;
            }
        </style>
        </head>
        '''
    )

<div id="shortestPathsTable"></div>
  <!-- Kuyruk Barı -->
    <div id="queueBar" style="display: none; position: fixed; bottom: 0; width: 100%; background-color: #f0f0f0; border-top: 2px solid #ccc; padding: 10px; box-shadow: 0 -2px 5px rgba(0,0,0,0.2);">
        <div id="queueContent" style="overflow-y: auto; max-height: 150px; margin-bottom: 10px;"></div>
        <button onclick="closeQueueBar()" style="float: right; background-color: #ff5c5c; color: white; border: none; padding: 10px 20px; cursor: pointer;">İptal</button>
    </div>

    
        <body>
        <div id="info-panel">
            <h3>Yazar Bilgileri</h3>
            <div id="info-content">
                Bir düğüme tıklayın...
            </div>
        </div>
        '''

<script>
   let lastHighlightedNode = null;

function handleClick(isterId) {
    if (isterId === 1) {
        findShortestPath();
    } else if (isterId === 2) {
        handleCooperationQueue();
    } else if (isterId === 4) {
        handleShortestPathsFromAuthor();
    } else if (isterId === 5) {
        findConnectionsByOrcid();
    } else if (isterId === 6) { 
        findAuthorWithMostConnections();
    } else if (isterId === 7) {
        findLongestPathFromAuthor();
    }
}
function closeShortestPathsTable() {
    let tableContainer = document.getElementById("shortestPathsTable");
    tableContainer.style.display = "none"; // Tabloyu g��rünmez yap
    tableContainer.querySelector("tbody").innerHTML = ""; // Tablo içeriğini temizle
}


    function handleShortestPathsFromAuthor() {
    let authorId = prompt("Lütfen A yazarının ORCID ID'sini giriniz:");
    if (!authorId) {
        alert("Geçersiz ORCID ID!");
        return;
    }

    let foundAuthor = nodes.get(authorId);
    if (!foundAuthor) {
        alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
        return;
    }

    // İşbirliği grafiği oluştur
    let graph = {};
    let queue = [authorId];
    let visited = new Set();

    while (queue.length > 0) {
        let current = queue.shift();
        if (visited.has(current)) continue;

        visited.add(current);
        let neighbors = network.getConnectedNodes(current);
        graph[current] = [];

        neighbors.forEach(neighbor => {
            if (!visited.has(neighbor)) {
                queue.push(neighbor);
                graph[current].push({ id: neighbor, weight: edges.get(network.getConnectedEdges(current).find(edgeId => edges.get(edgeId).to === neighbor || edges.get(edgeId).from === neighbor)).value || 1 });
            }
        });
    }

    // En kısa yolları hesapla
    let distances = {};
    let previous = {};
    let unvisited = new Set(Object.keys(graph));
    let tableContainer = document.getElementById("info-content");
    tableContainer.innerHTML = "<table><tr><th>Düğüm</th><th>Mesafe</th><th>Önceki</th></tr></table>";

    Object.keys(graph).forEach(node => {
        distances[node] = Infinity;
        previous[node] = null;
    });
    distances[authorId] = 0;

    while (unvisited.size > 0) {
        let currentNode = Array.from(unvisited).reduce((a, b) => distances[a] < distances[b] ? a : b);
        unvisited.delete(currentNode);

        graph[currentNode].forEach(neighbor => {
            let newDist = distances[currentNode] + neighbor.weight;
            if (newDist < distances[neighbor.id]) {
                distances[neighbor.id] = newDist;
                previous[neighbor.id] = currentNode;
            }
        });

        // Tabloyu güncelle
        let table = tableContainer.querySelector("table");
        table.innerHTML = "<tr><th>Düğüm</th><th>Mesafe</th><th>Önceki</th></tr>";
        Object.keys(distances).forEach(node => {
            let row = document.createElement("tr");
            row.innerHTML = `<td>${node}</td><td>${distances[node] === Infinity ? "∞" : distances[node]}</td><td>${previous[node] || "-"}</td>`;
            table.appendChild(row);
        });
    }

    alert("En kısa yollar hesaplandı ve tablo güncellendi!");
}
    function handleCooperationQueue() {
    let authorId = prompt("Lütfen yazarın ORCID ID'sini giriniz:");
    if (!authorId) {
        alert("Geçersiz ORCID ID!");
        return;
    }

    let foundAuthor = nodes.get(authorId);
    if (!foundAuthor) {
        alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
        return;
    }

    // İşbirliği yaptığı yazarları bul
    let collaborators = network.getConnectedNodes(authorId);
    if (collaborators.length === 0) {
        alert("Bu yazarın işbirliği yaptığı başka yazar bulunamadı!");
        return;
    }

    // Öncelik kuyruğunu oluştur
    let cooperationQueue = new CooperationPriorityQueue();

    // Ana yazarı ekle
    let mainAuthorPaperCount = getPaperCount(foundAuthor);
    cooperationQueue.enqueue(foundAuthor, mainAuthorPaperCount);

    // İşbirlikçi yazarları ekle
    collaborators.forEach(collaboratorId => {
        let collaborator = nodes.get(collaboratorId);
        if (collaborator) {
            let paperCount = getPaperCount(collaborator);
            cooperationQueue.enqueue(collaborator, paperCount);
        }
    });

    // Adımları göster
    let steps = cooperationQueue.getSteps();
    
    // Bilgi panelini güncelle
    const infoContent = document.getElementById("info-content");
    let contentHTML = `
        <h3>Kuyruk Oluşturma Adımları</h3>
        <p><strong>Seçilen Yazar:</strong> ${foundAuthor.label}</p>
        <div style="margin-top: 20px;">
    `;

    // Her adımı göster
    steps.forEach((step, index) => {
        contentHTML += `
            <div style="margin-bottom: 15px; padding: 10px; background-color: #2a2a2a; border-radius: 4px;">
                <h4>Adım ${index + 1}</h4>
                <div style="margin-left: 10px;">
        `;

        // Kuyruk durumunu göster
        step.queueState.forEach((item, qIndex) => {
            contentHTML += `
                ${item.author.label} (${item.paperCount} makale)
                ${qIndex < step.queueState.length - 1 ? ' → ' : ''}
            `;
        });

        contentHTML += `
                </div>
                <div style="margin-top: 5px; color: #4CAF50; font-size: 0.9em;">
                    Eklenen: ${step.newItem.author.label} (${step.newItem.paperCount} makale)
                </div>
            </div>
        `;
    });

    // Final durumu göster
    contentHTML += `
        <div style="margin-top: 20px; padding: 10px; background-color: #3a3a3a; border-radius: 4px;">
            <h4>Final Sıralaması</h4>
            <div style="margin-left: 10px;">
    `;

    cooperationQueue.getItems().forEach((item, index) => {
        contentHTML += `
            ${item.author.label} (${item.paperCount} makale)
            ${index < cooperationQueue.getItems().length - 1 ? ' → ' : ''}
        `;
    });

    contentHTML += `
            </div>
        </div>
    `;

    infoContent.innerHTML = contentHTML;
}

class CooperationPriorityQueue {
    constructor() {
        this.items = [];
        this.steps = [];
    }

    enqueue(author, paperCount) {
        const queueItem = { author, paperCount };
        
        // Kuyruğun mevcut durumunu kaydet
        let currentState = [...this.items];
        
        // Makale sayısına göre sıralama (büyükten küçüğe)
        let added = false;
        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].paperCount < queueItem.paperCount) {
                this.items.splice(i, 0, queueItem);
                added = true;
                break;
            }
        }
        if (!added) {
            this.items.push(queueItem);
        }

        // Bu adımı kaydet
        this.steps.push({
            action: "ekleme",
            newItem: queueItem,
            queueState: [...this.items]
        });

        return queueItem;
    }

    getItems() {
        return this.items;
    }

    getSteps() {
        return this.steps;
    }
}

function getPaperCount(node) {
    if (node.title) {
        const papers = node.title.match(/<b>Makaleler:<\/b><br>(.*?)(?=<\/div>|$)/s);
        if (papers && papers[1]) {
            return papers[1].split('<br>').filter(paper => paper.trim()).length;
        }
    }
    return 0;
}

function addOperationLog(container, author, paperCount, isEnqueue) {
    const operation = isEnqueue ? "Eklendi" : "Çıkarıldı";
    const backgroundColor = isEnqueue ? "#2a2a2a" : "#3a3a3a";
    
    const logItem = document.createElement("div");
    logItem.style.cssText = `
        padding: 8px;
        margin: 5px 0;
        background-color: ${backgroundColor};
        border-radius: 4px;
        border-left: 4px solid ${isEnqueue ? "#4CAF50" : "#f44336"};
    `;
    
    logItem.innerHTML = `
        <strong>${operation}:</strong> ${author.label}<br>
        <small>Makale Sayısı: ${paperCount}</small>
    `;
    
    container.appendChild(logItem);
    container.scrollTop = container.scrollHeight;
}
function findShortestPath() {
    let startNodeId = prompt("Lütfen başlangıç yazarının ORCID ID'sini giriniz:");
    if (!startNodeId) {
        alert("Geçersiz başlangıç ORCID ID!");
        return;
    }

    let endNodeId = prompt("Lütfen hedef yazarının ORCID ID'sini giriniz:");
    if (!endNodeId) {
        alert("Geçersiz hedef ORCID ID!");
        return;
    }

    let foundStartNode = nodes.get(startNodeId);
    let foundEndNode = nodes.get(endNodeId);

    if (!foundStartNode || !foundEndNode) {
        alert("Başlangıç veya hedef yazar bulunamadı!");
        return;
    }

    // Dijkstra algoritması ile en kısa yolu bul
    let shortestPath = dijkstra(startNodeId, endNodeId);
    if (!shortestPath) {
        alert("A ile B arasında bir yol bulunamadı.");
        return;
    }

    // Yolu grafiksel olarak göster
    highlightPath(shortestPath.path);

    // Bilgi panelini güncelle
    const infoContent = document.getElementById("info-content");
    infoContent.innerHTML = `
        <h3>En Kısa Yol Bilgileri</h3>
        <p><strong>Başlangıç:</strong> ${startNodeId}</p>
        <p><strong>Hedef:</strong> ${endNodeId}</p>
        <p><strong>En Kısa Yol:</strong> ${shortestPath.path.join(" → ")}</p>
        <p><strong>Toplam Ağırlık:</strong> ${shortestPath.totalWeight}</p>
    `;
}


function dijkstra(startNodeId, endNodeId) {
    let distances = {};
    let previous = {};
    let pq = new PriorityQueue();
    let visited = new Set();

    // Başlangıç değerlerini ayarla
    nodes.forEach(node => {
        distances[node.id] = Infinity;
        previous[node.id] = null;
    });
    distances[startNodeId] = 0;
    pq.enqueue(startNodeId, 0);

    while (!pq.isEmpty()) {
        let currentNode = pq.dequeue().element;
        if (visited.has(currentNode)) continue;
        visited.add(currentNode);

        // Eğer hedef düğüme ulaşıldıysa
        if (currentNode === endNodeId) {
            let path = [];
            let totalWeight = distances[endNodeId];
            while (currentNode) {
                path.unshift(currentNode);
                currentNode = previous[currentNode];
            }
            return { path, totalWeight };
        }

        // Komşuları işle
        let neighbors = network.getConnectedEdges(currentNode);
        neighbors.forEach(edgeId => {
            let edge = edges.get(edgeId);
            let neighbor = edge.from === currentNode ? edge.to : edge.from;

            if (!visited.has(neighbor)) {
                let newDist = distances[currentNode] + (edge.value || 1); // Kenar ağırlığı
                if (newDist < distances[neighbor]) {
                    distances[neighbor] = newDist;
                    previous[neighbor] = currentNode;
                    pq.enqueue(neighbor, newDist);
                }
            }
        });
    }

    return null; // Eğer hedef düğüme ulaşılamazsa
}

function highlightPath(path) {
    // Tüm kenar renklerini eski haline döndür
    edges.forEach(edge => {
        edges.update({ id: edge.id, color: { color: "#848484" } });
    });

    // En kısa yoldaki kenarları kırmızı yap
    for (let i = 0; i < path.length - 1; i++) {
        let source = path[i];
        let target = path[i + 1];

        // Kenarı bul ve kırmızıya boya
        edges.forEach(edge => {
            if ((edge.from === source && edge.to === target) || (edge.from === target && edge.to === source)) {
                edges.update({ id: edge.id, color: { color: "#ff0000" } });
            }
        });
    }

    // Ağın merkezlenmesi
    network.fit({
        nodes: path,
        animation: {
            duration: 1500,
            easingFunction: "easeInOutQuad"
        }
    });
}

class PriorityQueue {
    constructor() {
        this.items = [];
    }

    enqueue(element, priority) {
        let newItem = { element, priority };
        let added = false;

        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].priority > newItem.priority) {
                this.items.splice(i, 0, newItem);
                added = true;
                break;
            }
        }

        if (!added) this.items.push(newItem);
    }

    dequeue() {
        return this.items.shift();
    }

    isEmpty() {
        return this.items.length === 0;
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
    html_content = html_content.replace('</body>', '''
    <script>
        network.on("click", function(properties) {
            const nodeId = properties.nodes[0];
            if (nodeId) {
                const node = nodes.get(nodeId);
                const infoContent = document.getElementById("info-content");

                // Düğümün bağlantı sayısını hesapla
                const connectionCount = network.getConnectedNodes(nodeId).length;
                
                // Makaleleri kontrol et ve listele
                let papersList = '<li>Makale bulunamadı</li>';
                if (node.title) {
                    // HTML title özelliğinden makaleleri çıkar
                    const titleContent = node.title;
                    const papersMatch = titleContent.match(/<b>Makaleler:<\/b><br>(.*?)(?=<\/div>|$)/s);
                    if (papersMatch && papersMatch[1]) {
                        const papers = papersMatch[1].split('<br>').filter(paper => paper.trim());
                        if (papers.length > 0) {
                            papersList = papers.map(paper => `<li>${paper}</li>`).join('');
                        }
                    }
                }

                infoContent.innerHTML = `
                    <p><strong>ORCID:</strong> ${node.id}</p>
                    <p><strong>İsim:</strong> ${node.label}</p>
                    <p><strong>Bağlantı Sayısı:</strong> ${connectionCount}</p>
                    <p><strong>Makaleler:</strong></p>
                    <ul>${papersList}</ul>
                `;
            } else {
                document.getElementById("info-content").innerHTML = "Bir düğüme tıklayın...";
            }
        });
    </script>
    </body>
    ''')
    
   # Güncellenmiş HTML'i kaydet
    with open("graph_visualization.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def main():
    try:
        create_visualization("cleaned_graph_output.json")
        print("Görselleştirme graph_visualization.html dosyasına kaydedildi.")
    except Exception as e:
        print(f"Görselleştirme hatası: {str(e)}")

if __name__ == "__main__":
    main()
