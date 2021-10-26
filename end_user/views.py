from django.shortcuts import render,redirect
from django.views import View
from . import forms
from django.contrib import messages
from django.contrib.auth.models import UserManager, auth,User
import dbinfo
import gridfs
import base64
from bson.objectid import ObjectId

class HomePage(View):
    def get(self,request):
        collection = dbinfo.database['product_info']
        data = list()
        fs = gridfs.GridFS(dbinfo.database)
        for item in collection.find():
            image_path = fs.get(ObjectId(item['image_id']))
        
            product_info = {
                'uid':item['uid'],
                'price':item['price'],
                'product_name':item['product_name'],
                'image_path': base64.b64encode(image_path.read()).decode('utf-8')
            }
            data.append(product_info)


        content = {
            'page_title' : 'Home Page',
            'product_info' : data
        }
        return render(request,'index.html',content)

class LoginUser(View):
    def get(self,request):
        content = {
            'page_title' : 'Login Page',
            'login_form' : forms.LoginForm()
        }
        return render(request,'login_page.html',content)

    def post(self,request):
        username= request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Login successfully")
        else:
            messages.error(request,"username or password Wrong")
        return redirect('/')

class LogoutUser(View):
    def get(self,request):
        auth.logout(request)
        return redirect('/')

class SignupUser(View):
    def get(self,request):
        content ={
            'page_title':'sign up',
            'sign_up' : forms.SignUpForm()
        }
        return render(request,'sign_up.html',content)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
    
        new_user = User.objects.create_user(username=username,password=password,email=email)
        new_user.save()

        messages.success(request,"User added successfully")
        return redirect('/')