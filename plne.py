from gurobipy import Model, GRB

def main():
    # Nombre de produits
    nb_produits = int(input("Entrez le nombre de produits: "))
    produits = [input(f"Entrez le nom du produit {i+1}: ") for i in range(nb_produits)]
    
    # Données d'entrée
    demande = {p: int(input(f"Entrez la demande pour le produit {p}: ")) for p in produits}
    cout_achat = {p: float(input(f"Entrez le coût d'achat par lot pour le produit {p}: ")) for p in produits}
    cout_stockage = {p: float(input(f"Entrez le coût de stockage par unité pour le produit {p}: ")) for p in produits}
    cout_fixe_commande = {p: float(input(f"Entrez le coût fixe de commande pour le produit {p}: ")) for p in produits}
    taille_lot = {p: int(input(f"Entrez la taille du lot pour le produit {p}: ")) for p in produits}
    capacite_stockage = int(input("Entrez la capacité totale de stockage: "))

    # Créer le modèle
    m = Model()

    # Variables de décision
    x = {p: m.addVar(vtype=GRB.INTEGER, name=f"lots_{p}") for p in produits}
    y = {p: m.addVar(vtype=GRB.BINARY, name=f"commande_{p}") for p in produits}

    # Fonction objectif : Minimiser les coûts totaux
    m.setObjective(
        sum((cout_achat[p] * x[p] * taille_lot[p] + cout_fixe_commande[p] * y[p] + cout_stockage[p] * x[p] * taille_lot[p]) for p in produits),
        GRB.MINIMIZE
    )

    # Contraintes
    # Contrainte de demande
    for p in produits:
        m.addConstr(x[p] * taille_lot[p] >= demande[p], f"demande_{p}")
    
    # Contrainte de lien entre x et y
    for p in produits:
        m.addConstr(x[p] <= 1000 * y[p], f"lien_{p}")  # Assure que y_p = 1 si x_p > 0

    # Contrainte de capacité de stockage
    m.addConstr(sum(x[p] * taille_lot[p] for p in produits) <= capacite_stockage, "capacite_stockage")

    # Optimiser le modèle
    m.optimize()

    # Afficher les résultats
    if m.status == GRB.OPTIMAL:
        print("Solution optimale trouvée:")
        for p in produits:
            print(f"Produit {p}: Commander {x[p].X} lots, Commande active: {y[p].X}")
    else:
        print("Aucune solution optimale trouvée.")

if __name__ == "__main__":
    main()
