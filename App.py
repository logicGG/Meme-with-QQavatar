from flask import Flask, send_file
from flask_cors import CORS

from MemeTool import MemeTool

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

tool = MemeTool()


@app.route('/meme/<play>/<qq>', methods=['GET'])
def getMeme(play, qq):
    resultPath = tool.getDraw(play,qq)
    return send_file(resultPath)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
