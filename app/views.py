from django.shortcuts import render
from django.core.mail import send_mail
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from app.models import *
from app.serializers import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import set_password
import base64
from rest_framework.parsers import MultiPartParser
from django.conf import settings
import os 
from django.core.mail import send_mail
import google.generativeai as genai
from google.generativeai import configure, GenerativeModel
from rest_framework.permissions import IsAuthenticated
from django.core.files import File
from urllib.request import urlopen 
from django.http import JsonResponse
import base64
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserProfile, UploadedDocument
import PyPDF2
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class UserRegistrationAPIView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(type(request.data))
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        print(username,email,password)
        serializer = UserSerializer(data={'username':username,'email':email,'password':password})
        print(request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            nickname = request.data.get('nickname')
            title = request.data.get("title")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            country = request.data.get("country")
            city = request.data.get("city")
            university = request.data.get("university")

            try:
                temp_user = TempUser.objects.create(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    nickname=nickname,
                    title=title,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    city=city,
                    university=university
                )
            except Exception as e:
                return Response({'error_message': f"Error creating TempUser: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if temp_user:
                otp = generate_otp()
                print("otp is:", otp)

                temp_user.otp = otp
                temp_user.save()
                send_mail(
                        'OTP for Registration',
                        f'the otp for verification is {otp}',
                        'kalamallarajasekhar256@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                
                print("mail sent successfully")

                # user = authenticate(request, email=user_data['email'], password=user_data['password'])
                # if user is not None:
                    # login(request, user)
                    # request.session['username'] = user_data['username']
                    
                    # return Response("login successful")

                return Response({'temp_user_id': temp_user.id, 'otp': otp}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error_message': "TempUser ID not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error_message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserVerificationAPIView(APIView):
    permission_classes = [AllowAny]
    # temp_user_id = request.session.get('username')
    def post(self, request):
        UN = request.data.get('username')
        print(UN)
        otp =  request.data.get('otp')
        print(otp)
        entered_otp = request.data.get('otp')

        temp_user = TempUser.objects.get(username=UN)
        print(temp_user.username)
        correct_otp = temp_user.otp

        if str(entered_otp) == str(correct_otp):
            temp_user.is_verified = True
            temp_user.save()
            password = temp_user.password

            User.objects.create(username = temp_user.username,email=temp_user.email,password=password)
            user = User.objects.get(username=temp_user.username)
            # UO.password=set_password(password)
            user.set_password(password) 
            user.save()

            # UO.save()
            # Create user in the UserProfile table
            UID = ''
            for i in range(10):
                UID += str(random.randrange(0,9))
            print(UID)
            UserProfile.objects.create(user=user,uid=UID,otp='',is_verified=True,nickname=temp_user.nickname,title=temp_user.title,first_name=temp_user.first_name,last_name=temp_user.last_name,country=temp_user.country,city=temp_user.city,university=temp_user.university)
            # Remove temporary user data
            temp_user.delete()
            return Response({'message': 'User verified and created successfully'}, status=status.HTTP_200_OK)
        else:   
            return Response({'error_message': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

def generate_otp(length=6):
    otp = ''
    for _ in range(length):
        otp += str(random.randint(0, 9))
    return otp

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("username", username)
        print("password", password)
        # user = authenticate(username=username, password=password)
        try:
            # user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            print("user is ",user)
            

            print(user.password)
            print("user",user)

        except Exception as e:
            print(e)
            user = None

        if user and user.is_active:
            login(request, user)
            UO = UserProfile.objects.get(user=user)
            user_studies = Studies.objects.filter(user= UO)
            # print(user_studies)
            # print(type(user_studies))
            if not user_studies.exists():
                print("no user studies found")
            else:
                for i in user_studies:
                    print(i)
                    # print(emailgun)

            user_data = {
            'username': UO.user.username,
            'email': UO.user.email,
            'title':UO.title,
            'nickname':UO.nickname,
            'lastname':UO.last_name,
            'firstname':UO.first_name,
            'country':UO.country,
            'university':UO.university,
            'city':UO.city
            # Add other user details as needed
        }
            print(user_data)
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'error_message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogOutAPIView(APIView):
    def post(self,request):
        logout(request)
        return Response({'message':'Logout Successfull'})


class StudiesAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        pass

    def post(self, request,username):
        degree = request.data.get('degree')
        program = request.data.get('program')
        year = request.data.get('year')
        UO = User.objects.get(username=username)        
        print(UO)
        UPO = UserProfile.objects.get(user=UO)
        print(UPO.user.email)
        print(UPO.id)
        serializer = StudiesSerializer(data={'user':UPO.id,'degree':degree,'program':program,'year':year})
        print(serializer)
        if serializer.is_valid():
    
            serializer.save()
            print("data saved successfully")
        
            return Response({"message":"Data Inserted Successfully"})
        else:   
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("post method")
    

class DocumentUploadAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, username):
        print("username is ",username)
        pdfs =[]
        UO = User.objects.get(username=username)
        UPO = UserProfile.objects.get(user = UO)
        documents = UploadedDocument.objects.filter(user=UPO)

        for pdf in documents :
            pdf_file  =  pdf.file.read()
            base64_pdf = base64.b64encode(pdf_file).decode('utf-8')
            pdf_data = {'id':pdf.id,'base64_data':base64_pdf,'pdf_title':pdf.document_title}
            print(pdf_data['pdf_title'])
            pdfs.append(pdf_data)
            
        return JsonResponse({'pdfs':pdfs}, status=status.HTTP_200_OK)

    # def post(self, request,username):
    #     file = request.data.get('file')
    #     print("file_name is ",file.name)
    #     file_name = file.name
    #     document_title = request.data.get('title')

    #     user = User.objects.get(username=username)
    #     user_profile = UserProfile.objects.get(user=user)
    #     print(user_profile.id)

        # serializer = UploadedDocumentSerializer(data={'user': user_profile.id, 'file': file, 'document_title': file_name  })
        # print("the serializer is: ", serializer)
        # if serializer.is_valid():
        #     serializer.save()
        #     print("the instance is ",serializer.instance)
        #     fileinstance = serializer.instance 
        #     file_path = os.path.join(settings.MEDIA_ROOT, fileinstance.file.name)
        #     print("the path is: ",file_path)
        #     print(file_name,"uploaded successfully")

        #     return Response({'file_name':file_name,'message':"Document uploaded successfully"})
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
    from io import BytesIO

    def post(self, request,username):
        print(username)
        data = request.data
        print("data is  ",data)
       
        file = request.data.get('file')
        file_name = file.name
        document_title = request.data.get('title')
        
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        
        if file.name.lower().endswith(('.png', '.jpg')):
            img = Image.open(file)
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, f"{os.path.splitext(file_name)[0]}.pdf")
            img.save(pdf_file_path, "PDF", resolution=100.0)
            
            # Open the generated PDF file
            with open(pdf_file_path, 'rb') as pdf_file:
                # Create a BytesIO object to store the file content
                pdf_content = pdf_file.read()
                print(pdf_content)
                # Create a Django File object from the BytesIO object
                django_file = ContentFile(pdf_content, name=f"{os.path.splitext(file_name)[0]}.pdf")
                # Pass the Django File object to the serializer
                serializer = UploadedDocumentSerializer(data={'user': user_profile.id, 'file': django_file, 'document_title': os.path.splitext(file_name)[0]})
                print(serializer)
                print("out side valid")
                if serializer.is_valid():
                    print("SERIALIZER IS VALID" )
                    serializer.save()
                    print(serializer.data['file'])
                    print("the instance is ",serializer.instance)
                    fileinstance = serializer.instance 
                    file_path = os.path.join(settings.MEDIA_ROOT, fileinstance.file.name)
                    print("the path is: ",file_path)
                    return Response({'file_name': file_name, 'message': "Document uploaded successfully"})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif file.name.lower().endswith(('.pdf')):
            serializer = UploadedDocumentSerializer(data={'user': user_profile.id, 'file': file, 'document_title': file_name  })
            print("the serializer is: ", serializer)
            if serializer.is_valid():
                serializer.save()
                print("the instance is ",serializer.instance)
                fileinstance = serializer.instance 
                file_path = os.path.join(settings.MEDIA_ROOT, fileinstance.file.name)
                print("the path is: ",file_path)
                print(file_name,"uploaded successfully")

                return Response({'file_name':file_name,'message':"Document uploaded successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            

        else:
            return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)


        

    #     print(username)

    #     file = request.data.get('file')
    #     print(file)
    #     print("file_name is ",file.name)
    #     file_name = file.name
    #     document_title = request.data.get('title')
    #     user = User.objects.get(username=username)
    #     user_profile = UserProfile.objects.get(user=user)
    #     print(user_profile.id)
    #     if file.name.lower().endswith(('.png', '.jpg')):  # Check if it ends with .png or .jpg
    #     # Convert image to PDF

    #         img = Image.open(file)
    #         pdf_file_path = os.path.join(settings.MEDIA_ROOT, f"{file_name}.pdf")
    #         img.save(pdf_file_path, "PDF", resolution=100.0)
    #         file = open(pdf_file_path, 'rb')
    #         serializer = UploadedDocumentSerializer(data={'user': user_profile.id, 'file': file, 'document_title': file_name})
    #         print("the serializer is: ", serializer)
    #         if serializer.is_valid():
    #             serializer.save()
    #             print("the instance is ",serializer.instance)
    #             fileinstance = serializer.instance 
    #             file_path = os.path.join(settings.MEDIA_ROOT, fileinstance.file.name)
    #             print("the path is: ",file_path)
    #             print(file_name,"uploaded successfully")
    #             return Response({'file_name': file_name, 'message': "Document uploaded successfully"})
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        
from app.models import *

# class DocumentDelete(APIView):
#     def delete(self,request,id):
    
#         do = UploadedDocument.objects.get(id=id)
#         do.delete()

#         return Response("file deleted successfully")
         
    
from rest_framework.pagination import PageNumberPagination
class SpecificDocumentDisplayPagination(PageNumberPagination):
    page_size = 20  # Set the desired number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Set the maximum page size if neede
class SpecificDocumentDisplay(APIView):

    def get(self,request,username,id):

        UO = User.objects.get(username=username)
        print(username,UO)
        UPO = UserProfile.objects.get(user=UO)
        DO = UploadedDocument.objects.filter(user=UPO)
        for i in DO:
            if i.id == id:
                print(i,i.document_title)
                # return Response(i.file)
                print(i.file)
                pdf_file  =  i.file.read()
                base64_pdf = base64.b64encode(pdf_file).decode('utf-8')
                pdf_data = {'id':i.id,'base64_data':base64_pdf,'pdf_title':i.document_title}
                # print(pdf_data)
                return JsonResponse(pdf_data)
                
        return Response("not id")
        
    def post(self,request,username,id):
        print("delete called")
    
        do = UploadedDocument.objects.get(id=id)
        do.delete()
        return Response("file deleted successfully", status=status.HTTP_200_OK)
        # print(username,id)
        # UO = User.objects.get(username=username)
        # UPO = UserProfile.objects.get(user=UO)
        # Documents  = UploadedDocument.objects.filter(user=UPO)
        # for i in Documents:
        #     print("inside for loop")
        #     if i.id == id:
        #         i.delete()

        #         print("item deleted ")
        #         return Response("file deleted successfully", status=status.HTTP_200_OK)
        # return Response("Item Not Found")


# class SpecificDocumentDisplay(APIView):
#     pagination_class = SpecificDocumentDisplayPagination  # Set pagination class here

#     def get(self, request, username, id):
#         UO = User.objects.get(username=username)
#         UPO = UserProfile.objects.get(user=UO)
#         DO = UploadedDocument.objects.filter(id=id).order_by('upload_date')  # Update with the actual field

    
#         # Instantiate the pagination class
#         paginator = self.pagination_class()

#         # Paginate the queryset
#         paginated_queryset = paginator.paginate_queryset(DO, self.request)

#         pdfs = []
#         for i in paginated_queryset:
#             pdf_file = i.file.read()
#             base64_pdf = base64.b64encode(pdf_file).decode('utf-8')
#             pdf_data = base64_pdf
#             pdfs.append(pdf_data)
#         # print(pdfs)

#         return Response(pdfs)
#     pagination_class = SpecificDocumentDisplayPagination  # Set pagination class here

class GenerateContentView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        api_key = 'AIzaSyBlrcjFCOerZSDkC7YvaHoJ4elXDjaYWg8'
        configure(api_key=api_key)
        model = GenerativeModel('gemini-pro')
        question = request.data.get('question', '')
        print(len(question))

        s = "1 line definition of " + question
        print(s)
        try: 
            print("try block executed")
            response = model.generate_content(s)
            generated_text = response.text
            print(generated_text)

            return Response({'generated_text': generated_text})
        except Exception as e:
            print("except block", e)
            return Response({'error': str(e)}, status=500)


from google.cloud import translate_v3beta1 as translate
class TranslatePDFAPIView(APIView):
    # def get(self, request):
    #     # Handle GET request logic here
    #     # For example, you might want to return some information or instructions about using this API
    #     return Response("This is the TranslatePDFAPIView. Use POST method to translate PDFs.", status=status.HTTP_200_OK)

    def get(self,request,language,id):
        print("language is :",language)
        DO = UploadedDocument.objects.get(id=id)
        file_path = DO.file.path
        # print(DO)
        print("file path is :",file_path)

    
        client = translate.TranslationServiceClient.from_service_account_json(
            settings.GOOGLE_APPLICATION_CREDENTIALS)
        location = "us-central1"
        parent = f"projects/translateapi-409417/locations/{location}"
            
        with open(file_path, "rb") as document:
            document_content = document.read()
        # print(document_content)

            
        document_input_config = {
            "content": document_content,
            "mime_type": "application/pdf",
        }
        response = client.translate_document(
            request={
                "parent": parent,
                "target_language_code": language,
                "document_input_config": document_input_config,
                "is_translate_native_pdf_only":True,

            }
        )
        translated_filename = 'media/output.pdf'
        f = open(translated_filename, 'wb')
        f.write(response.document_translation.byte_stream_outputs[0])
        f.close()
        translated_pdf_content = response.document_translation.byte_stream_outputs[0]
        # Corrected base64 encoding
        translated_pdf_base64 = base64.b64encode(translated_pdf_content).decode('utf-8')
        # print(translated_pdf_base64)

        # return Response(translated_pdf_base64)
        # return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
        print("data translated and ready to send and sent")
        return Response({'translated_pdf':translated_pdf_base64,'message':"Translated Successfully and sended"})


# @permission_classes([IsAuthenticated])
# class UpdateProfileAPIView(APIView):
#     def get(self, request):
#         user_profile = UserProfile.objects.get(user=request.user)
#         serializer = UserSerializer(user_profile.user)
#         return Response(serializer.data)

#     def put(self, request):
#         user_profile = UserProfile.objects.get(user=request.user)
#         serializer = UserSerializer(user_profile.user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error_message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)






# @permission_classes([IsAuthenticated])
# class UpdateProfileAPIView(APIView):
#     def get(self, request):
#         user = request.user
#         instance = get_object_or_404(User, username=user.username)
#         serializer = StudentSerializer(instance)
#         return Response(serializer.data)

#     def put(self, request):
#         user = request.user
#         instance = get_object_or_404(User, username=user.username)
#         serializer = StudentSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error_message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class ResendOTPAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, temp_user_id):
#         temp_user = get_object_or_404(TempUser, id=temp_user_id)
#         new_otp = generate_otp()
#         temp_user.otp = new_otp
#         temp_user.save()

#         # Send new OTP logic here

#         return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)

from app.models import Universitie
class Universities(APIView):
    def get(Self,request):
            
        UC = Universitie.objects.all()
        print(UC)

        universities = []
        for i in UC:
            print(i.id,i.university_name) 
            universities.append([i.university_name,i.id]) 
        print("universities is ",universities)
        return Response(universities)
    def post(self,request):
        pass
from app.serializers import *

class COurses_View(APIView):
    def get(self,request,university_name):
        un = Universitie.objects.get(university_name=university_name)
        courses = Course.objects.filter(university_name=un)
        corses = CoursesSerializer(courses,many= True)
        print(type(corses))
        l=[]
        for i in corses.data:
            print(i)
            course_name = i['course_name']
            univercity_name = i['university_name']
            l.append(course_name)
        return Response(l)
#from here searching will happen 



from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict
import os
import fitz
import nltk

#nltk.download('punkt')
class SearchView(APIView):

    def process_pdf(self, pdf_path):
        try:
            text = self.extract_text_from_pdf(pdf_path)
            self.update_index(self.index, text, pdf_path)
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    def build_index_parallel(self, root_folder):
        self.index = defaultdict(list)

        with ProcessPoolExecutor() as executor:
            pdf_paths = [os.path.join(root_folder, filename) for filename in os.listdir(root_folder) if filename.lower().endswith('.pdf')]
            executor.map(self.process_pdf, pdf_paths)

        return self.index

    def build_index(self,root_folder):
        
        self.index = defaultdict(list)

        for foldername, subfolders, filenames in os.walk(root_folder):
            
            for filename in filenames:
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(foldername, filename)
                    
                    try:

                        text = self.extract_text_from_pdf(pdf_path)
                        

                        self.update_index(self.index, text, pdf_path)
                    except Exception as e:
                        print(f"Error processing {pdf_path}: {e}")
        #print("index is :",self.index)
        return self.index

    def extract_text_from_pdf(self, pdf_path):
        
        with fitz.open(pdf_path) as doc:
            text = ''.join(page.get_text() for page in doc)
        

        return text

    def update_index(self, index, text, pdf_path):
        
    
        index[text.lower()].append(pdf_path)

    def search_index(self, index ,query):
        
        self.index=index
        file_page = defaultdict(list)
        query_tokens = set(nltk.word_tokenize(query.lower()))

        for text, pdf_paths in self.index.items():
            text_tokens = set(nltk.word_tokenize(text.lower()))

            if query_tokens.issubset(text_tokens):
                for pdf_path in pdf_paths:
                    with fitz.open(pdf_path) as doc:
                        for page_num, page in enumerate(doc, start=1):
                            page_text = page.get_text()

                            if query_tokens.issubset(nltk.word_tokenize(page_text.lower())):
                                file_page[pdf_path].append(page_num)
        
        return file_page

    def post(self, request):
        print(request.data)
        root_folder = 'media/media/'
        index = self.build_index(root_folder)
        #print("the index is : ",index)

        query = request.data.get('search', '')
        results = self.search_index(index,query)
        
        

        pdf_datas =[]
        for l in results.keys():
            for i ,j in index.items():
                #print(j[0],l)

                
                if j[0]==l:
                    # print(j[0],l)
                    # print("matched")
                    string_data = i
                    bytes_data = string_data.encode('utf-8')

                    j1=j[0].split("/")[-1]
                    # print(bytes_data)
                    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
                    pdf_data = {'base64_data':base64_pdf,'pdf_title':j1}
                    pdf_datas.append(pdf_data)
                    
                    # print(pdf_data)
        # print(pdf_datas)


        return JsonResponse({'pdf_datas':pdf_datas})
        
        if results:
            response_data = {"message": "String found in the following PDF files:", "results": results}
            return Response(response_data, status=200)
        else:
            return Response({"message": "String not found in any PDF files."}, status=404)
        
class Search(APIView):
    def get(self,request,title):
        print(title)
         
        

        doc = UploadedDocument.objects.get(document_title=title)
        print(doc.file)

        print(doc)
        try:
            pdf_file  =  doc.file.read()
            base64_pdf = base64.b64encode(pdf_file).decode('utf-8')
            pdf_data = {'base64_data':base64_pdf}
            # print(pdf_data)
            return JsonResponse(pdf_data)
        except Exception as e:
            print(e)


        return JsonResponse({'base64_data':base64_pdf},status = 200)
        
    
        




        
