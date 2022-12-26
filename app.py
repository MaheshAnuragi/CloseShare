from collections import UserString
from flask import Flask
from flask import Flask, render_template,request,redirect, flash,session,url_for
from flask_sqlalchemy import SQLAlchemy
from requests_toolbelt import user_agent
from sqlalchemy.orm import query
from datetime import date
from datetime import datetime
import firebase
import pyrebase
from urllib.request import Request, urlopen
import os
import urllib.request
import webbrowser  
import ast
import webbrowser
import json
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask
from flask_mail import Mail, Message


app=Flask(__name__)
app.secret_key = "super secret key"
firebaseConfig = {
  'apiKey': "AIzaSyD1sDC4lgTk9pi1mO5HZh-TfOgV00veBVA",
  "databaseURL" : "https://distemp-80405-default-rtdb.firebaseio.com/",
  'authDomain': "distemp-80405.firebaseapp.com",
  'projectId': "distemp-80405",
  'storageBucket': "distemp-80405.appspot.com",
  'messagingSenderId': "436787642429",
  'appId': "1:436787642429:web:6bd7220c7097868a2aaa54"
}

##########################
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'closesharedis@gmail.com'
app.config['MAIL_PASSWORD'] = 'dis@12345'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


firebase = pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db=firebase.database()
auth=firebase.auth()
storage=firebase.storage()



user_mail="mahesh19172@gmail.com"




@app.route("/",methods=["GET", "POST"])
def login():
    global user_mail
    global user_ti
    if request.method == "POST":
        # print('post')
        # print(request.form["email"])
        email = request.form["email"]
        password = request.form["password"]

        try:
           
            user=auth.sign_in_with_email_and_password(str(email),str(password))
            # print(auth.current_user['email'])
            z=auth.get_account_info(user['idToken'])
            user_ti=user['idToken']
            user_mail=z['users'][0]['email'] 
            # flash('Login sucessfully ', category='sucessful')
            return redirect('/home')
        
        except:
           
            flash('Incorrect mail or password.', category='error')
            return render_template("login.html")
        
       

    return render_template("login.html")


@app.route('/aboutus')
def aboutus():
    # print(user_mail)
    return render_template('aboutus.html')


@app.route('/home')
def home():
    # print(user_mail)
    return render_template('home.html')

@app.route('/f')
def f():
    # print(user_mail)
    return render_template('f.html')


@app.route('/requestform',methods=["GET", "POST"])
def requestform():
    # print(user_mail)
    if request.method == "POST":
        # email = request.form["rname"]
        # print(rname+str('22222'))
        name=request.form.get("rname", False)
        rollno=request.form.get("rrollno", False)
        title=request.form.get("rtitle", False)
        description=request.form.get("rdescription", False)
        category=request.form.get("rcategory", False)
        phone=request.form.get("rphone", False)
        contactvia=request.form.get("rcontactvia", False)


        # print(name,rollno,title,description,category,phone,contactvia)
        
        # cu=auth.current_user['email']
        email=name+rollno
        data={'email':email,'name':name,'rollno':rollno,'title':title,'description':description,'category':category,'phone':phone,'comtactvia':contactvia,'Email':user_mail}
        db.child('students').child(email+'_'+title).set(data)
        # flash('Request Sent sucessfully', category='sucessful')
        # print(auth.current_user['email'])

        return render_template('requestPosted.html')
   

    return render_template("requestform.html")
    
    








storage=firebase.storage()

def givedata():
    return


@app.route('/placement',methods=["GET", "POST"])
def placement():
    
    p=db.child('Placement').get()
    all_data=[]
    for i in p.each():
        # print(i.key())
        k=i.val()
        # print(k)
        # print(k.keys())

        
        all_data.append(i.val())
        

    return render_template('placement.html',all_data=all_data)

    
    # return render_template('placement.html',all_companydata=all_companydata)

@app.route('/requests')
def requests():
    # print(user_mail)
    p=db.child('students').get()
    all_data=[]
    for i in p.each():
        email=i.key()
        # print('email= ',email)        
        data=i.val()
        # print('data= ',data)
        all_data.append((email,data))
    

    return render_template('requests.html',all_data=all_data,user_mail=user_mail)


# @app.route('/download/<string:k>', methods=['GET', 'POST'])
# def download(k):
#     # print(user_mail)

#     cloudfilename=k
#     storage.child(cloudfilename).download('',k)
#     url=storage.child(cloudfilename).get_url(None)

    
#     # req = Request(url)
#     # webpage = urlopen(req).read()
    
#     webbrowser.open(url)
#     all_companydata=give_file_locAnd_Name()



#     return render_template('placement.html',all_companydata=all_companydata)

@app.route('/view/<string:k>', methods=['GET', 'POST'])
def view(k):
    # print(user_mail)
    data=ast.literal_eval(k)
    

    return render_template('view.html',data=data)

# @app.route('/viewm/<string:k>', methods=['GET', 'POST'])
# def viewMP(k):
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#     print(k)
#     data=ast.literal_eval(k)
    

