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

logements_list = get_logements()

app = Flask(__name__)

@app.route('/logements')
def index():
    return render_template('logements.html', logements_list=logements_list)

if __name__ == '__main__':
    app.run(debug=True)

