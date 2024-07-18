from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name="home"),
    path('question', views.question,name="question"),
    path('login', views.loginPage,name="login"),
    path('home', views.logged,name="logged"),
    path('signup', views.signupPage,name="signup"),
    path('logout', views.logoutPage,name="logout"),
    path('profile', views.profile,name="profile"),
    path('help', views.help,name="help"),
    path('lesson', views.lesson,name="lesson"),
    path('level', views.level,name="level"),
    path('finish', views.finish,name="finish"),
    path('settings', views.setting,name="settings"),
    path('settings/profilesettings', views.profilesettings,name="profilesettings"),
    path('settings/usersettings', views.usersettings,name="usersettings"),
    path('course', views.course,name="course"),
    path('privacypolicy', views.privacy,name="privacy"),
    path('practiceexam', views.practice_exam,name="practiceexam"),
    path('mockexam', views.mock_exam,name="mockexam"),
    path('examresult', views.exam_result,name="examresult"),
    path('writtenmockresult', views.written_mock_result,name="writtenmockresult"),
    path('coursematerial', views.course_material,name="coursematerial"),
    path('test', views.test,name="test"),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)