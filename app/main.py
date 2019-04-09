from flask import Flask,render_template,jsonify,request,g
import pyodbc
import pandas
app = Flask(__name__)

############################################################################################################
####################################### Database connection ################################################
############################################################################################################

connstring = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:dnadbserver.database.windows.net,1433;Database=dnadb;Uid=dnaadmin@dnadbserver;Pwd=Insee555;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
cnxn = pyodbc.connect(connstring)
cursor = cnxn.cursor()

def get_db():
    if 'db' not in g:
        g.db = pyodbc.connect(connstring)
    return g.db

@app.teardown_appcontext
def teardown_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

############################################################################################################
####################################### Web app route ######################################################
############################################################################################################

#most simple return
@app.route('/')
def hello_world():
  return 'Hello, World!'

#render template with given function argument
@app.route('/name/<name>')
def hello_name(name):
  return render_template('index.html',name=name)

#Form example
@app.route('/form', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
  if request.method == 'POST':  #this block is only entered when the form is submitted
      language = request.form.get('language')
      framework = request.form['framework']

      return '''<h1>The language value is: {}</h1>
                <h1>The framework value is: {}</h1>'''.format(language, framework)

  return '''<form method="POST">
                Language: <input type="text" name="language"><br>
                Framework: <input type="text" name="framework"><br>
                <input type="submit" value="Submit"><br>
            </form>'''

#Query example: expect user to call something like http://127.0.0.1:5000/query?name='Dew'&age=30
@app.route('/query')
def getQuery():
  var_name = request.args.get('name')
  var_age = request.args.get('age')
  return 'The user {} has age {}'.format(var_name,var_age)

#get data from Azure SQL to Pandas > return value to web page
@app.route('/querypd')
def queryPandas():
  cnxn = get_db()
  sql = 'select * from asensor'
  data = pandas.read_sql(sql,cnxn)
  print(data)
  print(data.iloc[0,0])
  return 'Value from Dataframe: {}'.format(data.iloc[0,0])

#return as json
@app.route('/json')
def getJSON():
  a_dict = {
    'name':'INDG',
    'price': 12000
            }
  return jsonify(a_dict)

#test database
@app.route('/db')
def dbtest():
  db = get_db()
  sql = 'select count(recdate) from asensor'
  cur = db.execute(sql)
  rows = cur.fetchall()
  print(type(rows))
  # return render_template('show_entries.html',entries=rows)
  return 'fetchall type: {}, --- fetchall first item: {}, --- fetch all first of first: {}'.format(type(rows).__name__,rows[0],rows[0][0])

#read JSON input from POST request and return something
'''
- Get POSTMAN application
- Put the JSON data below to the body
  {
	"name" : "Dew",
	"age" : 30,
	"attribute" : { 
                  "money" : 100,
                  "unit"	: "THB",
                  "speed"	: 40
	              },
	"alist" : [true,false,true]
  }
- Send request to get example response
  - With POSTMAN: Select Body > Input the dictionary block above > Select method JSON(application/json) > Press SEND
  - With CURL command line: curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/api/echo-json -d '{"name": "Alice"}'

ref: https://raw.githubusercontent.com/noppGithub/img/master/flask/json_request.PNG
'''
@app.route('/jsonquery', methods=['POST']) #GET requests will be blocked
def jsonAction():
  #convert request json to Python dictionary
  reqdata = request.get_json()
  #parse input dictionary
  name = extractJSON('name',reqdata)
  age = extractJSON('age',reqdata)
  money = reqdata['attribute']['money']
  unit = reqdata['attribute']['unit']
  speed = reqdata['attribute']['speed']
  boolean_item = reqdata['alist'][0]
  formular = 'age + money + speed'
  #construct a dict for output
  a_dict = {
    'username' : name,
    'userage' : age,
    'attr' : {
      'formular' : formular,
      'output': age + money + speed
    },
    'userbln' : boolean_item
  }
  return jsonify(a_dict)

def extractJSON(strKey,json_input):
  # this function to help handle error when there is no target key in JSON input
  # print('Trying to extract jsoninput')
  varout = None
  if strKey in json_input:
    varout = json_input[strKey]
  # print('varout is {}'.format(varout))
  return varout


############################################################################################################
####################################### Start FLASK app ####################################################
############################################################################################################
if __name__ == '__main__':
  app.run()
