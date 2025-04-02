import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'pdf', 'png', 'jpg', 'jpeg'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for file upload and listing
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"File {filename} uploaded successfully!"

    files = os.listdir(UPLOAD_FOLDER)  # Get list of uploaded files
    return render_template('index.html', files=files)

# Route to view uploaded files
@app.route('/view/<filename>')
def view_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file_extension = filename.rsplit('.', 1)[1].lower()

    if file_extension in {'txt', 'csv', 'json'}:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return render_template('view.html', filename=filename, content=content)

    elif file_extension in {'png', 'jpg', 'jpeg'}:
        return render_template('view.html', filename=filename, image=True)

    elif file_extension == 'pdf':
        return send_from_directory(UPLOAD_FOLDER, filename)

    else:
        return "File format not supported for viewing."

# Route to serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=8080)