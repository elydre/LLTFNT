from mod.ColorPrint import colorprint as cprint
from mod.retutu import retutu
import os

path = "/"
score = 0

step = 0

filesystem = {
    "/" : {
        "home" : {
            "Lea" : {
                "documents" : {
                    "cours.txt" : None,
                    "perso.txt" : "Bonjour, je m'appelle Lea, et je veut vraiment aller voir le cours de maths de Mathis",
                },
                "pictures" : {
                    "chat.png" : None,
                    "chien.png" : None,
                },
            },
            "Mathis" : {
                "documents" : {
                    "maths.txt" : None,
                    "ordi.txt" : None,
                },
                "pictures" : {
                    "souris.png" : None,
                    "pic2.png" : None,
                },
            },
            "Loic" : {
                "documents" : {
                    "rpg.txt" : None,
                    "miaou.txt" : retutu,
                },
                "music" : {
                    "je_suis_un_poisson.mp3" : None,
                },
            },
        },
        "bin" : {
            "ls.bin" : None,
            "cd.bin" : None,
            "cat.bin" : None,
        },
        "etc" : {
            "passwd.txt" : None,
            "shadow.txt" : None,
        },
    }
}

def ls(path):
    # affiche le contenu du dossier
    liste = ["/"]
    liste.extend(path.split("/"))
    dossier = filesystem
    for i in liste:
        if i != "":
            dossier = dossier[i]
    print(f"Contenu de {path}:")
    for k, v in dossier.items():
        if isinstance(v, str) or v is None:
            cprint(f"\t{k} (fichier)", "yellow")
            if k == "perso.txt":
                global step, score
                step, score = 1, score + 1
                # affiche l'aide suivante
                quoi_faire()                
        else:
            cprint(f"\t{k} (dossier)", "blue")

def entry_to_path(entred_path):
    if len(entred_path) == 0:
        return path
    if entred_path[0] == "/":
        return entred_path

    liste = ["/"]
    liste.extend(path.split("/"))
    liste.extend(entred_path.split("/"))
    # remove empty strings and "."
    liste = [i for i in liste if i not in ["", "."]]
    # remove if "..", remove previous
    for i in range(len(liste)):
        if liste[i] == ".." and i > 0:
            liste[i] = ""
            liste[i-1] = ""
    return "/".join([i for i in liste if i != ""]).replace("//", "/")

def cheak_me_if_the_path_exist_please(entred_path):
    liste = ["/"]
    liste.extend(entred_path.split("/"))
    dossier = filesystem
    for i in liste:
        if i != "":
            if i in dossier:
                dossier = dossier[i]
            else:
                return False
    return True

def cd(x):
    # change le dossier courant
    new = entry_to_path(x)
    if not cheak_me_if_the_path_exist_please(new):
        cprint(f"Le dossier {new} n'existe pas", "red")
        return
    global path
    path = new
    print(f"Vous êtes maintenant dans le dossier {path}")
    
def cat(x):
    # affiche le contenu du fichier
    new = entry_to_path(x)
    if not cheak_me_if_the_path_exist_please(new):
        cprint(f"Le fichier {new} n'existe pas", "red")
        return
    liste = ["/"]
    liste.extend(new.split("/"))
    dossier = filesystem
    for i in liste:
        if i != "":
            dossier = dossier[i]
    cprint(dossier, "magenta")

def quoi_faire(): # sourcery skip: extract-duplicate-method, merge-duplicate-blocks
    if step == 0:
        cprint("Vous êtes dans le dossier /", "green")
        cprint("Votre mission est de trouver le fichier 'perso.txt'", "green")
        cprint("Pour cela, vous pouvez utiliser les commandes 'ls' et 'cd'", "green")
    if step == 1:
        cprint("Vous avez trouvé le fichier 'perso.txt'", "green")
        cprint("Vous pouvez maintenant lire son contenu, et aller a l'emplacement demandé", "green")
        cprint("Pour cela, vous pouvez utiliser la commande 'cat'", "green")
        commandes_disponibles["cat"] = lambda x : cat(x[0])

def cheat_up():
    global score, step
    step += 1
    print("new feature unlocked")
    quoi_faire()

commandes_disponibles = {
    "score" : lambda : print(f"Score: {score}"),
    "exit" : lambda : exit(),
    "ls" : lambda : ls(path),
    "cd" : lambda x="/" : cd(x[0]),
    "?" : lambda : quoi_faire(),
    "clear": lambda : os.system("cls") if os.name == "nt" else os.system("clear"),
    "cat" : lambda : cprint("Cat : commande pas encore débloquée", "#ff8800"),
    "cheat" : lambda : cheat_up(),
}

print("Bienvenue dans le terminal de l'ordinateur")
print("Pour afficher l'aide, tapez '?'")
print("Pour afficher le score, tapez 'score'")

quoi_faire()

while True:
    print(end=f"{path} $ ")
    cmd = input()
    commande = cmd.split(" ")
    if commande[0] in commandes_disponibles:
        if len(commande) > 1:
            commandes_disponibles[commande[0]](commande[1:])
        else:
            commandes_disponibles[commande[0]]()
    else:
        print("Commande inconnue")