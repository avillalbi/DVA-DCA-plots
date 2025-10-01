import pandas as pd

def filtrer_cycles(fichier_txt):
    """
    Filtre les cycles spécifiés dans un fichier TXT tabulé
    et crée automatiquement un nouveau fichier texte avec les résultats.

    :param fichier_txt: chemin du fichier d'entrée (.txt)
    :param cycles_a_garder: liste des numéros de cycles à conserver
    """
    # Demander à l'utilisateur les cycles
    entree = input("Entre les cycles à garder (séparés par des virgules) : ")
    cycles_a_garder = [int(x.strip()) for x in entree.split(",")]
    
    # Lire le fichier comme TSV
    df = pd.read_csv(fichier_txt, sep="\t")

    # Filtrer les cycles demandés
    df_filtre = df[df['# cycle'].round().astype(int).isin(cycles_a_garder)]

    # Construire un nom de fichier de sortie automatiquement
    fichier_sortie = fichier_txt+"_cycle_filtered.txt"

    # Écrire dans le fichier
    df_filtre.to_csv(fichier_sortie, sep="\t", index=False)

    print(f"✅ Fichier créé : {fichier_sortie}")
    return df_filtre

filtrer_cycles("SC_hand_03_pol")