#Cadastro de Clientes
from PyQt5 import uic, QtWidgets
import pyautogui as pya
import mysql.connector
from reportlab.pdfgen import canvas

#variavel com id 0
numero_id = 0

#Conexão com banco de dados
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='sistema'
)
#Checo se o banco foi conectado
if mydb.is_connected():
    db_info = mydb.get_server_info()
    print('Conectado ao servidor MySQL versão',db_info)
    cursor = mydb.cursor()
    cursor.execute("select database();")
    linha = cursor.fetchone()
    print("Conectado ao banco de dados ", linha)

#Função Editar
def editar():
    global numero_id

    linha = tela_listar.tableWidget.currentRow()

    mycursor = mydb.cursor()
    sql = "SELECT id_cliente FROM cliente"
    mycursor.execute(sql)
    dados_lidos = mycursor.fetchall()
    valor_id = dados_lidos[linha][0]
    sql2 = "SELECT * FROM cliente WHERE id_cliente=" + str(valor_id)
    mycursor.execute(sql2)
    cliente = mycursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit_2.setText(str(cliente[0][0]))
    tela_editar.lineEdit.setText(str(cliente[0][1]))
    tela_editar.lineEdit_3.setText(str(cliente[0][2]))
    tela_editar.lineEdit_4.setText(str(cliente[0][3]))
    tela_editar.lineEdit_5.setText(str(cliente[0][4]))
    tela_editar.lineEdit_6.setText(str(cliente[0][5]))
    tela_editar.lineEdit_9.setText(str(cliente[0][6]))
    tela_editar.lineEdit_10.setText(str(cliente[0][7]))
    tela_editar.lineEdit_11.setText(str(cliente[0][8]))
    tela_editar.lineEdit_12.setText(str(cliente[0][9]))
    tela_editar.lineEdit_13.setText(str(cliente[0][10]))
    tela_editar.lineEdit_14.setText(str(cliente[0][11]))
    tela_editar.lineEdit_7.setText(str(cliente[0][12]))
    tela_editar.lineEdit_15.setText(str(cliente[0][13]))
    tela_editar.lineEdit_16.setText(str(cliente[0][14]))
    tela_editar.lineEdit_17.setText(str(cliente[0][15]))

    numero_id = valor_id

#Função Salvar dados editador
def salvar_valor_editado():
    global numero_id

    nome = tela_editar.lineEdit.text()
    est_civil = tela_editar.lineEdit_3.text()

    rg = tela_editar.lineEdit_4.text()
    if len(rg) < 7:
        rg = rg.zfill(7)
    rg = '{}.{}.{}'.format(rg[:1], rg[1:4], rg[4:7])

    cpf = tela_editar.lineEdit_5.text()
    if len(cpf) < 11:
        cpf = cpf.zfill(11)
    cpf = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])

    sexo = tela_editar.lineEdit_6.text()

    endereco = tela_editar.lineEdit_9.text()
    numero = tela_editar.lineEdit_10.text()
    complemento = tela_editar.lineEdit_11.text()
    municipio = tela_editar.lineEdit_12.text()
    bairro = tela_editar.lineEdit_13.text()

    cep = tela_editar.lineEdit_14.text()
    if len(cep) < 8:
        cep = cep.zfill(8)
    cep = '{}-{}'.format(cep[:5], cep[5:8])

    uf = tela_editar.lineEdit_6.text()

    telefone = tela_editar.lineEdit_15.text()
    if len(telefone) < 8:
        telefone = telefone.zfill(8)
    telefone = '{}-{}'.format(telefone[:4], telefone[4:8])

    celular = tela_editar.lineEdit_16.text()
    if len(celular) < 11:
        celular = celular.zfill(11)
    celular = '({}) {}{}-{}'.format(celular[:2], celular[2:3], celular[3:7], celular[7:11])

    email = tela_editar.lineEdit_17.text()


    mycursor = mydb.cursor()
    mycursor.execute("UPDATE cliente SET nome ='{}',est_civil ='{}',rg ='{}',cpf ='{}',sexo = '{}',endereco ='{}',numero ='{}',complemento ='{}',municipio ='{}',bairro ='{}',cep ='{}', uf = '{}',telefone ='{}',celular ='{}',email ='{}' WHERE id_cliente ={}".format(nome,est_civil,rg,cpf,sexo,endereco,numero,complemento,municipio,bairro,cep,uf,telefone,celular,email,numero_id))
    mydb.commit()
    tela_editar.close()
    tela_listar.close()
    chama_segunda_tela()

#Função excluir linha da tabela
def excluir():

    linha = tela_listar.tableWidget.currentRow()
    tela_listar.tableWidget.removeRow(linha)

    mycursor = mydb.cursor()
    sql = "SELECT id_cliente FROM cliente"
    mycursor.execute(sql)
    dados_lidos = mycursor.fetchall()
    valor_id = dados_lidos[linha][0]
    sql2 = "DELETE FROM cliente WHERE id_cliente=" + str(valor_id)
    mycursor.execute(sql2)

