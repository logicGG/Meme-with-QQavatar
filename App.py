from flask import Flask, send_file, Response

from MemeTool import MemeTool

app = Flask(__name__)
tool = MemeTool()


@app.route('/meme/<play>/<qq>', methods=['GET'])
def getMeme(play, qq):
    resultPath = tool.getNeed(qq)
    return send_file(resultPath, mimetype='image/png')


if __name__ == '__main__':
    app.run()
