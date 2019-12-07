from django.db import models

class EmployeeModel(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    emp_name = models.CharField(max_length=40)
    emp_gender = models.CharField(max_length=10)
    emp_db=models.DateField()
    emp_quali = models.CharField(max_length=30)
    emp_blood_g = models.CharField(max_length=5)
    emp_contact = models.IntegerField()
    emp_department = models.CharField(max_length=15)
    emp_img = models.ImageField(upload_to="emp_img/")
    emp_password = models.CharField(max_length=8)
    email=models.EmailField(default=False)
class StudentModel(models.Model):
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=40)
    telugu = models.IntegerField()
    english = models.IntegerField()
    maths_A = models.IntegerField()
    maths_B = models.IntegerField()
    science = models.IntegerField()
    social = models.IntegerField()


