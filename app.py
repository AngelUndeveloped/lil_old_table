from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from supabase import create_client, Client
import os

app = Flask(__name__)
CORS(app)

# Set up supabase client
SUPABASE_URL=os.environ.get(SUPABASE_URL)
SUPABASE_KEY=os.environ.get(SUPABASE_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    response = supabase.table('items').select('*').execute()
    return jsonify(response)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    response = supabase.table('items').insert(data).execute()
    return jsonify(response.data)

@app.route('/items/<int:patient_id>', methods=['PUT'])
def update_item(id):
    data = request.json
    response = supabase.table('items').update(data).eq('id', id).execute()
    return jsonify(response.data)

@app.route('/items/<int:patient_id>', methods=['DELETE'])
def delete_item(id):
    response = supabase.table('items').delete().eq('id', id).execute()
    return jsonify(response.data)

if __name__ == '__main__':
    app.run(debug=True)