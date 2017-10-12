from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout,get_user_model
from .models import student
from .forms import UserForm,RegisterForm
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
number_list = {
    'cs101':'1','1':'cs101',
    'cs152':'2','2':'cs152',
    'cs154':'3','3':'cs154',
    'cs207':'4','4':'cs207',
    'cs213':'5','5':'cs213',
    'cs215':'6','6':'cs215',
    'cs251':'7','7':'cs251',
    'cs293':'8','8':'cs293',
}

def first_login(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')

    else:
        students = student.objects.get(login_id=request.user.username)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        institute = request.POST['institute']
        graduation = request.POST['graduation']
        year = request.POST['year']
        city = request.POST['city']
        course_list = request.POST.getlist('course_list')

        for code in course_list:
            students.courses += number_list[code]
        student_course = students.courses
        students.first_name= first_name
        students.last_name= last_name
        students.phone= phone
        students.institute= institute
        students.graduation= graduation
        students.year = year
        students.city= city
        students.save()
        return render(request,'index/index.html', {'course_lists':course_lists,'students':students,
                                                   'course_list':course_list,'number_list':number_list,
                                                   'student_course':student_course})

    return render(request, 'index/login.html')


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'index/login.html')
    # else:
    #     students = student.objects.filter(user=request.user)
    #     query = request.GET.get("q")
    #     if query:
    #         students = students.filter(
    #             Q(album_title__icontains=query) |
    #             Q(artist__icontains=query)
    #         ).distinct()
    #         return render(request, 'index/index.html', {'students': students,'course_lists':course_lists})
    else:
        students = student.objects.get(login_id=request.user.username)
        student_course = students.courses
        return render(request, 'index/index.html', {'course_lists':course_lists,'students':students,
                                                    'number_list': number_list,'student_course':student_course})

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
                students = student.objects.get(login_id=request.user.username)
                student_course = students.courses
                return render(request, 'index/index.html', {'students': students,'course_lists':course_lists,
                                                            'number_list': number_list,'student_course':student_course})
            else:
                return render(request, 'index/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'index/login.html', {'error_message': 'Invalid login'})
    return render(request, 'index/login.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():

        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        user.set_password(password)
        user.save()
        a= student(fname=first_name,lname=last_name,login_id=username,email_id=email)
        a.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                students = student.objects.filter(user=request.user)
                return render(request, 'index/first_login.html', {'students': students,'course_lists':course_lists})
    context = {
        "form": form,
    }
    return render(request, 'index/register.html', context)

