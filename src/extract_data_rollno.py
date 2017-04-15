import requests
import json
from bs4 import BeautifulSoup

def rollno_dataextract(rollno):
    '''
    The function returns a dict containing information about the student's performance record.
    Takes roll no as input and returns the student's grades.
    '''

    url = "https://erp.iitkgp.ernet.in/StudentPerformance/view_performance.jsp?rollno="+rollno
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'lxml')

    
    tables = soup.find_all('td', width='60%') 
    sem_list=[]      
    for table in tables[0:]:
        subject_group=[]
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        for row in table.find_all("tr")[1:]:
            text= []
            for td in row.find_all("td"):
                text.append(td.get_text())
                subject_data_dict = dict(zip(headings,text))
            subject_group.append(subject_data_dict)
        if(subject_group):
            if(subject_group[0]['Grade']):
                sem_list.append(subject_group)
    if(not sem_list):
        return None, None

        
    sgpa_list = soup.find_all("b",string = "SGPA")
    sgpa=[]
    for i in sgpa_list:
        i = i.find_parent("td")
        i = i.find_next_sibling("td")
        i = i.string
        if(i):
            sgpa.append(i)
    sgpa.reverse() 

    for sem in range(len(sem_list)):
        sem_copy =[]
        for sub in sem_list[sem]:
            if _determine(sub):
                sem_copy.append(sub)
        sem_list[sem] = sem_copy[:]
            
    for sem in range(len(sem_list)):
        credit=0
        sg_contr = 0
        for sub in sem_list[sem]:
            credit += int(sub['Credit'])
            sub['Grade'] = _grade_to_marks(sub['Grade'])
            if sub['Grade'] == 0 :
                return None, None
            sg_contr += int(sub['Credit']) * sub['Grade']
            key_to_remove = ['L-T-P', 'Subject Name', 'Subject Type']
            for key in key_to_remove:
                del sub[key]
        if (credit == 0):
            return None, None
        sem_list[sem].append({'Credit': credit, 'SGPA': round(sg_contr/credit, 2)})

    sem_list.reverse()
    if(sem_list[0][-1]['Credit']!=23):
        sem_list[0], sem_list[1] = sem_list[1], sem_list[0]
        sgpa[0], sgpa[1] = sgpa[1], sgpa[0]

    return sem_list, sgpa

def _grade_to_marks(x):
    '''
    The method takes the grade as input and returns its equivalent weight in the range of 0-10.
    '''
    dict_grade= {
        'EX': 10,
        'A': 9,
        'B': 8,
        'C': 7,
        'D': 6,
        'P': 5,
        'F': 0
    }
    marks =  dict_grade.get(x)
    if marks is None:
        return 0
    else:
        return marks

def _determine(x):
    '''
    The method determines whether the subject is of Depth type or an Extra Academic Activity,
    and returns a boolean value.

    This is later used to delete the subjects from the list which doesn't fit the criteria.
    '''

    if x['Subject No'][0:2] == 'EA':
        return False
    elif x['Subject Type'] != 'Depth':
        return False
    else:
        return True
