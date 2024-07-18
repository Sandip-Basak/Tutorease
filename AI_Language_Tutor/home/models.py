from django.db import models
import random
import string
import uuid
from django.conf import settings

# Other Functions

# Generate Status Symbol
def status_symbol(bool_value):
    tick_mark = "✔️"  # Unicode character for tick mark
    cross_mark = "❌"  # Unicode character for cross mark

    # Determine the symbol based on the boolean field value
    symbol = tick_mark if bool_value else cross_mark
    return symbol

# Generate unique referal code
def generate_unique_code():
    code_length = 6
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for _ in range(code_length))
    return code

# Generate unique file path for images
def unique_file_path(instance, filename):
    extension = filename.split('.')[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return f"institutes/images/{unique_filename}"


# Generate unique file path for pdfs
def pdf_unique_file_path(instance, filename):
    extension = filename.split('.')[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return f"institutes/pdf/{unique_filename}"

# Generate unique file path institute images
def institute_images_unique_file_path(instance, filename):
    extension = filename.split('.')[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return f"institute_images/{unique_filename}"

# Create your models here.
class MCQ_Data(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    level=models.DecimalField(max_digits=1,decimal_places=0)
    lesson_no=models.DecimalField(max_digits=2,decimal_places=0)
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    option1_link=models.FileField(upload_to=unique_file_path)
    option2_link=models.FileField(upload_to=unique_file_path)
    option3_link=models.FileField(upload_to=unique_file_path)
    option4_link=models.FileField(upload_to=unique_file_path)
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)


    def __str__(self):
        return f"Code: {self.code} Stage: {self.stage_number} Level: {self.level} Lesson: {self.lesson_no}"


class MCQ_Pic_Data(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    level=models.DecimalField(max_digits=1,decimal_places=0)
    lesson_no=models.DecimalField(max_digits=2,decimal_places=0)
    question=models.TextField(default="Choose the correct option")
    img_link=models.FileField(upload_to=unique_file_path)
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)


    def __str__(self):
        return f"Code: {self.code} Stage: {self.stage_number} Level: {self.level} Lesson: {self.lesson_no}"


class MCQ(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    level=models.DecimalField(max_digits=1,decimal_places=0)
    lesson_no=models.DecimalField(max_digits=2,decimal_places=0)
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)


    def __str__(self):
        return f"Code: {self.code} Stage: {self.stage_number} Level: {self.level} Lesson: {self.lesson_no}"


class Arrange(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    level=models.DecimalField(max_digits=1,decimal_places=0)
    lesson_no=models.DecimalField(max_digits=2,decimal_places=0)
    question=models.TextField()
    answer=models.TextField()
    options=models.TextField()
    number_of_options=models.DecimalField(max_digits=2,decimal_places=0)
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)

    def __str__(self):
        return f"Code: {self.code} Stage: {self.stage_number} Level: {self.level} Lesson: {self.lesson_no}"


class Match(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    level=models.DecimalField(max_digits=1,decimal_places=0)
    lesson_no=models.DecimalField(max_digits=2,decimal_places=0)
    data1=models.TextField()
    data2=models.TextField()
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)


    def __str__(self):
        return f"Code: {self.code} Stage: {self.stage_number} Level: {self.level} Lesson: {self.lesson_no}"


class UserData(models.Model):
    username=models.CharField(max_length=150, primary_key=True)
    name=models.CharField(max_length=100)
    institute_code=models.CharField(max_length=15, default='SELF')
    course=models.CharField(max_length=15)
    gender=models.CharField(max_length=6)

    def __str__(self):
        return f"{self.name} ({self.course})"


class UserProgressData(models.Model):
    username=models.CharField(max_length=150)
    course=models.CharField(max_length=15)
    approved=models.BooleanField(default=False)
    stage=models.DecimalField(max_digits=1,decimal_places=0)
    level=models.DecimalField(max_digits=2,decimal_places=0)
    lesson=models.DecimalField(max_digits=2,decimal_places=0)

    def __str__(self):
        # Determine the symbol based on the boolean field value
        symbol = status_symbol(self.approved)
        return f"{self.username} ({self.course}) {symbol}"


class Stages(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    stage_name=models.TextField()
    total_levels=models.DecimalField(max_digits=2,decimal_places=0,null=True, blank=True)
    overview=models.TextField()
    description=models.TextField()
    def __str__(self):
        return f"Stage:{self.stage_name} Code:{self.code}"


class Levels(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    stage_name=models.TextField()
    level=models.DecimalField(max_digits=2,decimal_places=0)
    total_lessons=models.DecimalField(max_digits=2,decimal_places=0,null=True, blank=True)
    description=models.TextField()
    def __str__(self):
        return f"Level: {self.level} Stage:{self.stage_name} Code:{self.code}"


class Lessons(models.Model):
    code=models.CharField(max_length=15)
    stage_number=models.DecimalField(max_digits=2,decimal_places=0)
    stage_name=models.TextField()
    level=models.DecimalField(max_digits=2,decimal_places=0)
    lesson_no=models.DecimalField(max_digits=2,decimal_places=0)
    description=models.TextField()
    def __str__(self):
        return f"Code:{self.code} Stage:{self.stage_name} Level: {self.level} Lesson: {self.lesson_no}"


class User_Query(models.Model):
    username=models.CharField(max_length=150)
    query=models.TextField()
    response=models.TextField()
    def __str__(self):
        return f"{self.username}"


class Institution(models.Model):
    institute_code=models.CharField(max_length=15, primary_key=True)
    referal_code=models.CharField(max_length=6,blank=True)
    name=models.CharField(max_length=100)
    description=models.TextField()
    total_students=models.DecimalField(max_digits=8,decimal_places=0,default=0)
    max_students=models.DecimalField(max_digits=8,decimal_places=0)
    no_of_courses=models.DecimalField(max_digits=6,decimal_places=0,default=0)
    logo=models.FileField(upload_to=institute_images_unique_file_path, null=True, blank=True)

    
    def save(self, *args, **kwargs):
        if not self.referal_code:
            self.referal_code = generate_unique_code()
            while Institution.objects.filter(referal_code=self.referal_code).exists():
                self.referal_code = generate_unique_code()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name}({self.institute_code})"


class All_Course_Details(models.Model):
    code=models.CharField(max_length=15, primary_key=True)
    institute_code=models.CharField(max_length=15)
    name=models.CharField(max_length=100)
    description=models.TextField()
    def __str__(self):
        return f"{self.name} ({self.code})"


class Mock_Test(models.Model):
    code=models.CharField(max_length=15)
    institute_code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0,default=-1)
    Total_Marks=models.DecimalField(max_digits=4,decimal_places=0)
    Total_Time=models.DecimalField(max_digits=4,decimal_places=0)
    approved=models.BooleanField(default=False)
    number_of_attempts=models.DecimalField(max_digits=4,decimal_places=0,default=5)

    def __str__(self):
        # Determine the symbol based on the boolean field value
        symbol = status_symbol(self.approved)
        return f"{self.code} {self.Mock_Test_Number} {symbol}"


class Mock_Test_MCQ_Type_1(models.Model):
    institute_code=models.CharField(max_length=15)
    code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0)
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    option1_link=models.FileField(upload_to=unique_file_path)
    option2_link=models.FileField(upload_to=unique_file_path)
    option3_link=models.FileField(upload_to=unique_file_path)
    option4_link=models.FileField(upload_to=unique_file_path)
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)

    def __str__(self):
        return f"{self.code} {self.Mock_Test_Number}"


class Mock_Test_MCQ_Pic_Data_Type_2(models.Model):
    institute_code=models.CharField(max_length=15)
    code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0)
    question=models.TextField(default="Choose the correct option")
    img_link=models.FileField(upload_to=unique_file_path)
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)

    def __str__(self):
        return f"{self.code} {self.Mock_Test_Number}"


