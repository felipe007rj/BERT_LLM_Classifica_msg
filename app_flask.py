from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.nn.functional import softmax

app = Flask(__name__)

# Carregar o modelo e o tokenizador
model_path = './modelo'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# Mapeamento de rótulos de string para números inteiros
label_to_index = {
    "Atendimento": 0,
    "Bloqueio, Desbloqueio ou Suspensão": 1,
    "Cancelamento": 2,
    "Cobrança": 3,
    "Dados Cadastrais": 4,
    "Instalação, Ativação ou Habilitação": 5,
    "Mudança de Endereço": 6,
    "Plano de Serviço, Ofertas, Bônus, Promoções": 7,
    "Qualidade, Funcionamento e Reparo": 8,
    "Ressarcimento": 9
}
index_to_label = {v: k for k, v in label_to_index.items()}

# Função para prever o tipo de reclamação
def predict_tipo_reclamacao(mensagem):
    inputs = tokenizer(mensagem, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)
    predicted_label = torch.argmax(probs, dim=1).item()
    return predicted_label, probs

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    local = request.form['local']
    idade = request.form['idade']
    tipo_reclamacao_esperado = request.form['tipo_reclamacao']
    mensagem_usuario = request.form['mensagem']

    # Prever o tipo de reclamação e obter as probabilidades
    predicted_label, probs = predict_tipo_reclamacao(mensagem_usuario)

    # Inserir os dados no banco de dados
    connection = sqlite3.connect('reclamacoes.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO reclamacoes (nome, local, idade, tipo_reclamacao, mensagem)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, local, idade, tipo_reclamacao_esperado, mensagem_usuario))  # Usar o tipo de reclamação esperado
    connection.commit()
    connection.close()

    # Verificar se a pessoa escolheu o tipo de reclamação correta
    if tipo_reclamacao_esperado == index_to_label[predicted_label]:
        confirmation_message = {'title': 'Reclamação Enviada', 'message': 'Parabéns! Você escolheu o tipo de reclamação correta.'}
    else:
        # Obter o tipo de reclamação correto
        correct_label = index_to_label[predicted_label]

        # Obter a porcentagem da classe correta
        percentage_correct = probs[0, predicted_label].item() * 100

        confirmation_message = {'title': 'Erro na Reclamação', 'message': f'Ops! Parece que houve um erro na escolha do tipo de reclamação. O tipo correto era {correct_label} com {percentage_correct:.2f}% de certeza. Por favor, tente novamente.'}

    return render_template('confirmation.html', confirmation_message=confirmation_message)


if __name__ == '__main__':
    app.run(debug=True)