#     return render_template('view.html')


@app.route('/resolved/<string:k>', methods=['GET', 'POST'])
def resolved(k):
    db.child('students').child(k).remove()

    return redirect('/requests')
    


@app.route('/respond/<string:k>', methods=['GET', 'POST'])
def respond(k):
    k=ast.literal_eval(k)
    request_owner_id=k['Email']
    request_title=k['title']
    request_owner_name=k['name']
    print(k)
    contactvia=k['comtactvia']
    phone=k['phone']


    msg = Message('Regarding CloseShare Request '+str(request_title)+'request',sender =user_mail,recipients =[request_owner_id] )
    msg.body = 'Hello ' +str(request_owner_name) +'\n  I am ready to help you out. Contact me on ' +str(contactvia) +'\n'+str(user_mail)+'\n'+str(phone)
    mail.send(msg)
    flash('Mail Sent sucessfully !!  ', category='sucessful')
    print('Reciver == ',k,'sender ==',user_mail)
    return redirect('/requests')
    

@app.route('/requestPosted')
def requestPosted():
    # print(user_mail)
    return render_template('requestPosted.html')




@app.route('/marketPlace')
def marketPlace():
    # print(user_mail)
        # print(user_mail)
    p=db.child('MP').get()
    # p=db.child('').get()
    all_data=[]
    for i in p.each():
        email=i.key()
        # print('email= ',email)        
        data=i.val()
        # print('data= ',data)
        all_data.append(data)
    
    all_pair=[]
    # print(all_data)
    if(len(all_data)%2==0):
        for i in range(0,len(all_data)-1,2):
        
            all_pair.append([all_data[i],all_data[i+1]])
    
    
    else:
        for i in range(0,len(all_data)-1,2):
        
            all_pair.append([all_data[i],all_data[i+1]])
        all_pair.append([all_data[len(all_data)-1]])

    

     

            





    return render_template('marketPlace.html',all_data=all_pair,user_mail=user_mail)
    




@app.route('/Add_MarketPlace',methods=['GET', 'POST'])
def AddMarketPlace():

    if request.method == "POST":
        # email = request.form["rname"]
        # print(rname+str('22222'))
        name=request.form['name']
        rollno=request.form['rollno']
        title=request.form['title']
        description=request.form["description"]
        photo = request.files['file']  
        phone=request.form["phone"]
        contactvia=request.form["contactvia"]
        email=name+rollno
        storage=firebase.storage()
        ## Upload
        try:
            filename=photo
            # cloudfilename=input('Enter the file name that you want to save on the cloud')
            cloudfilename=str(name)+'_'+str(rollno)+'_'+str(title)
            storage.child('MarketPlace').child(cloudfilename).put(filename)
            
            
            print('Uploaded Sucessfully')
            
        except:
            print('Please the enter the file again')
        sd=''
        if(len(description)>150):

            sd=description[0:150]
        else:
            sd=description
        data={'date':str(datetime.now().date()),'email':email,'name':name,'rollno':rollno,'title':title,'description':description,'sd':sd ,'photo':str(storage.child('MarketPlace').child(cloudfilename).get_url(user_ti)),'phone':phone,'comtactvia':contactvia,'Email':user_mail}
        print(data)
        db.child('MP').child(email+'_'+title).set(data)
       
        
        
        return render_template('home.html')

    

    return render_template('Add_MarketPlace.html')



@app.route('/Add_Questions',methods=['GET','POST'])
def Add_Questions():
     
    if request.method == "POST":
        
        name=request.form["QName"]
        CompanyName=request.form["QCompanyname"]
        date=request.form["QDate"]
       
        QRound=request.form["QRound"]
        
        QQuestions=request.form["QQuestion"]
        QQuestions=QQuestions.split('Q-')
        # print(QQuestions)
        Q=[]
        for i in QQuestions:
            if(len(i)>1):
                a=i.split('\r')
                a=a[0]
                a="Q"+a
                Q.append(a)
        # print(Q)
        today = datetime.today()
        d4 = today.strftime("%b-%d-%Y")
        # print(date)


        p=db.child('Placement').get()
        ke=[]
        va=[]
        tempd=dict()
        for i in p.each():
            ke.append(i.key())
            va.append(i.val())
        
        tempd=dict(zip(ke,va))
        AllQuestions=[]
        if( CompanyName in ke):
            AllQuestions.append(tempd[CompanyName]['QQuestions'])


        print(AllQuestions)
        

         
        for i in AllQuestions:
            Q.append(i)
        data={'name':name,'CompanyName':CompanyName.upper(),'Date':str(d4),'QRound':QRound,'Email':user_mail,'QQuestions':Q}
        # print(data)
        db.child('Placement').child(CompanyName).set(data)

        # # flash('Request Sent sucessfully', category='sucessful')
        # # print(auth.current_user['email'])

        return render_template('requestPosted.html')
   

    return render_template("Add_Questions.html")
    


    







if __name__=="__main__":
   
    app.run(debug=True)