from flask import Flask, render_template, request, jsonify, send_file
from werkzeug import secure_filename
from werkzeug.serving import WSGIRequestHandler
from utility import createFile
import os, posixpath
import base64, json

app = Flask(__name__)

source_dir = posixpath.join(os.getcwd(), "data")
if not os.path.exists(source_dir):
    os.mkdir(source_dir)

@app.route('/', methods=['GET'])
def startup():
    return jsonify({"message": "Upload Server working correctly"})

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filepath = posixpath.join(source_dir, secure_filename(f.filename))
        f.save(filepath)

        output = createFile(filepath, source_dir)
        if type(output) == str:
            return jsonify({"message": output})
            # return render_template('output.html', err=output)
        else:
            output_image = base64.b64encode(output)   
            print(len(output))  
            # return send_file(output_path, mimetype='image/gif')
            return jsonify({"image": str(output_image)})
            # return json.dumps(str(output_image))


if __name__ == '__main__':
    WSGIRequestHandler.wbufsize = -1
    app.run(host="0.0.0.0",port=8080, debug = True, use_reloader=False)

