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
# there are 3. Turns out they are  internal test accounts, which explains them


#removing all test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])

len(udacity_test_accounts)

def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print(len(non_udacity_enrollments))
print(len(non_udacity_engagement))
print(len(non_udacity_submissions))


# Exploring the difference between those who passed and those who didn't

# to standardize the data we'll use the first week of their engagement records
paid_students = {}
#for enrollment in non_udacity_enrollments:
#    if enrollment['is_canceled'] == False or enrollment['days_to_cancel'] > 7:
#        paid_students[enrollment['account_key']] = enrollment['join_date'] 

# we'll save the enrollment date from their latest enrollment (not just from a random enrollment)
for enrollment in non_udacity_enrollments:
    if enrollment['is_canceled'] == False or enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date'] 

        if account_key not in paid_students or \
            enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date
        

print(len(paid_students))

# filter engagement data for paid users duting their first week after enrolling
#def within_one_week(join_date, engagement_date):
#    time_delta = engagement_date - join_date
#    return time_delta.days < 7

# fixed within_one_week method
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

paid_engagement_in_first_week = []
for record in non_udacity_engagement:
    account_key = record['account_key']
    
    if account_key in list(paid_students.keys()) and within_one_week(paid_students[account_key], record['utc_date']):
        paid_engagement_in_first_week.append(record)

len(paid_engagement_in_first_week)

def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)


# calculating average time spent in classroom during the first week by paid customers
from collections import defaultdict

engagement_by_account = defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)

total_minutes_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes

total_minutes = list(total_minutes_by_account.values())

import numpy as np

np.mean(total_minutes)
np.std(total_minutes)
np.min(total_minutes)
np.max(total_minutes) # ~10568, something's off

#trying to investigate the 10568 max figure
import operator
#finding the key of the max value in a dictionary
max(total_minutes_by_account.items(), key=operator.itemgetter(1))[0] # returns '108'
#alternative metohod to find
#student_with_max_minutes = None
#max_minutes = 0

#for student, total_minutes in total_minutes_by_account.items():
#    if total_minutes > max_minutes:
#        max_minutes = total_minutes
#        student_with_max_minutes = student

#for engagement_record in paid_engagement_in_first_week:
#    if engagement_record['account_key'] == student_with_max_minutes:
#        print(engagement_record)

#engagement_by_account['108']

### as a result we fixed the within_one_week method


### calculating average amount of lessons completed during the first week by paid customers
#we'll put the code we used previously in functions

def get_total_metrics_by_account(metrics):
    total_metrics_by_account = {}
    for account_key, engagement_for_student in engagement_by_account.items():
        total_metrics = 0
        for engagement_record in engagement_for_student:
            total_metrics += engagement_record[metrics]
        total_metrics_by_account[account_key] = total_metrics
    return total_metrics_by_account

total_lessons_by_account = get_total_metrics_by_account('lessons_completed')

total_lessons = list(total_lessons_by_account.values())

np.mean(total_lessons)
np.std(total_lessons)
np.min(total_lessons)
np.max(total_lessons)

# even more abstract functions

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data

def describe_data(data):
    print(np.mean(data))
    print(np.std(data))
    print(np.min(data))
    print(np.max(data))
    
engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')
total_minutes_by_account = sum_grouped_items(engagement_by_account, 'total_minutes_visited')
total_lessons_by_account = sum_grouped_items(engagement_by_account, 'lessons_completed')

total_minutes = list(total_minutes_by_account.values())
describe_data(total_minutes)

total_lessons = list(total_lessons_by_account.values())
describe_data(total_lessons)


### calculating average amount of days the students visited the classroom at all (visited at least one course)

#adding a filed to the data has_visited to denote whether the person visited any courses that day
enhanced_engagement = list(paid_engagement_in_first_week)
for record in enhanced_engagement:
    if record['num_courses_visited'] > 0:
        record['has_visited'] = 1
    if record['num_courses_visited'] == 0:
        record['has_visited'] = 0

