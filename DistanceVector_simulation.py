import random
import networkx as nx
import matplotlib.pyplot as plt
import sys

class Router:
    """
    Classe router, modella il componenete fondamentale della rete su quale sarà possibile studiare il funzionamento del prtotocollo.
    Ogni router sarà caratterizzato da un nome e conterrà al suo interno la tabella di rooting.
    """
    def __init__(self, name):
        """
        Inizializzazione router, passato come paramtero il nome.
        La tabella di routing, verrà rappresentata tramite un dizionario che assocerà a ciascuna destinazione 
        il relativo costo e il next hop. Verrá mantenuto un set contenente i nomi dei router adiacenti ed un
        buffer, per le routing table ricevute ad ogni iterazione dell'algoritmo.
        
        :param name: nome da assegnare al router
        """
        self.name = name  # Nome del router
        self.routing_table = {}  # Tabella di routing: {destinazione: (costo, next hop )}
        self.neighbours = set() # Set dei router collegati direttamente
        self.communications_buffer = {} #  Buffer con i DV ricevuti {name, {destinazione: (costo, next hop )}}
        
    def add_neighbour(self, neighbour_name, cost):
        """
        Aggiunge un vicino diretto al router, ne va specificato nome e costo del collegamento.
        La entry che lo riguarda viene inserita anche nella routing table, specificando nel campo next hop che il colegamento é diretto
        
        :param neighbout_name 
        :param cost : costo del collegamento
        """
        self.neighbours.add(neighbour_name)
        self.routing_table[neighbour_name] = (cost, "DIRECT")

        
    def add_route_entry(self, destination, cost, next_hop):
        """
        Funzione per l'aggiunta diretta di una entry alla routing table
        
        :param destination : nome destinazione
        :param cost : costo del collegamento
        :param next hop 
        """
        self.routing_table[destination] = (cost, next_hop)

    def handle_route(self, destination, cost, next_hop):
        """
        Funzione che simula la gestione da parte del router della ricezione di un dv, valutazione ed eventuale 
        aggiunta o aggiornamento di una route.
        In particolare, viene clacolato il nuovo costo della route proposta aggiungendo il costo per raggiungere l'hop da cui é arrivato il dv,
        dopodiché qualora risultasse piu conveniente della route giá presente nella tabella, la entry verrá aggiornata.
        In caso la entry non fosse presente, verrá semplicemente aggiunta.
        Il valore di ritorno è true se la tabella subisce un aggiornamento, false altrimenti.
        
        :param destination : nome destinazione
        :param cost : costo del collegamento
        :param next hop 
        """
        updated = False
        new_cost = cost + self.routing_table[next_hop][0] #Calcolo del nuono costo sommando il costo per raggiungere il vicino.
        if destination not in self.routing_table or new_cost < self.routing_table[destination][0]:
            self.add_route_entry(destination, new_cost,next_hop)
            updated = True

        return updated
    
    def communicate_dv(self,sender,distance_vector):
        """
        Funzione che simula la comunicazione di un dv al router.
        Il router si limita ad aggiungerla al buffer di ricezione per futura gestione.
        
        :param sender : nome del router mittente del dv
        :param distance_vector
        """
        self.communications_buffer[sender] = distance_vector
    
    def handle_communications(self):
        """
        Smaltimento della coda dei dv ricevuti, viene effetuata al termine dell'iterazione.
        Ogni route ricevuta viene valutata, ció puo portare ad un eventuale aggiornamento della
        routing table del nodo, che viene comunicato mediante un Booleano di ritorno (True se la routing table é stata modificata)
        """
        
        changes = False
        for sender,distance_vector in self.communications_buffer.items():
            for dest,(cost, next_hop) in distance_vector.items():
                if self.handle_route(dest,cost,sender):
                    changes = True
        self.communications_buffer.clear
        return changes
    
    def get_printable_routing_table(self):
        """
        Creazione di una stringa rappresentante in maniera leggibile la tabella di routing di un nodo
        """
        # Header della tabella 
        table_str = f"Routing table di {self.name}:\n"
        table_str += f"{'Destinazione':<15} {'Costo':<10} {'Next Hop':<15}\n"
        table_str += "-" * 40 + "\n"

        # Contenuto della tabella
        for destination, (cost, next_hop) in self.routing_table.items():
            table_str += f"{destination:<15} {cost:<10} {next_hop:<15}\n"

        return table_str

    def get_name(self):
        return self.name
    
    def get_routing_table(self):
        return self.routing_table
    
    def get_neighbours(self):
        return self.neighbours 
    
