from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import re
import requests
import os

app = Flask(__name__)


# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Oct081098#@localhost/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/criar_tabelas')
def criar_tabelas():
    db.create_all()
    return "Tabelas criadas com sucesso!"

# Definição dos modelos do banco de dados
class Cliente(db.Model):
    __tablename__ = 'clientes'
    CNPJ = db.Column(db.String, primary_key=True)
    Primeiro_Nome = db.Column(db.String)
    Segundo_Nome = db.Column(db.String)
    Email = db.Column(db.String)
    Telefone = db.Column(db.String)
    Estado = db.Column(db.String)
    Cidade = db.Column(db.String)
    Bairro = db.Column(db.String)
    Rua = db.Column(db.String)
    Numero = db.Column(db.String)

class Obra(db.Model):
    __tablename__ = 'obras'
    OS = db.Column(db.String, primary_key=True)
    Primeiro_Nome_Contato = db.Column(db.String)
    Segundo_Nome_Contato = db.Column(db.String)
    Valor = db.Column(db.Float)
    Estado_Obra = db.Column(db.String)
    Cidade_Obra = db.Column(db.String)
    Bairro_Obra = db.Column(db.String)
    Rua_Obra = db.Column(db.String)
    Numero_Obra = db.Column(db.String)
    CNPJ_Cliente = db.Column(db.String, db.ForeignKey('clientes.CNPJ'), nullable=False)

class Compra(db.Model):
    __tablename__ = 'compras'
    Ordem_de_Compras = db.Column(db.String, primary_key=True)
    Obra_OS = db.Column(db.String, db.ForeignKey('obras.OS'), nullable=False)
    Materia_prima = db.Column(db.String)
    Consumiveis = db.Column(db.String)
    Miscelanea = db.Column(db.String)

# Função para remover a formatação de moeda do valor antes de salvar no banco
def formatar_valor(valor):
    # Remove "R$", espaços e troca vírgula por ponto
    valor_formatado = re.sub(r'[R$\s]', '', valor)  # Remove "R$", espaços
    valor_formatado = valor_formatado.replace('.', '').replace(',', '.')
    return float(valor_formatado)

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Dados do Cliente
        cnpj = request.form['cnpj']
        primeiro_nome = request.form['primeiro_nome']
        segundo_nome = request.form['segundo_nome']
        email = request.form['email']
        telefone = request.form['telefone']
        estado = request.form['estado']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        rua = request.form['rua']
        numero = request.form['numero']

        # Dados da Obra
        os = request.form['os']
        primeiro_nome_contato = request.form['primeiro_nome_contato']
        segundo_nome_contato = request.form['segundo_nome_contato']
        valor = request.form['valor']  # Valor com formatação "R$"
        estado_obra = request.form['estado_obra']
        cidade_obra = request.form['cidade_obra']
        bairro_obra = request.form['bairro_obra']
        rua_obra = request.form['rua_obra']
        numero_obra = request.form['numero_obra']

        # Dados da Compra
        ordem_compra = request.form['ordem_compra']  # Captura da ordem de compra
        materia_prima = request.form['materia_prima']
        consumiveis = request.form['consumiveis']
        miscelanea = request.form['miscelanea']

        # Formata o valor da obra para formato numérico
        valor_formatado = formatar_valor(valor)

        try:
            # Verifica se o cliente já existe
            cliente_existente = Cliente.query.filter_by(CNPJ=cnpj).first()

            # Se o cliente não existir, cria um novo
            if not cliente_existente:
                novo_cliente = Cliente(CNPJ=cnpj, Primeiro_Nome=primeiro_nome, Segundo_Nome=segundo_nome,
                                       Email=email, Telefone=telefone, Estado=estado, Cidade=cidade,
                                       Bairro=bairro, Rua=rua, Numero=numero)
                db.session.add(novo_cliente)
            else:
                # Atualiza os dados do cliente, se necessário
                cliente_existente.Estado = estado
                cliente_existente.Cidade = cidade
                # Pode-se atualizar outros campos aqui se necessário

            db.session.commit()  # Confirma a inserção ou atualização do cliente

            # Cadastra a obra
            nova_obra = Obra(OS=os, Primeiro_Nome_Contato=primeiro_nome_contato,
                             Segundo_Nome_Contato=segundo_nome_contato,
                             Valor=valor_formatado, Estado_Obra=estado_obra, Cidade_Obra=cidade_obra,
                             Bairro_Obra=bairro_obra, Rua_Obra=rua_obra, Numero_Obra=numero_obra, CNPJ_Cliente=cnpj)
            db.session.add(nova_obra)
            db.session.commit()  # Confirma a inserção da obra

            # Cadastra a compra vinculada à obra
            nova_compra = Compra(Obra_OS=os, Ordem_de_Compras=ordem_compra, Materia_prima=materia_prima,
                                 Consumiveis=consumiveis, Miscelanea=miscelanea)
            db.session.add(nova_compra)
            db.session.commit()  # Confirma a inserção da compra

            return redirect(url_for('cadastro'))
        except Exception as e:
            db.session.rollback()  # Desfaz as alterações em caso de erro
            return f"Ocorreu um erro: {str(e)}"

    return render_template('cadastro.html')

