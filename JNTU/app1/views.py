from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import json
from django_xhtml2pdf.utils import generate_pdf
from .models import StudentModel,EmployeeModel,AdminModel
from django.db import IntegrityError
from JNTU import settings as se
from django.http import HttpResponse
from django.core.serializers import serialize


def loginPage(request):
    try:
        value  = request.session["user"]
        return render(request,"welcome.html",{'data':value})
    except KeyError:
        return render(request,"login.html")

def loginCheck(request):
    name=request.POST["uname"]
    password = request.POST["password"]
    try:
        res = AdminModel.objects.get(admin_name=name,admin_password=password)
    except AdminModel.DoesNotExist:
        messages.error(request,"details are not matched")
        return redirect('login')
    else:
        request.session["user"] = name
        return render(request,"welcome.html",{"data":name})

def homePage(request):
    return render(request,"welcome.html")

def logOut(request):
    del request.session["user"]
    return loginPage(request)

def addEmployee(request):
    auto_id=0
    try:
        value = request.session["user"]
    except KeyError:
        return loginPage(request)
    else:
        try:
            res = EmployeeModel.objects.all()[::-1][0]
            auto_id= int(res.emp_id)+1
        except IndexError:
            auto_id = 1100
        return render(request,"addemp.html",{"id":auto_id,"data":value})

def saveEmployee(request):
    eid = request.POST.get("empid")
    ename = request.POST.get("ename")
    egender = request.POST.get("gender")
    edb = request.POST.get("edb")
    equali = request.POST.get("qualification")
    ebloodgr = request.POST.get("bloodgr")
    edepart = request.POST.get("edepart")
    econt = request.POST.get("econt")
    eimg = request.FILES["eimg"]
    email = request.POST.get("eemail")
    id_p = str(int(eid) + len(ename))
    epassword = email[1] + econt[0] + id_p[-1] + ename[-1].upper() + id_p[0] + email[0] + econt[-1] + email[2]
    try:
        EmployeeModel(emp_id=eid,emp_name=ename,emp_gender=egender,emp_db=edb,emp_quali=equali,
                  emp_blood_g=ebloodgr,emp_department=edepart,emp_contact=econt,
                  emp_img=eimg,email=email,emp_password=epassword).save()
    except IntegrityError:
        return render(request,"addemp.html")
    else:
        subject = "Employee Registration"
        message = '''dear %s, 
        you are registered in our college 
        your idno :%s
        your password :%s

            thank you..''' % (ename, eid, epassword)
        send_mail(subject, message, se.EMAIL_HOST_USER, [email])
        return render(request, "success.html", {"message": "registered successfully"})

def viewEmployee(request):
    res = EmployeeModel.objects.all()
    return render(request,"view.html",{"data":res})


def update_Delete(request):
    res = EmployeeModel.objects.all()
    return render(request,"updelete.html",{"data":res})


def updateEmployee(request,e_id):
    qs = EmployeeModel.objects.get(emp_id=e_id)
    return render(request,"update.html",{"data":qs})

def updateSave(request):
    u_eid = request.POST.get("empid")
    u_ename = request.POST.get("ename")
    u_egender = request.POST.get("gender")
    u_edb = request.POST.get("edb")
    u_equali = request.POST.get("qualification")
    u_ebloodgr = request.POST.get("bloodgr")
    u_edepart = request.POST.get("edepart")
    u_econt = request.POST.get("econt")
    u_eimg = request.FILES["eimg"]
    u_email = request.POST.get("eemail")
    u_id_p = str(int(u_eid) + len(u_ename))
    u_epassword = u_email[1] + u_econt[0] + u_id_p[-1] + u_ename[-1].upper() + u_id_p[0] + u_email[0] + u_econt[-1] + u_email[2]
    EmployeeModel(emp_id=u_eid, emp_name=u_ename, emp_gender=u_egender, emp_db=u_edb, emp_quali=u_equali,
                  emp_blood_g=u_ebloodgr, emp_department=u_edepart, emp_contact=u_econt,
                  emp_img=u_eimg, email=u_email, emp_password=u_epassword).save()
    subject = "Employee Details Update"
    message = '''dear %s, 
    your details are updated successfully 
    your idno :%s
    your password :%s

        thank you..''' % (u_ename, u_eid, u_epassword)
    send_mail(subject, message, se.EMAIL_HOST_USER, [u_email])
    return render(request, "success.html", {"message_update": "updated successfully"})


def deleteEmployee(request,e_id):
    EmployeeModel.objects.get(emp_id=e_id).delete()
    return render(request, "success.html", {"message_delete": "deleted successfully"})

@method_decorator(csrf_exempt, name='dispatch')
class EmpLoginCeck(View):
        def post(self, request):
            data = request.body
            emp_details = json.loads(data)
            print(emp_details)
            try:
                qs = EmployeeModel.objects.get(emp_id=emp_details["eidno"], emp_password=emp_details["epassword"])
                d1={"eid":qs.emp_id,"ename":qs.emp_name}
                js = json.dumps(d1)
                return HttpResponse(js,content_type="application/json", status=200)
            except EmployeeModel.DoesNotExist:
                return HttpResponse(content_type="application/json", status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SaveMarks(View):
    def post(self,request):
        data = request.body
        s_marks = json.loads(data)
        print(s_marks)
        try:
            qs = StudentModel(student_id=s_marks["student_id"],student_name=s_marks["student_name"],telugu=s_marks["telugu"],english=s_marks["english"],
                              maths_A=s_marks["maths_a"],maths_B=s_marks["maths_b"],science=s_marks["science"],
                              social=s_marks["social"]).save()
            return HttpResponse(content_type="application/json", status=200)
        except:
            return HttpResponse(content_type="application/json", status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateMarks(View):
    def put(self,request,s_id):
        try:
            print(s_id)
            old_data = StudentModel.objects.get(student_id=s_id)
        except StudentModel.DoesNotExist:
            return HttpResponse(content_type="application/json",status=400)
        else:
            json_data = serialize("json",[old_data])
            return HttpResponse(json_data,content_type="application/json", status=200)

def results(request):
    return render(request,"results.html")

def resultMixin(s_id):
    res1 = StudentModel.objects.get(student_id=s_id)
    marks_list = [res1.telugu,res1.english,res1.maths_A,res1.maths_B,res1.science,res1.social]
    new=[]
    grade = ""
    for x in marks_list:
        if x >= 35:
            new.append(x)
    total=0
    if len(new) == 6:
        for y in new:
            total = total +y
        if total <= 600 and total >500:
            grade = "A"
        elif total <= 500 and total >400:
            grade= "B"
        elif total <=400 and total >300:
            grade = "C"
        elif total <= 300 and total >=210:
            grade = "D"
    else:
        grade = "fail"

    context = {
        "data":res1,"total":total,"grade":grade
        }
    return context

def getResult(request):
    s_id = request.POST.get("sid")
    try:
        res = resultMixin(s_id)
    except StudentModel.DoesNotExist:
        return render(request,"results.html",{"error":"enter correct id"})
    else:
        return render(request,"getresult.html",context=res)

def pdfGenerate(request):
    id = request.POST.get("sid")
    resp = HttpResponse(content_type='application/pdf')
    context = resultMixin(id)
    result = generate_pdf('getresult.html', file_object=resp,context=context)
    return result

