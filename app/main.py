from flask import Flask,render_template
app = Flask(__name__)

#most simple return
@app.route('/')
def hello_world():
  return 'Hello, World!'

#render template with given function argument
@app.route('/name/<name>')
def hello_name(name):
  return render_template('index.html',name=name)


if __name__ == '__main__':
  app.run()
