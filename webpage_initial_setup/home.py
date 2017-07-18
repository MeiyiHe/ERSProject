#!/usr/bin/python
from flask import Flask,abort,render_template,request,redirect,url_for, send_file
from werkzeug import secure_filename
import re,os
from os.path import basename
from datetime import datetime
from subprocess import call
from importFunctionTest import rewritten
import uniqueList, returnUserUniqueList
from collections import defaultdict
import textProcess,textPreprocess,generateLib,generateLibW,covering
import final_analyze_textgridDIR

app = Flask(__name__)
#MEIYI 
ALLOWED_EXTENSIONS = 'txt'
upload_FOLDER = '/Users/meiyihe/Desktop/testUploadFile/uploads/'
#app.config['upload_FOLDER'] = upload_FOLDER 
AUDIO_FOLDER = '/Users/meiyihe/Downloads'
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
dest_FOLDER = '/Users/meiyihe/Desktop/testUploadFile/audio_uploaded'
#app.config['dest_FOLDER'] = dest_FOLDER
ALIGNER_DIR = '/Users/meiyihe/Prosodylab-Aligner'
app.config['ALIGNER_DIR'] = ALIGNER_DIR
CURRENT_DIR = '/Users/meiyihe/Desktop/testUploadFile/'

"""SIYA
ALLOWED_EXTENSIONS = 'txt'
upload_FOLDER = '/Users/Siya/Documents/uploads/'
#app.config['upload_FOLDER'] = upload_FOLDER 
AUDIO_FOLDER = '/Users/Siya/Downloads/'
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
dest_FOLDER = '/Users/Siya/Documents/audio_uploaded'
#app.config['dest_FOLDER'] = dest_FOLDER
ALIGNER_DIR = '/Users/Siya/Desktop/ERSPGroup/Prosodylab-Aligner/'
app.config['ALIGNER_DIR'] = ALIGNER_DIR
CURRENT_DIR = '/Users/Siya/Documents/ERSPtest/erspGit/ERSProject/webpage_initial_setup/'
"""

script = []
#align = []
audio = []
text = []
processed_script = []
old_user = False
incremental = False
tmp_list = []
loginChecking = defaultdict()
genlib_filelist = []
genlibW_fileslist = []


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
        global userDir
        userDir = user + 'Folder'
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
            command = 'mkdir {0}'.format(userDir)
            call(command.split(),cwd='user_folders',shell=False)
            command = 'mkdir {0}'.format(user)
            call(command.split(),cwd='user_folders/'+ userDir,shell=False)
            command = 'mkdir GL'
            call(command.split(),cwd='user_folders/'+ userDir +'/'+user, shell=False)
            command = 'cp <pause>.wav {0}'.format('user_folders/' +userDir+'/'+user+'/GL')
            call(command.split(),shell=False)

        dest_FOLDER = CURRENT_DIR + 'user_folders/' + userDir + '/'+user
        app.config['dest_FOLDER'] = dest_FOLDER
        upload_FOLDER = CURRENT_DIR + 'user_folders/' + userDir
        app.config['upload_FOLDER'] = upload_FOLDER
        
        return redirect(url_for('upload_file', user=user))
    return render_template('hello.html')