# Rota para a página de consulta
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        cnpj = request.form['cnpj']  # O CNPJ é recebido com pontuação
        os = request.form['os']  # A OS informada pelo usuário

        print(f"CNPJ recebido: {cnpj}")  # Verifica o CNPJ recebido no backend

        # Busca o cliente pelo CNPJ
        cliente = Cliente.query.filter_by(CNPJ=cnpj).first()
        print(f"Resultado da consulta (cliente): {cliente}")  # Verifica o resultado da busca no banco

        # Se o cliente for encontrado, busca as obras associadas ao CNPJ
        obras = []
        compras = {}
        if cliente:
            if os:
                # Se a OS for informada, filtra obras pela OS
                obras = Obra.query.filter_by(OS=os, CNPJ_Cliente=cnpj).all()
                print(f"Resultado da consulta (obras para a OS): {obras}")  # Verifica as obras relacionadas à OS
                # Busca compras relacionadas apenas às obras filtradas
                for obra in obras:
                    obra_compras = Compra.query.filter_by(Obra_OS=obra.OS).all()
                    if obra_compras:
                        compras[obra.OS] = obra_compras  # Agrupa compras por OS
            else:
                # Se não houver OS, busca todas as obras do cliente
                obras = Obra.query.filter_by(CNPJ_Cliente=cnpj).all()
                print(f"Resultado da consulta (todas as obras): {obras}")  # Verifica todas as obras

                # Busca compras relacionadas a todas as obras do CNPJ
                for obra in obras:
                    obra_compras = Compra.query.filter_by(Obra_OS=obra.OS).all()
                    if obra_compras:
                        compras[obra.OS] = obra_compras  # Agrupa compras por OS

            return render_template('consulta.html', cliente=cliente, obras=obras, compras=compras)
        else:
            return render_template('consulta.html', mensagem='Cliente não encontrado')

    return render_template('consulta.html')

# Função para limpar todas as tabelas do banco de dados
def limpar_banco():
    db.session.query(Compra).delete()
    db.session.query(Obra).delete()
    db.session.query(Cliente).delete()
    db.session.commit()

# Rota para limpar o banco de dados
@app.route('/limpar_banco')
def limpar():
    limpar_banco()
    return 'Banco de dados limpo com sucesso.'

# Rota para verificar se o CNPJ já está cadastrado
@app.route('/verificar_cnpj')
def verificar_cnpj():
    cnpj = request.args.get('cnpj').strip()  # CNPJ com máscara
    cliente = Cliente.query.filter_by(CNPJ=cnpj).first()  # Busca pelo CNPJ com máscara

    if cliente:
        return jsonify({
            'cadastrado': True,
            'primeiro_nome': cliente.Primeiro_Nome,
            'segundo_nome': cliente.Segundo_Nome,
            'email': cliente.Email,
            'telefone': cliente.Telefone,
            'estado': cliente.Estado,
            'cidade': cliente.Cidade,
            'bairro': cliente.Bairro,
            'rua': cliente.Rua,
            'numero': cliente.Numero
        })
    else:
        return jsonify({'cadastrado': False})




    # API's
    @app.route('/api/consulta-obra/<cnpj>', methods=['GET'])
    def consulta_obra(cnpj):
        # Remover caracteres especiais do CNPJ (como pontos, barras e traços)
        cnpj = re.sub(r'\D', '', cnpj)

        # Procurar o cliente pelo CNPJ
        cliente = Cliente.query.filter_by(CNPJ=cnpj).first()

        if not cliente:
            return jsonify({"error": "CNPJ não encontrado"}), 404

        # Procurar as obras associadas ao cliente
        obras = Obra.query.filter_by(CNPJ_Cliente=cnpj).all()

        if not obras:
            return jsonify({"error": "Nenhuma obra encontrada para este cliente"}), 404

        # Estrutura para armazenar a resposta
        resultado = {
            "cliente": {
                "CNPJ": cliente.CNPJ,
                "nome": f"{cliente.Primeiro_Nome} {cliente.Segundo_Nome}",
                "email": cliente.Email,
                "telefone": cliente.Telefone
            },
            "obras": []
        }

        # Adicionar os dados das obras e itens utilizados
        for obra in obras:
            # Buscar compras relacionadas à obra
            compras = Compra.query.filter_by(Obra_OS=obra.OS).first()

            obra_info = {
                "os": obra.OS,
                "valor": obra.Valor,
                "endereco": {
                    "rua": obra.Rua_Obra,
                    "bairro": obra.Bairro_Obra,
                    "numero": obra.Numero_Obra,
                    "cidade": obra.Cidade_Obra,
                    "estado": obra.Estado_Obra
                },
                "itens_utilizados": {
                    "materia_prima": compras.Materia_prima if compras else "",
                    "consumiveis": compras.Consumiveis if compras else "",
                    "miscelanea": compras.Miscelanea if compras else ""
                }
            }

            resultado["obras"].append(obra_info)

        return jsonify(resultado)

