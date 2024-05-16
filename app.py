from flask import Flask, request, send_file, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'D:/Downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    file_links = [f"<li  class = 'd-flex align-items-center justify-content-center'><a class='btn btn-primary w-75 h-25 ' href='{
        url_for('download_file', filename=file)}'>{file}</a></li><br>" for file in files]

    file_list = "<ul class='list-unstyled ;'>" + \
        "".join(file_links) + "</ul>"
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File List</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
    <form action="/upload" method="post" enctype="multipart/form-data">
         <input type="file" name="file">
         <input type="submit" value="Upload">
     </form>
        <div class="container">
            <h1 class="mt-5 mb-3 text-center">Uploaded Files</h1>
            {file_list}
        </div>
             
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """


# @app.route('/')
# def index():
#     return """
#     <form action="/upload" method="post" enctype="multipart/form-data">
#         <input type="file" name="file">
#         <input type="submit" value="Upload">
#     </form>
#     """

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return 'File uploaded successfully'


@app.route('/<filename>')
def download_file(filename):
    print(os.path.join(UPLOAD_FOLDER, filename))
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
