from flask import Flask,render_template,Blueprint,request,send_from_directory
import os 

app = Flask(__name__)
routes_files = Blueprint("routes_files",__name__)

PATH_FILES = os.getcwd()
print(PATH_FILES)

@app.route('/')
def index():
    return 'Hello Mundo'

@routes_files.get("/<string:username>/<string:name_files>")
def getFiles(name_files,username):
    if os.path.exists(PATH_FILES+'/'+username+'/'+name_files):
        return send_from_directory(PATH_FILES+'/'+username,name_files,as_attachment = True)
    else:
        return 

app.register_blueprint(routes_files)

if __name__ == '__main__':
    app.run(debug=True,port = '80',host= '0.0.0.0')