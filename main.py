from mod.ColorPrint import colorprint as cprint
from mod.retutu import retutu
import os

path = "/"
score = 0

quoi_faire_string = [ """
Vous êtes dans le dossier /
Votre mission est de trouver le fichier 'perso.txt'
Pour cela, vous pouvez utiliser les commandes 'ls' et 'cd'
""", """
Vous avez trouvé le fichier 'perso.txt'
Vous pouvez maintenant lire son contenu, et aller a l'emplacement demandé
Pour cela, vous pouvez utiliser la commande 'cat'
""", """
Vous avez lu le fichier 'perso.txt'
Vous pouvez maintenant créer un fichier 'maths.txt' dans le dossier 'documents' de Mathis
Pour cela, vous pouvez utiliser la commande 'touch'
""", """
Vous avez créé le fichier 'maths.txt'
Mais un seul fichier n'est pas suffisant, il faudrait un dossier !
Pour cela, vous pouvez utiliser la commande 'mkdir', directement dans le dossier de Mathis
""", """
Bravo ! Vous avez créé le dossier 'maths' dans le dossier 'documents' de Mathis
Maintenant, il faut déplacer le fichier 'maths.txt' dans le dossier 'maths'
Pour cela, vous pouvez utiliser la commande 'mv'
"""
]

step = 0

perso_content = "Bonjour, je m'appelle Lea, et je veut vraiment aller voir le cours de maths de Mathis"

filesystem = {
    "/" : {
        "home" : {
            "Lea" : {
                "documents" : {
                    "cours.txt" : None,
                    "perso.txt" : perso_content,
                },
                "pictures" : {
                    "chat.png" : None,
                    "chien.png" : None,
                },
            },
            "Mathis" : {
                "documents" : {
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

def edit_vales(in_step = 0, score_plus = 0):
    global step, score
    step = in_step
    score += score_plus

def entry_to_path(entred_path):
    if len(entred_path) == 0:
        return path
    if entred_path[0] == "/":
        while "//" in entred_path:
            entred_path = entred_path.replace("//", "/")
        return entred_path

    liste = ["/", *path.split("/"), *entred_path.split("/")]
    # remove empty strings and "."
    liste = [i for i in liste if i not in ["", "."]]
    # remove if "..", remove previous
    for i in range(len(liste)):
        if liste[i] == ".." and i > 0:
            liste[i] = ""
            liste[i-1] = ""
    output = "/".join(["/"] + [i for i in liste if i != ""])
    while "//" in output:
        output = output.replace("//", "/")
    return output

def cheak_me_if_the_path_exist_please(entred_path):
    liste = ["/", *[e for e in entred_path.split("/") if e != ""]]
    dossier = filesystem
    for i in liste:
        if i in dossier:
            dossier = dossier[i]
        else:
            return False
    return True

def ls():
    # affiche le contenu du dossier
    dossier = filesystem
    for i in ["/", *[e for e in path.split("/") if e != ""]]:
        dossier = dossier[i]
    print(f"Contenu de {path}:")
    for k, v in dossier.items():
        if isinstance(v, dict):
            cprint(f" {k} (dossier)", "blue")
            continue
        cprint(f" {k} (fichier)", "yellow")
        if k == "perso.txt":
            edit_vales(1, 1)
            # affiche l'aide suivante
            quoi_faire()

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
    dossier = filesystem
    for i in ["/", *[e for e in new.split("/") if e != ""]]:
        dossier = dossier[i]
    if isinstance(dossier, dict):
        cprint(f"{new} est un dossier, pas un fichier", "red")
        return
    cprint(dossier, "magenta")
    if dossier == perso_content:
        edit_vales(2, 1)
        # affiche l'aide suivante
        quoi_faire()

def touch(x):
    dossier = filesystem
    for i in ["/", *[e for e in path.split("/") if e != ""]]:
        dossier = dossier[i]
    dossier[x] = None
    # if the user made a file names "maths.txt" in the /home/Mathis/documents folder
    if path == "/home/Mathis/documents" and x == "maths.txt":
        edit_vales(3, 1)
        # affiche l'aide suivante
        quoi_faire()
        
def mkdir(x):
    dossier = filesystem
    for i in ["/", *[e for e in path.split("/") if e != ""]]:
        dossier = dossier[i]
    dossier[x] = {}
    # if the user made a folder names "maths" in the /home/Mathis/documents folder
    if path == "/home/Mathis/documents" and x == "maths":
        edit_vales(4, 1)
        # affiche l'aide suivante
        quoi_faire()

def mv(x, y):
    ...

def cheat_up(x):
    global score, step
    step += int(x)
    print(f"new feature unlocked (step = {step}, score = {score})")
    quoi_faire()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def term_help():
    for k, v in commandes_disponibles.items():
        if v[2].startswith("//") or v[0] > step:
            continue
        print("{: <6} : {}".format(k, v[2]))

def quoi_faire(): # sourcery skip: extract-duplicate-method, merge-duplicate-blocks
    if step < len(quoi_faire_string):
        cprint(quoi_faire_string[step][1:-1], "#00ffaa")
    else:
        cprint(f"Le texte pour step {step} n'a pas été défini", "red")

def too_much_arguments(args, kwargs):
    cprint("Trop d'arguments pour cette commande !", "red")

commandes_disponibles = {
    "score": (0, lambda *args, **kwargs: print(f"Score: {score}") if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs), "Affiche le score"),
    "exit":  (0, lambda *args, **kwargs: exit() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                   "Quitte le terminal"),
    "ls":    (0, lambda *args, **kwargs: ls() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                     "Affiche le contenu du dossier"),
    "cd":    (0, lambda x = "/", *args, **kwargs: cd(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),        "Change le dossier courant"),
    "?":     (0, lambda *args, **kwargs: quoi_faire() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),             "Affiche quoi faire"),
    "clear": (0, lambda *args, **kwargs: clear() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                  "Efface l'écran"),
    "cu":    (0, lambda x = "1", *args, **kwargs: cheat_up(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),  "// Cheat up"),
    "help":  (0, lambda *args, **kwargs: term_help() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),              "Affiche l'aide"),
    "cat":   (1, lambda x = "/", *args, **kwargs: cat(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),       "Affiche le contenu du fichier"),
    "touch": (2, lambda x = "/", *args, **kwargs: touch(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),     "Crée un fichier"),
    "mkdir" : (3, lambda x = "/", *args, **kwargs : mkdir(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),   "Crée un dossier"),
    "mv" : (4, lambda x = "/", y = "/", *args, **kwargs: mv(x, y) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs), "Déplace un fichier ou un dossier"),
}

print("Bienvenue dans LLTFNT (Linux Like Terminal For NSI Terminal)")
print("Tapez '?' pour savoir quoi faire ou 'help' pour l'aide")

quoi_faire()

while True:
    for e in (("user@lltfnt", "#55ff55"), (":", "white"), (path, "blue"), ("$ ", "white")):
        cprint(e[0], e[1], "k")
    cmd = input()
    commande = cmd.split(" ")
    if commande[0] in commandes_disponibles:
        if step < commandes_disponibles[commande[0]][0]:
            cprint("Vous n'avez pas encore débloqué cette commande", "red")
            cprint(f"Vous etes niveau {step} ({commandes_disponibles[commande[0]][0]} requis)", "red")
            continue
        if len(commande) > 1:
            commandes_disponibles[commande[0]][1](commande[1:])
        else:
            commandes_disponibles[commande[0]][1]()
    elif commande[0] != "":
        print("Commande inconnue")
