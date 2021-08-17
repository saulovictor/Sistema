from PyQt5 import uic, QtWidgets
import pyautogui as pya
import mysql.connector


numero_id =0


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='sistema'
)
if mydb.is_connected():
    db_info = mydb.get_server_info()
    print('Conectado ao servidor MySQL versão',db_info)
    cursor = mydb.cursor()
    cursor.execute("select database();")
    linha = cursor.fetchone()
    print("Conectado ao banco de dados ", linha)


def funcao_principal():

    nome = formulario.lineEdit.text()
    est_civil = formulario.lineEdit_3.text()

    rg = formulario.lineEdit_4.text()
    if len(rg) < 7:
        rg = rg.zfill(7)
    rg = '{}.{}.{}'.format(rg[:1], rg[1:4], rg[4:7])

    cpf = formulario.lineEdit_5.text()
    if len(cpf) < 11:
        cpf = cpf.zfill(11)
    cpf = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])

    endereco = formulario.lineEdit_9.text()
    numero = formulario.lineEdit_10.text()
    complemento = formulario.lineEdit_11.text()
    municipio = formulario.lineEdit_12.text()
    bairro = formulario.lineEdit_13.text()

    cep = formulario.lineEdit_14.text()
    if len(cep) < 8:
        cep = cep.zfill(8)
    cep = '{}-{}'.format(cep[:5], cep[5:8])

    uf = formulario.comboBox.currentText()

    telefone = formulario.lineEdit_15.text()
    if len(telefone) < 8:
        telefone = telefone.zfill(8)
    telefone = '{}-{}'.format(telefone[:4], telefone[4:8])

    celular = formulario.lineEdit_16.text()
    if len(celular) < 11:
        celular = celular.zfill(11)
    celular = '({}) {}{}-{}'.format(celular[:2], celular[2:3], celular[3:7], celular[7:11])

    email = formulario.lineEdit_17.text()


    sexo = ''

    if formulario.radioButton.isChecked():
        sexo = 'Masculino'
    elif formulario.radioButton_2.isChecked():
        sexo = 'Feminino'
    else:
        pya.alert('Selecione um sexo')


    print('Nome:',nome)
    print('Est. Civil:', est_civil)
    print('RG:', rg)
    print('CPF:', cpf)
    print('Sexo: ' + sexo)
    print('Endereço:', endereco)
    print('Numero:', numero)
    print('Complemento:', complemento)
    print('Municipio:', municipio)
    print('Bairro:', bairro)
    print('CEP:', cep)
    print('UF: ' + uf)
    print('Telefone:', telefone)
    print('Celular:', celular)
    print('E-mail', email)


    mycursor = mydb.cursor()
    sql = "INSERT INTO cliente (nome,est_civil,rg,cpf,sexo,endereco,numero,complemento,municipio,bairro,cep,uf,telefone,celular,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(nome), str(est_civil), str(rg), str(cpf), str(sexo), str(endereco), str(numero), str(complemento), str(municipio), str(bairro), str(cep), str(uf), str(telefone), str(celular), str(email))
    mycursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "Registro inserido.")
    pya.alert('Cadastrado com sucesso!')

    formulario.lineEdit.setText('')
    formulario.lineEdit_3.setText('')
    formulario.lineEdit_4.setText('')
    formulario.lineEdit_5.setText('')
    formulario.lineEdit_9.setText('')
    formulario.lineEdit_10.setText('')
    formulario.lineEdit_11.setText('')
    formulario.lineEdit_12.setText('')
    formulario.lineEdit_13.setText('')
    formulario.lineEdit_14.setText('')
    formulario.lineEdit_15.setText('')
    formulario.lineEdit_16.setText('')
    formulario.lineEdit_17.setText('')



app= QtWidgets.QApplication([])
formulario = uic.loadUi('formulario.ui')
formulario.comboBox.addItems(['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'])
formulario.pushButton.clicked.connect(funcao_principal)



formulario.show()
app.exec()