class DV_network:
    """
        Rappresentazione di una network sulla quale sará possibile simulare il funzionamento del protocollo distance vector.
        Verranno mantenuti i singoli router che la costituiscono ed un grafo per rappresentare graficamente la distribuzione dei collegamenti.
    """
    def __init__(self):
        """
        Inizializzazione della network, la lista dei router è inizializzata come vuota.
        """
        self.routers = {} # Router nella network: {nome: Router}
        self.graph = nx.Graph()  # Grafo di rete (ha solo scopi grafici)
        
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
            new_router.add_route_entry(node_name,0,"")
            self.add_router(new_router)
            self.graph.add_node(node_name)
        
        # Costruisco le connessioni iniziali per garantire ogni router abbia almeno una connsessione (peso random)
        for i in range(n - 1):
            node1_name = f"R{i+1}"
            node2_name = f"R{i+2}"
            cost = random.randint(1, 10)
            self.graph.add_edge(node1_name, node2_name, weight=cost)
            self.connect_routers(node1_name,node2_name,cost)
        
        # Aggiunta di archi casuali extra alla rete (peso random)
        for i in range(n):
            for j in range(i + 1, n):
                node1_name = f"R{i+1}"
                node2_name = f"R{j+1}"
                # Aggiungo un arco solo se non esiste già
                if not self.graph.has_edge(node1_name, node2_name) and random.choice([True, False, False, False,False,False]): #Una possibilita su 7 di generare un arco extra tra due nodi
                    cost = random.randint(1, 10)
                    self.graph.add_edge(node1_name, node2_name, weight=cost)
                    self.connect_routers(node1_name, node2_name, cost)


    def add_router(self, router):
        """
        Aggiunta di un router alla rete.
        
        :param router
        """
        self.routers[router.get_name()] = router

    def connect_routers(self, router1, router2, cost):
        """
        Connessione di due router presenti nella network
        
        :param router1: Nome del router 1
        :param router2: Nome del router 2
        :param cost: Costo del collegamento
        """
        self.routers[router1].add_neighbour(router2,cost)
        self.routers[router2].add_neighbour(router1,cost)
        
    def show(self):                   
        """
        Visualizza il grafo della network 
        """   
        # Layout del grafo
        pos = nx.spring_layout(self.graph)  
        labels = nx.get_edge_attributes(self.graph, 'weight')

        # Creazione della griglia per il layout della finestra
        fig = plt.figure(figsize=(12, 80))

        # Disegno del grafo
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_color='red')
             
        plt.tight_layout()
       
    def simulate(self):
        """
        Simulazione del protocollo di routing distance vector. 
        A ciascuna iterazione, viene fatto comunicare ad ogni router il propio distance vector ad ogni router adiacente.
        Al termine della comunicazione, ogni router procede ad elaboare i messaggi ed aggiornare la propria routing table.
        La simulazione termine quando al termine di un iterazione, viene comunicato che nessun router ha compiuto modifiche sulla propria routing table.
        """   
        changes = True
        max_it = 20
        iterations = 0
        
        print(f"################### PARTENZA ###################") 
                   
        #Gestione delle comunicazioni ed update delle tabelle di routing di ciascuno
        for router in self.routers.values(): 
            print(router.get_printable_routing_table())
        
        while iterations < max_it and changes:
            #Comunicazione dei dv tra i router adiacenti
            for router in self.routers.values():
                for neighbour_name in router.get_neighbours():
                    self.routers[neighbour_name].communicate_dv(router.get_name(),router.get_routing_table()) 
            
            iterations = iterations + 1
            print(f"################### Iterazione: {iterations} ###################") 
                   
            #Gestione delle comunicazioni ed update delle tabelle di routing di ciascuno
            changes = False
            for router in self.routers.values(): 
                if router.handle_communications(): 
                    changes = True  
                print(router.get_printable_routing_table())
            
            if not changes :
                print(f"Convergenza raggiunta in {iterations} iterazioni!")
            else :
                print("Convergenza non ancora raggiunta!\n")
                
        print("--Fine simulazione")
        
        
            
if __name__ == "__main__":
    # Richiede il numero di nodi all'utente
    n = int(input("Inserisci il numero di nodi del grafo (min 2, max 16): "))

    if n > 2 and n <= 16:
        network = DV_network()
        network.generate_network(n)
        network.show()
        network.simulate()
        plt.show()
    else:
        print("Il numero di nodi deve essere maggiore di zero.")
    sys.exit(0)