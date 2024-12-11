import random
import sys
import networkx as nx
import matplotlib.pyplot as plt

class Router:
    """
    Classe router, modella il componenete fondamentale della rete su quale sarà possibile studiare il funzionamento del prtotocollo.
    Ogni router sarà caratterizzato da un nome e conterrà al suo interno la tabella di rooting.
    """
    def __init__(self, name):
        """
        Inizializzazione router, passato come paramtero il nome.
        La tabella di routing, verrà rappresentata tramite un dizionario che assocerà a ciascuna destinazione 
        il relativo costo e il next hop.
        """
        self.name = name  # Nome del router
        self.routing_table = {}  # Tabella di routing: {destinazione: (costo, next hop )}
        self.neighbours = {} # Vicini diretti { nome : costo }
        
    def add_neighbour(self, neighbour_name, cost):
        """
        Aggiunge un vicino diretto al router, ne va specificato nome e costo del collegamento.
        """
        self.neighbours[neighbour_name] = cost
        self.routing_table[neighbour_name] = (cost, "DIRECT")

        
    def add__route_entry(self, destination, cost, next_hop):
        """
        Funzione per l'aggiunta diretta di una entry alla routing table
        """
        self.routing_table[destination] = (cost, next_hop)

    def communicate_route(self, destination, cost, next_hop):
        """
        Funzione che simula la gestione da parte del router della ricezione,valutazione ed eventuale 
        aggiunta o aggiornamento di una route.
        In particolare, viene clacolato il nuovo costo della route proposta aggiungendo uno al conteggio degli hop per raggiungerla.
        Dopodiché qualora risultasse piu conveniente della route giá presente nella tabella, la entry verrá aggiornata.
        In caso la entry non fosse presente, verrá semplicemente aggiunta.
        Il valore di ritorno è true se la tabella subisce un aggiornamento, false altrimenti.
        """
        updated = False
        new_cost = cost + self.routing_table[next_hop][0] #Calcolo del nuono costo sommando il costo per raggiungere il vicino.
        if destination not in self.routing_table or new_cost < self.routing_table[destination][0]:
            self.add_route_entry(destination, new_cost,next_hop)
            updated = True

        return updated
    
    def __str__(self):
        """
        Rappresentazione tabella di routing
        """
        table_str = f"Routing table di {self.name}:\n"
        for destination, (cost, next_hop) in self.routing_table.items():
            table_str += f"  Destinazione: {destination}, Costo: {cost}, Next Hop: {next_hop}\n"
        return table_str

    def get_name(self):
        return self.name
    
    
class DV_network:
    def __init__(self):
        """
        Inizializzazione della network, la lista dei router è inizializzata come vuota.
        """
        self.routers = {} # Router nella network: {nome: Router}
        self.graph = nx.Graph()
        
    def generate_network(self,n):
        """
        Genera una network con connessioni casuali di n nodi, viene garantito che ogni 
        router abbia almeno un collegamento con un altro router. I pesi dei collegamenti
        sono assegnati casualmente.
        
        :param n: Numero di nodi del grafo
        """
        # Creazione degli n nodi del grafo e dei router
        for i in range(n):
            node_name = f"R{i+1}"
            new_router = Router(node_name)
            self.add_router(new_router)
            self.graph.add_node(node_name)
        
        # Costruisco le connessioni iniziali per garantire ogni router abbia almeno una connsessione (peso random)
        for i in range(n - 1):
            node1_name = f"R{i+1}"
            node2_name = f"R{i+2}"
            cost = random.randint(1, 10)
            self.graph.add_edge(node1_name, node2_name, weight=cost)
            self.connect_routers(node1_name,node2_name,cost)
        
        # Aggiungta di archi casuali extra alla rete (peso random)
        for i in range(n):
            for j in range(i + 1, n):
                node1_name = f"R{i+1}"
                node2_name = f"R{j+1}"
                # Aggiungi un arco solo se non esiste già
                if not self.graph.has_edge(node1_name, node2_name) and random.choice([True, False]):
                    cost = random.randint(1, 10)
                    self.graph.add_edge(node1_name, node2_name, weight=cost)
                    self.connect_routers(node1_name, node2_name, cost)


    def add_router(self, router):
        """
        Aggiunta di un router alla rete.
        """
        self.routers[router.get_name()] = router

    def connect_routers(self, router1, router2, cost):
        """
        Connessione di due router presenti nella network
        
        :param router1: Nome del router 1
        :param router2: Nome del router 2
        :param cost2: Costo del collegamento
        """
        self.routers[router1].add_neighbour(router2, cost)
        self.routers[router2].add_neighbour(router1, cost)
        
    def visualizza_grafo(self):
        """
        Visualizza il grafo della network

        """
        pos = nx.spring_layout(self.graph)  # Layout del grafo
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_color='red')
        plt.show()

    # def simulate(self, iterations=10):
    #     """Simula l'aggiornamento delle tabelle di routing."""
    #     for i in range(iterations):
    #         print(f"--- Iteration {i + 1} ---")
    #         changes = False
    #         for router in self.routers.values():
    #             for neighbour_name in router.neighbours:
    #                 neighbour = self.routers[neighbour_name]
    #                 changes |= router.update_routing_table(neighbour.routing_table)

    #         # Mostra le tabelle aggiornate
    #         for router in self.routers.values():
    #             print(router)

    #         if not changes:
    #             print("Network converged!")
    #             break