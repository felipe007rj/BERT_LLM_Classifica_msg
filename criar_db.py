import sqlite3
from faker import Faker
import random

fake = Faker()

def create_table():
    connection = sqlite3.connect('reclamacoes.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reclamacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            local TEXT,
            idade INTEGER,
            tipo_reclamacao TEXT,
            mensagem TEXT
        )
    ''')
    connection.commit()
    connection.close()

def generate_message(tipo_reclamacao):
    dicionario = {
        "Atendimento": [
            "O atendimento foi péssimo! Não resolveram meu problema e fui tratado com descaso.",
            "O atendimento prestado deixou muito a desejar. Esperava mais consideração e suporte.",
            "Não obtive a ajuda necessária do suporte. Fiquei bastante insatisfeito com o atendimento.",
            "O suporte ao cliente foi ineficaz. Minha questão não foi resolvida de maneira satisfatória.",
            "Fui transferido para vários setores e ainda não obtive a solução para meu problema.",
            "O atendimento telefônico demorou muito e não resolveu minha situação.",
            "Esperava mais eficiência no atendimento. Infelizmente, minha questão persiste.",
            "O atendimento ao cliente deixou a desejar. Não me senti valorizado como cliente.",
            "Precisei esperar muito tempo para ser atendido. Isso é inaceitável.",
            "A equipe de suporte não foi capaz de resolver meu problema. Estou insatisfeito."
        ],
        "Bloqueio, Desbloqueio ou Suspensão": [
            "Meu celular foi bloqueado sem aviso prévio. Isso é inaceitável e prejudica minha rotina.",
            "Meu número foi bloqueado sem motivo. Isso está prejudicando minhas comunicações.",
            "Não consigo fazer chamadas devido ao bloqueio do meu número. Preciso de uma solução imediata.",
            "Estou incomunicável devido ao bloqueio do meu telefone. Isso é um transtorno.",
            "Meu chip foi bloqueado sem explicação. Exijo esclarecimentos e a resolução do problema.",
            "O bloqueio do meu número foi injustificado. Quero uma explicação e a retificação imediata.",
            "Fui surpreendido com o bloqueio do meu chip. Isso está causando muitos problemas.",
            "Minha linha foi bloqueada e não recebi nenhuma notificação prévia. Isso é inadmissível.",
            "Estou enfrentando dificuldades devido ao bloqueio do meu número. Preciso de assistência urgente.",
            "Meu telefone foi bloqueado sem motivo aparente. Quero uma solução rápida para essa situação."
        ],
        "Cancelamento": [
            "Ao tentar cancelar meu plano, fui transferido para diferentes setores, sem sucesso. Péssima experiência.",
            "Tentei cancelar o plano, mas fui transferido para diversos setores sem sucesso. Isso é um descaso.",
            "Não consigo cancelar meu serviço, mesmo após várias tentativas. Estou frustrado.",
            "Estou insatisfeito com o processo de cancelamento. Fui mal atendido e não obtive sucesso.",
            "O cancelamento do meu plano está sendo uma verdadeira dor de cabeça. Preciso de ajuda.",
            "Após solicitar o cancelamento, continuo recebendo faturas. Isso é inaceitável.",
            "Minha solicitação de cancelamento não foi processada corretamente. Estou bastante chateado.",
            "Estou enfrentando dificuldades para cancelar meu plano. A empresa precisa resolver isso.",
            "Ao solicitar o cancelamento, fui informado de taxas adicionais. Isso não foi previamente mencionado.",
            "O processo de cancelamento é burocrático e demorado. Isso é frustrante."
        ],
        "Cobrança": [
            "Recebi uma cobrança indevida e não consigo obter esclarecimentos. Preciso resolver isso urgentemente.",
            "Recebi uma cobrança adicional sem explicação. Absurdo.",
            "A fatura deste mês veio com um valor incorreto. Preciso de uma correção imediata.",
            "Fui surpreendido com uma cobrança não autorizada em minha conta. Isso é inaceitável.",
            "Estou questionando uma cobrança duplicada em minha fatura. Preciso de uma análise rápida.",
            "A cobrança deste mês está muito acima do esperado. Preciso entender os motivos.",
            "Não compreendo alguns itens na minha fatura. Gostaria de uma explicação detalhada.",
            "Minha fatura está incorreta, com serviços não contratados sendo cobrados. Isso precisa ser corrigido.",
            "Fui cobrado por um serviço que cancelei. Preciso de uma restituição.",
            "Não reconheço uma transação na minha fatura. Preciso de esclarecimentos urgentes."
        ],
        "Dados Cadastrais": [
            "Meus dados cadastrais estão incorretos, impactando o acesso aos serviços. Exijo uma solução imediata.",
            "Meus dados cadastrais foram alterados erroneamente. Preciso de correção.",
            "Ao acessar minha conta, percebi que alguns dados estão incorretos. Favor corrigir.",
            "As informações cadastrais em minha conta estão desatualizadas. Como posso atualizá-las?",
            "Recebi notificações sobre mudanças em meus dados cadastrais que não foram feitas por mim. Estou preocupado.",
            "Não consigo acessar minha conta devido a problemas nos dados cadastrais. Ajuda urgente é necessária.",
            "Ao tentar alterar meus dados, encontrei dificuldades no sistema. Isso precisa ser corrigido.",
            "Os dados cadastrais em minha conta estão desatualizados. Preciso corrigir essa situação.",
            "As alterações recentes em meus dados cadastrais não foram refletidas na minha conta. Favor corrigir.",
            "Estou enfrentando problemas devido a dados cadastrais incorretos. Preciso de assistência para resolver."
        ],
        "Instalação, Ativação ou Habilitação": [
            "A instalação do serviço foi um desastre. A conexão é instável e não atende às minhas necessidades.",
            "A instalação do serviço foi malfeita. Conexão instável e de baixa qualidade.",
            "Enfrentei problemas durante a instalação do serviço. A qualidade está abaixo do esperado.",
            "Após a ativação do serviço, percebi falhas na conexão. Isso precisa ser corrigido.",
            "Meu serviço foi ativado, mas a qualidade da conexão é péssima. Preciso de suporte técnico.",
            "Estou insatisfeito com o processo de ativação do serviço. Preciso de uma solução rápida.",
            "Ao habilitar meu dispositivo, enfrentei dificuldades técnicas. A empresa precisa resolver isso.",
            "A ativação do serviço não foi concluída com sucesso. Estou sem comunicação.",
            "Estou tendo problemas após a ativação do serviço. A conexão é intermitente.",
            "Após a habilitação do serviço, minha experiência tem sido frustrante. Preciso de assistência técnica."
        ],
        "Mudança de Endereço": [
            "Mudei de endereço, mas o serviço ainda está vinculado à minha residência anterior. Isso é inaceitável.",
            "Após mudar de endereço, meu serviço continua vinculado ao local anterior. Isso é um transtorno.",
            "Atualizei meu endereço, mas o serviço não foi transferido corretamente. Preciso resolver isso.",
            "Estou enfrentando dificuldades após a mudança de endereço. O serviço não está funcionando adequadamente.",
            "Ao mudar de endereço, fui informado de que o serviço seria transferido, mas isso não aconteceu.",
            "Mudei de residência e estou sem serviço devido a problemas na transferência. Ajuda é necessária.",
            "Após a mudança, meu serviço foi interrompido. Isso está causando inconvenientes.",
            "Não consigo usar os serviços no novo endereço. A mudança de endereço não foi efetivada.",
            "O serviço não está disponível no meu novo endereço após a mudança. Isso precisa ser resolvido.",
            "Estou sem comunicação após a mudança de endereço. A transferência do serviço não foi concluída."
        ],
        "Plano de Serviço, Ofertas, Bônus, Promoções": [
            "Não estou recebendo as promoções anunciadas. Isso é uma quebra de contrato e expectativas.",
            "As promoções anunciadas não foram aplicadas à minha conta. Isso é propaganda enganosa.",
            "Meu plano não está incluindo os bônus e ofertas prometidos. Estou desapontado.",
            "As promoções que me foram oferecidas não foram ativadas em minha conta. Como resolver isso?",
            "Estou insatisfeito com as ofertas do meu plano. Não correspondem ao que foi anunciado.",
            "Ao aderir a uma promoção, não recebi os benefícios prometidos. Preciso de esclarecimentos.",
            "Minha conta não reflete as promoções que aceitei. Isso está impactando minha satisfação como cliente.",
            "Não recebi os bônus prometidos ao contratar o serviço. Isso é frustrante.",
            "As ofertas e promoções que me foram apresentadas não estão sendo aplicadas ao meu contrato.",
            "Fui atraído por ofertas especiais, mas não estou desfrutando dos benefícios anunciados. Ajuda é necessária."
        ],
        "Qualidade, Funcionamento e Reparo": [
            "A qualidade do serviço é péssima, e os reparos feitos até agora não resolveram o problema.",
            "A qualidade do sinal é péssima. Tentativas de reparo não surtiram efeito.",
            "Enfrentei problemas de qualidade no serviço, mesmo após tentativas de reparo.",
            "Meu serviço está com falhas constantes, apesar das tentativas de reparo. Estou insatisfeito.",
            "Os reparos realizados não solucionaram os problemas de qualidade do serviço.",
            "Após as tentativas de reparo, a qualidade do serviço não melhorou. Estou descontente.",
            "O funcionamento do serviço está abaixo do esperado, mesmo após intervenções para reparo.",
            "Estou tendo problemas constantes no funcionamento do serviço, mesmo após solicitar reparos.",
            "Os reparos feitos no meu serviço não foram eficazes. A qualidade continua comprometida.",
            "Estou enfrentando dificuldades devido à baixa qualidade do serviço. Preciso de uma solução imediata."
        ],
        "Ressarcimento": [
            "Fiquei sem serviço por um período significativo. Exijo um ressarcimento pelos transtornos causados.",
            "Experimentei uma longa interrupção no serviço. Quero ser ressarcido.",
            "O serviço ficou fora do ar, e isso impactou minhas atividades. Preciso de compensação.",
            "Estou solicitando o ressarcimento devido à falta de serviço durante um período prolongado.",
            "Fui prejudicado financeiramente devido à interrupção prolongada do serviço. Quero compensação.",
            "O serviço não foi restaurado dentro do prazo prometido. Exijo compensação pelos prejuízos.",
            "Estou insatisfeito com a demora na resolução do problema. Preciso de ressarcimento.",
            "A interrupção do serviço causou inconvenientes significativos. Quero ser ressarcido.",
            "Perdi oportunidades devido à interrupção do serviço. Estou buscando compensação.",
            "Estou enfrentando prejuízos financeiros devido à falta de serviço. Exijo ressarcimento."
        ]
    }
    
    return random.choice(dicionario[tipo_reclamacao])

def insert_fake_data():
    create_table()

    connection = sqlite3.connect('reclamacoes.db')
    cursor = connection.cursor()

    for _ in range(100):
        nome = fake.name()
        local = fake.city()
        idade = random.randint(18, 60)
        tipo_reclamacao = random.choice([
            "Atendimento",
            "Bloqueio, Desbloqueio ou Suspensão",
            "Cancelamento",
            "Cobrança",
            "Dados Cadastrais",
            "Instalação, Ativação ou Habilitação",
            "Mudança de Endereço",
            "Plano de Serviço, Ofertas, Bônus, Promoções",
            "Qualidade, Funcionamento e Reparo",
            "Ressarcimento"
        ])
        mensagem = generate_message(tipo_reclamacao)

        cursor.execute('''
            INSERT INTO reclamacoes (nome, local, idade, tipo_reclamacao, mensagem)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, local, idade, tipo_reclamacao, mensagem))

    connection.commit()
    connection.close()


insert_fake_data()
