# Code Referece 
    # https://towardsdatascience.com/use-python-scripts-to-insert-csv-data-into-django-databases-72eee7c6a433
    # https://stackoverflow.com/questions/38374004/how-to-import-images-in-django-models-from-csv-excel
    # I took as a refernce the code from the previous links and code from my own midterms project for loading 
    # data, however, I addapted models, created function and use modular programing.   

# Libraries
import csv
import shutil
import os
import django
import sys 

# Inorder to access the projects models, the enviroment needs to be setup 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Models
from courses.models import *
from students.models import Student
from teachers.models import Teacher
from management.models import User

# Scipts for uploading the students, teacher and courses data into the database using django modules
def run():

    # Inorder to access the projects models, the enviroment needs to be setup 
    # Code refernce: bioweb app from AWD module
    sys.path.append("/eIntellectual") 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eIntellectual.settings') 
    django.setup()

    # Removes storage directories
    deletes_storage_dir('images/course_images')
    deletes_storage_dir('images/resources_files')
    deletes_storage_dir('images/student_images')
    deletes_storage_dir('images/teacher_images')
    
    # Loads each table using its respective model
    loads_data('teachers/static/tables/Teachers.csv', Teacher, name='Teachers')
    loads_data('courses/static/tables/Courses.csv', Course, name='Courses')
    loads_data('courses/static/tables/Resources.csv', Resource, name='Resources')
    loads_data('courses/static/tables/ResourcesTypes.csv', ResourceType, name='ResourcesTypes')
    loads_data('students/static/tables/Students.csv', Student, name='Students')
    loads_data('courses/static/tables/Enrollments.csv', Enrollment, name='Enrollments')

# deletes storage directory before loading more files into it
# Code Reference https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/
def deletes_storage_dir(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path) 

# Loads tables data for each model
def loads_data(file_path, obj, name):
    # model object 
    object = obj.objects

    # deletes stored instances
    object.all().delete()

    # open file
    with open(file_path) as table:
        reader = csv.reader(table)
        next(reader)                         # does not include header

        # calls functions for each table
        if name == 'Courses':
            courses_data(reader, object)
        elif name == 'Resources':
            resources_data(reader, object)
        elif name == 'ResourcesTypes':
            resourcesTypes_data(reader, object)
        elif name == 'Students':
            students_data(reader, object)
        elif name == 'Enrollments':
            enrollments_data(reader, object)
        elif name == 'Teachers':
            teachers_data(reader, object)

# Loads course data
def courses_data(reader, object):
    print('Courses table loading data...')

    # itarate over the rows to load data into DB
    for row in reader:
        table = object.create(code = row[0],
                            name = row[1],
                            category = row[2],
                            teacher = Teacher.objects.get(account_number=(row[3])),
                            date_created = row[4],
                            date_updated = row[5],
                            description = row[6]
                            )
        # read file in binary data to save it image
        try:
            im_file = open('courses/static/courses_images/'+row[7], 'rb')
        except:
            im_file = open('courses/static/courses_images/foo.jpg', 'rb')
        table.image.save(row[7], im_file)
        # save new instance 
        table.save()

# Loads course resources. Load Courses first because it is use as foreign key
def resources_data(reader, object):
    print('Resources table loading data...')

    # itarate over the rows to load data into DB
    for row in reader:
        table = object.create(code = row[0],
                            course = Course.objects.get(code=(row[1])),
                            timestamp = row[2],
                            text = row[4]
                            )
        # read file in binary data to save
        file = open('courses/static/resources_files/'+row[3], 'rb')

        # save new instance 
        table.content.save(row[3], file)

        # save new instance 
        table.save()

# Loads course resources types
def resourcesTypes_data(reader, object):
    print('ResourcesTypes table loading data...')

    # itarate over the rows to load data into DB
    for row in reader:
        table = object.create(resource =  Resource.objects.get(code=(row[0])),
                            resource_type = row[1]
                            )

        # save new instance 
        table.save()



# Loads Students data
def students_data(reader, object):
    print('Students table loading data...')

    # gets User object 
    user = User.objects
    # deletes any instance of User that is a student before loading this data
    user.filter(is_student = True).delete()


    # itarate over the rows to load data into DB
    for row in reader:
        # crates table for User
        user_table = user.create(username = row[5],
                                   is_student = True,
                                   is_teacher = False
                                   )
        user_table.set_password('longestpass098')     # this is not an safe way to add a password)
        # creates table for student
        table = object.create(user = User.objects.get(username=(row[5])),
                            account_number = row[0],
                            name = row[1],
                            last_name = row[2],
                            birthday = row[3],
                            email = row[4],
                            user_name = row[5],
                            start_date = row[6],
                            )
        # read file in binary data to save image
        try:
            im_file = open('students/static/students_photos/'+row[7], 'rb')
        except:
            im_file = open('students/static/students_photos/foo.jpg', 'rb')

        # save new instance 
        table.photo.save(row[7], im_file)
        # save new instance 
        user_table.save()
        table.save()



# Loads Teachers data
def teachers_data(reader, object):
    print('Teachers table loading data...')

    # gets User object 
    user = User.objects
    # deletes any instance of User that is a student before loading this data
    user.filter(is_teacher = True).delete()

    # itarate over the rows to load data into DB
    for row in reader:

        # crates table for User
        user_table = user.create(username = row[5],
                                   is_student = False,
                                   is_teacher = True
                                   )
        user_table.set_password('longestpass098')     # this is not an safe way to add a password)

        # creates table for student
        table = object.create(user = User.objects.get(username=(row[5])),
                            account_number = row[0],
                            name = row[1],
                            last_name = row[2],
                            birthday = row[3],
                            email = row[4],
                            user_name = row[5],
                            start_date = row[6],
                            )
        # read file in binary data to save it image
        try:
            im_file = open('teachers/static/teachers_photos/'+row[7], 'rb')
        except:
            im_file = open('teachers/static/teachers_photos/foo.jpg', 'rb')

        # save new instance 
        table.photo.save(row[7], im_file)
        # save new instance 
        user_table.save()
        table.save()

# Loads students enrollments
def enrollments_data(reader, object):
    print('Enrollments table loading data...')

    # itarate over the rows to load data into DB
    for row in reader:
        table = object.create(date = row[0],
                              student =  Student.objects.get(account_number=(row[1])),
                              course = Course.objects.get(code=(row[2]))
                            )

#         # # save new instance 
        table.save()