# API mapa

# Função auxiliar para obter coordenadas
# Função para obter coordenadas de um endereço usando Nominatim
# Função auxiliar para obter coordenadas


def obter_coordenadas(endereco):
    # Faz a requisição à API Nominatim
    response = requests.get(
        'https://nominatim.openstreetmap.org/search',
        params={'q': endereco, 'format': 'json', 'countrycodes': 'BR', 'bounded': 1}
    )

    # Verifica o código de status da resposta
    print("Response status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code != 200:
        print(f"Erro ao buscar coordenadas: {response.status_code} - {response.text}")
        return None, None, False  # Retorna também um indicador de sucesso

    # Tenta decodificar a resposta como JSON
    try:
        coordenadas = response.json()
    except ValueError:
        print(f"Erro ao decodificar JSON: {response.text}")
        return None, None, False  # Retorna também um indicador de sucesso

    # Verifica se a resposta contém coordenadas
    if coordenadas:
        lat, lon = coordenadas[0].get('lat'), coordenadas[0].get('lon')
        if lat and lon:
            return lat, lon, True  # Retorna as coordenadas e um indicador de sucesso

    # Se não houver coordenadas, retorna None
    print(f"Coordenadas não encontradas para o endereço: {endereco}")
    return None, None, False  # Retorna também um indicador de sucesso

# Função para formatar CNPJ
def formatar_cnpj(cnpj):
    # Formatar o CNPJ para o padrão com pontuação: "12.345.678/0001-90"
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


# Rota para buscar localização do cliente e obras
@app.route('/localizacao/<cnpj>', methods=['GET'])
def obter_localizacoes(cnpj):
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    cnpj_formatado = formatar_cnpj(cnpj_limpo)

    # Buscar o cliente
    cliente = Cliente.query.filter_by(CNPJ=cnpj_formatado).first()
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    # Montar endereço do cliente
    endereco_cliente = f"{cliente.Rua}, {cliente.Numero}, {cliente.Bairro}, {cliente.Cidade}, {cliente.Estado}, Brasil"
    print("Endereço do cliente:", endereco_cliente)
    lat_cliente, lon_cliente, sucesso_cliente = obter_coordenadas(endereco_cliente)

    if not sucesso_cliente:
        mensagem_api = "API Nominatim não está retornando, tente mais tarde"
        return render_template('map.html', cliente=None, obras=[], mensagem_api=mensagem_api)

    localizacao_cliente = {
        'tipo': 'cliente',
        'endereco': endereco_cliente,
        'latitude': lat_cliente,
        'longitude': lon_cliente
    }

    # Buscar todas as obras associadas ao cliente
    obras = Obra.query.filter_by(CNPJ_Cliente=cliente.CNPJ).all()
    localizacoes_obras = []
    obras_nao_carregadas = []  # Lista de obras que não foram carregadas

    for obra in obras:
        endereco_obra = f"{obra.Rua_Obra}, {obra.Numero_Obra}, {obra.Bairro_Obra}, {obra.Cidade_Obra}, {obra.Estado_Obra}, Brasil"
        print("Endereço da obra:", endereco_obra)

        lat_obra, lon_obra, sucesso_obra = obter_coordenadas(endereco_obra)
        if sucesso_obra:
            localizacoes_obras.append({
                'tipo': 'obra',
                'os': obra.OS,
                'endereco': endereco_obra,
                'latitude': lat_obra,
                'longitude': lon_obra
            })
        else:
            # Adiciona na lista de obras não carregadas
            obras_nao_carregadas.append(obra.OS)

    return render_template(
        'map.html',
        cliente=localizacao_cliente,
        obras=localizacoes_obras,
        obras_nao_carregadas=obras_nao_carregadas  # Passa a lista de obras com falha na API
    )

#Análise de Dados

@app.route('/analise_dados', methods=['GET', 'POST'])
def analise_dados():
    # Inicializa listas vazias
    numero_os = []
    valores = []

    if request.method == 'POST':
        cnpj = request.form['cnpj']  # Mantém o CNPJ com pontuação

        print(f"CNPJ recebido: {cnpj}")

        # Consulta SQLAlchemy para buscar obras pelo CNPJ do cliente
        obras = Obra.query.filter_by(CNPJ_Cliente=cnpj).all()  # Usa o CNPJ com pontuação

        # Extraindo dados para o gráfico, se houver obras
        if obras:
            numero_os = [obra.OS for obra in obras]
            valores = [obra.Valor for obra in obras]

        return render_template(
            'analise.html',
            numero_os=numero_os,
            valores=valores,
            cnpj=cnpj  # Passa o CNPJ formatado
        )

    return render_template('analise.html', numero_os=numero_os, valores=valores)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no PostgreSQL
    app.run(debug=True)






