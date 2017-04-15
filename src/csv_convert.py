
def data_to_csv_subject(data, filename):
	'''
	The function converts dataframe to csv.
	Takes only subjects as input.
	Parameters
	----------

	data: List of list of list of dict
	      `data` contains sem_lists of all the students
	'''

	f=open(filename,'w')
	for student in data:
		for sem in student:
			for subject in sem[:-1]:
				f.write(str(subject['Grade'])+ ',')
			f.write(str(sem[-1]['SGPA'])+', ,')
		f.write('\n')
	f.close()

def data_to_csv_sgpa(data, filename):
	'''
	The function converts dataframe to csv.
	Takes only sgpa as input.
	Parameters
	----------

	data: List of list of list of dict
	      `data` contains sem_lists of all the students
	'''
	f=open(filename,'w')
	for student in data:
		for sgpa in student:
			f.write(str(sgpa)+ ',')
		f.write('\n')
	f.close()