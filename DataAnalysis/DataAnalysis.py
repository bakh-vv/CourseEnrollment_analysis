import unicodecsv

#enrollments = []
#f = open('enrollments.csv', 'rb')
#reader = unicodecsv.DictReader(f) #creates an iterable, which can only be used once

#for row in reader:
#    enrollments.append(row) #to store it permanently we put it in a list

#f.close()


'''
alternatively, not to have to close the file:

enrollments = []
with open('enrollments.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)

    for row in reader:
        enrollments.append(row)

Mind the indenting, after the indenting finishes, the file closes
'''

'''
Even easier way, without having to use the loop

with open('enrollments.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    enrollments = list(reader)

'''

#with open('daily_engagement.csv', 'rb') as f:
#    reader = unicodecsv.DictReader(f)
#    daily_engagement = list(reader)

#with open('project_submissions.csv', 'rb') as f:
#    reader = unicodecsv.DictReader(f)
#    project_submissions = list(reader)

#since we have repetitive code, it would make sense to create a function

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

print(enrollments[0])

print(daily_engagement[0])
print(project_submissions[0])


