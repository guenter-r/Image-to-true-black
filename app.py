import os

from flask import Flask, flash, request, redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename


def create_app(test_config=None):
    # img upload settings:
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                ## todo here:
                # copy file saved above and pass it to the AMOLED function
                # store this file
                # render a site that shows both files / all files: more options of black reduced files
                return redirect(url_for('upload_file', result=filename, payload={'file':file}))
            else:
                filename = secure_filename(file.filename)
                return render_template('wrong_file.html', result=filename)        
        
        # initial d
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''
        # return render_template('img.html')

    return app