class Mock_Test_MCQ_Type_3(models.Model):
    institute_code=models.CharField(max_length=15)
    code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0)
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    marks=models.DecimalField(max_digits=1,decimal_places=0,default=1)

    def __str__(self):
        return f"{self.code} {self.Mock_Test_Number}"

class Mock_Test_Results(models.Model):
    username=models.CharField(max_length=150)
    institute_code=models.CharField(max_length=15)
    code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0)
    marks=models.DecimalField(max_digits=4,decimal_places=0)
    Total_Marks=models.DecimalField(max_digits=4,decimal_places=0)
    Total_Time=models.DecimalField(max_digits=4,decimal_places=0)

    def __str__(self):
        return f"{self.username} ({self.code}) {self.Mock_Test_Number} {self.marks}/{self.Total_Marks}"

class Written_Mock_Test(models.Model):
    code=models.CharField(max_length=15)
    institute_code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0,default=-1)
    Total_Marks=models.DecimalField(max_digits=4,decimal_places=0)
    Total_Time=models.DecimalField(max_digits=4,decimal_places=0)
    approved=models.BooleanField(default=False)
    number_of_attempts=models.DecimalField(max_digits=4,decimal_places=0,default=1)
    question_paper=models.FileField(upload_to=pdf_unique_file_path)

    def __str__(self):
        # Determine the symbol based on the boolean field value
        symbol = status_symbol(self.approved)
        return f"{self.code} {self.Mock_Test_Number} {symbol}"

class Written_Mock_Test_Results(models.Model):
    username=models.CharField(max_length=150)
    institute_code=models.CharField(max_length=15)
    code=models.CharField(max_length=15)
    Mock_Test_Number=models.DecimalField(max_digits=10,decimal_places=0)
    marks=models.DecimalField(max_digits=4,decimal_places=0)
    Total_Marks=models.DecimalField(max_digits=4,decimal_places=0)
    Total_Time=models.DecimalField(max_digits=4,decimal_places=0)
    question_link=models.FileField(upload_to=pdf_unique_file_path, null=True, blank=True)
    answer_sheet=models.FileField(upload_to=pdf_unique_file_path, null=True, blank=True)
    checked=models.BooleanField(default=False)

    def __str__(self):
        # Determine the symbol based on the boolean field value
        symbol = status_symbol(self.checked)
        return f"{self.username} ({self.code}-{self.Mock_Test_Number}) {self.marks}/{self.Total_Marks} {symbol}"

class Course_Material(models.Model):
    code=models.CharField(max_length=15)
    institute_code=models.CharField(max_length=15)
    topic=models.CharField(max_length=150)
    name=models.CharField(max_length=200)
    video_link=models.TextField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    document=models.FileField(upload_to=pdf_unique_file_path, null=True, blank=True)
    approved=models.BooleanField(default=False)

    def __str__(self):
        # Determine the symbol based on the boolean field value
        symbol = status_symbol(self.approved)
        return f"{self.code} {self.topic} ({self.name}) {symbol}"

class Course_Topic(models.Model):
    code=models.CharField(max_length=15)
    institute_code=models.CharField(max_length=15)
    topic=models.CharField(max_length=150)
    description=models.TextField(null=True, blank=True)
    approved=models.BooleanField(default=False)

    def __str__(self):
        # Determine the symbol based on the boolean field value
        symbol = status_symbol(self.approved)
        return f"{self.code} {self.topic} {symbol}"

# Security: Users cannot login with multiple devices
class LoggedInUser(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name="logged_in_user", on_delete=models.CASCADE)
    session_key=models.CharField(max_length=40,blank=True,null=True)

    def __str__(self):
        return self.user.username