@app.route('/upload/',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        file = request.files['file']
        print user
        if file:
            filename = secure_filename(file.filename)
            print "app.config[upload folder]"
            print app.config['upload_FOLDER']
            print "filename"
            print filename
            filepath = os.path.join(app.config['upload_FOLDER'],filename)
            file.save(filepath)

            replacements = {'. ':'.\n', '? ':'?\n', '! ':'!\n'}
            lines = []
            with open(filepath) as f:
                for line in f:
                    for src,target in replacements.iteritems():
                        line = line.replace(src, target)
                    lines.append(line)
            command = 'rm {0}'.format(filename)
            call(command.split(),cwd=app.config['upload_FOLDER'],shell=False)
            print lines
            with open(filepath,'w') as f:
                for line in lines:
                    f.write(line)

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
            filepath = os.path.join(app.config['upload_FOLDER'], filename)
            file.save(filepath)
            audio.append(filepath)
            return redirect(url_for('review',user=user))
    return render_template('requestAudio.html', user=user)

@app.route('/selectOptions/', methods=['GET', 'POST'])
def select_options():
    global synthe
    global outputPath
    synthe = False
    if request.method == 'POST':
        if request.form['button1'] == 'add_lib':
            
            synthe = False
            if old_user:
                returnUserUniqueList.returnUserSetCover(script[0], app.config['upload_FOLDER'])
                #script.append('scriptsSystem.txt')
            else:
                uniqueList.setCover(script[0], app.config['upload_FOLDER'])
                #script.append('scriptsRequest.txt')

            #return redirect(url_for('recorder', user=user))
        elif request.form['button1'] == 'synthesize':
            #not yet implemented
            filename = script[0] # full path
            #textPreprocess.preprocess(filename)
            ret_cover = covering.covering('user_folders/' + userDir + '/'+user, filename)
            #covering.covering(app.config['upload_FOLDER'],filename)
            if ret_cover == 1:
                print "SUCCESS, CHECK YOUR USER FOLDER"
                outputPath = filename[:-4]+'_output.wav'
                
                #return send_file(outputPath, mimetype="wav", as_attachment=True, attachment_filename=basename(os.path.splitext(filename)[0])+'_output.wav')
                return redirect(url_for('review', path=outputPath))
            #need more audios 
            else:
                print "returncover == 0 when press synthesizing ========================"
                incremental = True
                synthe = True
                
                #script.append('''file_need_to_record''')
                returnUserUniqueList.returnUserSetCover(script[0], app.config['upload_FOLDER'])
        return redirect(url_for('recorder', user=user))
            #return render_template('review.html')
    return render_template('selectOptions.html',user=user)
    

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        if request.form['button2'] == 'output':
            #print outputPath 
            
            return send_file(outputPath, mimetype="wav", as_attachment=True, attachment_filename=basename(os.path.splitext(script[0])[0])+'_output.wav')
        if request.form['button2'] == 'logout':
            
            return redirect(url_for('index'))
            
    return render_template('review.html')

    
@app.route('/recorder', methods=['GET', 'POST'])
def recorder():
    if request.method == 'POST':
        if request.form['sub_button'] == 'collect':
            submit_audio_all()
            command = 'python3 -m {0} -d {1} -a {2}'.format('aligner','eng.dict',app.config['dest_FOLDER'])
            call(command.split(), cwd=app.config['ALIGNER_DIR'], shell=False) 
            final_analyze_textgridDIR.grep_timestamp(app.config['dest_FOLDER'])
            # by this point, should have all the timestamp files necessary

            # item ---> full path, file extension '.txt'
            for item in genlib_filelist:
                textPreprocess.preprocess(item)
            for item in genlibW_fileslist:
                textPreprocess.preprocessW(item)

            for item in genlib_filelist:
                generateLib.generateLib(os.path.dirname(item),basename(os.path.splitext(item)[0]))
            for item in genlibW_fileslist:
                generateLibW.generateLibW(os.path.dirname(item),basename(os.path.splitext(item)[0]))

            for item in os.listdir(app.config['dest_FOLDER']):
                if os.path.isfile(os.path.join(app.config['dest_FOLDER'],item)):
                    os.rename(os.path.join(app.config['dest_FOLDER'],item), os.path.join(app.config['upload_FOLDER'],item))
            outputPath = ''
            if synthe == True:
                filename = script[0]
                ret_cover = covering.covering('user_folders/' + userDir + '/'+user, filename)
                outputPath = filename[:-4]+'_output.wav'
               # return send_file(outputPath, mimetype="wav", as_attachment=True, attachment_filename=basename(os.path.splitext(filename)[0])+'_output.wav')
                               
            return redirect(url_for('review', path=outputPath))
    
    tmp_list = read_uploaded_file()
    
    print tmp_list
    return render_template('recorder.html',sentence_list=tmp_list)

@app.route('/read_file', methods=['GET'])
def read_uploaded_file():

    filename = app.config['upload_FOLDER'] + '/scriptsRequest.txt'
    tmp = []
    print filename
    #filename = secure_filename(request.args.get('filename'))
    try:
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
            os.rename(os.path.join(app.config['AUDIO_FOLDER'],i), os.path.join(app.config['dest_FOLDER'],modified))
            newname = user+'_'+str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day)+str(datetime.now().hour)+str(datetime.now().minute)+modified
            command = 'ffmpeg -i {0} -ar 16000 -ac 1 {1}'.format(modified,newname)
            call(command.split(), cwd=app.config['dest_FOLDER'], shell=False)
            command = 'rm {0}'.format(modified)
            call(command.split(), cwd=app.config['dest_FOLDER'], shell=False)
            audio_namelist.append(os.path.splitext(os.path.join(app.config['dest_FOLDER'],newname))[0])


    if old_user:
        filename = script[0]
    else:
        filename = app.config['upload_FOLDER'] +'/scriptsSystem.txt'
    
    with open(filename) as f:
        text = f.read()
    
    
    splitted = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',text)

    print splitted
    for i in range(len(audio_namelist)):
        
        words = True
        for char in splitted[i]:
            if ord(char) != 32 and ord(char) != 10:
                if (ord(char) < 65) or ((ord(char) > 90) and (ord(char) < 97)) or (ord(char) > 122):
                    words = False

        textProcess.output_script(splitted[i], audio_namelist[i]+'.lab')
        if words == False:
            genlib_filelist.append(audio_namelist[i]+'.txt')
        else:
            genlibW_fileslist.append(audio_namelist[i]+'.txt')

        with open(audio_namelist[i]+'.txt', 'w+') as w:
            w.write(splitted[i])
    
    print genlib_filelist # just filenames without extensions
    print genlibW_fileslist # just filenames without extensions



def allowed_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.run(debug = True)






    
