from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": 3,
            "replicas": ["Server 1", "Server 2", "Server 3"]
        },
        "status": "successful"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)