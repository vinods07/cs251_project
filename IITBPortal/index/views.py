from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout,get_user_model
from .models import *
from .forms import *
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re
# Create your views here.
User = get_user_model()
course_lists = {
    'cs101':'Computer Programming and Utilization ',
    'cs152':'Abstractions and Paradigms in Programming Languages',
    'cs154':'Abstractions and Paradigms in Programming Languages Lab',
    'cs207':'Discrete Structures',
    'cs213':'Data Structures and Algorithms',
    'cs215':'Data Analysis and Interpretation',
    'cs251':'Software System Lab',
    'cs293':'Data Structures and Algorithms Lab',
}

INTEREST_LIST = {
    'Artificial Intelligence',
    'Image Processing',
    'Electrial Engineering',
    'Research',
    'Computer Graphics',
}

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

skills = [ 'competitive coding', 'web development', 'android development', 'machine learning']

tags = ['computer-science-and-artificial-intelligence-laboratory-csail', 'computer-vision',
                'electrical-engineering-computer-science-eecs', 'imaging', 'research']

tag_link = {'computer-science-and-artificial-intelligence-laboratory-csail':'Artificial Intelligence',
            'computer-vision':'Computer Graphics',
            'imaging':'Image Processing',
            'electrical-engineering-computer-science-eecs':'Electrial Engineering',
            'research':'Research',
            }

# def more_courses(request):
#     if not request.user.is_authenticated():
#         return render(request, 'index/login.html')
#     else:

