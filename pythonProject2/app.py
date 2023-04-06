from flask import Flask, render_template, request
from final import check_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']
    result = check_url(url)
    return result

if __name__ == '__main__':
    app.run(debug=True)
