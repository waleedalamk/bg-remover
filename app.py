from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    # Renders the index.html file
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']

    try:
        input_image = Image.open(file.stream)
        output_image = remove(input_image)

        # Save the result to a temporary in-memory file
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        # Send the file back to the user
        return send_file(output_buffer, mimetype='image/png', as_attachment=True, download_name="output.png")
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
