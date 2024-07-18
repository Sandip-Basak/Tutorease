from django.shortcuts import render,redirect
from home.models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
import requests
import json
import random


# Create your views here.

# Privacy Policy
def privacy(request):
    return render(request, 'privacy.html')

def home(request):
    return render(request, 'index.html')

def question(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if(request.GET.get('d') and request.session.get('stage',False) and request.session.get('level',False)):
                user=UserProgressData.objects.get(username=request.user.username,course=request.session['code'])
                lesson=request.GET.get('d')
                lesson=int(lesson.split()[-1])

                if(lesson<=user.lesson or request.session['level']<user.level or request.session['stage']<user.stage):
                    stage=request.session.get('stage',False)
                    level=request.session.get('level',False)
                    request.session['progress']=True
                    request.session['lesson']=lesson

                    if(Lessons.objects.filter(code=request.session['code'],stage_number=stage,level=level,lesson_no=lesson).exists()):
                        mcq1=MCQ_Data.objects.filter(code=request.session['code'],stage_number=stage,level=level,lesson_no=lesson)
                        mcq2=MCQ_Pic_Data.objects.filter(code=request.session['code'],stage_number=stage,level=level,lesson_no=lesson)
                        mcq3=MCQ.objects.filter(code=request.session['code'],stage_number=stage,level=level,lesson_no=lesson)
                        arrange=Arrange.objects.filter(code=request.session['code'],stage_number=stage,level=level,lesson_no=lesson)
                        match=Match.objects.filter(code=request.session['code'],stage_number=stage,level=level,lesson_no=lesson)
                        return render(request, "questions.html",{"mcq1":mcq1,"mcq2":mcq2,"mcq3":mcq3,"arrange":arrange,"match":match,"lesson":lesson})
                    else:
                        return redirect('/home')
                else:
                    messages.warning(request, f"Finish the previous lessons to access lesson {lesson}")
                    return redirect(f'/lesson?d={request.session["level"]}')
            else:
                return redirect('/home')
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')

# Work to be done here in finish
def finish(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if(request.session.get('lesson',False) and request.session.get('stage',False) and request.session.get('level',False) and request.session.get('progress',False)):
                user=UserProgressData.objects.filter(username=request.user.username,course=request.session['code'])[0]
                progress=request.session.get('progress')
                if(progress==True and int(request.session['lesson'])==user.lesson and int(request.session['level'])==user.level and int(request.session['stage'])==user.stage):
                    user.lesson += 1

                    level=Levels.objects.filter(code=user.course,stage_number=request.session['stage'],level=request.session['level'])
                    if(user.lesson>level[0].total_lessons):
                        user.lesson = 1
                        user.level += 1

                        stage=Stages.objects.filter(code=user.course,stage_number=request.session['stage'])
                        if(user.level>stage[0].total_levels):
                            user.level = 1
                            user.stage += 1
                    user.save()

            if(request.session.get('lesson',False)):
                del request.session['lesson']
            if(request.session.get('progress',False)):
                del request.session['progress']
            if(request.session.get('question_data',False)):
                del request.session['question_data']
            
            data={"Data_Updated": True}
            return JsonResponse(data)
        except:
            data={"Data_Updated": False}
            return JsonResponse(data)


def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
             messages.warning(request, "Invalid Login Credentials")
    if not request.user.is_anonymous:
        return redirect('/signup')
    else:
        return render(request, 'login.html')

def signupPage(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        name=request.POST.get('name')
        username=request.POST.get('username')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        referal_code=request.POST.get('referal')


        if "" not in (email,name,gender,password,repassword):

            if User.objects.filter(username=username).exists():

                messages.warning(request, "Account already exists with this Email ID !!!")
            else:
                try:
                    if password==repassword:
                        if (not "" == referal_code) and (Institution.objects.filter(referal_code=referal_code).exists()):
                            institute=Institution.objects.get(referal_code=referal_code)

                            if(institute.total_students<institute.max_students):
                                user=User.objects.create_user(email=email,username=username,password=password)
                                user.email=email
                                na=name.split()
                                user.first_name=na[0]
                                user.last_name=na[-1]
                                user.save()

                                institute.total_students += 1
                                institute.save()
                                userdata=UserData(username=username, name=name, gender=gender,institute_code=institute.institute_code)
                                userdata.save()
                                messages.success(request, "Account Created !!!Now you may Login")
                                return redirect('/login')
                            else:
                                messages.warning(request,"Invalid Referal Code")
                        elif "" == referal_code:
                            user=User.objects.create_user(email=email,username=username,password=password)
                            user.email=email
                            na=name.split()
                            user.first_name=na[0]
                            user.last_name=na[-1]
                            user.save()

                            userdata=UserData(username=username, name=name, gender=gender)
                            userdata.save()
                            messages.success(request, "Account Created !!!Now you may Login")
                            return redirect('/login')
                        else:
                            messages.warning(request,"Invalid Referal Code")
                    else:
                        messages.warning(request,"Passwords dosent match !!! Try again")
                except Exception as e:
                    # print(e)
                    messages.warning(request, "Some Error Occured !!! Please try again")
        else:

            messages.add_message(request,messages.INFO,"Field Empty !!! Please fill the form")
    if not request.user.is_anonymous:
        return redirect('/home')
    else:
        return render(request, 'signup.html')


def course(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            user=UserData.objects.filter(username=request.user.username)[0]
            if(user.course==""):
                if(request.GET.get('d')):
                    course=request.GET.get('d')
                    userdata=UserData.objects.filter(username=request.user.username)[0]
                    userdata.course=course
                    userdata.save()
                    return redirect("/home")
                else:
                    return render(request, 'course.html', {'course':All_Course_Details.objects.filter(institute_code=user.institute_code),'institution_data':request.session['institute_data']})
            else:
                return redirect("/home")
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')


def logged(request):
    if request.user.is_anonymous:
        return redirect("/")
    else:
        try:
            user=UserData.objects.filter(username=request.user.username)[0]

            if not request.session.get('institute_data',False):
                if user.institute_code!='SELF':
                    institute=Institution.objects.get(institute_code=user.institute_code)
                    institution_data={
                        'institute_code': user.institute_code,
                        'institute_name': institute.name,
                        'institute_logo': f"/media/{institute.logo}"
                    }
                else:
                    institution_data={
                        'institute_code': 'SELF',
                        'institute_name': 'Tutorease',
                        'institute_logo': 'static/images/bnw logo.png'
                    }
                request.session['institute_data']=institution_data

            if(user.course==""):
                return redirect("/course")
            if request.session.get('stage',False):
                del request.session['stage']
            if request.session.get('level',False):
                del request.session['level']
            if request.session.get('lesson',False):
                del request.session['lesson']
            if request.session.get('exam',False):
                del request.session['exam']
            if request.session.get('mock_test_no',False):
                del request.session['mock_test_no']
            if request.session.get('exam_type',False):
                del request.session['exam_type']

            request.session['code']=user.course
            request.session['institute_code']=user.institute_code

            data=UserProgressData.objects.filter(username=request.user.username,course=user.course)
            request.session['approved']=data[0].approved
            if data[0].approved:
                return render(request, 'home.html', {'UserData':data,'Levels': Stages.objects.filter(code=user.course),'institution_data':request.session['institute_data']})
            else:
                messages.warning(request,"The Course is not approved by your Institution")
                return render(request, 'home.html', {'UserData':data,'institution_data':request.session['institute_data']})
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/')


def practice_exam(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if request.session['approved']:
                if not "exam" in request.session:
                    request.session["exam"]=True
                    if request.session.get('stage',False) and request.session.get('level',False):
                        stage=request.session.get('stage')
                        level=request.session.get('level')

                        mcq1=get_random_objects(MCQ_Data.objects.filter(code=request.session['code'],stage_number=stage,level=level),5)
                        mcq2=get_random_objects(MCQ_Pic_Data.objects.filter(code=request.session['code'],stage_number=stage,level=level),5)
                        mcq3=get_random_objects(MCQ.objects.filter(code=request.session['code'],stage_number=stage,level=level),5)
                        time=15
                        total_marks=15
                    elif request.session.get('stage',False):
                        stage=request.session.get('stage')
                        mcq1=get_random_objects(MCQ_Data.objects.filter(code=request.session['code'],stage_number=stage),10)
                        mcq2=get_random_objects(MCQ_Pic_Data.objects.filter(code=request.session['code'],stage_number=stage),10)
                        mcq3=get_random_objects(MCQ.objects.filter(code=request.session['code'],stage_number=stage),10)
                        time=30
                        total_marks=30
                    else:
                        mcq1=get_random_objects(MCQ_Data.objects.filter(code=request.session['code']),10)
                        mcq2=get_random_objects(MCQ_Pic_Data.objects.filter(code=request.session['code']),10)
                        mcq3=get_random_objects(MCQ.objects.filter(code=request.session['code']),10)
                        time=30
                        total_marks=30

                    return render(request, 'exam.html',{"mcq1":mcq1,"mcq2":mcq2,"mcq3":mcq3,"time":time,"total_marks":total_marks,"data_save": False})
                else:
                    messages.warning(request, "Security Problem ! You may now restart your exam")
                    return redirect("/home")
            else:
                return redirect("/home")
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')

def mock_exam(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if request.session['approved']:
                if request.GET.get('d') and request.GET.get('t')=='mock' and Mock_Test.objects.filter(code=request.session['code'],Mock_Test_Number=request.GET.get('d'),approved=True).exists():
                    if not "exam" in request.session:
                        d=int(request.GET.get('d'))
                        mock=Mock_Test.objects.get(code=request.session['code'],Mock_Test_Number=d,approved=True)
                        if len(Mock_Test_Results.objects.filter(username=request.user.username,code=request.session['code'],Mock_Test_Number=d))<mock.number_of_attempts:
                            request.session["exam"]=True
                            request.session["exam_type"]="mock"
                            request.session["mock_test_no"]=d
                            mcq1=Mock_Test_MCQ_Type_1.objects.filter(code=request.session['code'],Mock_Test_Number=d)
                            mcq2=Mock_Test_MCQ_Pic_Data_Type_2.objects.filter(code=request.session['code'],Mock_Test_Number=d)
                            mcq3=Mock_Test_MCQ_Type_3.objects.filter(code=request.session['code'],Mock_Test_Number=d)
                            time=mock.Total_Time
                            total_marks=mock.Total_Marks
                            return render(request, 'exam.html',{"mcq1":mcq1,"mcq2":mcq2,"mcq3":mcq3,"time":time,"total_marks":total_marks,"data_save": True})
                        else:
                            messages.warning(request, "You have reached the limit for attempts permitted")
                            return redirect("/mockexam")
                    else:
                        messages.warning(request, "Security Problem ! You may now restart your exam")
                        return redirect("/home")
                elif request.GET.get('d') and request.GET.get('t')=='written_mock' and Written_Mock_Test.objects.filter(code=request.session['code'],Mock_Test_Number=request.GET.get('d'),approved=True).exists():
                    if not "exam" in request.session:
                        d=int(request.GET.get('d'))
                        written_mock=Written_Mock_Test.objects.get(code=request.session['code'],Mock_Test_Number=d,approved=True)
                        if len(Written_Mock_Test_Results.objects.filter(username=request.user.username,code=request.session['code'],Mock_Test_Number=d))<written_mock.number_of_attempts:
                            request.session["exam"]=True
                            request.session["exam_type"]="written_mock"
                            request.session["mock_test_no"]=d
                            time=written_mock.Total_Time
                            total_marks=written_mock.Total_Marks
                            return render(request, 'writtenmocktest.html',{"written_mock":written_mock,"time":time,"total_marks":total_marks,"data_save": True})
                        else:
                            messages.warning(request, "You have reached the limit for attempts permitted")
                            return redirect("/mockexam")
                    else:
                        messages.warning(request, "Security Problem ! You may now restart your exam")
                        return redirect("/home") 
                else:
                    if Mock_Test.objects.filter(code=request.session['code'],approved=True).exists() or Written_Mock_Test.objects.filter(code=request.session['code'],approved=True).exists():
                        return render(request, 'mock.html',{"mock": Mock_Test.objects.filter(code=request.session['code'],approved=True),"mock_results": Mock_Test_Results.objects.filter(username=request.user.username,institute_code=request.session["institute_code"],code=request.session["code"]),"written_mock": Written_Mock_Test.objects.filter(code=request.session['code'],approved=True),"written_mock_results": Written_Mock_Test_Results.objects.filter(username=request.user.username,institute_code=request.session["institute_code"],code=request.session["code"],checked=True)})
                    else:
                        messages.warning(request, "No Mock Test available for now")
                        return redirect("/home")
            else:
                return redirect("/home")
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')

def course_material(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if request.session['approved']:
                if request.GET.get('d') and Course_Material.objects.filter(code=request.session['code'],institute_code=request.session['institute_code'] , topic=request.GET.get('d'),approved=True).exists():
                    data=Course_Material.objects.filter(code=request.session['code'],institute_code=request.session['institute_code'] , topic=request.GET.get('d'),approved=True)
                    return render(request, 'videopage.html',{"materials": data,'institution_data':request.session['institute_data']})
                else:
                    if Course_Topic.objects.filter(code=request.session['code'],approved=True).exists():
                        return render(request, 'course_topic.html',{"topics": Course_Topic.objects.filter(code=request.session['code'],approved=True),'institution_data':request.session['institute_data']})
                    else:
                        messages.warning(request, "No Course Material available for now")
                        return redirect("/home")
            else:
                return redirect("/home")
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')   


def exam_result(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if request.session['approved'] and request.GET.get('d') and "exam" in request.session and "mock_test_no" in request.session and request.session["exam_type"]=="mock":
                marks=int(request.GET.get('d'))
                mock_test_no=request.session["mock_test_no"]
                mock_data=Mock_Test.objects.get(code=request.session['code'],Mock_Test_Number=mock_test_no)
                data=Mock_Test_Results(username=request.user.username,institute_code=mock_data.institute_code,
                                       code=request.session['code'],Mock_Test_Number=mock_test_no,marks=marks,
                                       Total_Marks=mock_data.Total_Marks, Total_Time=mock_data.Total_Time)
                data.save()
                data={"Data_Updated": True}
                return JsonResponse(data)
            else:
                data={"Data_Updated": False}
                return JsonResponse(data)
        except:
            data={"Data_Updated": False}
            return JsonResponse(data)


def written_mock_result(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if request.method == 'POST':
                if request.session['approved'] and "exam" in request.session and "mock_test_no" in request.session and request.session["exam_type"]=="written_mock":
                    uploaded_file = request.FILES['upload']
                    mock_test_no=request.session["mock_test_no"]
                    written_mock_data=Written_Mock_Test.objects.get(code=request.session['code'],Mock_Test_Number=mock_test_no)
                    data=Written_Mock_Test_Results(username=request.user.username,institute_code=request.session["institute_code"],
                                        code=request.session['code'],Mock_Test_Number=mock_test_no,marks=0,
                                        Total_Marks=written_mock_data.Total_Marks, Total_Time=written_mock_data.Total_Time,
                                        question_link=written_mock_data.question_paper,answer_sheet=uploaded_file)
                    data.save()
            elif request.method == 'GET':
                if request.session['approved'] and "exam" in request.session and "mock_test_no" in request.session and request.session["exam_type"]=="written_mock" and request.GET.get('d')=="failed":
                    mock_test_no=request.session["mock_test_no"]
                    written_mock_data=Written_Mock_Test.objects.get(code=request.session['code'],Mock_Test_Number=mock_test_no)
                    data=Written_Mock_Test_Results(username=request.user.username,institute_code=request.session["institute_code"],
                                        code=request.session['code'],Mock_Test_Number=mock_test_no,marks=0,
                                        Total_Marks=written_mock_data.Total_Marks, Total_Time=written_mock_data.Total_Time,
                                        question_link=written_mock_data.question_paper,checked=True)
                    data.save()

            return redirect('/home')
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')


def get_random_objects(all_objects,num):

    # Shuffle the queryset to randomize the order
    random_objects = list(all_objects.order_by('?'))

    # Slice the queryset to get the desired number of random objects
    random_objects = random_objects[:num]

    return random_objects

def logoutPage(request):
    logout(request)
    return redirect("/")

def profile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            user=UserProgressData.objects.get(username=request.user.username,course=request.session['code'])
            course=All_Course_Details.objects.get(code=request.session['code'])
            joining_date=User.objects.get(username=request.user.username).date_joined
            joining_date=joining_date.strftime('%d/%m/%Y')

            if Stages.objects.filter(code=request.session['code'],stage_number=user.stage).exists():
                stage=Stages.objects.get(code=request.session['code'],stage_number=user.stage)
                progress=int((user.level-1)/stage.total_levels*100)
            else:
                stage=Stages.objects.get(code=request.session['code'],stage_number=user.stage-1)
                progress=100
            return render(request, 'profile.html', {'UserData':UserData.objects.filter(username=request.user.username,course=user.course),"stage_name": stage.stage_name,"course": course,"progress": progress,"level":user.level,"joining_date": joining_date,'institution_data':request.session['institute_data']})
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')



def level(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if(request.GET.get('d') and request.session['approved']):
                user=UserProgressData.objects.filter(username=request.user.username,course=request.session['code'])
                level=int(request.GET.get('d'))
                if(level<=user[0].stage):
                    request.session['stage']=level
                    return render(request, 'level.html', {'Levels':Levels.objects.all().filter(code=user[0].course,stage_number=level),'UserData':user,'institution_data':request.session['institute_data']})
                else:
                    messages.warning(request, f"Finish the previous Stage to access {Stages.objects.all().filter(stage_number=level,code=request.session['code'])[0].stage_name} Stage")

            return redirect('/home')
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')


def lesson(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            if(request.GET.get('d') and request.session['approved']):
                # user_data=UserData.objects.filter(username=request.user.username)[0]
                user=UserProgressData.objects.filter(username=request.user.username,course=request.session['code'])
                level=int(request.GET.get('d'))
                if(level<=user[0].level or request.session['stage']<user[0].stage):
                    request.session['level']=level
                    return render(request, 'lessons.html', {'lesson':Lessons.objects.all().filter(code=user[0].course,stage_number=request.session['stage'],level=level),'institution_data':request.session['institute_data']})
                else:
                    messages.warning(request, f"Finish the previous levels to access Level {level}")
                    return redirect(f'/level?d={request.session["stage"]}')
            return redirect('/home')
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')


def setting(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        try:
            user=User.objects.get(username=request.user.username)
            user_data=UserData.objects.get(username=request.user.username)
            course=All_Course_Details.objects.get(code=user_data.course)
            request.session['code']=user_data.course

            data={
                "username": user.username,
                "email": user.email,
                "name": user_data.name,
                "course": course,
                "gender": user_data.gender
            }

            return render(request, 'settings.html', {"data": data, "course": All_Course_Details.objects.filter(~Q(code=user_data.course),institute_code=user_data.institute_code),'institution_data':request.session['institute_data']})
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')


def profilesettings(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        if request.method == 'POST':
            email=request.POST.get('email')
            name=request.POST.get('name')
            gender=request.POST.get('gender')
            course=request.POST.get('course')
            if "" not in (email,name,gender,course):
                try:
                    user=User.objects.filter(username=request.user.username)[0]
                    temp_name=name.split()
                    firstname,lastname=temp_name[0],temp_name[-1]
                    user.first_name=firstname
                    user.last_name=lastname
                    user.email=email
                    user.save()

                    user_data=UserData.objects.filter(username=request.user.username)[0]
                    user_data.name=name
                    user_data.course=course
                    user_data.gender=gender
                    user_data.save()
                    messages.success(request, "Profile updated")
                except:
                    messages.warning(request, "Some error occured")

            else:
                messages.warning(request, "Field empty !")
            return redirect("/settings")


def usersettings(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        if request.method == 'POST':
            pre_pass=request.POST.get('prepassword')
            new_pass=request.POST.get('newpassword')
            renew_pass=request.POST.get('renewpassword')
            if new_pass==renew_pass:
                if authenticate(username=request.user.username,password=pre_pass)!=None:
                    try:
                        user=User.objects.get(username=request.user.username)
                        user.set_password(new_pass)
                        user.save()
                        messages.success(request,"Password changed successfully")
                    except:
                        messages.warning(request,"Some error occured")
                else:
                    messages.warning(request,"Previous password dosen't match")
            else:
                messages.warning(request, "Passwords dosen't match")

        return redirect("/settings")

def help(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        try:
            if request.method == 'POST':
                msg=request.POST.get('msg')
                try:
                    data=User_Query(username=request.user.username, query=msg)
                    data.save()
                except:
                    messages.warning(request,"Some error occured !!! Try again")

            query = User_Query.objects.filter(username=request.user.username).order_by('-id').values()
            return render(request,'help.html',{'query': query,'institution_data':request.session['institute_data']})
        except:
            messages.warning(request, "Oops! Our server messed up")
            return redirect('/home')



def test(request):
    if request.user.is_superuser:
        if request.method == "GET" and request.GET.get('data')=='start':
            pass
        return render(request, "test.html")
    else:
        return redirect('/')
