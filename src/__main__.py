import requests
import json
from bs4 import BeautifulSoup
from extract_data_rollno import *
from csv_convert import *

def extract():

    dep = input("Enter department code in 2 letters. e.g. MA/CS/GG ")
    course = input("Enter 1 for B.tech , 2 for Int Msc., 3 for Dualdegree ")
    if(course=='1' or course=='2'):
        filename = dep
    else:
        filename = dep+'-Dual'

    sem_list_total = []
    sgpa_total = []

    for yr in range(15,9,-1):
        for stu in range(1,65):
            j = str(stu).rjust(2, '0')
            k = str(yr)
            rollno = k+dep+course+"00"+j

            sem_list, sgpa = rollno_dataextract(rollno)
            if (sem_list and sgpa):
                sem_list_total.append(sem_list)
                sgpa_total.append(sgpa)

            if(stu%5==0):
                print(stu,'done')

        print(yr,' year done')
    print('Done!')

    data_to_csv_subject(sem_list_total, filename + '_subject.csv')
    data_to_csv_sgpa(sgpa_total, filename + '_sgpa.csv')

if __name__ == '__main__':
    extract()