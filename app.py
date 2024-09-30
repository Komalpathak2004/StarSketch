from flask import Flask, request, render_template, send_file
import os
 # Import your function from the module

 app = Flask(__name__)

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the Features page
@app.route('/features')
def features():
    return render_template('features.html')

# Route to render the About page
@app.route('/about')
def about():
    return render_template('about.html')

# Route to render the Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to handle form submission

    if not topic:
        return "Topic is required", 400

    try:
        # Call the GenerateComic function
        pdf_path = GenerateComic(topic, style, target_lang)
        # Ensure the file exists before sending
        if os.path.isfile(pdf_path):
            return send_file(pdf_path, as_attachment=True)
        else:
            return "File not found", 404
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
