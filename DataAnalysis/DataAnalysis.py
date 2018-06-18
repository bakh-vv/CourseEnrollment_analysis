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

#print(enrollments[0])

#print(daily_engagement[0])
#print(project_submissions[0])


### Fixing Data Types

from datetime import datetime as dt

def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

print(enrollments[0])

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    
print(daily_engagement[0])


# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

print(project_submissions[0])


enrollment_num_rows = len(enrollments)
#enrollment_num_unique_students = len(set([dic['account_key'] for dic in enrollments]))

engagement_num_rows = len(daily_engagement)
#engagement_num_unique_students = len(set([dic['acct'] for dic in daily_engagement]))

submission_num_rows = len(project_submissions)          
#submission_num_unique_students = len(set([dic['account_key'] for dic in project_submissions]))

print(enrollment_num_rows)
print(engagement_num_rows)
print(submission_num_rows)


#renaming column name, to keep it the same among the 3 files, by creating a new one and then deleting the old one
for dict in daily_engagement:
    dict['account_key'] = dict['acct']

for dict in daily_engagement:
    del dict['acct']

# creating a function that investigates the 3 files, replacing the repetitive code above
def get_unique_students(data):
    return set([dic['account_key'] for dic in data])

unique_enrolled_students = get_unique_students(enrollments)
enrollment_num_unique_students = len(unique_enrolled_students)
unique_engagement_students = get_unique_students(daily_engagement)
engagement_num_unique_students = len(unique_engagement_students)
unique_project_submitters = get_unique_students(project_submissions)
submission_num_unique_students = len(unique_project_submitters)

print(enrollment_num_unique_students)
print(engagement_num_unique_students)
print(submission_num_unique_students)

#finding any one enrolled student that doesn't appear in an engagement document
for record in enrollments:
    if record['account_key'] not in unique_engagement_students:
        print(record)
        break

# checking if there are enrolled students that don't appear in the engagement document that stayed enrolled
# at least one day
surprising_enrollments = []
for record in enrollments:
    if record['account_key'] not in unique_engagement_students and record['join_date'] != record['cancel_date']:
        surprising_enrollments.append(record)
        


    
