from random import choice
from time import sleep


SEPARATOR: str = "|"


def serveur_read(serveur: str) -> str:
    with open(f"{serveur}\multiconf.txt",'r') as f:
        return f.read()


def serveur_write(serveur: str, parametre: str) -> str:
    with open(f'{serveur}\multiconf.txt', 'w') as f:
        f.write(parametre)


def affichage(mot: list) -> None:
    for l in mot:
        print(l, end="")


def fin(motM: list, nom: str, serveur: str) -> None:
    if serveur is not None:
        parametres: str = serveur_read(serveur)

    else:
        print(f'Bravo tu a trouvé le mot "', end="")
        
        affichage(motM)

        input('"\nAppuyer sur "Entrée" pour revenir au menu principal: \n')
        return
    
    parametres: list = parametres.split(SEPARATOR)

    joueur1: str = parametres[0]
    joueur2: str = parametres[1]
    
    motM: str = parametres[2]
    gagnant: str = parametres[3]

    print('Bravo tu a trouvé le mot "', end="")
    affichage(motM)

    if gagnant == "None":
        parametre: str = joueur1 + SEPARATOR + joueur2 + SEPARATOR + motM + SEPARATOR + nom

        if serveur is not None:
            serveur_write(serveur, parametre)

        print('" en premier.')

    else:
        print('" mais en dernier.', gagnant, "a trouvé la réponse avant toi. Tu as donc perdu")
        parametre: str = f"None{SEPARATOR}None"

        if serveur is not None:
            serveur_write(serveur, parametre)


def Multijeur() -> None:
    def connection() -> tuple[str, bool] | tuple[None, None]:
        for i in range(1, 4):
            serveur: str = f"Serveur {i}"
            
            parametre: str = serveur_read(serveur)
            parametre: str = list(parametre.split(SEPARATOR))

            joueur1: str = parametre[0]
            joueur2: str = parametre[1]
            
            if joueur1 == "None":
                joueur1: str = nom
                hote: bool = True
                parametre: str = joueur1 + SEPARATOR + joueur2

            elif joueur2 == "None":
                joueur2: str = nom
                hote: str = False
                parametre: str = joueur1 + SEPARATOR + joueur2

            else:
                continue
            
            serveur_write(serveur, parametre)
            return serveur, hote

        return (None, None)

    while True:
        nom: str = input("Saisie ton nom: ")

        if nom == "None" or SEPARATOR in nom:
            print("Tu ne peux pas utiliser ce nom")
            continue

        serveur, hote = connection()

        if (serveur, hote) == (None, None):
            print("\nTous les serveurs sont plein, veillez ré-ésseiller plus tard")
            break

        print("En attente de joueur...")

        while True:
            if serveur is not None:
                parametre: str = serveur_read(serveur)

            else:
                raise Exception
            
            parametre: str = parametre.split(SEPARATOR)

            joueur1: str = parametre[0]
            joueur2: str = parametre[1]

            if joueur1 is not "None" and joueur2 is not "None":
                break

            sleep(0.7)

        if hote == True:
            with open('mot.txt','r') as f:
                motT: str = f.read()
            
            motT: list = list(motT.split(" "))            
            motM: str = choice(motT)
            
            joueur1: str = parametre[0]
            joueur2: str = parametre[1]
            joueurG: str = "None"
            
            parametre: str = joueur1 + SEPARATOR + joueur2 + SEPARATOR + motM + SEPARATOR + joueurG

            if serveur is not None:
                serveur_write(serveur, parametre)

            else:
                raise Exception
            
            print("Préparatif en cour...")
            sleep(1)

        else:
            print("Préparatif en cour...")
            sleep(1)

            if serveur is not None:
                parametre: str = serveur_read(serveur)

            else:
                raise Exception
            
            parametre: list = list(parametre.split(SEPARATOR))
            motM: str = parametre[2]

        initialisation(motM, nom, serveur)
        break


def initialisation(motM=None, nom=None, serveur=None):
    vie: int = None

    if motM == None:
        with open('mot.txt','r') as f:
            motT: str = f.read()

        motT: list = list(motT.split(" "))
        motM: str = choice(motT)
        vie: int = 5

        print(motM)

    motM1: list = list(motM)
    motM: list = list(motM)
    nbL: int = len(motM)

    for l in range(0,nbL):
        motM1[l] = "_"

    saisie(motM, motM1, nbL, vie, nom, serveur)


def testLettre(ch: str, motM: str, motM1: str, nbL: int, vie: int = None, nom: str = None, serveur: str = None):
    if motM.count(ch) == 0:
        if vie is not None:
            vie -= 1
        
        print(f"Il n'y a pas de {ch}")
        saisie(motM, motM1, nbL, vie, nom, serveur)

    else:
        for i in range(0,nbL):
            if ch == motM[i]:
                if motM1[i] == "_":
                    motM1[i] = ch  

                else:
                    print("Tu a déjà saisie cette lettre")  

        if motM1 == motM:
            fin(motM, nom, serveur)

        else:
            saisie(motM, motM1, nbL, vie, nom, serveur)

    
def testMot(ch: str, motM: str, motM1: str, nbL: int, vie: int = None, nom: str = None, serveur: str = None):
    ch: list = list(ch)

    if ch == motM:
        fin(ch, nom, serveur)
        return

    if vie is not None:
        vie -= 1
    
    print("Mauvaise réponse")
    saisie(motM, motM1, nbL, vie, nom, serveur)


def saisie(motM: str, motM1: str, nbL: int, vie: int = None, nom: str = None, serveur: str = None):
    affichage(motM1)

    if vie != 0:
        if vie is not None:
            print("\n", f"Il te reste {vie} vie")

    else:
        print("\nTu n'a plus de vie\n")
        menu()

    while True:
        ch: str = input("\nSaisie une lettre ou un mot: ")

        if len(ch) == 1:
            testLettre(ch, motM, motM1, nbL, vie, nom, serveur)
            break

        elif len(ch) == 0:
            print("Tu n'a rien écris")
            continue

        else:
            testMot(ch, motM, motM1, nbL, vie, nom, serveur)
            break
  

def menu_list_mode():
    print("\nMode de jeu:\n1) Solo\n2)Multijoueur\n3)Crédit")

    while True:
        choix: str = input("Entrer le numéro du mode de jeu à laquelle vous voulez jouer: ")

        if choix == "1":
            initialisation()

        elif choix == "2":
            Multijeur()

        elif choix == "3":
            print("\nCodé par Maxence Moreau")
            input("Appuyer sur Entrée pour revenir au menu: ")
            menu()

        else:
            print("Entrée non valide")


def menu():
    print("\nBienvenu dans mon jeu du pendu")
    sleep(1)
    input('Appuyer sur "Entrée" pour commencer: ')
    menu_list_mode()
    menu()


menu()