from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client
from flask import Flask, render_template, request

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


def get_logements():
    response = supabase.table('logements').select('*').execute()
    logements = response.data
    print(logements)
    return logements

def logement_details(ID_logement):
    response = supabase.table('logements').select('*').eq("id", ID_logement).execute()
    first_element = response.data[0]

    # Accéder à la valeur de l'attribut `critere_1_description`
    ID_logement= first_element['id']
    loyer = first_element['loyer']
    description = first_element['description']
    nom = first_element['nom']
    return ID_logement,loyer, description, nom

def questionnaire(ID_logement) :

     response = supabase.table('recherches').select('*').eq("ID_logement", ID_logement).execute()
     # Accéder au premier élément de la liste `data`
     first_element = response.data[0]

     # Accéder à la valeur de l'attribut `critere_1_description`
     ID_recherche= first_element['id']
     question_1 = first_element['critere_1_description']
     question_2 = first_element['critere_2_description']
     question_3 = first_element['critere_3_description']
     return ID_recherche,question_1, question_2, question_3   



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gestioneo/login')
def login():
    return "Page de login"

@app.route('/gestioneo/inscription')
def inscription():
    return "Page d'inscription"

@app.route('/gestioneo/logements')
def offres():
    logements_list = get_logements()
    return render_template('logements.html', logements_list=logements_list)

@app.route('/gestioneo/logement_<int:ID_logement>')
def logement(ID_logement):
    logement_info = logement_details(ID_logement)
    return render_template('logement.html', ID_logement=logement_info[0],loyer=logement_info[1], description=logement_info[2],nom=logement_info[3])


@app.route('/gestioneo/recherche_<int:ID_logement>')
def recherche(ID_logement):
     questions = questionnaire(ID_logement)
     return render_template('questionnaire.html', question_1=questions[1],question_2=questions[2],question_3=questions[3])

@app.route('/gestioneo/submit_<int:ID_logement>', methods=['POST'])
def submit(ID_logement):
     ID_recherche=questionnaire(ID_logement)[0]
     réponse_1 = request.form['Réponse_1']
     réponse_2 = request.form['Réponse_2']
     réponse_3 = request.form['Réponse_3']
     email = request.form['Réponse_4']
     # Code pour enregistrer la réponse dans la base de données
     prospect = supabase.table("prospects").insert({'ID_recherche':ID_recherche,"reponse_1":réponse_1 , "reponse_2":réponse_2 , "reponse_3":réponse_3 , "email":email }).execute()
     assert len(prospect.data) > 0
     return "Merci pour votre réponse !"




if __name__ == '__main__':
    app.run(debug=True)
