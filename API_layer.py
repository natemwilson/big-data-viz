from flask import Flask
import xmlrpc.client


app = Flask(__name__)
proxy = xmlrpc.client.ServerProxy('http://0.0.0.0:22228/')


@app.route('/corr/<this>/<that>')
def serve_corr(this, that):
    return str(proxy.summarizer.correlation_matrix.get_correlation(this, that))

@app.route('/max/')


if __name__ == '__main__':
    app.run()