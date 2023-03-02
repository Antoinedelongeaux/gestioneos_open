from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client
from flask import Flask, render_template, request

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

ID_logement = 1

def logement_details(ID_logement):
    response = supabase.table('logements').select('*').eq("id", ID_logement).execute()
    first_element = response.data[0]

    # Accéder à la valeur de l'attribut `critere_1_description`
    ID_logement= first_element['id']
    loyer = first_element['loyer']
    description = first_element['description']
    nom = first_element['nom']
    return ID_logement,loyer, description, nom


logement_info = logement_details(ID_logement)

app = Flask(__name__)

@app.route('/logement_'+str(logement_info[0]))
def index():
    return render_template('logement.html', loyer=logement_info[1], description=logement_info[2],nom=logement_info[3])

if __name__ == '__main__':
    app.run(debug=True)
