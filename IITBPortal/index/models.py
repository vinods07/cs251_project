from django.db import models
from django.contrib.auth.models import Permission, User
from django.conf import settings
from datetime import datetime
# Create your models here.

class Student(models.Model):
    user = models.ForeignKey(User)
    email_id = models.EmailField(max_length=150,default='')
    login_id = models.CharField(max_length=100,default='')
    first_name = models.CharField(max_length=250,default='')
    last_name = models.CharField(max_length=250,default='')
    phone = models.CharField(max_length=250,default='')
    university = models.CharField(max_length=250,default='')
    city = models.CharField(max_length=250,default='')
    profile_pic = models.FileField(default='blank-user.jpg')
    is_professor = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' : ' + self.login_id

class Course(models.Model):
    course_code = models.CharField(max_length=20,default="")
    course_name = models.CharField(max_length=250,default="")
    course_info = models.CharField(max_length=500, default='')
    all_students = models.ManyToManyField(Student)

    def __str__(self):
        return self.course_code + ' : ' + self.course_name


class Topic(models.Model):
    course = models.ForeignKey(Course)
    topic_name = models.CharField(max_length=100, default='')
    topic_info = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.topic_name


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=250, default='')
    assignment_info = models.CharField(max_length=500, default='')
    parent_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)
    assignment_content_file = models.FileField(null=True, blank=True,)
    date_added = models.DateTimeField(default=datetime.now)
    deadline = models.DateTimeField(default=datetime.now)
    submissions = models.ManyToManyField(
        User,
    )

    def __str__(self):
        return self.assignment_name + ' : ' + self.parent_topic.topic_name


class Course_Material(models.Model):
    course_material_name = models.CharField(max_length=250)
    course_material_info = models.TextField()
    parent_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)
    course_content_file = models.FileField(null=True, blank=True,)

    def __str__(self):
        return self.course_material_name + ' : ' + self.parent_topic.topic_name


class Interest(models.Model):
    interest_name = models.CharField(max_length=250, default='')
    all_students = models.ManyToManyField(Student)

    def __str__(self):
        return self.interest_name


class Quiz(models.Model):
    parent_topic = models.ForeignKey(Topic, default=None)

    quiz_name = models.CharField(max_length=100, default='')
    quiz_info = models.CharField(max_length=500, default='')
    quiz_attempted = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz_name

class Grade(models.Model):
    parent_student = models.ForeignKey(Student, default=None)
    parent_quiz = models.ForeignKey(Quiz, default=None)
    quiz_attempted = models.BooleanField(default=False)
    #evaluation scheme +4 -1
    total_marks = models.IntegerField(default=100)
    marks_obtained = models.IntegerField(default=0)

    def __str__(self):
        return self.parent_quiz.quiz_name + " marks"

class Question(models.Model):
    parent_quiz = models.ForeignKey(Quiz, default=None)
    question_text = models.CharField(max_length=500, default='')
    is_subjective = models.BooleanField(default=False)
    option1 = models.CharField(max_length=100,default='')
    option2 = models.CharField(max_length=100, default='')
    option3 = models.CharField(max_length=100, default='')
    option4 = models.CharField(max_length=100, default='')
    correct_answer = models.CharField(max_length=20, default='')
    answer_given_by_student = models.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.id) + ' ' + self.parent_quiz.quiz_name + ' ' + self.parent_quiz.parent_topic.topic_name + ' '+ self.question_text


class Answer_record(models.Model):
    parent_student = models.ForeignKey(Student,default=None)
    parent_question = models.ForeignKey(Question,default=None)
    ans_given = models.CharField(max_length=20,default='')

    def __str__(self):
        return self.parent_question.question_text


class News_feed(models.Model):

    image_url = models.CharField(max_length=500,default="")
    href_url = models.CharField(max_length=500, default="")
    topic = models.CharField(max_length=500,default="")
    desc = models.CharField(max_length=1000, default="")
    date = models.CharField(max_length=100, default="")
    tag = models.CharField(max_length=500, default="")
    my_tag = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.topic

