from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from datetime import date
import mysql.connector

# Funções de Usuário
def cadastrar_primeiro_usuario():
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    resultado = cursor.fetchone()

    if resultado[0] == 0:
        nome = 'admin'
        email = 'admin@admin.com'
        senha = 'admin'
        tipo_usuario = 'administrador'

        comando_SQL = '''INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)'''
        valores = (nome, email, senha, tipo_usuario)

        cursor.execute(comando_SQL, valores)
        conexao.commit()
        loginWindow.show()
    else:
        loginWindow.show()


def login():
    global tipo_usuario  # Declare a variável como global
    nome_usuario = loginWindow.txtNomeLogin.text()
    senha_usuario = loginWindow.txtSenhaLogin.text()

    if not nome_usuario or not senha_usuario:
        loginWindow.lblMsg.setText("Por favor, preencha todos os campos.")
        return

    cursor = conexao.cursor()
    comando_SQL = "SELECT id, nome, tipo_usuario FROM usuarios WHERE nome = %s AND senha = %s"
    valores = (nome_usuario, senha_usuario)
    cursor.execute(comando_SQL, valores)
    resultado = cursor.fetchone()

    if resultado:
        global id_usuario_logado
        id_usuario_logado = resultado[0]
        tipo_usuario = resultado[2]

        loginWindow.close()
        formulario.show()
        usuarios.show()  # Abre a janela de usuários
        formulario.lblMsg.setText(f"Bem-vindo, {resultado[1]} ({tipo_usuario})!")
    else:
        loginWindow.lblMsg.setText("Nome de usuário ou senha incorretos.")





def inserir_usuario():
    # Verifica se o usuário logado é um administrador
    if id_usuario_logado and tipo_usuario == 'administrador':
        nome = usuarios.txtNomeUsuario.text()
        email = usuarios.txtEmailUsuario.text()
        senha = usuarios.txtSenhaUsuario.text()
        tipo_usuario_novo = usuarios.comboBoxTipoUsuario.currentText()

        # Validação para garantir que os campos não estão vazios
        if not nome or not email or not senha or not tipo_usuario_novo:
            usuarios.lblMsg.setText('Por favor, preencha todos os campos.')
            return

        cursor = conexao.cursor()
        comando_SQL = '''
        INSERT INTO usuarios (nome, email, senha, tipo_usuario)
        VALUES (%s, %s, %s, %s)
        '''
        valores = (nome, email, senha, tipo_usuario_novo)
        cursor.execute(comando_SQL, valores)
        conexao.commit()

        usuarios.lblMsg.setText('Usuário cadastrado com sucesso!')
        usuarios.txtNomeUsuario.setText('')
        usuarios.txtEmailUsuario.setText('')
        usuarios.txtSenhaUsuario.setText('')
        usuarios.comboBoxTipoUsuario.setCurrentIndex(0)
    else:
        usuarios.lblMsg.setText('Apenas administradores podem cadastrar usuários.')


def excluir_usuario():
    # Verifica se o usuário logado é um administrador
    if id_usuario_logado and tipo_usuario == 'administrador':
        remover = usuarios.tableWidget.currentRow()
        usuarios.tableWidget.removeRow(remover)

        cursor = conexao.cursor()
        cursor.execute('SELECT id FROM usuarios')
        leitura_banco = cursor.fetchall()
        valor_id = leitura_banco[remover][0]
        comando_SQL = f'DELETE FROM usuarios WHERE id = "{valor_id}"'
        cursor.execute(comando_SQL)
        conexao.commit()
        usuarios.lblMsg.setText('Usuário excluído com sucesso!')
    else:
        usuarios.lblMsg.setText('Apenas administradores podem excluir usuários.')


def listar_usuarios():
    usuarios.show()
    cursor = conexao.cursor()

    # Atualize a consulta para não incluir a coluna de ID
    comando_SQL = 'SELECT nome, email, tipo_usuario FROM usuarios'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    # Atualize o número de colunas para 3 (sem o ID)
    usuarios.tableWidget.setRowCount(len(leitura_banco))
    usuarios.tableWidget.setColumnCount(3)  # nome, email, tipo_usuario

    for L in range(len(leitura_banco)):
        for C in range(3):  # Agora iteramos apenas sobre 3 colunas
            usuarios.tableWidget.setItem(L, C, QTableWidgetItem(str(leitura_banco[L][C])))



