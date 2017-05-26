from flask import Flask,abort,render_template,request,redirect,url_for, send_file
from werkzeug import secure_filename
import os
from importFunctionTest import rewritten
app = Flask(__name__)


UPLOAD_FOLDER = '/Users/Siya/Documents/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

script = []
audio = []
text = []
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
            return redirect(url_for('upload_audio', user=user))
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
    return render_template('recorder.html')



if __name__ == '__main__':
    app.run(debug = True)






    
