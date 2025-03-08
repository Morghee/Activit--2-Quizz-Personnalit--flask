# Import de la classe Flask du module flask
from flask import Flask, render_template, session, redirect
#On importe la liste
from questions import questions
from resultats import resultats
# Import de Operating System
import os

# Création d'une instance de la classe Flask = notre app
app = Flask("Mon premier test")
app.secret_key = os.urandom(24)

# Route de la page d'accueil
@app.route('/')
def index():
    session["nb_question"] = 0
    session["score"] = {"sonic":0, "amy":0, "dr":0, "tails":0}

    return render_template("index.html")

# Route de la question
@app.route('/question')
def question():
    global questions
    nb_question = session["nb_question"]
    if nb_question < len(questions) :
        #On récupère l'énoncé de la question
        enonce = questions[nb_question]["enonce"]
        #On copie le dictionnaire qui stocke la question et les réponses possibles
        question_copy = questions[nb_question].copy()
        question_copy.pop("enonce")
        #on récupère les valeurs = les réponses
        reponses = list(question_copy.values())
        #on récupère les clefs associées = pour les scores
        clefs = list(question_copy.keys())
        #Cookie pour stocker l'ordre ds réponses possibles
        session["clefs"] = clefs
        #on affiche la page question avec les différentes réponses possbile
        return render_template("question.html", question = enonce, reponses = reponses)

    else :
        global resultats
        #On trie les scores de manière décroissante sous forme de liste
        score_trie = sorted(session["score"], key = session["score"].get, reverse = True)
        #On récupère la 1e valeur de la liste qui est le nom de celui qui a eu le plus de tkt
        nom_vainqueur = score_trie[0]
        #On récupère la description du vainqueur
        description = resultats[nom_vainqueur]
        #On affiche les résultats en injectant nos variables stockant le nom et la description des perrso
        return render_template("resultats.html", vainqueur = nom_vainqueur, description = description)

#Route pour passer à la question suivante
@app.route('/reponse/<numero>')
def reponse(numero):
    #On incrémente numero_question pour passer à l'utilisateur suivant
    session["nb_question"] += 1
    #On récupère le nom du personnage dont la réponse a été sélectionnée
    nom_perso = session["clefs"][int(numero)]
    #On incrémente les scores du perso dont la réponse a été sélectionnée
    session["score"][nom_perso] += 1
    #On redirige vers le route question pour passer à la question suivante
    return redirect("/question")











# Exécution de l'application toujours en dernier
app.run(host='0.0.0.0', port = 81)