# Funções de Cadastro de Pessoas
def inserir():
    nome = formulario.txtNome.text()
    endereco = formulario.txtEndereco.text()
    telefone = formulario.txtTelefone.text()
    tipo_servico = formulario.txtTipoServico.text()
    status_servico = formulario.comboBoxStatus.currentText()

    if not nome or not endereco or not telefone or not tipo_servico:
        formulario.lblMsg.setText('Por favor, preencha todos os campos.')
        return

    data_cadastro = date.today()

    cursor = conexao.cursor()
    comando_SQL = '''
    INSERT INTO pessoas (nome, endereco, telefone, tipo_servico, data_cadastro, status_servico, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    valores = (nome, endereco, telefone, tipo_servico, data_cadastro, status_servico, id_usuario_logado)

    cursor.execute(comando_SQL, valores)
    conexao.commit()

    formulario.lblMsg.setText('Dados cadastrados com sucesso!')
    formulario.txtNome.setText('')
    formulario.txtEndereco.setText('')
    formulario.txtTelefone.setText('')
    formulario.txtTipoServico.setText('')
    formulario.comboBoxStatus.setCurrentIndex(0)

def lista_relatorio():
    lista.show()
    cursor = conexao.cursor()

    comando_SQL = '''
    SELECT p.nome, p.endereco, p.telefone, p.tipo_servico, p.data_cadastro, p.status_servico, u.nome AS nome_usuario
    FROM pessoas p
    JOIN usuarios u ON p.id_usuario = u.id
    ORDER BY p.data_cadastro DESC
    '''
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    lista.tableWidget.setRowCount(len(leitura_banco))
    lista.tableWidget.setColumnCount(7)

    for L in range(len(leitura_banco)):
        for C in range(7):
            lista.tableWidget.setItem(L, C, QTableWidgetItem(str(leitura_banco[L][C])))

def excluir():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM pessoas')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[remover][0]
    comando_SQL = f'DELETE FROM pessoas WHERE ID = "{valor_id}"'
    cursor.execute(comando_SQL)
    conexao.commit()

def edit():
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

    id_atual = valor_id
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarNome.setText(leitura_banco[0][1])
    editar.txtAlterarEndereco.setText(leitura_banco[0][2])
    editar.txtAlterarTelefone.setText(leitura_banco[0][3])
    editar.txtAlterarTipoServico.setText(leitura_banco[0][4])

def salvar_dados():
    global id_atual

    id = int(editar.txtAlterarId.text())
    nome = editar.txtAlterarNome.text()
    endereco = editar.txtAlterarEndereco.text()
    telefone = editar.txtAlterarTelefone.text()
    tipo_servico = editar.txtAlterarTipoServico.text()

    cursor = conexao.cursor()
    sql = "UPDATE pessoas SET nome = %s, endereco = %s, telefone = %s, tipo_servico = %s WHERE id = %s;"
    valores = (nome, endereco, telefone, tipo_servico, id)

    cursor.execute(sql, valores)
    conexao.commit()

    editar.close()
    lista.close()
    formulario.show()

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
loginWindow = uic.loadUi("loginWindow.ui")
loginWindow.btnLogin.clicked.connect(login)

formulario = uic.loadUi('formulario.ui')
formulario.btnCadastrar.clicked.connect(inserir)
formulario.btnRelatorio.clicked.connect(lista_relatorio)

usuarios = uic.loadUi('usuarios.ui')
usuarios.btnCadastrarUsuario.clicked.connect(inserir_usuario)
usuarios.btnExcluirUsuario.clicked.connect(excluir_usuario)
usuarios.btnListarUsuarios.clicked.connect(listar_usuarios)

lista = uic.loadUi('lista.ui')
lista.btnAlterarRegistro.clicked.connect(edit)
lista.btnApagarRegistro.clicked.connect(excluir)

editar = uic.loadUi('editar.ui')
editar.btnConfirmarAlteracao.clicked.connect(salvar_dados)

# Exibe a janela principal de cadastro
cadastrar_primeiro_usuario()
app.exec()
