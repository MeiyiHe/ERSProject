from flask import Flask,abort,render_template,request,redirect,url_for, send_file
from werkzeug import secure_filename
from copy import deepcopy
import os,sys
from importFunctionTest import rewritten
#reload(sys)
#sys.setdefaultencoding('utf8')
app = Flask(__name__)


"""
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), 'mpu.crt')
key = os.path.join(os.path.dirname(__file__), 'mpu.key')
"""
# # TLS seems better
# from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1)
# cer = os.path.join(os.path.dirname(__file__), 'mpu.crt')
# key = os.path.join(os.path.dirname(__file__), 'mpu.key')


#app.secret_key = 'somekey'



ALLOWED_EXTENSIONS = 'txt'
UPLOAD_FOLDER = '/Users/Siya/Documents/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#context = (cer, key)
#app.run(host='132.239.95.117', debug = True, ssl_context=context)
# app.run(host='0.0.0.0', port=5000, debug = True, ssl_context=context)




script = []
audio = []
text = []
#sentence_list = []

@app.route('/')
def index():
    return redirect(url_for('hello'))

@app.route('/hello/', methods = ['GET','POST'])
def hello():
    if request.method == 'POST':
        print "requesting name and email"
        global email
        email = ''.join(request.form['email'])
        global user
        user = ''.join(request.form['userName'])

        return redirect(url_for('upload_file', user=user))    
    return render_template('hello.html')


@app.route('/upload/',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        file = request.files['file']
        print user
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(filepath)
            script.append(filepath)
            return redirect(url_for('select_options',user=user))
            #return render_template('requestAudio.html')
    return render_template('file_upload.html', user=user)

@app.route('/requestAudio', methods=['GET', 'POST'])
def upload_audio():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            audio.append(filepath)
            return redirect(url_for('review',user=user))
    return render_template('requestAudio.html', user=user)

@app.route('/selectOptions/', methods=['GET', 'POST'])
def select_options():
    if request.method == 'POST':
        if request.form['button1'] == 'add_lib':
            return redirect(url_for('recorder',user=user))
            #return redirect(url_for('upload_audio', user=user))
        elif request.form['button1'] == 'synthesize':
            #not yet implemented
            return hello()
    
    return render_template('selectOptions.html',user=user)

@app.route('/review', methods=['GET', 'POST'])
def review():
    """print script
    print audio
    with open(script[0],'r') as f:
        for line in f:
            text.append(str(line))
        txt = ''.join(text)
    print txt"""
    return redirect(url_for('recorder',user=user))
    #return render_template('review.html',text=txt )
@app.route('/recorder')
def recorder():
    #read_uploaded_file()
    tmp_list = read_uploaded_file()
    print tmp_list
    return render_template('recorder.html',sentence_list=tmp_list)

@app.route('/read_file', methods=['GET'])
def read_uploaded_file():
    filename = script[0]
    tmp = []
    #filename = secure_filename(request.args.get('filename'))
    try:
        if filename and allowed_filename(filename):
            print "file allowed"
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                for char in f.read():
                    if char != '\n':
                        tmp.append(char)
                sentence_list = ''.join(tmp)
                sentence_list = unicode(sentence_list, 'ascii', 'ignore')
                

            return sentence_list
    except IOError:
        pass
    return "Unable to read file"

def allowed_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug = True)






    
