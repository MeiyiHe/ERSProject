#!/usr/bin/python
from flask import Flask,abort,render_template,request,redirect,url_for, send_file
from werkzeug import secure_filename
import re,os
from subprocess import call
from importFunctionTest import rewritten
import uniqueList
from collections import defaultdict
import textProcess
import final_analyze_textgridDIR

app = Flask(__name__)

ALLOWED_EXTENSIONS = 'txt'
UPLOAD_FOLDER = '/Users/Siya/Documents/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
AUDIO_FOLDER = '/Users/Siya/Downloads/'
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
DEST_FOLDER = '/Users/Siya/Documents/audio_uploaded'
app.config['DEST_FOLDER'] = DEST_FOLDER
ALIGNER_DIR = '/Users/Siya/Desktop/ERSPGroup/Prosodylab-Aligner/'
app.config['ALIGNER_DIR'] = ALIGNER_DIR



script = []
#align = []
audio = []
text = []
processed_script = []
old_user = False
loginChecking = defaultdict()
#loginChecking['meiyi'] = 'mehe@ucsd.edu'

with open('userInfo.txt', 'r') as info:
    for line in info:
        line = line.strip('\n').split()
        loginChecking[line[0]] = line[1]


@app.route('/')
def index():
    return redirect(url_for('hello'))

@app.route('/hello/', methods = ['GET','POST'])
def hello():
    global loginChecking
    global greetings
    if request.method == 'POST':
        #print "requesting name and email"
        global email
        email = ''.join(request.form['email'])
        global user
        user = ''.join(request.form['userName'])
        
        if user in loginChecking and loginChecking[user] == email:
            #global greetings
            greetings = "welcome back"
            old_user = True
            # if already exist 
            print greetings

            print loginChecking[user]
        else:
            #global greetings
            greetings = "hello, first time user"
            userInfo = open('newUser.txt', 'w+')
            userInfo.write(user)
            userInfo.write('\t')
            userInfo.write(email)
            userInfo.write('\n')
            userInfo.close()
            loginChecking[user] = email
            print loginChecking

            with open('userInfo.txt', 'a+') as outfile:
                with open('newUser.txt', 'r') as infile:
                    for line in infile:
                        outfile.write(line)
        
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
            #uniqueList.setCover(filepath)

            #script.append('scriptsRequest.txt') # the script will be presented to the user
            #align.append('scriptsSystem.txt') # the script used for forced alignment
            return redirect(url_for('select_options',user=user))
            #return render_template('requestAudio.html')
    return render_template('file_upload.html', user=user,greetings= greetings)

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
            if old_user:
                pass
                #script.append('scriptsSystem.txt')
            else:
                uniqueList.setCover(script[0])
                #script.append('scriptsRequest.txt')

            return redirect(url_for('recorder', user=user))
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
@app.route('/recorder', methods=['GET', 'POST'])
def recorder():
    #read_uploaded_file()
    if request.method == 'POST':
        if request.form['sub_button'] == 'collect':
            submit_audio_all()
            command = 'python3 -m {0} -d {1} -a {2}'.format('aligner','eng.dict',app.config['DEST_FOLDER'])
            call(command.split(), cwd=app.config['ALIGNER_DIR'], shell=False) 
            final_analyze_textgridDIR.grep_timestamp(app.config['DEST_FOLDER'])

            return render_template('review.html')
    tmp_list = read_uploaded_file()
    
    print tmp_list
    return render_template('recorder.html',sentence_list=tmp_list)

@app.route('/read_file', methods=['GET'])
def read_uploaded_file():
    if old_user:
        filename = script[0]
    else:
        filename = 'scriptsRequest.txt'
    tmp = []
    print filename
    #filename = secure_filename(request.args.get('filename'))
    try:
        """
        if filename and allowed_filename(filename):
            print "file allowed"
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                for char in f.read():
                    if char != '\n':
                        tmp.append(char)
                sentence_list = ''.join(tmp)
                sentence_list = unicode(sentence_list, 'ascii', 'ignore')
            

            return sentence_list
        """
        if filename and allowed_filename(filename):
            print "file allowed"
            with open( filename) as f:
                for char in f.read():
                    if char != '\n':
                        tmp.append(char)
                sentence_list = ''.join(tmp)
                sentence_list = unicode(sentence_list, 'ascii', 'ignore')
            

            return sentence_list        
    except IOError:
        pass
    return "Unable to read file"

@app.route('/submit_all', methods=['GET'])
def submit_audio_all():
    audio_namelist = []

    mtime = lambda f: os.stat(os.path.join(app.config['AUDIO_FOLDER'], f)).st_mtime

    for i in sorted(os.listdir(app.config['AUDIO_FOLDER']), key=mtime):
        if os.path.isfile(os.path.join(app.config['AUDIO_FOLDER'],i)) and 'MyRecording' in i:
            modified = i.replace(' ','')
            os.rename(os.path.join(app.config['AUDIO_FOLDER'],i), os.path.join(app.config['DEST_FOLDER'],modified))
            newname = 'p'+modified
            command = 'ffmpeg -i {0} -ar 16000 -ac 1 {1}'.format(modified,newname)
            call(command.split(), cwd=app.config['DEST_FOLDER'], shell=False)
            command = 'rm {0}'.format(modified)
            call(command.split(), cwd=app.config['DEST_FOLDER'], shell=False)
            audio_namelist.append(os.path.splitext(os.path.join(app.config['DEST_FOLDER'],newname))[0])

    if old_user:
        filename = script[0]
    else:
        filename = 'scriptsSystem.txt'
    
    with open(filename) as f:
        text = f.read()
    
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

    for i in range(len(audio_namelist)):
        textProcess.output_script(sentences[i], audio_namelist[i]+'.lab')
        with open(audio_namelist[i]+'.txt', 'w+') as w:
            w.write(sentences[i])

        







def allowed_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.run(debug = True)






    
