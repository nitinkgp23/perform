from flask import Flask , request , render_template
import pandas as pd
from sklearn.externals import joblib
from src.knn_corrector import *
from src.extract_data_rollno import *

app = Flask(__name__)

def manual_process(dep, sgpa_list):
    '''
    '''
    yr = 5 if dep =='MA' else 4
    data_used = len(sgpa_list)
    predict_series = pd.Series(sgpa_list)
    sg_predict = []
    for sem in range(data_used + 1, 2*yr + 1 ):
        filename  = 'src/models/' + dep + '_' + str(sem) +'sem_' + str(data_used) + '_sgpa.pkl'
        clf = joblib.load(filename)
        sg_predict.append(round(float(clf.predict(predict_series)[0]),2))

    diff = correct_knn_sgpa(dep, sgpa_list)
    #if diff>1 or diff<-1:
    for i in range(2*yr-data_used):
        sg_predict[i] += round(diff,2)

    return sg_predict

def viarollno_process(dep, gradelist):
    '''
    '''
    yr = 5 if dep =='MA' else 4
    data_used = len(gradelist)
    input_list = []
    for sem in gradelist:
        for grade in sem:
            input_list.append(grade)
    predict_series = pd.Series(input_list)
    sg_predict = []
    for sem in range(data_used + 1, 2*yr + 1 ):
        filename  = 'src/models/' + dep + '_sem' + str(sem) +'_data' + str(data_used) + '_subject.pkl'
        clf = joblib.load(filename)
        sg_predict.append(round(float(clf.predict(predict_series)[0]),2))
    
    diff = correct_knn_subject(dep, gradelist)
    #if diff>1 or diff<-1:
    for i in range(2*yr-data_used):
        sg_predict[i] += round(diff,2)
    return sg_predict

def _rollno_to_gradelist(rollno):
    sem_list, sgpa = rollno_dataextract(rollno)
    grade_list_total = []
    for sem in sem_list:
        grade_list_sem = []
        for subject in sem[:-1]:
            grade_list_sem.append(subject['Grade'])
        grade_list_total.append(grade_list_sem)

    return grade_list_total

def _sgpastr_to_sgpalist(sgpa_list_str):
    sgpa_list = sgpa_list_str.split()
    sgpa_list = [float(x) for x in sgpa_list]

    return sgpa_list

def name_to_dep(dep_name):
    return {
        'Mathematics and Computing': 'MA',
        'Computer Science': 'CS',
        'Electronics and Communication Engineering': 'EC',
        'Civil Engineering': 'CE',
        'Electrical Engineering': 'EE'
    }[dep_name]

@app.route('/' , methods=['GET','POST'])
def processit():
    if request.method == 'POST':

        if bool(request.form['which-sgpa']) == True:
            sgpa_list_str = request.form['which-sgpa']
            dep_name = request.form['dep']
            dep = name_to_dep(dep_name)
            sgpa_list = _sgpastr_to_sgpalist(sgpa_list_str)
            predicted_sg = manual_process(dep, sgpa_list)

            return render_template('result.html', sglist = predicted_sg)

        else :
            rollno = request.form['which-rollno']
            dep_name = request.form['dep']
            dep = name_to_dep(dep_name)
            gradelist = _rollno_to_gradelist(rollno)
            predicted_sg = viarollno_process(dep, gradelist)

            return render_template('result.html', sglist = predicted_sg)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
