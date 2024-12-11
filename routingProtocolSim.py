import random
import sys
import networkx as nx
import matplotlib.pyplot as plt
import components

def genera_network(n):
    """
    Genera una network con connessioni casuali di n nodi, viene garantito che ogni 
    router abbia almeno un collegamento con un altro router. I pesi dei collegamenti
    sono assegnati casualmente.
    
    :param n: Numero di nodi del grafo
    :return: Oggetto network da cui interagire con i router, Grafo pesato NetworkX (rappresentazione grafica della rete).
    """
    grafo = nx.Graph()
    network = components.DV_network()
    
    # Creazione degli n nodi del grafo e dei router
    for i in range(n):
        node_name = f"R{i+1}"
        grafo.add_node(node_name )
        network.add_router(components.Router(node_name ))
    
    # Costruisco le connessioni iniziali per garantire ogni router abbia almeno una connsessione (peso random)
    for i in range(n - 1):
        node1_name = f"R{i+1}"
        node2_name = f"R{i+2}"
        peso = random.randint(1, 10)
        grafo.add_edge(node1_name, node2_name, weight=peso)
        network.connect_routers(node1_name,node2_name,peso)
    
    # Aggiungta di archi casuali extra alla rete (peso random)
    for i in range(n):
        for j in range(i + 1, n):
            node1_name = f"R{i+1}"
            node2_name = f"R{j+1}"
            # Aggiungi un arco solo se non esiste già
            if not grafo.has_edge(node1_name, node2_name) and random.choice([True, False]):
                peso = random.randint(1, 10)
                grafo.add_edge(node1_name, node2_name, weight=peso)
                network.connect_routers(node1_name,node2_name,peso)

    return network,grafo

def stampa_grafo(grafo):
    """
    Stampa il grafo in formato leggibile

    :param grafo: Oggetto NetworkX
    """
    for u, v, data in grafo.edges(data=True):
        print(f"Arco ({u}, {v}): peso {data['weight']}")

def visualizza_grafo(grafo):
    """
    Visualizza il grafo utilizzando Matplotlib

    :param grafo: Oggetto NetworkX
    """
    pos = nx.spring_layout(grafo)  # Layout del grafo
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels, font_color='red')
    plt.show()

if __name__ == "__main__":
    # Richiede il numero di nodi all'utente
    n = int(input("Inserisci il numero di nodi del grafo (max 10): "))

    if n > 0 and n <= 10:
        network,grafo = genera_network(n)
        stampa_grafo(grafo)
        visualizza_grafo(grafo)
    else:
        print("Il numero di nodi deve essere maggiore di zero.")
    sys.exit(0)
    