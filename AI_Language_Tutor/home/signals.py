# Signals
from home.models import *
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import user_logged_in, user_logged_out


# Lessons Updated
@receiver(post_save, sender=Lessons)
def Lessons_Created_Handler(sender, instance, created, *args, **kwargs):
    if created:
        print(f"New Lesson Created:- Code-{instance.code}, Stage No.-{instance.stage_number}, Level-{instance.level}, Lesson-{instance.lesson_no}")
        level=Levels.objects.filter(code=instance.code,stage_number=instance.stage_number,level=instance.level)
        if(len(level)==1):
            level[0].total_lessons=len(Lessons.objects.filter(code=instance.code,stage_number=instance.stage_number,level=instance.level))
            level[0].save()
    else:
        print("Old Data is re-saved")
        level=Levels.objects.filter(code=instance.code,stage_number=instance.stage_number,level=instance.level)
        if(len(level)==1):
            level[0].total_lessons=len(Lessons.objects.filter(code=instance.code,stage_number=instance.stage_number,level=instance.level))
            level[0].save()


@receiver(post_delete, sender=Lessons)
def Lessons_Deleted_Handler(sender, instance, *args, **kwargs):
    print(f"Lesson Deleted:- Code-{instance.code}, Stage No.-{instance.stage_number}, Level-{instance.level}, Lesson-{instance.lesson_no}")
    level=Levels.objects.filter(code=instance.code,stage_number=instance.stage_number,level=instance.level)
    if(len(level)==1):
        level[0].total_lessons=len(Lessons.objects.filter(code=instance.code,stage_number=instance.stage_number,level=instance.level))
        level[0].save()



# Levels Updated
@receiver(post_save, sender=Levels)
def Levels_Created_Handler(sender, instance, created, *args, **kwargs):
    if created:
        print(f"New Level Created:- Code-{instance.code}, Stage No.-{instance.stage_number}, Level-{instance.level}")
        stage=Stages.objects.filter(code=instance.code,stage_number=instance.stage_number)
        if(len(stage)==1):
            stage[0].total_levels=len(Levels.objects.filter(code=instance.code,stage_number=instance.stage_number))
            stage[0].save()
    else:
        print("Old Data is re-saved")
        stage=Stages.objects.filter(code=instance.code,stage_number=instance.stage_number)
        if(len(stage)==1):
            stage[0].total_levels=len(Levels.objects.filter(code=instance.code,stage_number=instance.stage_number))
            stage[0].save()


@receiver(post_delete, sender=Levels)
def Levels_Deleted_Handler(sender, instance, *args, **kwargs):
    print(f"Level Deleted:- Code-{instance.code}, Stage No.-{instance.stage_number}, Level-{instance.level}")
    stage=Stages.objects.filter(code=instance.code,stage_number=instance.stage_number)
    if(len(stage)==1):
        stage[0].total_levels=len(Levels.objects.filter(code=instance.code,stage_number=instance.stage_number))
        stage[0].save()

# User Updated
@receiver(post_save, sender=UserData)
def UserData_Created_Handler(sender, instance, created, *args, **kwargs):
    if not created:
        print("Old Data is re-saved")
        if(not UserProgressData.objects.filter(username=instance.username,course=instance.course).exists()):
            if instance.institute_code=="SELF":
                data=UserProgressData(username=instance.username,course=instance.course,approved=True,stage=1,level=1,lesson=1)
            else:
                data=UserProgressData(username=instance.username,course=instance.course,stage=1,level=1,lesson=1)
            data.save()


@receiver(post_delete, sender=UserData)
def UserData_Deleted_Handler(sender, instance, *args, **kwargs):
    print(f"User Deleted")
    data=UserProgressData.objects.filter(username=instance.username)
    for i in data:
        i.delete()


# User Delete
@receiver(post_delete, sender=User)
def User_Deleted_Handler(sender, instance, *args, **kwargs):
    print(f"User Deleted")
    data=UserData.objects.filter(username=instance.username)
    institute_code=data[0].institute_code

    for i in data:
        i.delete()

    data=User_Query.objects.filter(username=instance.username)
    for i in data:
        i.delete()

    if institute_code!="SELF":
        institute=Institution.objects.get(institute_code=institute_code)
        institute.total_students=len(UserData.objects.filter(institute_code=institute_code))
        institute.save()
    



# Institution Course Updated
@receiver(post_save, sender=All_Course_Details)
def Institute_Course_Created_Handler(sender, instance, created, *args, **kwargs):
    if created:
        print(f"New SELF Course Created:- Code-{instance.code}, Institute Code-{instance.institute_code}, Name-{instance.name}, Description-{instance.description}")
        institute=Institution.objects.get(institute_code=instance.institute_code)
        institute.no_of_courses=len(All_Course_Details.objects.filter(institute_code=instance.institute_code))
        institute.save()
    else:
        print("Old Data is re-saved")
        institute=Institution.objects.get(institute_code=instance.institute_code)
        institute.no_of_courses=len(All_Course_Details.objects.filter(institute_code=instance.institute_code))
        institute.save()


@receiver(post_delete, sender=All_Course_Details)
def Institute_Course_Deleted_Handler(sender, instance, *args, **kwargs):
    print(f"SELF Course Deleted:- Code-{instance.code}, Institute Code-{instance.institute_code}, Name-{instance.name}, Description-{instance.description}")
    institute=Institution.objects.get(institute_code=instance.institute_code)
    institute.no_of_courses=len(All_Course_Details.objects.filter(institute_code=instance.institute_code))
    institute.save()




# Security: One user one session, adding session to LoggedInUser
@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))

@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()