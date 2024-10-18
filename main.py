from random import choice
from time import sleep

SEPARATOR = "|"

def serveur_read(serveur):
    f = open(f"{serveur}\multiconf.txt",'r')
    parametre=f.read()
    f.close()
    return(parametre)

def serveur_write(serveur, parametre):
    f = open(f'{serveur}\multiconf.txt','w')
    f.write(parametre)
    f.close()

def affichage(motM1):
    for l in motM1:
        print(l,end=" ")

def fin(motM, nom, serveur):
    if serveur!=None:
        parametre=serveur_read(serveur)
    else:
        print(f'Bravo tu a trouvé le mot "', end="")
        for l in motM:
            print(l, end="")
        input('"\nAppuyer sur "Entrée" pour revenir au menu principal: \n')
        return
    parametre=list(parametre.split(SEPARATOR))
    joueur1=parametre[0]
    joueur2=parametre[1]
    motM=parametre[2]
    gagnant=parametre[3]

    print('Bravo tu a trouvé le mot "',end="")
    for l in motM:
        print(l, end="")

    if gagnant=="None":
        parametre=joueur1+SEPARATOR+joueur2+SEPARATOR+motM+SEPARATOR+nom
        if serveur!=None:
            serveur_write(serveur, parametre)
        print('" en premier.')
    else:
        print('" mais en dernier.', gagnant, "a trouvé la réponse avant toi. Tu as donc perdu")
        parametre=f"None{SEPARATOR}None"
        if serveur!=None:
            serveur_write(serveur, parametre)

def Multijeur():
    def connection():
        for i in range(1, 4):
            with open(f'Serveur {i}\multiconf.txt','r') as f:
                parametre=f.read()

            parametre=list(parametre.split(SEPARATOR))
            joueur1=parametre[0]
            joueur2=parametre[1]
            
            if joueur1=="None":
                f = open(f'Serveur {i}\multiconf.txt','w')
                joueur1=nom
                hote=True
                parametre=joueur1+SEPARATOR+joueur2
                f.write(parametre)
                f.close()
                serveur=f"Serveur {i}"
            elif joueur2=="None":
                f = open(f'Serveur {i}\multiconf.txt','w')
                joueur2=nom
                hote=False
                parametre=joueur1+SEPARATOR+joueur2
                f.write(parametre)
                f.close()
                
            else:
                continue
            
            serveur=f"Serveur {i}"
            return serveur, hote
        return (None, None)

    while True:
        nom=input("Saisie ton nom: ")
        if nom=="None" or SEPARATOR in nom:
            print("Tu ne peux pas utiliser ce nom")
            continue
        serveur, hote = connection()
        if (serveur, hote) == (None, None):
            print("\nTous les serveurs sont plein, veillez ré-ésseiller plus tard")
            break

        print("En attente de joueur...")
        while True:
            if serveur=="Serveur 1":
                parametre=serveur_read()
            elif serveur=="Serveur 2":
                parametre=serveurR2()
            elif serveur=="Serveur 3":
                parametre=serveurR3()
            parametre=parametre.split(SEPARATOR)
            joueur1=parametre[0]
            joueur2=parametre[1]
            if joueur1!="None" and joueur2!="None":
                break
            sleep(0.7)

        if hote==True:
            f = open('mot.txt','r')
            motT=f.read()
            f.close()
            motT=list(motT.split(" "))            
            motM=choice(motT)

            joueur1=parametre[0]
            joueur2=parametre[1]
            joueurG="None"
            parametre=joueur1+SEPARATOR+joueur2+SEPARATOR+motM+SEPARATOR+joueurG
            if serveur=="Serveur 1":
                parametre=serveur_write(parametre)
            elif serveur=="Serveur 2":
                parametre=serveurW2(parametre)
            elif serveur=="Serveur 3":
                parametre=serveurW3(parametre)
            print("Préparatif en cour...")
            sleep(1)
        else:
            print("Préparatif en cour...")
            sleep(1)
            if serveur=="Serveur 1":
                parametre=serveur_read()
            elif serveur=="Serveur 2":
                parametre=serveurR2()
            elif serveur=="Serveur 3":
                parametre=serveurR3()
            parametre=list(parametre.split(SEPARATOR))
            motM=parametre[2]
        initialisation(motM, nom, serveur)
        break

def initialisation(motM=None, nom=None, serveur=None):
    vie = None
    if motM==None:
        f = open('mot.txt','r')
        motT = f.read()
        f.close()
        motT = list(motT.split(" "))
        motM = choice(motT)
        vie = 5
        print(motM)
    motM1 = list(motM)
    motM = list(motM)
    nbL = len(motM)

    for l in range(0,nbL):
        motM1[l]="_"
    saisie(motM, motM1, nbL, vie, nom, serveur)

def testLettre(ch, motM, motM1, nbL, vie=None, nom=None, serveur=None):
    if motM.count(ch)==0:
        print(f"Il n'y a pas de {ch}")
        vie=vie-1
        saisie(motM, motM1, nbL, vie, nom, serveur)
    else:
        for i in range(0,nbL):
            if ch==motM[i]:
                if motM1[i]=="_":
                    motM1[i]=ch                    
                else:
                    print("Tu a déjà saisie cette lettre")                    
        if motM1==motM:
            fin(motM, nom, serveur)
        else:
            saisie(motM, motM1, nbL, vie, nom, serveur)
    
def testMot(ch, motM, motM1, nbL, vie=None, nom=None, serveur=None):
    ch=list(ch)
    if ch==motM:
        fin(ch, nom, serveur)
    else:
        print("Mauvaise réponse")
        if vie != None:
            vie=vie-1
        saisie(motM, motM1, nbL, vie, nom, serveur)

def saisie(motM, motM1, nbL, vie=None, nom=None, serveur=None):
    affichage(motM1)
    if vie!=0:
        if vie != None:
            print("\n", f"Il te reste {vie} vie")
    else:
        print("\nTu n'a plus de vie\n")
        menu()
    while 1:
        ch=input("\nSaisie une lettre ou un mot: ")
        if len(ch)==1:
            testLettre(ch, motM, motM1, nbL, vie, nom, serveur)
            break
        elif len(ch)==0:
            print("Tu n'a rien écris")
            continue
        else:
            testMot(ch, motM, motM1, nbL, vie, nom, serveur)
            break
  
def menu_list_mode():
    print("\nMode de jeu:\n1) Solo\n2)Multijoueur\n3)Crédit")
    while 1:
        try:
            choix=input("Entrer le numéro du mode de jeu à laquelle vous voulez jouer: ")
            choix=int(choix)
            break
        except:
            print("Entrée non valide")
            continue
    if choix==1:
        initialisation()
    elif choix==2:
        Multijeur()
    elif choix==3:
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