#Função gerar arquivo PDF
def gerar_pdf():

    mycursor = mydb.cursor()
    sql = "SELECT * FROM cliente"
    mycursor.execute(sql)
    dados_lidos = mycursor.fetchall()

    y = 0
    pdf = canvas.Canvas("cadastro_clientes.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(100, 800, "Relatorio de clientes cadastrados")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(50, 750, "NOME")
    pdf.drawString(200, 750, "CPF")
    pdf.drawString(300, 750, "CELULAR")
    pdf.drawString(400, 750, "EMAIL")


    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(200, 750 - y, str(dados_lidos[i][4]))
        pdf.drawString(300, 750 - y, str(dados_lidos[i][14]))
        pdf.drawString(400, 750 - y, str(dados_lidos[i][15]))


    pdf.save()
    pya.alert("PDF FOI GERADO COM SUCESSO!")


#Função principal tela de cadastro de clientes
def funcao_principal():

    nome = tela_cadastro_cliente.lineEdit.text()
    est_civil = tela_cadastro_cliente.lineEdit_3.text()

    rg = tela_cadastro_cliente.lineEdit_4.text()
    if len(rg) < 7:
        rg = rg.zfill(7)
    rg = '{}.{}.{}'.format(rg[:1], rg[1:4], rg[4:7])

    cpf = tela_cadastro_cliente.lineEdit_5.text()
    if len(cpf) < 11:
        cpf = cpf.zfill(11)
    cpf = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])

    sexo = tela_cadastro_cliente.comboBox_2.currentText()

    endereco = tela_cadastro_cliente.lineEdit_9.text()
    numero = tela_cadastro_cliente.lineEdit_10.text()
    complemento = tela_cadastro_cliente.lineEdit_11.text()
    municipio = tela_cadastro_cliente.lineEdit_12.text()
    bairro = tela_cadastro_cliente.lineEdit_13.text()

    cep = tela_cadastro_cliente.lineEdit_14.text()
    if len(cep) < 8:
        cep = cep.zfill(8)
    cep = '{}-{}'.format(cep[:5], cep[5:8])

    uf = tela_cadastro_cliente.comboBox.currentText()

    telefone = tela_cadastro_cliente.lineEdit_15.text()
    if len(telefone) < 8:
        telefone = telefone.zfill(8)
    telefone = '{}-{}'.format(telefone[:4], telefone[4:8])

    celular = tela_cadastro_cliente.lineEdit_16.text()
    if len(celular) < 11:
        celular = celular.zfill(11)
    celular = '({}) {}{}-{}'.format(celular[:2], celular[2:3], celular[3:7], celular[7:11])

    email = tela_cadastro_cliente.lineEdit_17.text()



    mycursor = mydb.cursor()
    sql = "INSERT INTO cliente (nome,est_civil,rg,cpf,sexo,endereco,numero,complemento,municipio,bairro,cep,uf,telefone,celular,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(nome), str(est_civil), str(rg), str(cpf), str(sexo), str(endereco), str(numero), str(complemento), str(municipio), str(bairro), str(cep), str(uf), str(telefone), str(celular), str(email))
    mycursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "Registro inserido.")
    pya.alert('Cadastrado com sucesso!')

    tela_cadastro_cliente.lineEdit.setText('')
    tela_cadastro_cliente.lineEdit_3.setText('')
    tela_cadastro_cliente.lineEdit_4.setText('')
    tela_cadastro_cliente.lineEdit_5.setText('')
    tela_cadastro_cliente.lineEdit_9.setText('')
    tela_cadastro_cliente.lineEdit_10.setText('')
    tela_cadastro_cliente.lineEdit_11.setText('')
    tela_cadastro_cliente.lineEdit_12.setText('')
    tela_cadastro_cliente.lineEdit_13.setText('')
    tela_cadastro_cliente.lineEdit_14.setText('')
    tela_cadastro_cliente.lineEdit_15.setText('')
    tela_cadastro_cliente.lineEdit_16.setText('')
    tela_cadastro_cliente.lineEdit_17.setText('')

#Função para chamar tela de listagem de cliente
def chama_segunda_tela():
    tela_listar.show()

    mycursor = mydb.cursor()
    sql = "SELECT * FROM cliente"
    mycursor.execute(sql)
    dados_lidos = mycursor.fetchall()


    tela_listar.tableWidget.setRowCount(len(dados_lidos))
    tela_listar.tableWidget.setColumnCount(16)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 16):
            tela_listar.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app= QtWidgets.QApplication([])
tela_cadastro_cliente = uic.loadUi('tela_cadastro_cliente.ui')
tela_listar = uic.loadUi('tela_listar.ui')
tela_editar = uic.loadUi('tela_editar.ui')
tela_cadastro_cliente.pushButton.clicked.connect(funcao_principal)
tela_cadastro_cliente.pushButton_2.clicked.connect(chama_segunda_tela)
tela_listar.pushButton.clicked.connect(editar)
tela_listar.pushButton_3.clicked.connect(excluir)
tela_listar.pushButton_4.clicked.connect(gerar_pdf)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)

#Aqui estão os valores de cada comboBOx
tela_cadastro_cliente.comboBox.addItems(['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'])
tela_cadastro_cliente.comboBox_2.addItems(['Masculino', 'Feminino'])


tela_cadastro_cliente.show()
app.exec()
