# serializers.py
from rest_framework import serializers
# from .models import UserProfile, Studies, UploadedDocument, DocumentComment, CommentReply, EmailVerification, UserStudies
from django.contrib.auth.models import User
from app.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        
class StudiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studies
        fields = ['user','degree','program','year']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__' 

class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['user', 'file', 'document_title']
    def get_file_path(self, obj):
        # Method to retrieve the file path
        return obj.file.path


    # def create(self, validated_data):
    #     return UploadedDocument.objects.create(**validated_data)
    

class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['university_name','course_name']









































































# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'



# class UploadedDocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UploadedDocument
#         fields = '__all__'

# class DocumentCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DocumentComment
#         fields = '__all__'

# class CommentReplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommentReply
#         fields = '__all__'

# class EmailVerificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmailVerification
#         fields = '__all__'

# class UserStudiesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserStudies
#         fields = '__all__'
