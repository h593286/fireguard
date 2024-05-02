from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='/Users/eilertskram/Documents/GitHub/fireguard/static')

@app.route('/')
def subscriber():
    return send_from_directory(app.static_folder, 'subtest.html')

if __name__ == '__main__':
    app.run(debug=True)
