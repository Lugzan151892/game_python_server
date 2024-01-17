from flask import Flask

app = Flask(__name__)

print('Hello world')
@app.route('/')
def get_test():
    return 'hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)