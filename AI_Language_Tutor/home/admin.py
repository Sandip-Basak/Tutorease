from typing import Any
from django.contrib import admin
from home.models import *



# Filters
class InstituteFilter(admin.SimpleListFilter):
    title = 'Institute'
    parameter_name = 'institute_code'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            institutes = Institution.objects.values_list('institute_code', flat=True).distinct()
            return [(institute, institute) for institute in institutes]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(institute_code=self.value())

class CodeFilter(admin.SimpleListFilter):
    title = 'Code'
    parameter_name = 'code'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            codes = All_Course_Details.objects.values_list('code', flat=True).distinct()
            return [(code, code) for code in codes]
        else:
            user=UserData.objects.get(username=request.user.username)
            codes = All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True).distinct()
            return [(code, code) for code in codes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(code=self.value())
        
class TopicFilter(admin.SimpleListFilter):
    title = 'Topic'
    parameter_name = 'topic'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            topics=Course_Topic.objects.values_list('topic', flat=True).distinct()
            return [(topic, topic) for topic in topics]
        else:
            user=UserData.objects.get(username=request.user.username)
            topics=Course_Topic.objects.filter(institute_code=user.institute_code).values_list('topic', flat=True).distinct()
            return [(topic, topic) for topic in topics]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(topic=self.value())


# UserData and UserProgressData has course instead of code field       
class UserCourseFilter(admin.SimpleListFilter):
    title = 'Code'
    parameter_name = 'code'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            codes = All_Course_Details.objects.values_list('code', flat=True).distinct()
            return [(code, code) for code in codes]
        else:
            user=UserData.objects.get(username=request.user.username)
            codes = All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True).distinct()
            return [(code, code) for code in codes]

    def queryset(self, request, queryset):
        if self.value():
            # Thats why its dublicate
            return queryset.filter(course=self.value())

class StageNumberFilter(admin.SimpleListFilter):
    title = 'Stage Number'
    parameter_name = 'stage_number'

    def lookups(self, request, model_admin):
        stage_numbers = Stages.objects.values_list('stage_number', flat=True).distinct()
        return [(stage_number, stage_number) for stage_number in stage_numbers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stage_number=self.value())

class LevelFilter(admin.SimpleListFilter):
    title = 'Level'
    parameter_name = 'level'

    def lookups(self, request, model_admin):
        levels = Levels.objects.values_list('level', flat=True).distinct()
        return [(level, level) for level in levels]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(level=self.value())

class LessonNoFilter(admin.SimpleListFilter):
    title = 'Lesson Number'
    parameter_name = 'lesson_no'

    def lookups(self, request, model_admin):
        lesson_numbers = Lessons.objects.values_list('lesson_no', flat=True).distinct()
        return [(lesson_no, lesson_no) for lesson_no in lesson_numbers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(lesson_no=self.value())
        
class MockTestNoFilter(admin.SimpleListFilter):
    title = 'Mock Test No'
    parameter_name = 'Mock_Test_Number'

    def lookups(self, request, model_admin):
        mock_numbers = Mock_Test.objects.values_list('Mock_Test_Number', flat=True).distinct()
        return [(mock_no, mock_no) for mock_no in mock_numbers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Mock_Test_Number=self.value())



# Custom Model's Registration Class
class UserQueryAdmin(admin.ModelAdmin):
    search_fields = ['username', 'query', 'response']
    def get_queryset(self, request):
        # Filter queryset to include only instances where response is None
        return super().get_queryset(request).filter(response="")
admin.site.register(User_Query, UserQueryAdmin)



class UserDataAdmin(admin.ModelAdmin):
    list_filter = (InstituteFilter,UserCourseFilter,)
    search_fields = ['username', 'name']
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(course__in=course)
admin.site.register(UserData,UserDataAdmin)



class UserProgressDataAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_filter = (UserCourseFilter,)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(course__in=course)
        
    def get_readonly_fields(self, request, obj=None):
        # Define a list of fields that you want to be read-only
        if request.user.is_superuser:
            # Superuser can edit all fields
            return []
        else:
            # For other users, specify the fields that should be read-only
            allowed_fields=['username','course','stage','level','lesson']
            return allowed_fields
admin.site.register(UserProgressData,UserProgressDataAdmin)



class StageAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter,StageNumberFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
    def get_readonly_fields(self, request, obj=None):
        # Define a list of fields that you want to be read-only
        if request.user.is_superuser:
            # Superuser can edit all fields
            return []
        else:
            # For other users, specify the fields that should be read-only
            allowed_fields=['total_levels']
            return allowed_fields
admin.site.register(Stages,StageAdmin)



class LevelAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter,StageNumberFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
    def get_readonly_fields(self, request, obj=None):
        # Define a list of fields that you want to be read-only
        if request.user.is_superuser:
            # Superuser can edit all fields
            return []
        else:
            # For other users, specify the fields that should be read-only
            allowed_fields=['total_lessons']
            return allowed_fields
admin.site.register(Levels,LevelAdmin)



class LessonAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter,StageNumberFilter,LevelFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(Lessons,LessonAdmin)



class MCQ_DataAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter, StageNumberFilter, LevelFilter, LessonNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(MCQ_Data, MCQ_DataAdmin)



class MCQ_Pic_DataAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter, StageNumberFilter, LevelFilter, LessonNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(MCQ_Pic_Data,MCQ_Pic_DataAdmin)



class MCQAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter, StageNumberFilter, LevelFilter, LessonNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(MCQ,MCQAdmin)



class ArrangeAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter, StageNumberFilter, LevelFilter, LessonNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(Arrange,ArrangeAdmin)



class MatchAdmin(admin.ModelAdmin):
    list_filter = (CodeFilter, StageNumberFilter, LevelFilter, LessonNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(Match,MatchAdmin)



class All_Course_DetailsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = (InstituteFilter,)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            course=list(All_Course_Details.objects.filter(institute_code=user.institute_code).values_list('code', flat=True))
            return super().get_queryset(request).filter(code__in=course)
admin.site.register(All_Course_Details,All_Course_DetailsAdmin)



class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    change_form_template = 'admin/Institution_Admin_Template.html'
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Institution,InstitutionAdmin)



class Institution_MockTestAdmin(admin.ModelAdmin):
    list_filter = (InstituteFilter,CodeFilter,)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Mock_Test,Institution_MockTestAdmin)


