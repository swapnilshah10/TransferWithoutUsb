from flask import Flask, request, send_file, render_template_string, abort, url_for
import os
import zipfile
import io
from mimetypes import guess_type

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

    file_links = []
    for file in files:
        file_path = os.path.join(full_path, file)
        mime_type, _ = guess_type(file_path)
        if mime_type and mime_type.startswith('image'):
            file_links.append(f"""
                <li class='list-group-item' style = 'display: flex;
'>
                    <a href='{os.path.join(request.path, file)}' style ='margin-left: auto;
  margin-right: auto;' >
                        <img src='{os.path.join(request.path, file)}' class='img-thumbnail' alt='{file}' style='max-width: 200px;
  '>
                    </a>
                </li>
            """)
        else:
            file_links.append(f"""
                <li class='list-group-item'>
                    <a class='btn btn-secondary w-100' href='{os.path.join(request.path, file)}'>{file}</a>
                </li>
            """)

    dir_links = [f"""
        <li class='list-group-item'>
            <a class='btn btn-info w-100' href='{os.path.join(request.path, directory)}'>{directory}</a>
        </li>
    """ for directory in directories]

    file_list = "<ul class='list-group'>" + \
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
        <div class="container mt-5">
            <h1 class="text-center mb-4">File Browser</h1>
            <div class="text-center mb-3">
                <a href="{url_for('index', subpath=subpath, download='1')}" class="btn btn-danger mb-3">Download Current Folder as ZIP</a>
            </div>
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
