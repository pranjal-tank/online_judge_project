from random import sample
from django.db import models
from ckeditor.fields import RichTextField
class Problems(models.Model):
    problem_st= RichTextField(blank=True,null=True)
    in_formate=RichTextField(blank=True,null=True)
    out_formate=RichTextField(blank=True,null=True)
    problem_nm=models.CharField(max_length=50)
    problem_code=models.CharField(max_length=3)
    problem_diff=models.CharField(max_length=6)

    def __str__(self):
        return self.problem_nm
    
# ---------------------------------------------------------------------------------------------------------

class Solutions(models.Model):
    problem=models.ForeignKey(Problems,on_delete=models.CASCADE)
    solution_problem=models.CharField(max_length=50)
    problem_code=models.CharField(max_length=3)
    problem_diff=models.CharField(max_length=6,default="easy")
    solution_lang=models.CharField(max_length=7,default="c++")
    verdict=models.CharField(max_length=20)
    uname=models.CharField(max_length=50,default="user")
    submission_time=models.DateTimeField("submitted_at")

    def __str__(self) :
        return self.verdict
    
# ---------------------------------------------------------------------------------------------------------

class Testcases(models.Model):
    Problem=models.ForeignKey(Problems,on_delete=models.CASCADE)
    problem_input=models.TextField(max_length=1000)
    problem_output=models.TextField(max_length=1000)
    
    def __str__(self):
        return self.problem_input

      
# ---------------------------------------------------------------------------------------------------------