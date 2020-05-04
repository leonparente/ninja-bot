# ninja-bot
Esse é o protótipo gerado para o desafio da Olist no MegaHack.

## Plataformas testadas
  - Ubuntu 18.04
  - Debian 9/10

## Setup

Primeiramente você deve clonar o repositorio git do ninja-bot e acessa-lo
```bash
git clone https://github.com/leonparente/ninja-bot.git
cd ninja-bot
```
O NinjaBot Server depende do python 3 para funcionar e algumas dependecias. Primeiramente, garanta que seu ambiente possua o python3 executando os comandos:
```bash
sudo apt install python3-dev python3-pip
```
O mais recommentado é que você utilize um ambiente virtual python para evitar instalar os pacotes globalmente e garantir um ambiente isolado. Entao crie o ambiente virtual e ative-o:
```bash
python3 -m venv ./venv
source ./venv/bin/activate
```

Agora deve instalar as dependências do ninja bot nesse ambiente virtual:
```bash
pip install -U pip
pip install rasa
pip install flask
pip install unidecode
```
Seu setup está pronto!

## Executando
Para executar o servidor do ninja bot, basta executar o servidor flask:
```bash
python3 app.py
```
O servidor gerará a rota 'http://localhost:5000/question' para a qual deve-se enviar um comando POST com um JSON contendendo a pergunta e as caracteristicas do produto.

### Exemplo de JSON

```json
{
  "pergunta": "Oii.. Ainda tem disponivel?",
  "caracteristicas":
  {
    "marca":"Eletrolux",
    "quatidade":10,
    "Freezer":"Sim",
    "Frost-free":"Não",
    "Dimensões":"200x120x70"
  }
}
```

OBS: nesse servidor de demonstração, caso o BOT nao saiba a resposta, ele responderá "Desculpe! não sei a resposta para a sua pergunta, irei perguntar ao vendedor". Esse é o trigger para enviar a pergunta ao vendedor.

## Testando via shell




