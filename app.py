import os, uuid
from flask import Flask, flash, request, redirect, url_for
from flask import render_template, send_from_directory
from werkzeug.utils import secure_filename

from scripts.true_black import true_black


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
            threshold = int(request.form.get('threshold'))
            print(threshold)
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template('success.html', filename=filename, threshold=threshold)
            else:
                filename = secure_filename(file.filename)
                return render_template('wrong_file.html', result=filename)        
        
        return render_template('index.html')
        
    @app.route('/<filename>/<threshold>', methods=['GET'])
    def show_image(filename, threshold):
        new_file_name = true_black(app.config['UPLOAD_FOLDER'], filename, threshold)
        return send_from_directory(app.config['UPLOAD_FOLDER'], new_file_name)
    
    @app.route('/test')
    def test():
        return '<h1>test</h1>'

    return app
