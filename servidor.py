from flask import Flask,render_template,Blueprint,request,send_from_directory
import os 

servidor = Flask(__name__)
routes_files = Blueprint("routes_files",__name__)

PATH_FILES = os.getcwd()
print(PATH_FILES)

@servidor.route('/')
def index():
    return 'Hello Mundo'

@routes_files.get("/<string:username>/<string:name_files>")
def getFiles(name_files,username):
    return send_from_directory(PATH_FILES+'/'+username,name_files,as_attachment = True)

servidor.register_blueprint(routes_files)

if __name__ == '__main__':
    servidor.run(threaded=True,port = '4000')