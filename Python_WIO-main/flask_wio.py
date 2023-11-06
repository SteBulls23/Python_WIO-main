
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,request,jsonify
import MySQLdb
from MySQLdb.cursors import DictCursor
import json
app = Flask(__name__)
mydb = MySQLdb.connect( host="SteBulls23.mysql.pythonanywhere-services.com",
                            user="SteBulls23",
                            password="wioterminal",
                            database="SteBulls23$wioterminal")

mydbDict = MySQLdb.connect( host="SteBulls23.mysql.pythonanywhere-services.com",
                            user="SteBulls23",
                            password="wioterminal",
                            database="SteBulls23$wioterminal",
                            cursorclass=DictCursor)

@app.route('/')
def hello_world():
    mycursor= mydb.cursor()
    mycursor.execute("select * from tb_wio;")
    myresult = mycursor.fetchall()
    lista="";
    for x in myresult:
        lista = lista + "<br>macaddress = " + x[2]

    return 'Hello wioterminal!<br>' + lista

#chiamo da wio pagina ...../checkmac/?mac=12:23:34:45:56&code=1234:

@app.route('/checkmac', methods=['GET'])
def checkmac():
    try:
        #in request args l'array con i parametri
        args= request.args;
        #estraggo macaddress
        mac="12:12:12";
        mac=args.get("macaddress");
        code=args.get("code");
        ret=""
        mycursor= mydb.cursor()
        #carico i record con lo stesso macaddress
        mycursor.execute("select * from tb_wio where macaddress='" + mac + "';")
        myresult = mycursor.fetchall()
        #se 001 trovato e quindi gia' presente
        if (mycursor.rowcount== 1):
            mycursorcode= mydb.cursor()
            #carico i record con lo stesso macaddress
            mycursorcode.execute("select * from tb_wio where macaddress='" + mac + "' and code ='" + code +   "' ;")
            myresultcode = mycursorcode.fetchall()
            if (mycursorcode.rowcount== 1):
                myid=myresultcode[0][0]
            else:
                myid=0;
            ret= str(myid)
        else:  # lo inserisco
            mycur = mydb.cursor()
            sql = "INSERT INTO tb_wio (wio, macaddress) VALUES (%s, %s)"
            val = ("wio terminal", mac)
            mycur.execute(sql, val)
            mydb.commit()
            mycursor= mydb.cursor()
            mycursor.execute("select * from tb_wio where macaddress='" + mac + "';")
            myresult = mycursor.fetchall()
            #se 001 trovato e quindi gia' presente
            myid=myresult[0][0]
            ret= str(myid)
        return ret

    except Exception as e:
        ret= "macaddress" + str(mac) + "The error is: " + str(e)
        return ret

@app.route('/getstats', methods=['GET'])
def getstats():
    #in request args l'array con i parametri
    args= request.args;
    #estraggo idwio
    idwio=args.get("idwio");
    ret=""
    mycursor= mydb.cursor()
    #carico i record con lo stesso macaddress
    mycursor.execute("SELECT min(value) as mymin ,max(value) as mymax, avg(value) as myavg, count(value) as mycnt FROM tb_wiodata where idwio = " + idwio + " group by idwio;")
    myresult = mycursor.fetchall()
    #se 001 trovato e quindi gia' presente
    if (mycursor.rowcount== 1):
        mymin=myresult[0][0]
        mymax=myresult[0][1]
        myavg=myresult[0][2]
        mycnt=myresult[0][3]

        ret= "min=" + str(mymin) + " - max="+str(mymax) + " - avg=" + str(myavg) + " - count=" + str(mycnt)
    else:  # lo inserisco
        ret= "no data"
    return ret


#chiamo da wio pagina ...../checkmac/?mac=12:23:34:45:56:

@app.route('/insdbvalue', methods=['GET'])
def insdbvalue():
    #in request args l'array con i parametri
    args= request.args;
    #estraggo macaddress
    mac=args.get("macaddress");
    val=args.get("value");
    typ=args.get("type");
    ret=""
    mycursor= mydb.cursor()
    #carico i record con lo stesso macaddress
    mycursor.execute("select * from tb_wio where macaddress='" + mac + "';")
    myresult = mycursor.fetchall()
    #se 001 trovato e quindi gia' presente
    if (mycursor.rowcount== 1):
        id=myresult[0][0]
        mycur = mydb.cursor()
        sql = "INSERT INTO tb_wiodata (idwio, value,type) VALUES (%s, %s,%s)"
        val = (id,val,typ)
        mycur.execute(sql, val)
        mydb.commit()
        ret= val + " inserito"
    return ret

@app.route('/getJson/<int:idwio>')
def getJson(idwio):
    return jsonify(message="My id " + str(idwio) + " and I am OK")


@app.route('/getstatsJson/<int:idwio>', methods=['GET'])
def getstatsJson(idwio):
    try:
        if (str(idwio)==""):
           ret= jsonify("[{err:'no data'}]")
           return ret
        ret=""
        mycursor= mydbDict.cursor()
        #carico i record con lo stesso macaddress
        mycursor.execute("SELECT min(value) as mymin ,max(value) as mymax, avg(value) as myavg , count(idwio) as mycnt  FROM tb_wiodata where idwio = " + str(idwio) + " group by idwio;")
        myresult = mycursor.fetchall()
        #se 001 trovato e quindi gia' presente
        if (mycursor.rowcount>0):
            ret= jsonify(myresult)
        else:
            ret= jsonify("[{err:\"no data\"}]")
        return ret
    except Exception as e:
        ret= "idwio" + str(idwio) + "The error is: " + str(e)
        return ret


@app.route('/insdbJson/<idwio>',methods=['POST'])
def insdbJson(idwio):
    try:
        val = request.json['value']
        typ= request.json['type']
        id =str(idwio)
        mycur = mydb.cursor()

        sql = "INSERT INTO tb_wiodata (idwio, value,type) VALUES (%s, %s,%s)"
        val = (idwio,val,typ)
        mycur.execute(sql, val)
        mydb.commit()
        return "inserito"
    except Exception as e:
        return str(request.json) + str(e)
