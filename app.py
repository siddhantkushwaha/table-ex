import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename

from main import run

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(path)

            tables = []
            for i, table in enumerate(run(path), 0):
                result_path = f'static/table-{i}.csv'
                table.to_csv(result_path, index=False)
                tables.append(result_path)

            return render_template('main.html', tables=tables)

    return render_template('main.html')


if __name__ == '__main__':
    app.run()
