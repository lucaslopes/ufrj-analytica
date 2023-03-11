from flask import Flask, jsonify, request


app = Flask(__name__)


def main():
    app.run(debug=True)
    return True


__name__ == '__main__' and main()