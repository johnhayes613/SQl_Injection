import openai

openai.api_key = 'sk-proj-ZXikCxowEwDNEVn19oIUT3BlbkFJNlje1gWaSCMYlBOX2RPn'

def get_sqlmap_results():
    with open('output.txt', 'r') as file:
        sqlmap_output = file.read()
    return sqlmap_output

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

sqlmap_results = get_sqlmap_results()
question = "What vulnerabilities were found?"
prompt = f"SQLmap results:\n{sqlmap_results}\n\n{question}"
answer = ask_openai(prompt)
print(answer)
