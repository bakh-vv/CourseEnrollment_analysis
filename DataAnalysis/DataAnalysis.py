import unicodecsv

enrollments = []
f = open('enrollments.csv', 'rb')
reader = unicodecsv.DictReader(f) #creates an iterable, which can only be used once

for row in reader:
    enrollments.append(row) #to store it permanently we put it in a list

f.close()

enrollments[0]



