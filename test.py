from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/signUp')
def signUp():
    print("It Worked!")
    return render_template('index.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    return json.dumps({'status':'OK'});

if __name__=="__main__":
    app.run()
