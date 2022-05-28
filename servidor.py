from flask import Flask,render_template,Blueprint,request,send_from_directory,send_file
import os 

servidor = Flask(__name__)
# routes_files = Blueprint("routes_files",__name__)
servidor.debug = True
PATH_FILES = os.getcwd()
print(PATH_FILES)

@servidor.route('/')
def index():
    return 'Hello Mundo'

@servidor.route('/dl/<username>/<filename>')
def return_files_tut(username,filename):
    file_path = '/app/'+username+'/'
    print(file_path)
    if os.path.exists(file_path):
        return send_file(file_path+filename, as_attachment=True, attachment_filename='')
    else:
        lista=os.listdir('/app/')
        msg = ''
        cont = 1
        for f in lista:
            msg += str(cont)+'-'+str(f)+'\n'
            cont +=1 
        return msg

# @routes_files.route("/<string:username>/<string:name_files>",methods=['GET'])
# def getFiles(name_files,username):
#     try:
#         if './'+username+'/'+name_files:
#             print('Existe')
#         return send_from_directory('./'+username,path=name_files,as_attachment = True)
#     except Exception as e:
#         return e

# servidor.register_blueprint(routes_files)
if __name__ == '__main__':
    servidor.run(threaded=True,port = '4000')