from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from datetime import date
import mysql.connector


def inserir():
    '''função para capturar os dados da tela de cadastro'''
    nome = formulario.txtNome.text()
    endereco = formulario.txtEndereco.text()
    telefone = formulario.txtTelefone.text()
    tipo_servico = formulario.txtTipoServico.text()
    status_servico = formulario.comboBoxStatus.currentText()

    # Validação para garantir que os campos não estão vazios
    if not nome or not endereco or not telefone or not tipo_servico:
        formulario.lblMsg.setText('Por favor, preencha todos os campos.')
        return

    data_cadastro = date.today()  # Captura a data atual

    formulario.lblMsg.setText('Dados cadastrados com sucesso')

    # Conexão e inserção no banco de dados
    cursor = conexao.cursor()
    comando_SQL = '''
    INSERT INTO pessoas (nome, endereco, telefone, tipo_servico, data_cadastro, status_servico)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    valores = (nome, endereco, telefone, tipo_servico, data_cadastro, status_servico)

    cursor.execute(comando_SQL, valores)
    conexao.commit()

    # Limpar os campos após o cadastro
    formulario.txtNome.setText('')
    formulario.txtEndereco.setText('')
    formulario.txtTelefone.setText('')
    formulario.txtTipoServico.setText('')
    formulario.comboBoxStatus.setCurrentIndex(0)


def lista_relatorio():
    '''Mostra o relatório de cadastro de pessoas, ordenado por mais recente'''
    lista.show()
    cursor = conexao.cursor()

    # Consulta SQL com ordenação decrescente pela data de cadastro
    comando_SQL = '''
    SELECT nome, endereco, telefone, tipo_servico, data_cadastro, status_servico
    FROM pessoas
    ORDER BY data_cadastro DESC
    '''
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    # Configurar o número de linhas e colunas na tabela
    lista.tableWidget.setRowCount(len(leitura_banco))  # Quantidade de registros (linhas)
    lista.tableWidget.setColumnCount(6)  # Número de colunas a exibir (nome, endereço, telefone, tipo de serviço, data, status)

    # Preencher a tabela com os dados do banco
    for L in range(len(leitura_banco)):
        for C in range(6):
            lista.tableWidget.setItem(L, C, QTableWidgetItem(str(leitura_banco[L][C])))


id_atual = int

def excluir():
    '''Função para excluir uma pessoa da lista'''
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM pessoas')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[remover][0]  # Pega o ID da linha selecionada
    comando_SQL = f'DELETE FROM pessoas WHERE ID = "{(valor_id)}"'
    cursor.execute(comando_SQL)
    conexao.commit()

def edit():
    '''Função para carregar os dados de uma pessoa para edição'''
    editar.show()
    global id_atual
    dados = lista.tableWidget.currentRow()
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM pessoas')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[dados][0]
    comando_SQL = f'SELECT * FROM pessoas WHERE ID = "{valor_id}"'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    id_atual = valor_id  # Armazena o ID atual para atualização
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarNome.setText(leitura_banco[0][1])
    editar.txtAlterarEndereco.setText(leitura_banco[0][2])
    editar.txtAlterarTelefone.setText(leitura_banco[0][3])
    editar.txtAlterarTipoServico.setText(leitura_banco[0][4])

def salvar_dados():
    '''Função para salvar as alterações de uma pessoa editada'''
    global id_atual

    id = int(editar.txtAlterarId.text())
    nome = editar.txtAlterarNome.text()
    endereco = editar.txtAlterarEndereco.text()
    telefone = editar.txtAlterarTelefone.text()
    tipo_servico = editar.txtAlterarTipoServico.text()

    cursor = conexao.cursor()
    sql = "UPDATE pessoas SET id = %s, nome = %s, endereco = %s, telefone = %s, tipo_servico = %s WHERE id = %s;"
    valores = (id, nome, endereco, telefone, tipo_servico, id)

    cursor.execute(sql, valores)
    conexao.commit()

    editar.close()  # Fecha a janela de edição
    lista.close()  # Fecha a janela de lista
    formulario.show()  # Volta para o formulário principal

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="dev",
    password="1234",
    database="cadastro_pessoas"
)

# Inicializa o aplicativo PyQt5
app = QtWidgets.QApplication([])

# Carrega as interfaces do UI
formulario = uic.loadUi('formulario.ui')
formulario.btnCadastrar.clicked.connect(inserir)  # Conecta o botão de cadastrar à função inserir
formulario.btnRelatorio.clicked.connect(lista_relatorio)  # Conecta o botão de relatório à função lista_relatorio

lista = uic.loadUi('lista.ui')
lista.btnAlterarRegistro.clicked.connect(edit)  # Conecta o botão de alterar à função edit
lista.btnApagarRegistro.clicked.connect(excluir)  # Conecta o botão de excluir à função excluir

editar = uic.loadUi('editar.ui')
editar.btnConfirmarAlteracao.clicked.connect(salvar_dados)  # Conecta o botão de salvar à função salvar_dados

# Exibe a janela principal de cadastro
formulario.show()
app.exec()
