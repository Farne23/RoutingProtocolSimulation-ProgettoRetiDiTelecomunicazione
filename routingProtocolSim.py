import components
import sys


if __name__ == "__main__":
    # Richiede il numero di nodi all'utente
    n = int(input("Inserisci il numero di nodi del grafo (min 2, max 10): "))

    if n > 2 and n <= 10:
        network = components.DV_network()
        network.generate_network(n)
        network.visualizza_grafo()
    else:
        print("Il numero di nodi deve essere maggiore di zero.")
    sys.exit(0)
    