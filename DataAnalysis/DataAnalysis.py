import unicodecsv

enrollments = []
f = open('enrollments.csv', 'rb')
reader = unicodecsv.DictReader(f) #creates an iterable, which can only be used once

for row in reader:
    enrollments.append(row) #to store it permanently we put it in a list

f.close()

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

enrollments[0]



