from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/age', methods=['POST'])
def age():
    data = request.json
    name = data['name']
    quote = f'Hello, {name}!'
    return jsonify({'quote': quote})


def main():
    app.run(debug=True)
    return True


__name__ == '__main__' and main()