engagement_by_account = group_data(enhanced_engagement, 'account_key')
total_visited_days_by_account = sum_grouped_items(engagement_by_account, 'has_visited')
total_visited_days = list(total_visited_days_by_account.values())
describe_data(total_visited_days)


### splitting out passing and non-passing students engagement data
subway_project_lesson_keys = ['746169184', '3176718735']
good_ratings = ['PASSED', 'DISTINCTION']

passing_engagement = []
non_passing_engagement = []

students_who_passed = []
for record in paid_submissions:
    account_key = record['account_key']
    if (record['assigned_rating'] == 'PASSED' or record['assigned_rating'] == 'DISTINCTION') and \
        record['lesson_key'] in subway_project_lesson_keys and account_key not in students_who_passed:
        students_who_passed.append(account_key)

for record in paid_engagement_in_first_week:
    if record['account_key'] in students_who_passed:
        passing_engagement.append(record)
    else:
        non_passing_engagement.append(record)
        
len(passing_engagement)
len(non_passing_engagement)


# comparing students who pass and those who don't
passing_engagement_by_account = group_data(passing_engagement, 'account_key')

p_total_minutes_by_account = sum_grouped_items(passing_engagement_by_account, 'total_minutes_visited')
p_total_minutes = list(p_total_minutes_by_account.values())
describe_data(p_total_minutes)

p_total_lessons_by_account = sum_grouped_items(passing_engagement_by_account, 'lessons_completed')
p_total_lessons = list(p_total_lessons_by_account.values())
describe_data(p_total_lessons)

p_total_visited_days_by_account = sum_grouped_items(passing_engagement_by_account, 'has_visited')
p_total_visited_days = list(p_total_visited_days_by_account.values())
describe_data(p_total_visited_days)

non_passing_engagement_by_account = group_data(non_passing_engagement, 'account_key')

n_total_minutes_by_account = sum_grouped_items(non_passing_engagement_by_account, 'total_minutes_visited')
n_total_minutes = list(n_total_minutes_by_account.values())
describe_data(n_total_minutes)

n_total_lessons_by_account = sum_grouped_items(non_passing_engagement_by_account, 'lessons_completed')
n_total_lessons = list(n_total_lessons_by_account.values())
describe_data(n_total_lessons)

n_total_visited_days_by_account = sum_grouped_items(non_passing_engagement_by_account, 'has_visited')
n_total_visited_days = list(n_total_visited_days_by_account.values())
describe_data(n_total_visited_days)

# check if students who passed subway are more likely to pass other projects
students_who_passed_other = [] #len = 486 people
for record in paid_submissions:
    account_key = record['account_key']
    if (record['assigned_rating'] == 'PASSED' or record['assigned_rating'] == 'DISTINCTION') and \
        record['lesson_key'] not in subway_project_lesson_keys and account_key not in students_who_passed_other:
        students_who_passed_other.append(account_key)

passed_subway_and_more = set(students_who_passed).intersection(set(students_who_passed_other)) # len = 434
# means only 52 people passed any other course after not passing subway
# 647 people passed subway. the rate of passing other projects is 434/647= 0.67

# number of student in engagement records who don't pass subway
len(set([dict['account_key'] for dict in non_passing_engagement])) #348
# rate of passing other projects is 52/348 = 0.15


### Histograms
data = [1, 2, 1, 3, 3, 1, 4, 2]

import matplotlib.pyplot as plt
import seaborn as sns
#plt.hist(data)

#plt.ion()

#plt.hist(p_total_minutes)
#plt.hist(p_total_lessons)
#plt.hist(p_total_visited_days)
#plt.hist(n_total_minutes)
#plt.hist(n_total_lessons)
#plt.hist(n_total_visited_days)



### Making plots nicer

#bins argument, which sets the number of bins used by your histogram
import seaborn as sns
plt.hist(p_total_visited_days, bins=8)
plt.xlabel("Number of days")
plt.ylabel("Number of students")
plt.title("Amount of active days in the first week")
plt.show()

sns.distplot(n_total_visited_days)
plt.show()


