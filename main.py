from mod.ColorPrint import colorprint as cprint
from mod.retutu import retutu
from time import sleep
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
Note : ce n'est pas le vrai mv, mais un mv simplifié, on ne peut déplacer qu'un fichier dans un dossier au même emplacement !
""", """
Bravo ! Vous avez déplacé le fichier 'maths.txt' dans le dossier 'maths'
Par contre, il y a un problème, le fichier 'maths.txt' est vide !
La commande 'touch' ne permet pas de créer un fichier avec du contenu
Par contre, vous pouvez utiliser la commande 'echo' pour écrire dans un fichier (syntaxe : `echo "contenu" > fichier`)
La commande ls ne fonctionne plus correctement, allez donc la fixer en écrivant "LS" dans son fichier ! (le fichier est dans le dossier '/bin')
""", """
C'est bon, la commande 'ls' fonctionne à nouveau !
Maintenant, on peut afficher l'arborescence du dossier du système de fichier
Cette commande s'appelle 'tree', mais elle n'existe pas encore !
Pour l'installer, vous pouvez utiliser la commande 'apt' en superutilisateur (syntaxe : `sudo apt install tree`)
""", """
Bravo ! Vous pouvez maintenant utiliser la commande 'tree' !
Maintenant, vous pouvez afficher l'arborescence du dossier du système de fichier
""", """
Bravo ! vous avez affiché l'arborescence du dossier du système de fichier
Vous avez terminé l'activité, un easter eggs est caché, à vous de le trouver !
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

def tree():
    # affiche l'arborescence du dossier
    dossier = filesystem
    for i in ["/", *[e for e in path.split("/") if e != ""]]:
        dossier = dossier[i]
    print(f"Arborescence de {path}:")
    def print_tree(dossier, level = 0):
        for k, v in dossier.items():
            if isinstance(v, dict):
                cprint(f"{'  '*level} {k} (dossier)", "blue")
                print_tree(v, level + 1)
                continue
            cprint(f"{'  '*level} {k} (fichier)", "yellow")
    print_tree(dossier)
    if path == "/":
        edit_vales(8, 1)
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
    # we go to the x and y folder
    x_path, y_path = "/", "/"
    if path != "/":
        x_path = f"{path}/"
        y_path = f"{path}/"
    x_path, y_path = x_path + x, y_path + y
    # we remove the last element of the path
    x_path = "/".join(x_path.split("/")[:-1])
    y_path = "/".join(y_path.split("/")[:-1])
    dossier_x = filesystem
    dossier_y = filesystem
    for i in ["/", *[e for e in x_path.split("/") if e != ""]]:
        try:
            dossier_x = dossier_x[i]
        except Exception:
            cprint(f"Le fichier {x_path} n'existe pas", "red")
            return
    for i in ["/", *[e for e in y_path.split("/") if e != ""]]:
        try:
            dossier_y = dossier_y[i]
        except Exception:
            cprint(f"Le dossier {y_path} n'existe pas", "red")
            return
    if x not in dossier_x:
        cprint(f"Le fichier {x} n'existe pas", "red")
        return
    if isinstance(dossier_y, str):
        cprint(f"{y} est un fichier, pas un dossier", "red")
        return
    dossier_x[y][x] = dossier_x[x]
    del dossier_x[x]
    # if the user moved a file names "maths.txt" in the /home/Mathis/documents folder
    if x_path == "/home/Mathis/documents" and x == "maths.txt":
        edit_vales(5, 1)
        # affiche l'aide suivante
        quoi_faire()
        
def echo(x, *args):
    # if it's just a print
    if len(args[0]) == 0:
        cprint(x, "magenta")
        return
    # if it's a file creation
    dossier = filesystem
    for i in ["/", *[e for e in path.split("/") if e != ""]]:
        dossier = dossier[i]
    if args[0][0] != ">":
        cprint("Syntaxe incorrecte", "red")
        return
    if len(args[0]) == 1:
        cprint("Syntaxe incorrecte", "red")
        return
    if len(x) < 2:
        cprint("Syntaxe incorrecte", "red")
        return
    if x[0] != '"' or x[-1] != '"':
        cprint("Syntaxe incorrecte", "red")
        return
    dossier[args[0][1]] = x[1:-1]
    # if the user put "LS" in the file "/bin/ls.bin"
    if path == "/bin" and args[0][1] == "ls.bin" and x[1:-1] == "LS":
        edit_vales(6, 1)
        # affiche l'aide suivante
        quoi_faire()

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
    cprint("Le nombre d'arguments pour cette commande n'est pas correct !", "red")

