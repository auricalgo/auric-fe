from flask import Flask, jsonify, request
from nandan import final_run

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def run_health():

    return 'True'

@app.route('/api/data', methods=['GET'])
def run_api():

    final_run()

    return jsonify('True')



if __name__ == '__main__':
    app.run(port=5020,debug=False)
