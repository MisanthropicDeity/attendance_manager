from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance, Course, AttendanceDetail
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .utils import facestore, get_attendance_from_id, get_chart
from .forms import StudentForm
from django.views.generic.detail import DetailView
from attendance_management.settings import BASE_DIR
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files import File  
import urllib
from PIL import Image
import pandas as pd
import os
from datetime import timedelta
from django.utils import timezone

# Create your views here.


def home(request):
    return render(request, 'role/index.html')


def register(request):
    counter=1
    if request.method == 'POST':
        if request.POST.get("Sign up"):
            uname = request.POST['username']
            rno = request.POST['rollno']
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            us = User.objects.create_user(uname, email, password)
            std = Student.objects.create(
                user=us, name=name, email=email, roll_no=rno)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('register')
        if request.POST.get("Login"):
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.success(request, f'Wrong Credentials')
    return render(request, 'role/register.html')

def dashboard(request):
    if request.method == 'POST':
        if request.POST.get("train"):
            facestore(request)
        if request.POST.get("course"):
            return redirect('addcourse')

    std = Student.objects.filter(user=request.user)
    att = Attendance.objects.filter(student=std[0])
    fro = timezone.now().date() - timedelta(days=7)
    to = timezone.now().date()
    count=0
    for sub in att:
        if sub.percentage<75:
            if sub.total_classes==0:
                continue
            count = count+1
    val = [] 
    finalval = []
    for st in std:
        for cou in st.course.all():
           val.append(cou)
    for item in val:
        att = Attendance.objects.filter(course = item,student = st)
        for ok in att:
            finalval.append(ok)

    context = {
        'std' : std,
        'finalval' : finalval,
        'count' : count,
    }
    return render(request, 'role/dashboard.html',context)

def get_data(request,*args,**kwargs):
    labels = ["Present","Absent"] 
    data = [10,20]
    data = {
     "data" : data,
     "labels" : labels,
     "customers" : 20, 
    }
    return JsonResponse(data)



def addcourse(request):
    mycourses = None  
    myenroll = []
    notenroll = []
    flag = False
    st = Student.objects.filter(user=request.user)
    if request.method == 'POST':
        if request.POST.get("wow"):
            year = request.POST['year']
            branch = request.POST['branch']
            mycourses = Course.objects.filter(year=year,branch=branch)
            for wow in st:
                stdenroll = wow.course.all()
                break
            for course in mycourses:
                for std in stdenroll:
                    if std.name==course.name:
                        myenroll.append(std)
                        flag = True
                        break
                if flag is not True:
                    notenroll.append(course)
                flag=False
        if request.POST.get("update"):
            mylist = request.POST.getlist("checkbox")
            print(mylist)
            if len(mylist)==0:
                return redirect('dashboard')
            for cc in st[0].course.all():
                st[0].course.remove(cc)
            for cou in mylist:
                objlist = Course.objects.filter(name=cou)
                obj = objlist[0]
                print(obj)
                st[0].course.add(obj)
                att = Attendance.objects.filter(course=obj,student=st[0])
                if len(att)==0:
                    newobj = Attendance.objects.create(course=obj,student=st[0],class_attended=0,total_classes=0)
                    newobj.save()
            return redirect('dashboard')
        if request.POST.get("remove"):
            print('working')
            for cc in st[0].course.all():
                st[0].course.remove(cc)
            return redirect('dashboard')
    
    context = {
        'myenroll' : myenroll,
        'notenroll' : notenroll,
        'std' : st,
    }  
    return render(request,'role/addcourse.html',context)

class CourseDetail(DetailView):
    def get(self,request,*args, **kwargs):
        pk = kwargs['pk']
        cc = Course.objects.get(id=pk)
        print(cc)
        st =Student.objects.filter(user=request.user)
        print(st[0])
        content= {
            'cc' : cc,
        }
        return render(request,'role/course_detail.html',content)
    def post(self,request,*args,**kwargs):
        fro = request.POST['from']
        to = request.POST['to']
        pk = kwargs['pk']
        cc = Course.objects.get(id=pk)
        st =Student.objects.filter(user=request.user)
        att = Attendance.objects.filter(course=cc,student=st[0])
        data = AttendanceDetail.objects.filter(date__range=[fro,to],attendance_field=att[0])
        content= {
            'cc' : cc,
            'data' : data,
            'att' : att,
        }
        return render(request,'role/course_detail.html',content)

def profile(request):
    if request.method=='POST':
        st =Student.objects.filter(user=request.user)
        form = StudentForm(request.POST,request.FILES,instance = st[0],initial={'name': st[0].name})
        if form.is_valid():
            form.save()
    else :
        st =Student.objects.filter(user=request.user)
        form = StudentForm(instance = st[0])
    context = {
        'st' : st[0],
        'form' : form
    }        
    return render(request,'role/profile.html',context)



