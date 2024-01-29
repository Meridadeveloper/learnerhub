from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    # path('validate-otp/', UserRegistrationAndOTPValidation.as_view(), name='validate-otp'),
    path('ValidateOTP/',UserVerificationAPIView.as_view(),name='ValidateOTP'),
    path('LoginAPIView/',LoginAPIView.as_view(),name='LoginAPIView'),
    path('LogOutAPIView/',LogOutAPIView.as_view(),name = 'LogOutAPIView'),
    path('StudiesAPIView/<str:username>',StudiesAPIView.as_view(),name='StudiesAPIView'),
    path('DocumentUploadAPIView/<str:username>/',DocumentUploadAPIView.as_view(),name='DocumentUploadAPIView'),
    # path('DocumentUploadAPIView/',DocumentUploadAPIView.as_view(),name='DocumentUploadAPIView'),

    path('SpecificDocumentDisplay/<str:username>/<int:id>',SpecificDocumentDisplay.as_view(),name='SpecificDocumentDisplay'),
    path('GenerateContentView/',GenerateContentView.as_view(),name='GenerateContentView'),
    path('TranslatePDFAPIView/<str:language>/<int:id>',TranslatePDFAPIView.as_view(),name='TranslatePDFAPIView'),
    # path('DocumentDelete/<int:str>',DocumentDelete.as_view(),name='DocumentDelete'),
    path('Universities/',Universities.as_view(),name='Universities'),
    path('COurses_View/<str:university_name>',COurses_View.as_view(),name = 'COurses_View'),
    path('SearchView/',SearchView.as_view(),name='SearchView'),
    path('Search/<str:title>/',Search.as_view(),name='Search'),




    
]
