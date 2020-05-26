import os
from flask import Flask, request
from werkzeug.utils import secure_filename
#from IBM import Model

UPLOAD_FOLDER = 'folder'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg','mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api_key = " "
model_id = " "


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 #           model = Model(
#                           "folder/"+str(file.filename),
#                           api_key=api_key,
#                           model_id=model_id
#                        )
 #           result = model.label_predict()
            return "%s uploead com sucesso "  % filename

    if request.method == 'GET':
        return """
    <!doctype html>
    <html>
    <head>
    <title>Envia sua imagem</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    </head>
    <center>



    <div class="jumbotron">
      <h1 class="display-4">Demo Mask Detect Covid 19</h1>
      <p class="lead">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p>
      <hr class="my-4">
      <p>It uses utility classes for typography and spacing to space content out within the larger container.</p>
      <p class="lead">

        <form action="" method=post enctype=multipart/form-data>
         <p><input type=file name=file>
         <input type=submit value=Upload>
        </form>
      </p>

    </div>
    </center>
    </html>
    """

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5551,debug=True)

