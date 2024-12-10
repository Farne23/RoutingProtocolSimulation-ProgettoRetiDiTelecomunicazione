"""
Classe router, modella il componenete fondamentale della rete su quale sarà possibile studiare il funzionamento del prtotocollo.
Ogni router sarà caratterizzato da un nome e conterrà al suo interno la tabella di rooting.
"""
class Router:
    def __init__(self, name):
        """
        Inizializzazione router, passato come paramtero il nome.
        La tabella di rotuing, verrà rappresentata tramite un dizionario che assocerà a ciascuna destinazione (espressa come ip), 
        il relativo costo e l'indirizzo dell'hop succesivo.
        Il costo viene espresso secondo la metrica hop count, tiene conto dunque soltanto del numero di router intermedi tra sorgente 
        e destinazione. (RIP supporta un massimo di 15 HOP, oltre questa soglia la destinazione é considerata irragiungibile)
        """
        self.name = name  # Nome del router
        self.routing_table = {}  # Tabella di routing: {destinazione: (costo, prossimo_hop)}
    
    def add_entry(self, destination, cost, next_hop):
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
        new_cost = cost + 1
        if destination not in self.routing_table or new_cost < self.routing_table[destination][0]:
            self.add_entry(destination, new_cost,next_hop)
            updated = True

        return updated

    def remove_route(self, destination):
        """
        Rimozione di un percorso dalla tabella di routing
        """
        if destination in self.routing_table:
            del self.routing_table[destination]

    def __str__(self):
        """
        Rappresentazione tabella di routing
        """
        table_str = f"Routing table di {self.name}:\n"
        for destination, (cost, next_hop) in self.routing_table.items():
            table_str += f"  Destinazione: {destination}, Costo: {cost}, Next Hop: {next_hop}\n"
        return table_str