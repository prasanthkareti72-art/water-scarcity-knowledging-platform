from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import pymysql
from datetime import date
import numpy as np

global uname

def Videos(request):
    if request.method == 'GET':
        return render(request, 'Videos.html', {})

def Download(request):
    if request.method == 'GET':
        global fileList
        name = request.GET.get('requester', False)
        with open("WaterApp/static/files/"+name, "rb") as file:
            data = file.read()
        file.close()        
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response   

def AccessAdvice(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center width=100%><tr><th><font size="3" color="black">Expert Name</th><th><font size="3" color="black">Water Saving Techniques & Ideas</th>'
        output+='<th><font size="3" color="black">Post Date</th><th><font size="3" color="black">Download Tools/Videos on Water Saving</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'water',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM techniques")
            rows = cur.fetchall()
            for row in rows:
                name = row[0]
                technique = row[1]
                file = row[2]
                upload_date = row[3]
                output += '<tr><td><font size="3" color="black">'+str(name)+'</td><td><font size="3" color="black">'+str(technique)+'</td>'
                output+='<td><font size="3" color="black">'+upload_date+'</td>'
                output +='<td><a href=\'Download?requester='+file+'\'><font size=3 color=black>Download</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"    
        context= {'data':output}
        return render(request, 'UserScreen.html', context)    

def AccessMap(request):
    if request.method == 'GET':
        areaname = "Rajasthan"
        areaname = areaname+" most drought areas"
        areaname = areaname.replace(" ","+")
        output = '<iframe width="800" height="650" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q='+areaname+'&amp;ie=UTF8&amp;&amp;output=embed"></iframe><br/>'
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def ShareKnowledgeAction(request):
    if request.method == 'POST':
        global uname
        ideas = request.POST.get('t1', False)
        ideas = ideas.replace("'","")
        myfile = request.FILES['t2'].read()
        fname = request.FILES['t2'].name
        dd = str(date.today())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'water',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO techniques VALUES('"+uname+"','"+ideas+"','"+fname+"','"+dd+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if os.path.exists("WaterApp/static/files/"+fname):
            os.remove("WaterApp/static/files/"+fname)
        with open("WaterApp/static/files/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        context= {'data':"<font size=3 color=blue>Your technique successfully saved in Centralized server & Shared with other social users</font>"}
        return render(request, 'UserScreen.html', context)

def ShareKnowledge(request):
    if request.method == 'GET':
       return render(request, 'ShareKnowledge.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})  

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        page = "UserLogin.html"
        status = "Invalid login"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'water',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    status = "Welcome "+username
                    page = "UserScreen.html"
                    break		
        context= {'data': status}
        return render(request, page, context)

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'water',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'water',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Signup Process Completed'
        context= {'data':output}
        return render(request, 'Signup.html', context)
      