class Institution_Written_MockTestAdmin(admin.ModelAdmin):
    list_filter = (InstituteFilter,CodeFilter,)
    change_form_template = 'admin/Written_Mock_Test_Admin_Template.html'
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Written_Mock_Test,Institution_Written_MockTestAdmin)

class Written_Mock_Test_Result_Admin(admin.ModelAdmin):
    search_fields = ['username','Mock_Test_Number']
    list_filter = (InstituteFilter, CodeFilter,)
    # exclude = ('question_link', 'answer_sheet',)
    change_form_template = 'admin/Written_Mock_Test_Result_Admin_Template.html'
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
    def get_readonly_fields(self, request, obj=None):
        # Define a list of fields that you want to be read-only
        if request.user.is_superuser:
            # Superuser can edit all fields
            return []
        else:
            # For other users, specify the fields that should be read-only
            allowed_fields=['username','institute_code','code','Mock_Test_Number','Total_Marks','Total_Time']
            return allowed_fields
admin.site.register(Written_Mock_Test_Results,Written_Mock_Test_Result_Admin)


class Mock_Test_MCQ_Type_1_Admin(admin.ModelAdmin):
    list_filter = (InstituteFilter, CodeFilter, MockTestNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Mock_Test_MCQ_Type_1,Mock_Test_MCQ_Type_1_Admin)



class Mock_Test_MCQ_Pic_Data_Type_2_Admin(admin.ModelAdmin):
    list_filter = (InstituteFilter, CodeFilter, MockTestNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Mock_Test_MCQ_Pic_Data_Type_2,Mock_Test_MCQ_Pic_Data_Type_2_Admin)



class Mock_Test_MCQ_Type_3_Admin(admin.ModelAdmin):
    list_filter = (InstituteFilter, CodeFilter, MockTestNoFilter)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Mock_Test_MCQ_Type_3,Mock_Test_MCQ_Type_3_Admin)

class Mock_Test_Result_Admin(admin.ModelAdmin):
    search_fields = ['username','Mock_Test_Number']
    list_filter = (InstituteFilter, CodeFilter,)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Mock_Test_Results,Mock_Test_Result_Admin)

class Course_TopicAdmin(admin.ModelAdmin):
    list_filter = (InstituteFilter,CodeFilter,)
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Course_Topic,Course_TopicAdmin)

class Course_MaterialAdmin(admin.ModelAdmin):
    list_filter = (InstituteFilter,CodeFilter,TopicFilter,)
    change_form_template = 'admin/Course_Material_Admin_Template.html'
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            user=UserData.objects.get(username=request.user.username)
            return super().get_queryset(request).filter(institute_code=user.institute_code)
admin.site.register(Course_Material,Course_MaterialAdmin)


# Register your models here.


