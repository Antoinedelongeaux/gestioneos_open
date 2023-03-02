from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client
from flask import Flask, render_template, request


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

ID_logement=1

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

questions = questionnaire(ID_logement)

app = Flask(__name__)


@app.route('/recherche_'+ str(questions[0]))
    

def index():
     return render_template('questionnaire.html', question_1=questions[1],question_2=questions[2],question_3=questions[3])

@app.route('/submit', methods=['POST'])
def submit():
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