def add_topic(request,course_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        form = TopicForm(request.POST or None, request.FILES or None)
        course = get_object_or_404(Course, pk=course_id)
        student = get_object_or_404(Student, login_id=request.user.username)
        if form.is_valid():
            a = Topic()
            a.course = course
            a.topic_name = request.POST['topic_name']
            a.topic_info = request.POST['topic_info']
            a.save()
            return render(request, 'index/detail.html', {'student': student,'course':course})

        context = {
            "form": form,'course':course,
        }
        return render(request, 'index/add_topic.html', context)


def profile(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        return render(request, 'index/profile.html', {'student': student})

def update_profile_pic(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            student = get_object_or_404(Student, login_id=request.user.username)

            student.profile_pic = request.FILES['profile_pic']
            file_type = student.profile_pic.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'student': student,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'index/update_profile.html', context)
            student.save()
            return render(request, 'index/profile.html', {'student': student})
        context = {
            "form": form,
        }
        return render(request, 'index/update_profile.html', context)

def course(request,course_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        course = get_object_or_404(Course, pk=course_id)
        topics = Topic.objects.filter(course=course)
        all_assignments = Assignment.objects.all()
        all_course_materials = Course_Material.objects.all()

        return render(request,'index/detail.html',{'student':student,'course':course,'topics':topics,'all_assignments':all_assignments,
                                                   'all_course_materials':all_course_materials,'INTERESTS':INTEREST_LIST,
                                                   })

def registered_courses(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        courses = Course.objects.filter(all_students=student)
        return render(request, 'index/courses.html', {'student': student, 'courses': courses,'INTERESTS':INTEREST_LIST})

def first_login(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student,user=request.user)
        if student.email_id == '':
            first_time = True
        else:
            first_time = False
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        institute = request.POST['institute']
        city = request.POST['city']
        email_id = request.POST['email']
        course_list = request.POST.getlist('course_list')

        for code in course_list:
            student.course_set.create(course_code = code,course_name = course_lists[code])

        student.first_name= first_name
        student.last_name= last_name
        student.phone= phone
        student.university= institute
        student.city= city
        student.email_id=email_id
        student.save()
        if first_time:
            return render(request,'index/update_interests.html', {'course_lists':course_lists,'student':student,
                                                   'course_list':course_list,'INTERESTS':INTEREST_LIST})
        else:
            return render(request, 'index/profile.html', {'course_lists': course_lists, 'student': student,
                                                        'course_list': course_list,'INTERESTS':INTEREST_LIST})



def index(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        news_feed = News_feed.objects.all()
        interests = Interest.objects.filter(all_students=student)
        return render(request, 'index/index.html', {'student': student,
                                                    'news_feed': news_feed, 'interests':interests,'INTERESTS':INTEREST_LIST})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,'course_lists':course_lists,
    }
    return render(request, 'index/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                student = get_object_or_404(Student, login_id=request.user.username)
                news_feed = News_feed.objects.all()
                interests = Interest.objects.filter(all_students=student)
                return render(request, 'index/index.html', {'student': student,
                                                            'news_feed': news_feed, 'course_lists': course_lists, 'interests':interests})
            else:
                return render(request, 'index/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'index/login.html', {'error_message': 'Invalid login'})
    return render(request, 'index/login.html',{'INTERESTS':INTEREST_LIST})


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():

        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user.set_password(password)
        user.save()
        a = Student(user=user,first_name=first_name,last_name=last_name,login_id=username)
        a.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                student = get_object_or_404(Student, login_id=request.user.username)
                return render(request, 'index/first_login.html', {'student': student,'course_lists':course_lists})
    context = {
        "form": form,
        'INTERESTS':INTEREST_LIST
    }
    return render(request, 'index/register.html', context)


def update_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        first_time = False
        return render(request, 'index/first_login.html', {'course_lists':course_lists,'student':student,
                                                          'first_time':first_time,'INTERESTS':INTEREST_LIST})

def add_interests(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        return render(request, 'index/update_interests.html', {'student': student,'INTERESTS':INTEREST_LIST})

def update_interests(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        interest_list = request.POST.getlist('interest_list')
        all_interest = Interest.objects.filter(all_students=student)
        for int in all_interest:
            int.all_students.remove(student)
        for interest in interest_list:
            print(interest)
            int = get_object_or_404(Interest, interest_name=interest)
            int.all_students.add(student)

        return render(request, 'index/profile.html', {'student': student,'INTERESTS':INTEREST_LIST})

def all_courses(request):
    courses = Course.objects.all()
    student = get_object_or_404(Student, login_id=request.user.username)
    return render(request,'index/all_courses.html', {'student': student,'courses':courses,'INTERESTS':INTEREST_LIST})

def register_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    student = get_object_or_404(Student, login_id=request.user.username)
    course.all_students.add(student)
    courses = student.course_set.all()
    return render(request,'index/courses.html',{'student': student,'INTERESTS':INTEREST_LIST,
                                                'courses':courses})

def course_info(request,course_id):
    course = get_object_or_404(Course, pk=course_id)
    student = get_object_or_404(Student, login_id=request.user.username)
    context = {'course': course, 'student':student}
    return render(request, 'index/course_info.html', context)

def add_assignment(request,topic_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        form = AssignmentForm(request.POST or None, request.FILES or None)
        student = get_object_or_404(Student, login_id=request.user.username)
        topic = get_object_or_404(Topic, pk=topic_id)
        if form.is_valid():
            a = Assignment()
            a.assignment_name = request.POST['assignment_name']
            a.assignment_content_file = request.FILES['assignment_file']
            a.parent_topic = topic
            a.assignment_info = request.POST['assignment_info']
            a.deadline = request.POST['deadline']

            a.save()
            student = get_object_or_404(Student, login_id=request.user.username)
            course = topic.course
            all_assignments = Assignment.objects.all()
            all_course_materials = Course_Material.objects.all()
            return render(request, 'index/detail.html',
                          {'student': student, 'course': course, 'topic': topic, 'all_assignments': all_assignments,
                           'all_course_materials': all_course_materials,'form':form})
        return render(request, 'index/add_assignment.html',{'student': student,'form':form,'topic': topic,})



def add_course_material(request,topic_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        form = MaterialForm(request.POST or None, request.FILES or None)
        student = get_object_or_404(Student, login_id=request.user.username)
        topic = get_object_or_404(Topic, pk=topic_id)
        if form.is_valid():
            a = Assignment()
            a.assignment_name = request.POST['assignment_name']
            a.assignment_content_file = request.FILES['assignment_file']
            a.parent_topic = topic
            a.assignment_info = request.POST['assignment_info']
            a.save()
            student = get_object_or_404(Student, login_id=request.user.username)
            course = topic.course
            all_assignments = Assignment.objects.all()
            all_course_materials = Course_Material.objects.all()
            all_quizzes = {}
            return render(request, 'index/detail.html',
                          {'student': student, 'course': course, 'topic': topic, 'all_assignments': all_assignments,
                           'all_course_materials': all_course_materials,'form':form,'all_quizzes':all_quizzes})
        return render(request, 'index/add_assignment.html',{'student': student,'form':form,'topic': topic,})


def refresh_feed(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)

        for feed in News_feed.objects.all():
            feed.delete()

        for tag in tags:
            quote_page = requests.get('http://news.mit.edu/topic/' + tag)

            # print (quote_page.text)

            soup = BeautifulSoup(quote_page.text, 'lxml')

            for u in soup.find_all("ul", class_="view-news-items"):
                for l in u.find_all("li"):
                    a = News_feed()
                    a.topic = str(l.find("h3").text)
                    a.tag = str(tag)
                    a.my_tag = tag_link[a.tag]
                    a.desc = str(l.find("p").text)
                    a.image_url = str(l.find("img"))
                    a.date = str(l.find("em").text)
                    m = re.search('href="(.+?)">', str(l.find("h3").a))
                    if m:
                        found = m.group(1)
                        a.href_url = "http://news.mit.edu" + str(found)
                    a.save()

        news_feed = News_feed.objects.all()
        interests = Interest.objects.filter(all_students=student)
        interests_name = map(lambda inter: inter.interest_name, interests)
        return render(request, 'index/index.html', {'course_lists': course_lists, 'student': student,
                                                    'news_feed': news_feed,'interests':interests,'interests_name':interests_name})

def add_resourse(request,topic_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        form = MaterialForm(request.POST or None, request.FILES or None)
        student = get_object_or_404(Student, login_id=request.user.username)
        topic = get_object_or_404(Topic, pk=topic_id)
        if form.is_valid():
            a = Course_Material()
            a.course_material_name = request.POST['material_name']
            a.course_content_file = request.FILES['material_file']
            a.parent_topic = topic
            a.course_material_info = request.POST['material_info']

            a.save()
            student = get_object_or_404(Student, login_id=request.user.username)
            course = topic.course
            all_assignments = Assignment.objects.all()
            all_course_materials = Course_Material.objects.all()
            return render(request, 'index/detail.html',
                          {'student': student, 'course': course, 'topic': topic, 'all_assignments': all_assignments,
                           'all_course_materials': all_course_materials,'form':form})
        return render(request, 'index/add_resourse.html',{'student': student,'form':form,'topic': topic,})

def add_quiz(request,topic_id):
    form = QuizForm(request.POST or None, request.FILES or None)
    student = get_object_or_404(Student, login_id=request.user.username)
    topic = get_object_or_404(Topic, pk=topic_id)

    if form.is_valid():
        a= Quiz()
        a.parent_topic = topic
        a.quiz_name = request.POST['quiz_name']
        a.quiz_info = request.POST['quiz_info']
        a.save()
        return render(request, 'index/add_question.html',
                      {'student': student,'topic': topic,
                       'form': form,'quiz':a })
    return render(request, 'index/add_quiz.html', {'student': student, 'form': form,
                                                       'topic': topic })

def add_question(request,topic_id,quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')

    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        topic = get_object_or_404(Topic, pk=topic_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        a= Question()
        a.parent_quiz = quiz
        a.question_text = request.POST['question_text']
        temp = request.POST['is_subjective']
        if temp=='subjective':
            a.is_subjective = True
        else:
            a.is_subjective = False

        a.option1 = request.POST['option1']
        a.option2 = request.POST['option2']
        a.option3 = request.POST['option3']
        a.option4 = request.POST['option4']

        a.correct_answer = request.POST['correct_answer']
        a.save()
        questions = quiz.question_set.all()

        return render(request, 'index/quiz.html',
                      {'student': student,'topic': topic,'questions':questions,'quiz':quiz})

def add_another_question(request,quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        # topic = get_object_or_404(Topic, pk=topic_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = quiz.question_set.all()
        topic = quiz.parent_topic
        return render(request, 'index/add_question.html',
                      {'student': student, 'questions': questions, 'topic': topic,'quiz':quiz})


def take_quiz(request,quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        #topic = get_object_or_404(Topic, pk=topic_id)
        quiz =  get_object_or_404(Quiz, pk=quiz_id)
        if not student.is_professor:
            a=Grade()
            a.parent_student =student
            a.parent_quiz = quiz
            a.quiz_attempted = True
            a.save()

        questions = quiz.question_set.all()
        topic = quiz.parent_topic
        return render(request, 'index/quiz.html',
                      {'student': student,'questions':questions,'topic':topic,'quiz':quiz})

#Evaluating the questions
def evaluate_quiz(request, quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        # topic = get_object_or_404(Topic, pk=topic_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = quiz.question_set.all()
        topic = quiz.parent_topic
        if request.method == "POST":

            total = 0
            obtained_marks = 0

            for question in questions:
                try:
                    temp = request.POST['question' + str(question.id)]
                except:
                    temp=""
                rec = Answer_record()
                rec.parent_question = question
                rec.parent_student = student
                rec.ans_given = str(temp)
                rec.save()

                if temp:
                    if temp==question.correct_answer:
                        obtained_marks+=4
                    else:
                        obtained_marks-=1

                total+=4


            a= get_object_or_404(Grade,parent_student=student,parent_quiz=quiz)

            a.total_marks = total
            a.marks_obtained = obtained_marks
            a.save()
            rec = student.answer_record_set.all()
            return render(request, 'index/quiz_result.html',
                          {'student': student,'questions':questions,'topic':topic,'quiz':quiz,
                           'grade':a,'record':rec})

        else:
            try:
                a = Grade.objects.get(parent_student=student, parent_quiz=quiz)
            except:
                a = None
            rec = student.answer_record_set.all()
            return render(request, 'index/quiz_result.html',
                          {'student': student, 'questions': questions, 'topic': topic,
                           'quiz': quiz,'grade':a,'record':rec})


def result(request, quiz_id):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    else:
        student = get_object_or_404(Student, login_id=request.user.username)
        # topic = get_object_or_404(Topic, pk=topic_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = quiz.question_set.all()
        topic = quiz.parent_topic

        try:
            a = Grade.objects.get(parent_student=student,parent_quiz=quiz)
        except:
            a = None
        rec = student.answer_record_set.all()
        return render(request, 'index/quiz_result.html',
                      {'student': student, 'questions': questions, 'topic': topic, 'quiz': quiz,
                       'grade':a,'record':rec})
