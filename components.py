"""
Classe router, modella il componenete fondamentale della rete su quale sarà possibile studiare il funzionamento del prtotocollo.
Ogni router sarà caratterizzato da un nome e conterrà al suo interno la tabella di rooting.
"""
class Router:
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
        self.neighbours.add(neighbour_name,cost)
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
    
    
class DV_network:
    def __init__(self):
        """
        Inizializzazione della network, la lista dei router è inizializzata come vuota.
        """
        self.routers = {}

    def add_router(self, name):
        """
        Aggiunta di un router alla rete.
        """
        self.routers[name] = Router(name)

    def connect_routers(self, router1, router2, cost):
        """
        Connessione di due router
        """
        self.routers[router1].add_neighbour(router2, cost)
        self.routers[router2].add_neighbour(router1, cost)

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