from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
from django.contrib import auth
config = {
    'apiKey': "AIzaSyC7CwSdibkme6dYtpIV7EkQtWOhInvM35s",
    'authDomain': "taf-form-app.firebaseapp.com",
    'databaseURL': "https://taf-form-app.firebaseio.com",
    'projectId': "taf-form-app",
    'storageBucket': "taf-form-app.appspot.com",
    'messagingSenderId': "449679668786",
    'appId': "1:449679668786:web:ceeec7fe9145e14860ae2b",
    'measurementId': "G-N0HZKJY5RN"
  };
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()



def login(request):
    return render(request, "login.html")

def postsign(request):
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message='invalid credentials'
        return render(request, 'login.html', {'messg':message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "postsign.html", {'e':email})

def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render(request, "login.html")

def signup(request):
    return render(request, 'signup.html')

def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email, passw)
    except:
        message='Unable to create account try again. password must be longer than 5 characters'
        return render(request, 'login.html', {'messg':message})
    uid = user['localId']
    data={'name':name, 'status':'1'}
    database.child('users').child(uid).child('details').set(data)
    return render(request, 'login.html')

def create(request):
    return render(request, 'create.html')

def postcreate(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    First = request.POST.get('First')
    Last = request.POST.get('Last')
    ID = request.POST.get('ID')
    Degree = request.POST.get('Degree')
    Major = request.POST.get('Major')
    Minors = request.POST.get('Minors')
    Term = request.POST.get('Term')
    Year = request.POST.get('Year')
    Chapter = request.POST.get('Chapter')
    Courses = request.POST.get('Courses')
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        print("info"+str(a))
        data = {
            'First':First,
            'Last':Last,
            'ID':ID,
            'Degree':Degree,
            'Major':Major,
            'Minors':Minors,
            'Term':Term,
            'Year':Year,
            'Chapter':Chapter,
            'Courses':Courses,
        }
        database.child('users').child(a).child('reports').child('millis').set(data, idtoken)
        name = database.child('users').child(a).child('details').child('name').get(idtoken).val()
        return render(request, 'postsign.html')
    except KeyError:
        message='User has logged out. Please sign in'
        return render(request, 'login.html', {'messg':message})

def check(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    try:
        timestamps = database.child('users').child(a).child('reports').shallow().get().val()
        list_time=[]
        for i in timestamps:
            list_time.append(i)
        list_time.sort(reverse=True)
        print(list_time)
    except KeyError:
        message='A form has not yet been pushed to the database'
        return render(request, 'postsign.html', {'messg':message})
    First_Name = []
    for i in list_time:
        first=database.child('users').child(a).child('reports').child(i).child('First').get().val()
        First_Name.append(first)
    Last_Name = []
    for i in list_time:
        last=database.child('users').child(a).child('reports').child(i).child('Last').get().val()
        Last_Name.append(last)
    ID = []
    for i in list_time:
        id=database.child('users').child(a).child('reports').child(i).child('ID').get().val()
        ID.append(id)
    Degree = []
    for i in list_time:
        degree=database.child('users').child(a).child('reports').child(i).child('Degree').get().val()
        Degree.append(degree)
    Major = []
    for i in list_time:
        major=database.child('users').child(a).child('reports').child(i).child('Major').get().val()
        Major.append(major)
    Minors = []
    for i in list_time:
        minors=database.child('users').child(a).child('reports').child(i).child('Minors').get().val()
        Minors.append(minors)
    Term = []
    for i in list_time:
        term=database.child('users').child(a).child('reports').child(i).child('Term').get().val()
        Term.append(term)
    Year = []
    for i in list_time:
        year=database.child('users').child(a).child('reports').child(i).child('Year').get().val()
        Year.append(year)
    Chapter = []
    for i in list_time:
        chapter=database.child('users').child(a).child('reports').child(i).child('Chapter').get().val()
        Chapter.append(chapter)
    Courses = []
    for i in list_time:
        courses=database.child('users').child(a).child('reports').child(i).child('Courses').get().val()
        Courses.append(courses)
    print(First_Name)
    comb_list = zip(list_time, First_Name, Last_Name, ID, Degree, Major, Minors, Term, Year, Chapter, Courses)
    name = database.child('users').child(a).child('details').child('name').get(idtoken).val()
    return render(request, 'check.html', {'comb_list':comb_list, 'e':name})
