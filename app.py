from flask import Flask, request, jsonify
import mysql.connector
import subprocess
import openai

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    #password="123456",
    database="dummy_db"
)

#openai.api_key = 'OpenAI API key here'

def get_sqlmap_results():
    with open('output.txt', 'r') as file:
        sqlmap_output = file.read()
    return sqlmap_output

def ask_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return '''
        <form action="/login" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    user = cursor.fetchone()
    
    if user:
        return "Login successful!"
    else:
        return "Login failed!"

@app.route('/run_sqlmap', methods=['POST'])
def run_sqlmap():
    data = request.json
    url = data['url']
    
    result = subprocess.run(
        ['python', 'sqlmap.py', '-u', url, '--data', '--dump'],
        capture_output=True, text=True
    )
    
    with open('output.txt', 'w') as file:
        file.write(result.stdout)
    
    return jsonify(results=result.stdout)

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.json
    question = data['question']
    
    sqlmap_results = get_sqlmap_results()
    prompt = f"SQLmap results:\n{sqlmap_results}\n\n{question}"
    answer = ask_openai(prompt)
    
    return jsonify(answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
