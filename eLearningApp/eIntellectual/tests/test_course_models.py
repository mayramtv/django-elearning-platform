
import datetime
from datetime import date

from django.test import TestCase
from courses.models import Course, Resource, ResourceType, Enrollment
from teachers.models import Teacher
from students.models import Student

from django.core.exceptions import ValidationError

class CourseTestCase(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Teacher", last_name="Lastname")
        self.course = Course.objects.create(code="CN0001", 
                                            teacher=self.teacher, 
                                            date_created=date(2022,10,15),
                                            date_updated=date(2022,10,16))

    # __str__ function representation 
    def test_str_representation(self):
        object_mod = Course.objects.get(code="CN0001")
        self.assertEqual(str(object_mod), "CN0001")

    # Course.date_created happens before date.now()
    def test_date_created(self):
        course = Course.objects.get(code="CN0001")
        self.assertLessEqual(course.date_created, datetime.datetime.now())

    # Course.date_updated happens before date.now()
    def test_date_updated(self):
        course = Course.objects.get(code="CN0001")
        self.assertLessEqual(course.date_updated, datetime.datetime.now())

    # Course.date_updated happens after or on the date_created
    def test_date_updated_after_date_created(self):
        course = Course.objects.get(code="CN0001")
        self.assertLessEqual(course.date_created, course.date_updated)

    # Course.code is requested
    def test_required_code(self):
        object_mod = Course(code=None)
        with self.assertRaises(ValidationError):
            object_mod.full_clean() 

    # Course.name is required
    def test_name_required(self):
        object_mod = Course(name=None)
        with self.assertRaises(ValidationError):
            object_mod.full_clean() 
    
    # Course.teacher relationship
    def test_course_teacher_relationship(self):
        course = Course.objects.get(code="CN0001")
        self.assertEqual(str(course.teacher.name), "Teacher")


class ResourceTestCase(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Teacher", last_name="Lastname")
        self.course = Course.objects.create(code="CN0001", teacher=self.teacher)
        self.resource = Resource.objects.create(code="CN0001.1", 
                                                course=self.course, 
                                                timestamp='10/15/2022',
                                                content="../../seeding_files/test_PDF_file.pdf",
                                                text="Text field description")
        self.resourceType = ResourceType.objects.create(resource=self.resource,
                                                        resource_type="type")

    # Resource.code is requested
    def test_required_code(self):
        object_mod = Resource(code=None)
        with self.assertRaises(ValidationError):
            object_mod.full_clean()  

    # Resource.course relationship
    def test_resource_course_relationship(self):
        resource = Resource.objects.get(code="CN0001.1")
        self.assertEqual(str(resource.course.code), "CN0001")

    # Resource.timestamp happens before date.now()
    def test_date_updated(self):
        course = Course.objects.get(code="CN0001")
        self.assertLessEqual(course.date_updated, datetime.datetime.now())

    # ResourceType.resource relationship
    def test_resourcesTypes_resource_relationship(self):
        resourceType = ResourceType.objects.get(resource=self.resource)
        self.assertTrue(isinstance(resourceType, ResourceType))

class EnrollmentTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(code="CN0001")
        self.student = Student.objects.create(user_name="user1")
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)

    # Enrollment.student and Enrollment.course relationship
    def test_enrollment_student_relationship(self):
        enrollment = Enrollment.objects.get(course__code="CN0001")
        self.assertTrue(enrollment.student.user_name == "user1")



