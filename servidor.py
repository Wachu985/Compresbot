from flask import Flask,render_template,Blueprint,request,send_from_directory
import os 

servidor = Flask(__name__)
routes_files = Blueprint("routes_files",__name__)

PATH_FILES = os.getcwd()
print(PATH_FILES)

@servidor.route('/')
def index():
    return 'Hello Mundo'

@routes_files.route("/<string:username>/<string:name_files>",methods=['GET'])
def getFiles(name_files,username):
    try:
        if './'+username+'/'+name_files:
            print('Existe')
        return send_from_directory('./'+username,path=name_files,as_attachment = True)
    except Exception as e:
        return e

servidor.register_blueprint(routes_files)
if __name__ == '__main__':
    servidor.run(threaded=True,port = '4000',debug=True)