from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
from django.utils import timezone  # Import timezone module

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=10,default='xxxx')
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    nickname = models.CharField(max_length=255,blank=True,default='',unique=True)
    title = models.CharField(max_length=4,blank=True,default='')
    first_name = models.CharField(max_length=100,blank=True,default='')
    last_name = models.CharField(max_length=100,blank=True,default='')
    country = models.CharField(max_length=100,blank=True,default='')
    city = models.CharField(max_length=100,blank=True,default='')
    university = models.CharField(max_length=100, default='')
    star_rating = models.IntegerField(default=0)
    account_created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username

class TempUser(models.Model):
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    nickname = models.CharField(max_length=255,blank=True,default='',unique=True)
    title = models.CharField(max_length=4,blank=True,default='')
    first_name = models.CharField(max_length=100,blank=True,default='')
    last_name = models.CharField(max_length=100,blank=True,default='')
    country = models.CharField(max_length=100,blank=True,default='')
    city = models.CharField(max_length=100,blank=True,default='')
    university = models.CharField(max_length=100, default='')
    star_rating = models.IntegerField(default=0)
    account_created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.username

class Studies(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    year = models.DateField()
    
    def __str__(self):
        return self.user.user.username

class Universitie(models.Model):
    university_name = models.CharField(max_length=1000,unique=True)

    def __str__(self):

        return self.university_name

class Course(models.Model):
    university_name = models.ForeignKey(Universitie,on_delete=models.CASCADE)

    course_name = models.CharField(max_length=100)

  
    def __str__(self):
        un = self.university_name.university_name
        return self.course_name +' ' +   un 

class UploadedDocument(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100,default='')
    file = models.FileField(upload_to='media/')
    document_title = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    # converted_text = models.FileField(upload_to='converted_pdfs/', blank=True, null=True)

    def __str__(self):

        return self.document_title

class User_Groups(models.Model):
    pass






















































# class DocumentComment(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
#     comment_date = models.DateTimeField(default=timezone.now)

# class CommentReply(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     comment = models.ForeignKey(DocumentComment, on_delete=models.CASCADE, related_name='replies')
#     text = models.TextField()
#     reply_date = models.DateTimeField(default=timezone.now)

