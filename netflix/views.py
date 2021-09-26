from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import List
import re,csv, io, requests, json
from django.contrib.auth import login as authlogin,authenticate
from django.contrib.auth import logout as authlogout
from django.contrib.auth.models import User
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import random
import numpy as np
# Create your views here.
my_api_key = '330b07991c772bc0116e9e8bbdaf7d73'
base_url = 'https://api.themoviedb.org/3/'

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        context ={}
        
        title=List.objects.all()
        query=title.values_list('title')
        url = f'{base_url}search/tv?api_key={my_api_key}&query={query[1]}&first_air_date_year=2004'
        responce=requests.get(url)
        
      
        context['responce']=responce.json()
        print(responce)
        context['id']=request.user.id
        user_id=request.user.id
        print(user_id)
        if user_id % 2== 0:
            title_all=List.objects.all()
            a=[]
            id=title_all.values_list('id',flat=True)
            print(id)
            for i in id:
                check_id=i%2
                
                
                if check_id*i==0:
                    i=i
                    a+=[i]
                    value=random.choice(a)
                    print(value)
                    context['list']=List.objects.filter(id=value)
                    print(context['list'])
                    
                else:
                    a+=[i]
                    value=random.choice(a)
                    context['list']=List.objects.filter(id=value)
        else:
            title_all=List.objects.all()
            
            id=title_all.values_list('id',flat=True)
            a=[]
            print(id)
            for i in id:
                check_id=i%2
                if check_id != 0:
                    a+=[i]
                    value=random.choice(a)
                    context['list']=List.objects.filter(id=value)
                else:
                    a+=[i]
                    value=random.choice(a)
                    context['list']=List.objects.filter(id=value)
        print(context)
        all=List.objects.all()
        context['random']=all
        
        request.session['value']=value
        trending_tv_url=f'{base_url}trending/tv/day?api_key={my_api_key}'
        trending_tv_responce=requests.get(trending_tv_url)
        trending_tv_result=trending_tv_responce.json()
        context['trending_tv_result']=trending_tv_result

        trending_url=f'{base_url}trending/movie/day?api_key={my_api_key}'
        trending_responce=requests.get(trending_url)
        trending_result=trending_responce.json()
        context['trending_result']=trending_result
        
        action_url=f'{base_url}discover/movie?api_key={my_api_key}&with_genres=28'
        action_responce=requests.get(action_url)
        action_result=action_responce.json()
        context['action_result']=action_result

        comedy_url=f'{base_url}discover/movie?api_key={my_api_key}&with_genres=35'
        comedy_responce=requests.get(comedy_url)
        comedy_result=comedy_responce.json()
        context['comedy_result']=comedy_result

        
        romance_url=f'{base_url}discover/movie?api_key={my_api_key}&with_genres=10749'
        romance_responce=requests.get(romance_url)
        romance_result=romance_responce.json()
        context['romance_result']=romance_result
        
        return (render(request,'home.html',context))
         
@login_required(login_url='login')
def video_play(request,slug):
    value=request.session['value']
    context={}
    title=List.objects.filter(id=value)
    
    
    query=title.values_list('title')
    a="\n".join(str(x[0]) for x in query)
    print(a)
    
    url = f'{base_url}search/tv?api_key={my_api_key}&query={a}&page=1&language=en'
    responce=requests.get(url)
    result=responce.json()
    
    for i in result['results']:
        if i['name']==a:
            context['responce']=i
            id=i['id']
            print(context['responce'])
            video_url=f'{base_url}tv/{id}/videos?api_key={my_api_key}&language=en-US'
            video_responce=requests.get(video_url)
            video_result=video_responce.json()
            print(video_result)
            context['video']=video_result['results'][1]
            request.session['i']=i
            print(request.session['i'])
    context['list']=List.objects.filter(id=value)
    
    return render(request,'video_play.html',context)           
def index(request):
    return render(request,'index.html')
def logout(request):
    authlogout(request)
    return redirect('index')
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password= request.POST.get('password')
        username = User.objects.get(email=email).username
        print(username)
        user=authenticate(request,username=username,password=password)
        
        print(user)
        if user is not None:
            authlogin(request, user)
            time.sleep(2)
            return redirect('home')
        else:
            msg='Email or Password is incorrect'
            return render(request,'login.html',{'msg':msg})
    return render(request,'login.html')
def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password= request.POST.get('password')
        user_name=request.POST.get('user_name')
        conform_pass=request.POST.get('conform')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        upper=False
        for q in str(password):
            if q.isupper:
                upper=True
                break
        if password==conform_pass:
            if upper==True:
                if regex.search(str(password))!=None:
                    if str(password).isalpha()==False:
                        if User.objects.filter(email=email).exists():
                                msg='user exists'
                                return render(request,'signup.html',{'msg':msg},None)
                        elif User.objects.filter(username=user_name).exists():
                            time.sleep(2)
                            msg='Please choose different username'
                            
                            return render(request,'signup.html',{'msg':msg})
                        else:
                            user = User.objects.create(username=user_name, email=email)
                            user.set_password(password)
                            user.save()
                            authlogin(request,user)
                            msg='An email has been sent to your given address. Please click the link in the mail to continue.'
                            return render(request,'signup.html',{'msg':msg})
                    else:
                        msg='Atleast one number required'
                        return render(request,'signup.html',{'msg':msg})
                else:
                    msg='Atleast one special charecter required'
                    return render(request,'signup.html',{'msg':msg})
            else:
                msg='Atlest one uppercase letter'
                return render(request,'signup.html',{'msg':msg})
        else:
            msg='Password Does Not Match'
            return render(request,'signup.html',{'msg':msg})

        
           

    return render(request,'signup.html',None)