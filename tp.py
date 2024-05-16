from flask import Flask, request, send_file, render_template_string, abort, url_for
import os
import zipfile
import io

app = Flask(__name__)

ROOT_DIR = os.path.abspath('D:/')
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)


@app.route('/')
@app.route('/<path:subpath>')
def index(subpath=''):
    full_path = os.path.join(ROOT_DIR, subpath)
    if not os.path.exists(full_path):
        return abort(404)

    if request.args.get('download') == '1':
        return download_zip(full_path)

    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)

    items = os.listdir(full_path)
    files = [item for item in items if os.path.isfile(
        os.path.join(full_path, item))]
    directories = [item for item in items if os.path.isdir(
        os.path.join(full_path, item))]

    file_links = [f"<li><a class='btn btn-secondary' href='{
        os.path.join(request.path, file)}'>{file}</a></li>" for file in files]
    dir_links = [f"<li><a class='btn btn-info' href='{os.path.join(
        request.path, directory)}'>{directory}</a></li>" for directory in directories]
    file_list = "<ul class='list-unstyled'>" + \
        "".join(dir_links + file_links) + "</ul>"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Browser</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5 mb-3 text-center">File Browser</h1>
            <a href="{url_for('index', subpath=subpath, download='1')}" class="btn btn-danger mb-3">Download Current Folder as ZIP</a>
            {file_list}
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """, subpath=subpath)


def download_zip(full_path):
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        if os.path.isdir(full_path):
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=full_path)
                    zf.write(file_path, arcname=arcname)
        else:
            zf.write(full_path, os.path.basename(full_path))
    memory_file.seek(0)
    zip_filename = os.path.basename(full_path) + '.zip'
    return send_file(memory_file, download_name=zip_filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join(ROOT_DIR, file.filename))
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
