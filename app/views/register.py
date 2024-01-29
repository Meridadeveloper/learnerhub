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