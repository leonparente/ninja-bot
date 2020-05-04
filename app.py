import os
import io
import sys
import json
import subprocess
import requests
from unidecode import unidecode
from flask import Flask, request, abort

def is_boolean_feature(value):
    value = str(value)
    if unidecode(value.lower()) == "sim" or unidecode(value.lower()) == "nao":
        return True
    return False

def generate_domain(dictionary):
    with open(os.path.dirname(os.path.abspath(__file__))+"/domain.yml", "w") as file:
        file.write("session_config:\n")
        file.write("  session_expiration_time: 60.0\n")
        file.write("  carry_over_slots_to_new_session: true\n")
        file.write("intents:\n")
        for key,value in dictionary.items():
            file.write("- perguntar_"+unidecode(key.lower()).replace(" ", "_")+"\n")

        file.write("entities:\n")
        for key,value in dictionary.items():
            file.write("- "+unidecode(key.lower()).replace(" ", "_")+"\n")
        
        file.write("responses:\n")
        file.write("  utter_fallback:\n")
        file.write("  - text: \"Desculpe! não sei a resposta para a sua pergunta, irei perguntar ao vendedor.\"\n")
        for key,value in dictionary.items():
            decode_key = unidecode(key.lower()).replace(" ", "_")
            file.write("  utter_"+decode_key+":\n")
            if is_boolean_feature(value):
                if unidecode(value.lower()) == "sim":
                    file.write("  - text: \"Olá. Tudo bem? O produto possui "+key+".\"\n")
                    file.write("  - text: \"Oi. Tudo bem? O produto possui "+key+".\"\n")
                    file.write("  - text: \"Olá! O produto possui "+key+".\"\n")
                    file.write("  - text: \"Oi! O produto possui "+key+".\"\n")
                else:
                    file.write("  - text: \"Olá. Tudo bem? O produto não possui "+key+".\"\n")
                    file.write("  - text: \"Oi. Tudo bem? O produto não possui "+key+".\"\n")
                    file.write("  - text: \"Olá! O produto não possui "+key+".\"\n")
                    file.write("  - text: \"Oi! O produto não possui "+key+".\"\n")
            elif decode_key != "quantidade":
                value = str(value)
                file.write("  - text: \"Olá. Tudo bem? "+key+" do produto é "+value+".\"\n")
                file.write("  - text: \"Oi. Tudo bem? "+key+" do produto é "+value+".\"\n")
                file.write("  - text: \"Olá! "+key+" do produto é "+value+".\"\n")
                file.write("  - text: \"Oi! "+key+" do produto é "+value+".\"\n")
            else:
                if value >= 0:
                    value = str(value)
                    file.write("  - text: \"Olá. Tudo bem? Temos "+value+" unidades ainda.\"\n")
                    file.write("  - text: \"Oi. Tudo bem? Temos "+value+" unidades ainda.\"\n")
                    file.write("  - text: \"Olá! Temos "+value+" unidades ainda.\"\n")
                else:
                    file.write("  - text: \"Olá. Tudo bem? Infelizmente o produto está indisponível no momento.\"\n")
                    file.write("  - text: \"Oi. Tudo bem? Tudo bem? Infelizmente o produto não está disponível no momento.\"\n")

def generate_nlu(dictionary):
    with open(os.path.dirname(os.path.abspath(__file__))+"/data/nlu.md", "w") as file:
        for key,value in dictionary.items():
            decode_key = unidecode(key.lower())
            file.write("## intent:perguntar_"+decode_key.replace(" ", "_")+"\n")
            if is_boolean_feature(value):
                file.write("- tem "+key+"?\n")
                file.write("- possui "+key+"?\n")
                file.write("- vem com "+key+"?\n")
                file.write("- tem "+decode_key+"?\n")
                file.write("- possui "+decode_key+"?\n")
                file.write("- vem com "+decode_key+"?\n\n")
            elif decode_key != "quantidade":
                file.write("- qual é a "+key+"?\n")
                file.write("- qual é o "+key+"?\n")
                file.write("- qual e "+key+"\n")
                file.write("- qual "+key+"?\n")
                file.write("- qual é a "+decode_key+"?\n")
                file.write("- qual é o "+decode_key+"?\n")
                file.write("- qual e "+decode_key+"\n")
                file.write("- qual "+decode_key+"?\n\n")
            else:
                file.write("- quantos tem ainda?\n")
                file.write("- quantos ainda tem?\n")
                file.write("- qual a quantidade disponivel?\n")
                file.write("- tem disponivel ainda?\n")
                file.write("- ainda tem?\n\n")

def generate_stories(dictionary):
    with open(os.path.dirname(os.path.abspath(__file__))+"/data/stories.md", "w") as file:
        for key,value in dictionary.items():
            decode_key = unidecode(key.lower()).replace(" ", "_")
            file.write("## teste_"+decode_key+"\n")
            file.write("* perguntar_"+decode_key+"\n")
            file.write("    - utter_"+decode_key+"\n\n")

app = Flask(__name__)

@app.route('/')
def mainpage():
    return "This is a Ninja bits Server test"

@app.route('/question', methods=['POST'])
def question():
    data = request.get_json()
    try:
        pergunta = data['pergunta']
        generate_domain(data['caracteristicas'])
        generate_nlu(data['caracteristicas'])
        generate_stories(data['caracteristicas'])
    except:
        abort(400, "Invalid JSON data")
    subprocess.call(["rasa", "train"])
    process = subprocess.Popen(["rasa", "run","--enable-api"],stdout=subprocess.PIPE)
    try:
        process.wait(30)
    except subprocess.TimeoutExpired:
        pass
    data = json.dumps({"sender": "Rasa", "message": pergunta})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
    res = res.json()
    resposta = res[0]['text']
    process.kill()
    return resposta

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