def apt(x, as_sudo):  # sourcery skip: extract-method
    if not as_sudo:
        cprint("Vous devez être root pour utiliser cette commande", "red")
        return
    if x[0] == "update":
        cprint("Toutes les sources sont à jour!", "white")
    if x[0] == "upgrade":
        cprint("Tous les paquets sont à jour!", "white")
    if x[0] == "install":
        if x[1] == "tree":
            cprint("installation de tree  [", "white", "k")
            for _ in range(20):
                cprint("=", "#00aaff", "k")
                sleep(0.1)
            cprint("]\ntree installé avec succès!", "white")
            edit_vales(7, 1)
            # affiche l'aide suivante
            quoi_faire()
        else:
            cprint(f"Le paquet {x[1]} n'existe pas", "red")

def sudo(commande):
    if len(commande) == 0:
        cprint("Syntaxe incorrecte", "red")
        return
    print(f"la commande '{' '.join(commande)}' a été lancée avec les droits root")
    if commande[0] == "apt":
        apt(commande[1:], True)
    elif commande[0] in commandes_disponibles:
        if step < commandes_disponibles[commande[0]][0]:
            cprint("Vous n'avez pas encore débloqué cette commande", "red")
            cprint(f"Vous etes niveau {step} ({commandes_disponibles[commande[0]][0]} requis)", "red")
            return
        if len(commande) > 1:
            commandes_disponibles[commande[0]][1](commande[1:])
        else:
            commandes_disponibles[commande[0]][1]()
    else:
        cprint("Commande inconnue", "red")


commandes_disponibles = {
    "score": (0, lambda *args, **kwargs: print(f"Score: {score}") if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                   "Affiche le score"),
    "exit":  (0, lambda *args, **kwargs: exit() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                                     "Quitte le terminal"),
    "ls":    (0, lambda *args, **kwargs: ls() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                                       "Affiche le contenu du dossier"),
    "cd":    (0, lambda x = "/", *args, **kwargs: cd(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                          "Change le dossier courant"),
    "?":     (0, lambda *args, **kwargs: quoi_faire() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                               "Affiche quoi faire"),
    "clear": (0, lambda *args, **kwargs: clear() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                                    "Efface l'écran"),
    "cu":    (0, lambda x = "1", *args, **kwargs: cheat_up(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                    "// Cheat up"),
    "help":  (0, lambda *args, **kwargs: term_help() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                                "Affiche l'aide"),
    "cat":   (1, lambda x = "/", *args, **kwargs: cat(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                         "Affiche le contenu du fichier"),
    "touch": (2, lambda x = "/", *args, **kwargs: touch(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                       "Crée un fichier"),
    "mkdir": (3, lambda x = "/", *args, **kwargs : mkdir(x[0]) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                      "Crée un dossier"),
    "mv":    (4, lambda x = "/", *args, **kwargs: mv(x[0], x[1]) if (len(args) == len(kwargs) == 0 and len(x) == 2) else too_much_arguments(args, kwargs),    "Déplace un fichier ou un dossier"),
    "echo":  (5, lambda x = "/", *args, **kwargs: echo(x[0], x[1:]) if (len(args) == len(kwargs) == 0 and len(x) >= 1) else too_much_arguments(args, kwargs), "Déplace un fichier ou un dossier"),
    "sudo":  (6, lambda x = [], *args, **kwargs:  sudo(x) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                           "Execute une commande en tant que root"),
    "apt":   (6, lambda x = [], *args, **kwargs:  apt(x, 0) if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                         "Gestionnaire de paquets"),
    "tree":  (7, lambda *args, **kwargs: tree() if (len(args) == len(kwargs) == 0) else too_much_arguments(args, kwargs),                                     "Affiche l'arborescence du dossier courant"),
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
        cprint("Commande inconnue", "red")
