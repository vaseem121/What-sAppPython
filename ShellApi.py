import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    subprocess.call(['newscrap.py'], shell=True)
    return 'Success'
app.run()