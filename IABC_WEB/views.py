
from email import message
from email.policy import default
import http
from multiprocessing import context
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .models import *
from members.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse
import datetime
from dateutil.relativedelta import relativedelta
import json
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import render_to_pdf
from IABC.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage
from django.conf import settings



# Create your views here.


def home(request):
    type_obj=request.user
    if request.user.is_authenticated and type_obj.is_admin:
        return redirect('IABC_WEB:admember')
    elif request.user.is_authenticated and type_obj.is_bidder:
        return redirect('IABC_WEB:bidder_app')
    elif request.user.is_authenticated and type_obj.is_nonmember:
        info = User.objects.get(pk=request.user.id)
        return render(request, 'index.html', {'info':info})
    elif request.user.is_authenticated and type_obj.is_member:
        mem = Members.objects.get(user_id=request.user.id)
        info = User.objects.get(pk=request.user.id)
        context = {
            'mem':mem,
            'info':info 
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def downloadables(request):
    return render(request, 'downloadables.html')

def my_account(request, acc_id):
    type_obj=request.user
    if request.user.is_authenticated:
        info = User.objects.get(pk=acc_id)
        return render(request, 'user-myaccount.html', {'info':info})

    else:
        return redirect('IABC_WEB:home')


def view_profile(request, acc_id):
    if request.user.is_authenticated:
        info = User.objects.get(pk=acc_id)
        return render(request, 'user-viewprofile.html', {'info':info})
    else:
        return redirect('IABC_WEB:home')
    
def edit_profile(request, acc_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            info = User.objects.get(pk=acc_id)
            return render(request, 'user-editviewprofile.html', {'info':info})
        elif request.method == "POST":
            try:
                info = User.objects.get(pk=acc_id)
                firstName = request.POST.get('firstName')
                middleName = request.POST.get('middleName')
                lastName = request.POST.get('lastName')
                email = request.POST.get('email')
                info.firstName = firstName
                info.middleName = middleName
                info.lastName = lastName
                info.email = email
                info.save()
                return HttpResponseRedirect(reverse('IABC_WEB:view_profile', args=(acc_id,)))
            except:
                messages.success(request, "Email is already used by another user")
                return HttpResponseRedirect(reverse('IABC_WEB:view_profile', args=(acc_id,)))
            
            #info = User.objects.get(pk=acc_id)
            #firstName = request.POST.get('firstName')
            #middleName = request.POST.get('middleName')
           # lastName = request.POST.get('lastName')
          #  email = request.POST.get('email')
          #  info.firstName = firstName
          #  info.middleName = middleName
          #  info.lastName = lastName
          #  info.email = email
          #  info.save()
           # return HttpResponseRedirect(reverse('IABC_WEB:view_profile', args=(acc_id,)))
           
    else:
        return redirect('IABC_WEB:home')
    
#Awards proof of payment for users
def userawards_proof(request, acc_id):
    try:
        id = request.user.id
        info = Awards_student.objects.filter(user_id=id).filter(is_paid=False)
        info2 = Awards_prof.objects.filter(user_id=id).filter(is_paid=False)
        info3 = User.objects.get(pk=acc_id)
        context = {'info':info, 'info2':info2, 'info3':info3}
        return render(request, 'user-proofofpaymentawards.html', context)
    except:
        return render(request, 'user-proofofpaymentawards.html')

def userawards_proofupload(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        file = request.FILES.get('proof')
        try:
            info = Awards_student.objects.get(pk=acc_id)
            info.file = file
            info.save()
            messages.success(request, "Succesfully Attached!")
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))
        except:
            
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))


def userawards_proofupload2(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        file = request.FILES.get('proof1')
        try:
            info = Awards_prof.objects.get(pk=acc_id)
            info.file = file
            info.save()
            messages.success(request, "Succesfully Attached!")
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))
        except:
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))



def userawards_proofdel(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        try:
            info = Awards_student.objects.get(pk=acc_id)
            info.delete()
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))
        except:
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,))) 


def userawards_proofdel2(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        try:
            info = Awards_prof.objects.get(pk=acc_id)
            info.delete()
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))
        except:
            return HttpResponseRedirect(reverse('IABC_WEB:userawards_proof', args=(id,)))            




#membership proof of payment for users
def usermembers_proof(request, acc_id):
    id = request.user.id
    info3 = User.objects.get(pk=id)
    try:
        id = request.user.id
        info = Members.objects.get(user_id=id)
        info3 = User.objects.get(pk=id)
        if info.is_paid==False:
            context = {'info':info, 'info3':info3}
            return render(request, 'user-proofofpaymentmembership.html', context)
        else:
            context = {'info3':info3}
            return render(request, 'user-proofofpaymentmembership.html', context)
    except:
        context = {'info3':info3}
        return render(request, 'user-proofofpaymentmembership.html', context)


def usermembers_proofupload(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        file = request.FILES.get('proof')
        try:
            info = Members.objects.get(pk=acc_id)
            info.file = file
            info.save()
            messages.success(request, "Succesfully Attached!")
            return HttpResponseRedirect(reverse('IABC_WEB:usermembers_proof', args=(id,)))
        except:
            
            return HttpResponseRedirect(reverse('IABC_WEB:usermembers_proof', args=(id,)))


def usermembers_proofdel(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        try:
            info = Members.objects.get(pk=acc_id)
            info.delete()
            return HttpResponseRedirect(reverse('IABC_WEB:usermembers_proof', args=(id,)))
        except:
            return HttpResponseRedirect(reverse('IABC_WEB:usermembers_proof', args=(id,))) 




def usertransachistory(request, acc_id):
    try:
        id = request.user.id
        info = OnlinePaymentHistory.objects.filter(user_id=id)
        info3 = User.objects.get(pk=id)
        context = {'info':info, 'info3':info3}
        return render(request, 'user-transacthistory.html', context)
    except:
        return render(request, 'user-transacthistory.html')


def renewalproof(request, acc_id):
    id = request.user.id
    info3 = User.objects.get(pk=id)
    try:
        id = request.user.id
        info = Members.objects.get(user_id=id)
        info3 = User.objects.get(pk=id)
        if info.for_renewal==True:
            context = {'info':info, 'info3':info3,}
            return render(request, 'user-proofofpaymentrenewal.html', context)
        else:
            context = {'info3':info3,}
            return render(request, 'user-proofofpaymentrenewal.html', context)
    except:
        context = {'info3':info3,}
        return render(request, 'user-proofofpaymentrenewal.html', context)


def renewalproofupload(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        file = request.FILES.get('proof')
        try:
            info = Members.objects.get(pk=acc_id)
            info.renewalfile = file
            info.save()
            messages.success(request, "Succesfully Attached!")
            return HttpResponseRedirect(reverse('IABC_WEB:renewalproof', args=(id,)))
        except:
            
            return HttpResponseRedirect(reverse('IABC_WEB:renewalproof', args=(id,)))

def renewalproofdelete(request, acc_id):
    if request.method == 'POST':
        id = request.user.id
        try:
            info = Members.objects.get(pk=acc_id)
            info.for_renewal=False
            info.save()
            return HttpResponseRedirect(reverse('IABC_WEB:renewalproof', args=(id,)))
        except:
            return HttpResponseRedirect(reverse('IABC_WEB:renewalproof', args=(id,))) 




def adrenewal(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.method == "GET":
    
                admmember = Members.objects.filter(for_renewal=True)
                
                
                context = {  'admmember':admmember ,

                    }

                return render(request, 'admin-renewal.html', context)
            elif request.method == "POST":
                search = request.POST.get('search')
                admmember = Members.objects.filter(email_address__contains=search).filter(for_renewal=True)
                context = {'admmember':admmember}
                return render(request, 'admin-renewal.html', context)
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')


def adminrenewalproof(request, mem_id):
    if request.user.is_authenticated:
        mem = Members.objects.get(pk=mem_id)
        mem.for_renewal = False
        mem.received_email = False
        mer = datetime.datetime.strptime(mem.expiry_date, "%Y-%m-%d").date()
        newexpiry = mer + relativedelta(years=1)
        mem.expiry_date = newexpiry
        mem.save()
        return redirect('IABC_WEB:adrenewal')









def admintransachistory(request):
    try:
        id = request.user.id
        info = OnlinePaymentHistory.objects.all()
        info3 = User.objects.get(pk=id)
        context = {'info':info, 'info3':info3}
        return render(request, 'admin-transacthistory.html', context)
    except:
        return render(request, 'admin-transacthistory.html')












def awardspaid(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            awardsstudentpaid = Awards_student.objects.filter(is_paid=True)
            awardsprofpaid = Awards_prof.objects.filter(is_paid=True)
            return render(request, 'admin-awardspaid.html', {'awardsprofpaid':awardsprofpaid,'awardsstudentpaid':awardsstudentpaid})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

#for student
def awardspaid_details(request, ent_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            award = Awards_student.objects.get(pk=ent_id)
            return render(request, 'admin-viewawardspaid.html', {'award':award})
        except:
            return render(request, 'admin-viewawardspaid.html')
    else:
        return redirect('members:home')

#for professional
def awardspaid_details2(request, ent_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            award = Awards_prof.objects.get(pk=ent_id)
            return render(request, 'admin-viewawardspaid.html', {'award':award})
        except:
            return render(request, 'admin-viewawardspaid.html')
    else:
        return redirect('members:home')




def awardspaid_del(request, awardspaid_id):
    if request.method == 'POST':
        awardsstudentpaid = Awards_student.objects.get(id=awardspaid_id)
        awardsstudentpaid.delete()
        return redirect('IABC_WEB:awardspaid')
    elif request.method == 'GET':
        awardsprofpaid = Awards_prof.objects.get(id=awardspaid_id)
        awardsprofpaid.delete()
        return redirect('IABC_WEB:awardspaid')

def awardspending_del(request, awardspend_id):
    if request.method == 'POST':
        awardsstudentpaid = Awards_student.objects.get(id=awardspend_id)
        awardsstudentpaid.delete()
        return redirect('IABC_WEB:awardspending')
    elif request.method == 'GET':
        awardsprofpaid = Awards_prof.objects.get(id=awardspend_id)
        awardsprofpaid.delete()
        return redirect('IABC_WEB:awardspending')


def awardspending(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            awardsstudentpending = Awards_student.objects.filter(is_paid=False)
            awardsprofpending = Awards_prof.objects.filter(is_paid=False)
            return render(request, 'admin-awardspending.html', {'awardsprofpending':awardsprofpending, 'awardsstudentpending':awardsstudentpending})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

#for student
def awardspending_details(request, ent_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            award = Awards_student.objects.get(pk=ent_id)
            return render(request, 'admin-viewawardspending.html', {'award':award})
        except:
            return render(request, 'admin-viewawardspending.html')
    else:
        return redirect('members:home')

#for professional
def awardspending_details2(request, ent_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            award = Awards_prof.objects.get(pk=ent_id)
            return render(request, 'admin-viewawardspending2.html', {'award':award})
        except:
            return render(request, 'admin-viewawardspending2.html')
    else:
        return redirect('members:home')


def awardspending_edit(request, ent_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            award = Awards_student.objects.get(pk=ent_id)
            stat = request.POST.get('remarks')
            if stat == "True":
                award.is_paid = True
                award.save()
                return redirect('IABC_WEB:awardspending')
            else:
                award.is_paid = False
                award.save()
                return redirect('IABC_WEB:awardspending')
        except:
            return redirect('IABC_WEB:awardspending')
    else:
        return redirect('members:home')

def awardspending_edit2(request, ent_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            award = Awards_prof.objects.get(pk=ent_id)
            stat = request.POST.get('remarks')
            if stat == "True":
                award.is_paid = True
                award.save()
                return redirect('IABC_WEB:awardspending')
            else:
                award.is_paid = False
                award.save()
                return redirect('IABC_WEB:awardspending')
        except:
            return redirect('IABC_WEB:awardspending')
    else:
        return redirect('members:home')




#def viewawardspaid(request, award_id):
    #awardsstudpaid = Awards_student.objects.get(pk=award_id)
    #awardsprofpaid = Awards_prof.objects.get(pk=award_id)
    #context = {'awardsstudpaid':awardsstudpaid , 'awardsprofpaid': awardsprofpaid}

    #return render

def awardsform(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.filter(id=id)
        div = Division.objects.all()
        category = Category.objects.all()
        cert = Certification.objects.all()
        return render(request, 'user-awardsform.html', {'info':info, 'div':div, 'category': category, 'cert':cert})
    else: 
        return HttpResponse('Login ka muna boi')


def awardsform2(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.filter(id=id)
        return render(request, 'user-awardsform2.html', {'info':info,})


def attach(request):
    if request.method == 'POST':
        if request.POST.get("attachh"):
            request.session['_ebill_data'] = request.POST
            data = request.session.get('_ebill_data')
            messages.success(request, 'Succesfully Attached!')  
            return redirect('IABC_WEB:awardsform2')
        else:
            return HttpResponse(data['tin'])
    else:
        return HttpResponse(data['comp'])
    # messages.success(request, 'Something went wrong!')  
    # return redirect('IABC_WEB:awardsform2')

#convert awards ebill to pdf
def aebill_pdf(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        dates = date.today()
        if info.is_member == True:
            data = request.session.get('_ebill_data')
            data2 = request.session.get('_submit_data')
            checks = data2['Awards']
            if checks == "student":
                template = get_template('awards-ebillstudent.html')
                context = {'dates':dates, 'comp':data['comp'], 'address':data['address'], 'tin':data['tin'], 'contp':data['contp'], 'contn':data['contn'],}

                html = template.render(context)
                pdf = render_to_pdf('awards-ebillstudent.html', context)

                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "E_BILL-%s.pdf" %info.lastName
                    content = "inline; filename=%s" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")


            else:
                template = get_template('awards-ebillmembers.html')
                context = {'dates':dates, 'comp':data['comp'], 'address':data['address'], 'tin':data['tin'], 'contp':data['contp'], 'contn':data['contn'],}

                html = template.render(context)
                pdf = render_to_pdf('awards-ebillmembers.html', context)

                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "E_BILL-%s.pdf" %info.lastName
                    content = "inline; filename=%s" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")

        elif info.is_nonmember == True:
            data = request.session.get('_ebill_data')
            data2 = request.session.get('_submit_data')
            checks = data2['Awards']
            if checks == "student":
                template = get_template('awards-ebillstudent.html')
                context = {'dates':dates, 'comp':data['comp'], 'address':data['address'], 'tin':data['tin'], 'contp':data['contp'], 'contn':data['contn'],}

                html = template.render(context)
                pdf = render_to_pdf('awards-ebillstudent.html', context)

                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "E_BILL-%s.pdf" %info.lastName
                    content = "inline; filename=%s" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")


            else: 
                template = get_template('awards-ebillnonmembers.html')
                context = {'dates':dates, 'comp':data['comp'], 'address':data['address'], 'tin':data['tin'], 'contp':data['contp'], 'contn':data['contn'],}

                html = template.render(context)
                pdf = render_to_pdf('awards-ebillnonmembers.html', context)

                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "E_BILL-%s.pdf" %info.lastName
                    content = "inline; filename=%s" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")

def awardssubmit(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if request.method == 'POST':
            awardsrad = request.POST.get("Awards", None)
            if "student" == awardsrad:
                ename=request.POST.get('sname')
                eschool=request.POST.get('sschool')
                edeg=request.POST.get('sdegree')
                enum=request.POST.get('snum')
                eemail=request.POST.get('semail')
                etitle=request.POST.get('entitle')
                ediv=request.POST.get('divi')
                ecat=request.POST.get('categ')
                before=request.POST.get('before')
                year= request.POST.get('year')
                entform=request.FILES.get('entform')
                cert=request.POST.get('cert')
                certf=request.FILES.get('certf')
                wplan=request.FILES.get('wplan', False)
                wsample=request.FILES.get('wsample')
                wsample2=request.FILES.get('wsample2')
                wsample3=request.FILES.get('wsample3')
                remarks=request.POST.get('remarkss')

                request.session['_submit_data'] = request.POST
    
                try:
                    student=Awards_student.objects.get(email_add=eemail)
                    messages.error(request, "Email Already Taken")
                    return redirect('IABC_WEB:awardsform')
                except ObjectDoesNotExist:
                    
                    student = Awards_student.objects.create(entrant_name=ename,mobile_num=enum,email_add=eemail,entrant_school=eschool,entrant_degree=edeg,entry_title=etitle,year=year, division=ediv, category=ecat, entry_form=entform, certtype=cert, certification_form=certf,  work_plan=wplan, work_sample=wsample, work_sample2=wsample2, work_sample3=wsample3, user_id=info, remarks=remarks)

                    if before == "yes":
                        student.entered_before = True
                    else :
                        student.entered_before = False

                    
                    info.save()
                    student.save()
                    return redirect('IABC_WEB:awardsform2')

            elif "profesh" == awardsrad: 
                ename=request.POST.get('pname')
                eorg=request.POST.get('peorg')
                ceorg=request.POST.get('pcorg')
                enum=request.POST.get('pnum')
                eemail=request.POST.get('pemail')
                etitle=request.POST.get('entitle')
                pmemb=request.POST.get('pmemb')
                pmemnum=request.POST.get('pmemnum')
                ptitle=request.POST.get('ptitle')
                ediv=request.POST.get('divi')
                ecat=request.POST.get('categ')
                before=request.POST.get('before')
                year= request.POST.get('year')
                entform=request.FILES.get('entform')
                cert=request.POST.get('cert')
                certf=request.FILES.get('certf')
                wplan=request.FILES.get('wplan')
                wsample=request.FILES.get('wsample')
                wsample2=request.FILES.get('wsample2')
                wsample3=request.FILES.get('wsample3')
                agency=request.POST.get('pagency')
                remarks=request.POST.get('remarkss')

                request.session['_submit_data'] = request.POST
                try:
                    student=Awards_prof.objects.get(email_add=eemail)
                    messages.error(request, "Email Already Taken")
                    return redirect('IABC_WEB:awardsform')
                except ObjectDoesNotExist:
                    prof = Awards_prof.objects.create(entrant_name=ename,mobile_num=enum,email_add=eemail,entrant_org=eorg,client_org=ceorg,entry_title=etitle,entrant_membershipnum=pmemnum,entrant_title=ptitle,year=year, division=ediv, category=ecat, entry_form=entform, certtype=cert, certification_form=certf,  work_plan=wplan, work_sample=wsample, work_sample2=wsample2, work_sample3=wsample3, user_id=info, agency=agency, remarks=remarks)

                    #if pmemb == True:


                    if before == "yes":
                        prof.entered_before = True
                    else :
                        prof.entered_before = False

                    if pmemb == "yes":
                        prof.entered_before = True
                    else :
                        prof.entered_before = False

                    info.save()
                    prof.save()
                    return redirect('IABC_WEB:awardsform2')




def memberapp(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.filter(id=id)
        chart_a = Chart_A.objects.all()
        chart_b = Chart_B.objects.all()
        chart_c = Chart_C.objects.all()
        chart_d = Chart_D.objects.all()
        chart_e = Chart_E.objects.all()
        chart_f = Chart_F.objects.all()
        chart_g = Chart_G.objects.all()
        context = { 'info':info, 'chart_a':chart_a, 'chart_b':chart_b, 'chart_c':chart_c , 'chart_d':chart_d  , 'chart_e':chart_e  , 'chart_f':chart_f  , 'chart_g':chart_g 
        }

        return render(request, 'user-application.html', context)
    else: 
        return HttpResponse('Login ka muna boi')

def paymentopt(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(pk=id)
        data = request.session.get('_submit_data')
        checks = data['Awards']
        if info.is_member == True:
            checker = True
            if checks == "student":
                info = True
                price=Prices.objects.get(priceName="Awards Student")
                context={'info':info, 'price':price}
                return render(request, 'user-paymentopt.html', context)
            elif checks == "profesh":
                price=Prices.objects.get(priceName="Awards Member")
                context={'checker':checker, 'price':price}
                return render(request, 'user-paymentopt.html', context)
        elif info.is_member == False:
            if checks == "student":
                info = True
                price=Prices.objects.get(priceName="Awards Student")
                context={'info':info, 'price':price}
                return render(request, 'user-paymentopt.html',  context)
            elif checks == "profesh":
                price=Prices.objects.get(priceName="Awards Non-Member")
                context={'price':price}
                return render(request, 'user-paymentopt.html', context)


def paymentoptmember(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(pk=id)
       
        price=Prices.objects.get(priceName="Membership")
        context={'price':price, 'info':info}
        return render(request, 'user-paymentoptmem.html', context)

def paymentoptrenew(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(pk=id)
       
        price=Prices.objects.get(priceName="Membership")
        context={'price':price, 'info':info}
        return render(request, 'user-paymentoptrenew.html', context)



def onlinepay(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            #priceawastud = Prices.objects.get(priceName="Awards Student")
            #priceawaprofmem = Prices.objects.get(priceName="Awards Member")
            #priceawaprofnon = Prices.objects.get(priceName="Awards Non-Member")
            #pricemem = Prices.objects.get(priceName="Membership")
            try :
                mem = Members.objects.get(user_id=id)
                if info.is_member == True:
                    
                    data = request.session.get('_submit_data')
                
                
                    checks = data['Awards']
                    checks1 = data['Awards']
                
                    if checks == "student":
                            if Awards_student is None:
                                    awards = Awards_student.objects.get(user_id=id)
                                    awards.is_paid = True
                                    awards.save()
                                    history = OnlinePaymentHistory.objects.create(typeProduct="Awards Student", user_id=info)
                                    history.save()
                                    mail_id=info.email
                                    email=EmailMessage(
                                        'IABC Payment Notification',
                                        'Your paypal account has been deducted P500',
                                        settings.EMAIL_HOST_USER,
                                        [mail_id]
                                    )
                                    email.fail_silently = True
                                    email.send()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form1')
                                    
                            elif Awards_student is not None:
                                    awards = Awards_student.objects.filter(user_id=id)
                                    awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa in awardss:
                                        awa=awa+1
                                    awardss1 = Awards_student.objects.get(id=awa-1)
                                    awardss1.is_paid = True
                                    awardss1.save()
                                    history = OnlinePaymentHistory.objects.create(typeProduct="Awards Student", user_id=info)
                                    history.save()
                                    mail_id=info.email
                                    email=EmailMessage(
                                        'IABC Payment Notification',
                                        'Your paypal account has been deducted P500',
                                        settings.EMAIL_HOST_USER,
                                        [mail_id]
                                    )
                                    email.fail_silently = True
                                    email.send()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form2')
                                    
                
                        
                    elif checks1 == "profesh" :     
                                        
                            if Awards_prof is None:
                                        awards2 = Awards_prof.objects.get(user_id=id)
                                        awards2.is_paid = True
                                        awards2.save()
                                        history = OnlinePaymentHistory.objects.create(typeProduct="Awards Professional", user_id=info)
                                        history.save()
                                        mail_id=info.email
                                        email=EmailMessage(
                                            'IABC Payment Notification',
                                            'Your paypal account has been deducted P6000',
                                            settings.EMAIL_HOST_USER,
                                            [mail_id]
                                        )
                                        email.fail_silently = True
                                        email.send()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form1')
                            elif Awards_prof is not None:
                                        awards2 = Awards_prof.objects.filter(user_id=id)
                                        awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa1 in awardss2:
                                            awa1=awa1+1
                                        awardss3 = Awards_prof.objects.get(id=awa1-1)
                                        awardss3.is_paid = True
                                        awardss3.save()
                                        history = OnlinePaymentHistory.objects.create(typeProduct="Awards Professional", user_id=info)
                                        history.save()
                                        mail_id=info.email
                                        email=EmailMessage(
                                            'IABC Payment Notification',
                                            'Your paypal account has been deducted P6000',
                                            settings.EMAIL_HOST_USER,
                                            [mail_id]
                                        )
                                        email.fail_silently = True
                                        email.send()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form2')

                elif info.is_member == False:
                    data = request.session.get('_submit_data')
                    try: 
                        checks = data['Awards']
                        checks1 = data['Awards']
                    
                        if checks == "student":
                                if Awards_student is None:
                                        awards = Awards_student.objects.get(user_id=id)
                                        awards.is_paid = True
                                        awards.save()
                                        history = OnlinePaymentHistory.objects.create(typeProduct="Awards Student", user_id=info)
                                        history.save()
                                        mail_id=info.email
                                        email=EmailMessage(
                                            'IABC Payment Notification',
                                            'Your paypal account has been deducted P500',
                                            settings.EMAIL_HOST_USER,
                                            [mail_id]
                                        )
                                        email.fail_silently = True
                                        email.send()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Student Awards form1')
                                        
                                elif Awards_student is not None:
                                        awards = Awards_student.objects.filter(user_id=id)
                                        awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa in awardss:
                                            awa=awa+1
                                        awardss1 = Awards_student.objects.get(id=awa-1)
                                        awardss1.is_paid = True
                                        awardss1.save()
                                        history = OnlinePaymentHistory.objects.create(typeProduct="Awards Student", user_id=info)
                                        history.save()
                                        mail_id=info.email
                                        email=EmailMessage(
                                            'IABC Payment Notification',
                                            'Your paypal account has been deducted P500',
                                            settings.EMAIL_HOST_USER,
                                            [mail_id]
                                        )
                                        email.fail_silently = True
                                        email.send()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Student Awards form2')
                                        
                    
                            
                        elif checks1 == "profesh" :     
                                            
                                if Awards_prof is None:
                                            awards2 = Awards_prof.objects.get(user_id=id)
                                            awards2.is_paid = True
                                            awards2.save()
                                            history = OnlinePaymentHistory.objects.create(typeProduct="Awards Professional", user_id=info)
                                            history.save()
                                            mail_id=info.email
                                            email=EmailMessage(
                                                'IABC Payment Notification',
                                                'Your paypal account has been deducted P8000',
                                                settings.EMAIL_HOST_USER,
                                                [mail_id]
                                            )
                                            email.fail_silently = True
                                            email.send()
                                            del request.session['_submit_data']
                                            return redirect('members:home')
                                            #return HttpResponse('Prof Awards form1')
                                elif Awards_prof is not None:
                                            awards2 = Awards_prof.objects.filter(user_id=id)
                                            awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                            for awa1 in awardss2:
                                                awa1=awa1+1
                                            awardss3 = Awards_prof.objects.get(id=awa1-1)
                                            awardss3.is_paid = True
                                            awardss3.save()
                                            history = OnlinePaymentHistory.objects.create(typeProduct="Awards Professional", user_id=info)
                                            history.save()
                                            mail_id=info.email
                                            email=EmailMessage(
                                                'IABC Payment Notification',
                                                'Your paypal account has been deducted P8000',
                                                settings.EMAIL_HOST_USER,
                                                [mail_id]
                                            )
                                            email.fail_silently = True
                                            email.send()
                                            del request.session['_submit_data']
                                            return redirect('members:home')
                                            #return HttpResponse('Prof Awards form2')
                    except TypeError:
                        mem.is_paid = True
                        info.is_member = True
                        info.is_nonmember = False
                        info.save()
                        mem.save()
                        history = OnlinePaymentHistory.objects.create(typeProduct="Membership", user_id=info)
                        history.save()
                        mail_id=info.email
                        email=EmailMessage(
                            'IABC Payment Notification',
                            'Your paypal account has been deducted P18,000',
                            settings.EMAIL_HOST_USER,
                            [mail_id]
                        )
                        email.fail_silently = True
                        email.send()
                        return redirect('members:home')
                        #return HttpResponse('Good Job!')                
                                
            except ObjectDoesNotExist:
                data = request.session.get('_submit_data')
                
                
                checks = data['Awards']
                checks1 = data['Awards']
               
                if checks == "student":
                        if Awards_student is None:
                                awards = Awards_student.objects.get(user_id=id)
                                awards.is_paid = True
                                awards.save()
                                history = OnlinePaymentHistory.objects.create(typeProduct="Awards Student", user_id=info)
                                history.save()
                                mail_id=info.email
                                email=EmailMessage(
                                    'IABC Payment Notification',
                                    'Your paypal account has been deducted P500',
                                    settings.EMAIL_HOST_USER,
                                    [mail_id]
                                )
                                email.fail_silently = True
                                email.send()
                                del request.session['_submit_data']
                                return redirect('members:home')
                                #return HttpResponse('Student Awards form1')
                                
                        elif Awards_student is not None:
                                awards = Awards_student.objects.filter(user_id=id)
                                awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                for awa in awardss:
                                    awa=awa+1
                                awardss1 = Awards_student.objects.get(id=awa-1)
                                awardss1.is_paid = True
                                awardss1.save()
                                history = OnlinePaymentHistory.objects.create(typeProduct="Awards Student", user_id=info)
                                history.save()
                                mail_id=info.email
                                email=EmailMessage(
                                    'IABC Payment Notification',
                                    'Your paypal account has been deducted P500',
                                    settings.EMAIL_HOST_USER,
                                    [mail_id]
                                )
                                email.fail_silently = True
                                email.send()
                                del request.session['_submit_data']
                                return redirect('members:home')
                                #return HttpResponse('Student Awards form2')
                                
               
                    
                elif checks1 == "profesh" :     
                                    
                        if Awards_prof is None:
                                    awards2 = Awards_prof.objects.get(user_id=id)
                                    awards2.is_paid = True
                                    awards2.save()
                                    history = OnlinePaymentHistory.objects.create(typeProduct="Awards Professional", user_id=info)
                                    history.save()
                                    mail_id=info.email
                                    email=EmailMessage(
                                        'IABC Payment Notification',
                                        'Your paypal account has been deducted P8000',
                                        settings.EMAIL_HOST_USER,
                                        [mail_id]
                                    )
                                    email.fail_silently = True
                                    email.send()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Prof Awards form1')
                        elif Awards_prof is not None:
                                    awards2 = Awards_prof.objects.filter(user_id=id)
                                    awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa1 in awardss2:
                                        awa1=awa1+1
                                    awardss3 = Awards_prof.objects.get(id=awa1-1)
                                    awardss3.is_paid = True
                                    awardss3.save()
                                    history = OnlinePaymentHistory.objects.create(typeProduct="Awards Professional", user_id=info)
                                    history.save()
                                    mail_id=info.email
                                    email=EmailMessage(
                                        'IABC Payment Notification',
                                        'Your paypal account has been deducted P8000',
                                        settings.EMAIL_HOST_USER,
                                        [mail_id]
                                    )
                                    email.fail_silently = True
                                    email.send()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Prof Awards form2')
                                
                
                        
                    
                
                    


def overtc(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            try :
                mem = Members.objects.get(user_id=id)
                if info.is_member == True:
                    
                    data = request.session.get('_submit_data')
                
                
                    checks = data['Awards']
                    checks1 = data['Awards']
                
                    if checks == "student":
                            if Awards_student is None:
                                    awards = Awards_student.objects.get(user_id=id)
                                    awards.is_paid = False
                                    awards.save()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form1')
                                    
                            elif Awards_student is not None:
                                    awards = Awards_student.objects.filter(user_id=id)
                                    awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa in awardss:
                                        awa=awa+1
                                    awardss1 = Awards_student.objects.get(id=awa-1)
                                    awardss1.is_paid = False
                                    awardss1.save()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form2')
                                    
                
                        
                    elif checks1 == "profesh" :     
                                        
                            if Awards_prof is None:
                                        awards2 = Awards_prof.objects.get(user_id=id)
                                        awards2.is_paid = False
                                        awards2.save()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form1')
                            elif Awards_prof is not None:
                                        awards2 = Awards_prof.objects.filter(user_id=id)
                                        awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa1 in awardss2:
                                            awa1=awa1+1
                                        awardss3 = Awards_prof.objects.get(id=awa1-1)
                                        awardss3.is_paid = False
                                        awardss3.save()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form2')

                elif info.is_member == False:
                    data = request.session.get('_submit_data')
                    try:
                        checks = data['Awards']
                        checks1 = data['Awards']
                    
                        if checks == "student":
                                if Awards_student is None:
                                        awards = Awards_student.objects.get(user_id=id)
                                        awards.is_paid = False
                                        awards.save()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Student Awards form1')
                                        
                                elif Awards_student is not None:
                                        awards = Awards_student.objects.filter(user_id=id)
                                        awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa in awardss:
                                            awa=awa+1
                                        awardss1 = Awards_student.objects.get(id=awa-1)
                                        awardss1.is_paid = False
                                        awardss1.save()
                                        del request.session['_submit_data']
                                        return redirect('members:home')
                                        #return HttpResponse('Student Awards form2')
                                        
                    
                            
                        elif checks1 == "profesh" :     
                                            
                                if Awards_prof is None:
                                            awards2 = Awards_prof.objects.get(user_id=id)
                                            awards2.is_paid = False
                                            awards2.save()
                                            del request.session['_submit_data']
                                            return redirect('members:home')
                                            #return HttpResponse('Prof Awards form1')
                                elif Awards_prof is not None:
                                            awards2 = Awards_prof.objects.filter(user_id=id)
                                            awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                            for awa1 in awardss2:
                                                awa1=awa1+1
                                            awardss3 = Awards_prof.objects.get(id=awa1-1)
                                            awardss3.is_paid = False
                                            awardss3.save()
                                            del request.session['_submit_data']
                                            return redirect('members:home')
                                            #return HttpResponse('Prof Awards form2'
                    except TypeError:
                        mem.is_paid = False
                        info.is_member = True
                        info.is_nonmember = False
                        info.save()
                        mem.save()
                        return redirect('members:home')
                        #return HttpResponse('Good Job!')                
                                
            except ObjectDoesNotExist:
                data = request.session.get('_submit_data')
                
                
                checks = data['Awards']
                checks1 = data['Awards']
               
                if checks == "student":
                        if Awards_student is None:
                                awards = Awards_student.objects.get(user_id=id)
                                awards.is_paid = False
                                awards.save()
                                del request.session['_submit_data']
                                return redirect('members:home')
                                #return HttpResponse('Student Awards form1')
                                
                        elif Awards_student is not None:
                                awards = Awards_student.objects.filter(user_id=id)
                                awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                for awa in awardss:
                                    awa=awa+1
                                awardss1 = Awards_student.objects.get(id=awa-1)
                                awardss1.is_paid = False
                                awardss1.save()
                                del request.session['_submit_data']
                                return redirect('members:home')
                                #return HttpResponse('Student Awards form2')
                                
               
                    
                elif checks1 == "profesh" :     
                                    
                        if Awards_prof is None:
                                    awards2 = Awards_prof.objects.get(user_id=id)
                                    awards2.is_paid = False
                                    awards2.save()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Prof Awards form1')
                        elif Awards_prof is not None:
                                    awards2 = Awards_prof.objects.filter(user_id=id)
                                    awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa1 in awardss2:
                                        awa1=awa1+1
                                    awardss3 = Awards_prof.objects.get(id=awa1-1)
                                    awardss3.is_paid = False
                                    awardss3.save()
                                    del request.session['_submit_data']
                                    return redirect('members:home')
                                    #return HttpResponse('Prof Awards form2')
def check(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            try :
                mem = Members.objects.get(user_id=id)
                if info.is_member == True:
                    
                    data = request.session.get('_submit_data')
                
                
                    checks = data['Awards']
                    checks1 = data['Awards']
                
                    if checks == "student":
                            if Awards_student is None:
                                    awards = Awards_student.objects.get(user_id=id)
                                    awards.is_paid = False
                                    awards.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form1')
                                    
                            elif Awards_student is not None:
                                    awards = Awards_student.objects.filter(user_id=id)
                                    awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa in awardss:
                                        awa=awa+1
                                    awardss1 = Awards_student.objects.get(id=awa-1)
                                    awardss1.is_paid = False
                                    awardss1.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form2')
                                    
                
                        
                    elif checks1 == "profesh" :     
                                        
                            if Awards_prof is None:
                                        awards2 = Awards_prof.objects.get(user_id=id)
                                        awards2.is_paid = False
                                        awards2.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form1')
                            elif Awards_prof is not None:
                                        awards2 = Awards_prof.objects.filter(user_id=id)
                                        awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa1 in awardss2:
                                            awa1=awa1+1
                                        awardss3 = Awards_prof.objects.get(id=awa1-1)
                                        awardss3.is_paid = False
                                        awardss3.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form2')

                elif info.is_member == False:
                    data = request.session.get('_submit_data')
                    try:
                        checks = data['Awards']
                        checks1 = data['Awards']
                    
                        if checks == "student":
                                if Awards_student is None:
                                        awards = Awards_student.objects.get(user_id=id)
                                        awards.is_paid = False
                                        awards.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Student Awards form1')
                                        
                                elif Awards_student is not None:
                                        awards = Awards_student.objects.filter(user_id=id)
                                        awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa in awardss:
                                            awa=awa+1
                                        awardss1 = Awards_student.objects.get(id=awa-1)
                                        awardss1.is_paid = False
                                        awardss1.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Student Awards form2')
                                        
                    
                            
                        elif checks1 == "profesh" :     
                                            
                                if Awards_prof is None:
                                            awards2 = Awards_prof.objects.get(user_id=id)
                                            awards2.is_paid = False
                                            awards2.save()
                                            return redirect('members:home')
                                            #return HttpResponse('Prof Awards form1')
                                elif Awards_prof is not None:
                                            awards2 = Awards_prof.objects.filter(user_id=id)
                                            awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                            for awa1 in awardss2:
                                                awa1=awa1+1
                                            awardss3 = Awards_prof.objects.get(id=awa1-1)
                                            awardss3.is_paid = False
                                            awardss3.save()
                                            return redirect('members:home')
                                            #return HttpResponse('Prof Awards form2'
                    except TypeError:
                        mem.is_paid = False
                        info.is_member = True
                        info.is_nonmember = False
                        info.save()
                        mem.save()
                        return redirect('members:home')
                        #return HttpResponse('Good Job!')                 
                                
            except ObjectDoesNotExist:
                data = request.session.get('_submit_data')
                
                
                checks = data['Awards']
                checks1 = data['Awards']
               
                if checks == "student":
                        if Awards_student is None:
                                awards = Awards_student.objects.get(user_id=id)
                                awards.is_paid = False
                                awards.save()
                                return redirect('members:home')
                                #return HttpResponse('Student Awards form1')
                                
                        elif Awards_student is not None:
                                awards = Awards_student.objects.filter(user_id=id)
                                awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                for awa in awardss:
                                    awa=awa+1
                                awardss1 = Awards_student.objects.get(id=awa-1)
                                awardss1.is_paid = False
                                awardss1.save()
                                return redirect('members:home')
                                #return HttpResponse('Student Awards form2')
                                
               
                    
                elif checks1 == "profesh" :     
                                    
                        if Awards_prof is None:
                                    awards2 = Awards_prof.objects.get(user_id=id)
                                    awards2.is_paid = False
                                    awards2.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Prof Awards form1')
                        elif Awards_prof is not None:
                                    awards2 = Awards_prof.objects.filter(user_id=id)
                                    awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa1 in awardss2:
                                        awa1=awa1+1
                                    awardss3 = Awards_prof.objects.get(id=awa1-1)
                                    awardss3.is_paid = False
                                    awardss3.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Prof Awards form2')

    if request.method == 'POST':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            try:
                mem = Members.objects.get(user_id=id)
                if info.is_member == True:
                    data = request.session.get('_submit_data')
                    checks = data['Awards']
                    checks1 = data['Awards']
                
                    if checks == "student":
                            if Awards_student is None:
                                    awards = Awards_student.objects.get(user_id=id)
                                    cperson = request.POST.get('cperson')
                                    cnum = request.POST.get('cnum')
                                    address = request.POST.get('address')
                                    cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=None,  awards_studentid=awards)
                                    awards.is_paid = False
                                        
                                    cpay.save()
                                    
                                    awards.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form1')
                                    
                            elif Awards_student is not None:
                                    awards = Awards_student.objects.filter(user_id=id)
                                    awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa in awardss:
                                        awa=awa+1
                                    awardss1 = Awards_student.objects.get(id=awa-1)
                                    cperson = request.POST.get('cperson')
                                    cnum = request.POST.get('cnum')
                                    address = request.POST.get('address')
                                    cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=None,  awards_studentid=awardss1)
                                   
                                    awardss1.is_paid = False   
                                    cpay.save()
                                    
                                    awardss1.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form2')

                    elif checks1 == "profesh" :     
                                        
                            if Awards_prof is None:
                                        awards2 = Awards_prof.objects.get(user_id=id)
                                        cperson = request.POST.get('cperson')
                                        cnum = request.POST.get('cnum')
                                        address = request.POST.get('address')
                                        cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=awards2,  awards_studentid=None)
                                            
                                        cpay.save()
                                        awards2.is_paid = False
                                        awards2.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form1')
                            elif Awards_prof is not None:
                                        awards2 = Awards_prof.objects.filter(user_id=id)
                                        awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa1 in awardss2:
                                            awa1=awa1+1
                                        awardss3 = Awards_prof.objects.get(id=awa1-1)
                                        cperson = request.POST.get('cperson')
                                        cnum = request.POST.get('cnum')
                                        address = request.POST.get('address')
                                        cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=awardss3,  awards_studentid=None)
                                            
                                        cpay.save()
                                        awardss3.is_paid = False
                                        awardss3.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form2')

                elif info.is_member == False:
                        info.is_pending = True
                        info.is_nonmember = False
                        info.save()
                        return redirect('members:home')
                        #return HttpResponse('Good Job!')  
                    

            except ObjectDoesNotExist:
                    data = request.session.get('_submit_data')
                
                
                    checks = data['Awards']
                    checks1 = data['Awards']
                
                    if checks == "student":
                            if Awards_student is None:
                                    awards = Awards_student.objects.get(user_id=id)
                                    cperson = request.POST.get('cperson')
                                    cnum = request.POST.get('cnum')
                                    address = request.POST.get('address')
                                    cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=None,  awards_studentid=awards)
                                    awards.is_paid = False
                                        
                                    cpay.save()
                                    
                                    awards.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form1')
                                    
                            elif Awards_student is not None:
                                    awards = Awards_student.objects.filter(user_id=id)
                                    awardss = Awards_student.objects.filter(user_id=id).values_list('id', flat=True)
                                    for awa in awardss:
                                        awa=awa+1
                                    awardss1 = Awards_student.objects.get(id=awa-1)
                                    cperson = request.POST.get('cperson')
                                    cnum = request.POST.get('cnum')
                                    address = request.POST.get('address')
                                    cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=None,  awards_studentid=awardss1)
                                   
                                    awardss1.is_paid = False   
                                    cpay.save()
                                    
                                    awardss1.save()
                                    return redirect('members:home')
                                    #return HttpResponse('Student Awards form2')

                    elif checks1 == "profesh" :     
                                        
                            if Awards_prof is None:
                                        awards2 = Awards_prof.objects.get(user_id=id)
                                        cperson = request.POST.get('cperson')
                                        cnum = request.POST.get('cnum')
                                        address = request.POST.get('address')
                                        cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=awards2,  awards_studentid=None)
                                            
                                        cpay.save()
                                        awards2.is_paid = False
                                        awards2.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form1')
                            elif Awards_prof is not None:
                                        awards2 = Awards_prof.objects.filter(user_id=id)
                                        awardss2 = Awards_prof.objects.filter(user_id=id).values_list('id', flat=True)
                                        for awa1 in awardss2:
                                            awa1=awa1+1
                                        awardss3 = Awards_prof.objects.get(id=awa1-1)
                                        cperson = request.POST.get('cperson')
                                        cnum = request.POST.get('cnum')
                                        address = request.POST.get('address')
                                        cpay = Checkpayment.objects.create(cperson=cperson, cnum=cnum, address=address, user_id =info, membership_id = None,  awards_profid=awardss3,  awards_studentid=None)
                                            
                                        cpay.save()
                                        awardss3.is_paid = False
                                        awardss3.save()
                                        return redirect('members:home')
                                        #return HttpResponse('Prof Awards form2')

def onlinepayrenew(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            #priceawastud = Prices.objects.get(priceName="Awards Student")
            #priceawaprofmem = Prices.objects.get(priceName="Awards Member")
            #priceawaprofnon = Prices.objects.get(priceName="Awards Non-Member")
            #pricemem = Prices.objects.get(priceName="Membership")
            
            mem = Members.objects.get(user_id=id)
            mem.received_email = False    
            mer = datetime.datetime.strptime(mem.expiry_date, "%Y-%m-%d").date()
            newexpiry = mer + relativedelta(years=1)
            mem.expiry_date=newexpiry
            mem.save()
            #mem.is_paid = True
            #info.is_member = True
            #info.is_nonmember = False
            #info.save()
            #mem.save()
            history = OnlinePaymentHistory.objects.create(typeProduct="Renewal", user_id=info)
            history.save()
            mail_id=info.email
            email=EmailMessage(
                    'IABC Payment Notification',
                    'Your paypal account has been deducted P18,000 for renewal',
                    settings.EMAIL_HOST_USER,
                    [mail_id]
                        )
            email.fail_silently = True
            email.send()
            return redirect('members:home')
             #return HttpResponse('Good Job!')                
                                
                                

def overtcrenew(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            
            mem = Members.objects.get(user_id=id)
                
            mem.for_renewal = True
            #info.is_member = True
            #info.is_nonmember = False
            #info.save()
            mem.save()
            return redirect('members:home')
            #return HttpResponse('Good Job!')                
                                
            
def checkrenew(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            info = User.objects.get(id=id)
            if request.method == 'GET':
                if request.user.is_authenticated:
                    id = request.user.id
                    info = User.objects.get(id=id)
                    
                    mem = Members.objects.get(user_id=id)
                        
                    mem.for_renewal = True
                    #info.is_member = True
                    #info.is_nonmember = False
                    #info.save()
                    mem.save()
                    return redirect('members:home')
                    #return HttpResponse('Good Job!')    

            #if request.method == 'POST':
                #if request.user.is_authenticated:
                    #id = request.user.id
                    #info = User.objects.get(id=id)
                    #mem = Members.objects.get(user_id=id)
                        


def admember(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.method == "GET":
    
                admmember = Members.objects.filter(is_paid=True)
                
                
                context = {  'admmember':admmember ,

                    }

                return render(request, 'admin-members.html', context)
            elif request.method == "POST":
                search = request.POST.get('search')
                admmember = Members.objects.filter(email_address__contains=search).filter(is_paid=True)
                context = {'admmember':admmember}
                return render(request, 'admin-members.html', context)
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')


def pendmember(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.method == "GET":

                pendmember= Members.objects.filter(is_paid=False)
                
                
                context = {  'pendmember':pendmember ,

                    }

                return render(request, 'admin-pendingmembers.html', context)
            elif request.method == "POST":
                search = request.POST.get('search')
                pendmember = Members.objects.filter(email_address__contains=search).filter(is_paid=False)
                context = {'pendmember':pendmember}
                return render(request, 'admin-pendingmembers.html', context)

        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def viewmember(request, viewmem_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            viewmember=Members.objects.get(pk=viewmem_id)
            return render(request, 'admin-viewmembers.html', {'viewmember':viewmember})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def viewpendmember(request, viewpendmem_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            viewpendmember=Members.objects.get(pk=viewpendmem_id)
            context = {'viewpendmember':viewpendmember}
            return render(request, 'admin-viewpendingmembers.html', context)
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def editviewmember(request, editviewmem_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.method == "GET":
                editviewmember=Members.objects.get(pk=editviewmem_id)
                
                return render(request, 'admin-editviewmembers.html', {'editviewmember':editviewmember})
            elif request.method == "POST":
                editviewmember=Members.objects.get(pk=editviewmem_id)
                memid = editviewmember.user_id
                info = User.objects.get(email=memid)
                expiry = request.POST.get('expiry')
                firstName = request.POST.get('fname')
                middleName = request.POST.get('mname')
                lastName = request.POST.get('lname')
                email = request.POST.get('email')
                #info.firstName = firstName
                #info.middleName = middleName
                #info.lastName = lastName
                #if email == info.email:
                    #messages.error(request, "Email is already taken")
                    #return HttpResponseRedirect(reverse('IABC_WEB:editviewmember', args=(editviewmem_id,)))
                #else:
                    #info.email = email
                editviewmember.received_email= False
                editviewmember.expiry_date=expiry
                editviewmember.save()
                #info.save()
                messages.success(request, "Save Successfully")
                return HttpResponseRedirect(reverse('IABC_WEB:editviewmember', args=(editviewmem_id,)))
        
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')



def editpendmember(request, editpendmem_id):
    if request.method == "GET":
        editpendmember=Members.objects.get(pk=editpendmem_id)
        return render(request, 'admin-viewpendingmembers.html', {'editpendmember':editpendmember})
    elif request.method == "POST":
        editpendmember=Members.objects.get(pk=editpendmem_id)
        memid = editpendmember.user_id
        info = User.objects.get(email=memid)
        remarks = request.POST.get('remarks')
        if remarks == "1":
            editpendmember.is_paid = True
            info.is_member = True
            info.is_nonmember=False        
            info.save()
            editpendmember.save()
            return redirect('IABC_WEB:pendmember')
        elif remarks == "2":
            editpendmember.is_paid = False
            info.is_member = False        
            info.save()
            editpendmember.save()
            return HttpResponseRedirect(reverse('IABC_WEB:viewpendmember', args=(editpendmem_id,)))
        else:
            return HttpResponseRedirect(reverse('IABC_WEB:viewpendmember', args=(editpendmem_id,)))



def member_del(request, mem_id):
    member=Members.objects.get(pk=mem_id)
    memid = member.user_id
    info = User.objects.get(email=memid)
    info.is_member = False
    info.is_nonmember = True
    #info.is_active = False
    #info.date_inactive = datetime.datetime.now()
    info.save()
    member.delete()
    return redirect('IABC_WEB:admember')

def pendmember_del(request, pendmem_id):
    member=Members.objects.get(pk=pendmem_id)
    pendmemid = member.user_id
    info = User.objects.get(email=pendmemid)
    info.is_pending = False
    info.is_nonmember = True
    #info.is_active = False
    #info.date_inactive = datetime.datetime.now()
    info.save()
    member.delete()
    return redirect('IABC_WEB:pendmember')

def membersubmit(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
    try :
        member = Members.objects.get(user_id=id)
        if member.is_paid == True:
            messages.success(request, "You are already a member")
            return redirect('IABC_WEB:memberapp')
        else:
            messages.success(request, "You have already submitted an application")
            return redirect('IABC_WEB:memberapp')
    except ObjectDoesNotExist:

            nick_name = request.POST.get('Nickname')
            desig = request.POST.get('Desig')
            comp = request.POST.get('comp')
            flr = request.POST.get('flr')
            bldg = request.POST.get('bldg')
            strt = request.POST.get('strt')
            brgy = request.POST.get('brgy')
            city = request.POST.get('city')
            reg = request.POST.get('reg')
            post = request.POST.get('post')
            tel = request.POST.get('tel')
            fax = request.POST.get('fax')
            mobile = request.POST.get('mobile')
            bday = request.POST.get('bday')
            check = request.POST.getlist("check", None)
            question_1 = request.POST.get('que1')
            question_2 = request.POST.get('que2')
            question_3 = request.POST.get('que3')
            question_4 = request.POST.get('que4')
            question_5 = request.POST.get('que5')
            question_6 = request.POST.get('que6')
            question_7 = request.POST.get('que7')
            question_8 = request.POST.get('que8')
            question_9 = request.POST.get('que9')
            question_10 = request.POST.get('que10')
            contact = request.POST.getlist("contact", None)
            announce = request.POST.getlist("announce", None)
            prof = request.FILES.get('profile')

        #chart_a = Chart_A.objects.get(industry_Name=question_3)
            #chart_b = Chart_B.objects.get(business_type=question_4)
            #chart_c = Chart_C.objects.get(current_title=question_5)
            #chart_d = Chart_D.objects.get(key_area=question_6)
            #chart_e = Chart_E.objects.get(employee_no=question_7)
            #chart_f = Chart_F.objects.get(experience=question_8)
            #chart_f1 = Chart_F.objects.get(experience=question_9)
            #chart_f2 = chart_f1.experience
            #chart_g = Chart_G.objects.get(about=question_10)
            

            if request.method == 'POST':
                members = Members.objects.create(nick_name=nick_name, designation=desig, company_name=comp,floor_no=flr,building_no=bldg,street=strt,baranggay=brgy,city=city,region=reg,postal_zip=post,telephone_no=tel,fax_no=fax,mobile_no=mobile,email_address=info.email,birthday=bday, question_1=question_1, question_2=question_2, industry_Name=question_3, business_type=question_4, current_title=question_5, key_area=question_6, employee_no=question_7,experience=question_8,interest=question_9,  about =question_10, profile_photo=prof, user_id=info)

                if "Membership" in check:
                    members.membership = True
                if "Excel" in check:
                    members.ceo_excel = True
                if "Regional" in check:
                    members.regional_conf = True
                if "Media" in check:
                    members.media_relations = True
                if "Digital" in check:
                    members.digital_comm = True
                if "PhilQuill" in check:
                    members.phil_quill = True
                if "Public" in check:
                    members.publication = True
                if "Sponsor" in check:
                    members.sponsorship = True
                if "yes" in contact:
                    members.share_contact = True
                if "yes" in announce:
                    members.receive_announce = True
                
                    
                members.save()
            return redirect('IABC_WEB:memberform2')



def memberform2(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.filter(id=id)
        return render(request, 'user-memberform.html', {'info':info,})


def attach2(request):
    if request.method == 'POST':
        if request.POST.get("attachh"):
            request.session['_memebill_data'] = request.POST
            messages.success(request, 'Succesfully Attached!')  
            return redirect('IABC_WEB:memberform2')
        else:
            return HttpResponse("There was an unexpected error")
    else:
        return HttpResponse("There was an unexpected error")


def memebill_pdf(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        dates = date.today()
        data = request.session.get('_memebill_data')
        template = get_template('membership-ebillapplication.html')
        context = {'dates':dates, 'comp':data['comp'], 'address':data['address'], 'tin':data['tin'], 'contp':data['contp'], 'contn':data['contn'],}

        html = template.render(context)
        pdf = render_to_pdf('membership-ebillapplication.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "E_BILL-%s.pdf" %info.lastName
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    else:
        return redirect('IABC_WEB:home')


def renewform(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.filter(id=id)
        return render(request, 'user-renewform.html', {'info':info,})

def renewattach(request):
    if request.method == 'POST':
        if request.POST.get("renew-attach"):
            request.session['_renew_data'] = request.POST
            messages.success(request, 'Succesfully Attached!')  
            return redirect('IABC_WEB:renewform')
        else:
            return HttpResponse("There was an unexpected error")
    else:
        return HttpResponse("There was an unexpected error")


def renewbill_pdf(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        dates = date.today()
        data = request.session.get('_renew_data')
        template = get_template('membership-ebillrenew.html')
        context = {'dates':dates, 'comp':data['comp'], 'address':data['address'], 'tin':data['tin'], 'contp':data['contp'], 'contn':data['contn'],}

        html = template.render(context)
        pdf = render_to_pdf('membership-ebillrenew.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "E_BILL-%s.pdf" %info.lastName
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    else:
        return redirect('IABC_WEB:home')








def nonmember(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            non_members= User.objects.filter(is_nonmember=True).filter(is_admin=False).filter(is_bidder=False).filter(is_active=True)
            context = {'non_members' : non_members}
            return render(request, 'admin-nonmembers.html', context)
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def nonmember_view(request, non_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = User.objects.get(pk=non_id)
            return render(request, 'admin-viewnonmembers.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def nonmember_edit(request, non_id):
    if request.method == 'GET':
        info = User.objects.get(pk=non_id)
        return render(request, 'admin-editviewnonmembers.html', {'info':info})
    elif request.method == "POST":
        try:
            info = User.objects.get(pk=non_id)
            firstName = request.POST.get('firstName')
            middleName = request.POST.get('middleName')
            lastName = request.POST.get('lastName')
            email = request.POST.get('email')
            info.firstName = firstName
            info.middleName = middleName
            info.lastName = lastName
            info.email = email
            info.save()
            return HttpResponseRedirect(reverse('IABC_WEB:nonmember_view', args=(non_id,)))
        except:
            messages.success(request, "Email is already used by another user")
            return HttpResponseRedirect(reverse('IABC_WEB:nonmember_view', args=(non_id,)))

def nonmember_del(request, non_id):
    non_member=User.objects.get(pk=non_id)
    non_member.is_active = False
    non_member.date_inactive = datetime.datetime.now()
    non_member.save()
    return redirect('IABC_WEB:nonmember')
    #non_member.delete()
    #return redirect('IABC_WEB:nonmember')


def viewproj_track(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin | info.is_bidder == True:
            if request.method == 'GET':
                try:
                    proj = ProjectTrackerName.objects.all()
                    context = {'proj':proj, 'info':info}     
                    return render(request, 'generalprojecttracker.html', context)
                    #try:
                       
                        #proy=ProjectTracker.objects.all()
                        #proj = ProjectTrackerName.objects.all()
                       
                        #for x in proj:
                            #t=0
                            #r=0
                            #l=0
                            #k=x.id
                            #prot=ProjectTracker.objects.filter(proj_id=k)
                            #for j in prot:
                                #o=j.id
                                #t=t+1
                                #pror=ProjectTracker.objects.get(id=o)
                                #if pror.percent == "100":
                                    #r=r+1
                                    #continue
                                           
                            #l=l+1
                            #if r | t !=0:
                                #if t == r:
                                    #prol=ProjectTrackerName.objects.get(id=k)
                                    #prol.progress="Complete"
                                    #prol.save()
                            #else: 
                                #continue   
                            
                        #percent = (r/t)*100
                        #percent = round(percent)
                        #context = {'proj':proj, 
                        #'info':info }
                        #return HttpResponse(r+t)
                        #return render(request, 'generalprojecttracker.html', context)
                        

                    #except ObjectDoesNotExist:
                        #proj = ProjectTrackerName.objects.all()
                        #context = {'proj':proj, 'info':info}     
                        #return render(request, 'generalprojecttracker.html', context)

                except ObjectDoesNotExist:
                    return render(request, 'generalprojecttracker.html')

            if request.method == 'POST':
                date = request.POST.get('date')
                event = request.POST.get('event') 
                project=ProjectTrackerName.objects.create(event_name=event, event_date=date, user_id=info)
                messages.success(request, "Succesfully Added!")
                return redirect('IABC_WEB:viewproj_track')
        else:
                return redirect('members:home')
    else:
        return redirect('members:home')


def viewproj_track2(request, proje_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        adm = User.objects.filter(is_admin=True)
        bid = User.objects.filter(is_bidder=True)
        projj = proje_id
        if info.is_admin | info.is_bidder == True:
            if request.method == "GET":
                try:            
                    proj = ProjectTracker.objects.filter(proj_id=proje_id)
                    proij = ProjectTrackerName.objects.get(id=proje_id)
                    act = Activity.objects.all()
                    context = {'proj':proj, 'info':info, 'projj':projj, 'proij':proij, 'adm':adm, 'bid':bid, 'act':act}
                    #return HttpResponse(d1)
                    return render(request, 'generalprojecttracker2.html', context)

                except ObjectDoesNotExist:
                    return render(request, 'generalprojecttracker2.html', projj)
        else:
                return redirect('members:home')
    else:
        return redirect('members:home')

def addproj(request, proje_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        proj = ProjectTrackerName.objects.get(id=proje_id)
        if info.is_admin | info.is_bidder == True:
            if request.method == "POST":
                date = request.POST.get('date')
                deadline = request.POST.get('deadl')
                act = request.POST.get('act')
                user = request.POST.get('users')
                if act == "End":
                    d3 = datetime.date.today()
                    d4 =datetime.datetime.today()
                    add = ProjectTracker.objects.create(date_dur=d3, deadline=d3,act_Task=act, remarks="",assign=user,assignby=info.firstName,percent="100", proj_id=proj)
                    proj.event_end=d4
                    proj.save()
                    add.save()
                    #return HttpResponse(proj.progress)
                    messages.success(request, "Succesfully Added!")
                    return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(proje_id,)))
                elif act == "Meeting":
                    add = ProjectTracker.objects.create(date_dur=proj.event_date, deadline=deadline,act_Task=act, remarks="",assign=user,assignby=info.firstName, proj_id=proj)
                    proj.save()
                    add.save()
                    #return HttpResponse(proj.progress)
                    messages.success(request, "Succesfully Added!")
                    return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(proje_id,)))
                else:
                    d1 = datetime.date.today() 
                    d2 = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
                    add = ProjectTracker.objects.create(date_dur=date, deadline=deadline,act_Task=act, remarks="",assign=user,assignby=info.firstName, proj_id=proj)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(proje_id,)))

                #if d1 > d2:
                    #add.status = "Late"
                    #add.save()
                    #messages.success(request, "Succesfully Added!")
                    #return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(proje_id,)))
                #else :    
                    #add.save()
                    #messages.success(request, "Succesfully Added!")
                    #return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=#(proje_id,)))
        else:
            return redirect('members:home')
    else:
        return redirect('members:home')

def editproj(request, proje_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin | info.is_bidder == True:
            if request.method == "POST":
                track=ProjectTracker.objects.get(id=proje_id)
                prot=ProjectTracker.objects.filter(id=proje_id).values_list('proj_id', flat=True)
                pit = list(prot)
                pot = pit[0]
                newstatus = request.POST.get('stat')
                #newremark = request.POST.get('actt')
                track.status = newstatus
                #track.act_Task = newremark
                track.save()
                #return HttpResponse(pot)
                return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(pot,)))
        else:
            return redirect('members:home')
    else:
        return redirect('members:home')

def proj_remarks(request, proje_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin | info.is_bidder == True:
            if request.method == "POST":
                track=ProjectTracker.objects.get(id=proje_id)
                prot=ProjectTracker.objects.filter(id=proje_id).values_list('proj_id', flat=True)
                pit = list(prot)
                pot = pit[0]
              
                newremark = request.POST.get('remark')
               
                track.remarks = newremark
                track.save()
                return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(pot,)))
        else:
            return redirect('members:home')
    else:
        return redirect('members:home')

def checklist(request, proje_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        proj = ProjectTracker.objects.get(id=proje_id)
        if info.is_admin | info.is_bidder == True:
            if request.method == "GET":
                try:
                    proj = ProjectTracker.objects.get(id=proje_id)
                    checkes=Checklist.objects.filter(proj_id=proj)
                    context ={'proj':proj, 'checkes':checkes}
                    #return HttpResponse(proj)
                    return render (request, 'generalprojecttracker3.html', context)

                except ObjectDoesNotExist:
                    proj = ProjectTracker.objects.get(id=proje_id)
                    #return HttpResponse("hello")
                    return render (request, 'generalprojecttracker3.html', {'proj':proj})

            if request.method == "POST":
                if 'add' in request.POST:
                    #track=Checklist.objects.get(proid=proje_id)
                    
                    checkl = request.POST.get('list')
                    checke=Checklist.objects.create(checks=checkl, proj_id=proj)
                    checke.save()
                    prot=ProjectTracker.objects.filter(id=proje_id).values_list('id', flat=True)
                    pit = list(prot)
                    pot = pit[0]
                    
                    #return HttpResponse(pot)
                    return HttpResponseRedirect(reverse('IABC_WEB:checklist', args=(pot,)))
                elif 'savers' in request.POST:
                    checkl = request.POST.getlist("checkk", None)
                    try:
                        checke=Checklist.objects.filter(proj_id=proje_id)
                        prot=ProjectTracker.objects.filter(id=proje_id).values_list('proj_id', flat=True)
                        pit = list(prot)
                        pot = pit[0]
                        p=0
                        r=0
                        for x in checke:
                            k=x.id
                            p=p+1
                            checker=Checklist.objects.get(id=k)
                            if checker.checks in checkl:
                                if checker.end_date == None:
                                    r=r+1
                                    checker.end_date = datetime.datetime.now() 
                                    checker.listcheck=True
                                    checker.save()
                                else:
                                    r=r+1
                                    continue
                        percent = (r/p)*100
                        percent = round(percent)
                        proj.percent = percent
                        if percent == 100:
                        
                            proj.complete_date = datetime.datetime.now()
                            proj.save()
                        else: 
                            proj.complete_date = None
                            proj.save()
                        proj.save()
                        #return HttpResponse(percent)
                        return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(pot,)))
                    except ZeroDivisionError:
                        prot=ProjectTracker.objects.filter(id=proje_id).values_list('id', flat=True)
                        pit = list(prot)
                        pot = pit[0]
                        return HttpResponseRedirect(reverse('IABC_WEB:checklist', args=(pot,)))
                elif 'back' in request.POST:
                    prot=ProjectTracker.objects.filter(id=proje_id).values_list('proj_id', flat=True)
                    pit = list(prot)
                    pot = pit[0]
                    return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(pot,)))
        else:
            return redirect('members:home')
    else:
        return redirect('members:home')

def act_list(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin | info.is_bidder == True:
            if request.method == 'GET':
                try:
                    act = Activity.objects.all()
                    return render(request,'admin-activitycrud.html', {'act':act})
                except ObjectDoesNotExist:
                    return render(request,'admin-activitycrud.html')
            if request.method == 'POST':
                acts = request.POST.get('act')
                actt = Activity.objects.create(activity=acts)
                actt.save()
                messages.success(request, "Succesfully Added!")
                return redirect('IABC_WEB:act_list')


def delproj_trac(request, ent_id):
    
    # are=request.POST['ent_id']
    proj = ProjectTrackerName.objects.get(pk=ent_id)
    # projjson=json.dumps(proj)
    # empty={"success":False, "data":projjson}
    
    # try:
    proj.delete()
    #     empty["success"]=True
        
    # except:
    #     empty["success"]=False
    return redirect('IABC_WEB:viewproj_track')

def delproj_trac2(request, ent_id):
    
    # are=request.POST['ent_id']
    proj = ProjectTracker.objects.get(id=ent_id)
    prof = ProjectTracker.objects.filter(id=ent_id).values_list('proj_id', flat=True)
    proy = list(prof)
    pot=proy[0]
    
    # projjson=json.dumps(proj)
    # empty={"success":False, "data":projjson}
    
    # try:
    proj.delete()
    #     empty["success"]=True
        
    # except:
    #     empty["success"]=False
    #return HttpResponse(pot) 
    return HttpResponseRedirect(reverse('IABC_WEB:viewproj_track2', args=(pot,)))
    
def bidderviewprop(request, bid_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            
            try:
                bid=BidderSubmission.objects.get(user_id=bid_id)

                return render(request, 'admin-viewbiddersproposal.html', {'bid':bid})
            except BidderSubmission.DoesNotExist:
                return render(request, 'admin-viewbiddersproposal.html')
    else:
            return redirect('members:home')



def view_bidders(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.user.is_authenticated:
                context = User.objects.filter(is_bidder=True).filter(is_active=True)
                return render(request, 'admin-viewbidders.html', {'context':context})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')


def bidder_del(request, bid_id):
    bidder=User.objects.get(pk=bid_id)
    bidder.is_active = False
    bidder.date_inactive = datetime.datetime.now()
    bidder.save()
    return redirect('IABC_WEB:view_bidders')
    #bidder.delete()
    #return redirect('IABC_WEB:view_bidders')


def bidder_dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        try:
            mes = BidderSubmission.objects.get(user_id=id)
            context = {'mes':mes}
            if info.is_bidder == True:
                if mes.comments == '':
                    return render(request, 'bidder-dashboard.html', context)
                else:
                    return render(request, 'bidder-dashboard.html', context)
            else:
                return redirect('members:home')
        except BidderSubmission.DoesNotExist:
            return render(request, 'bidder-dashboard.html')
    else:
            return redirect('members:home')


def bidder_app(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_bidder == True:
            try:
                check = BidderSubmission.objects.get(user_id=id)
                if check.file:
                    return render(request, 'bidder-application.html',{'check':check})
                else :
                    var= "True"
                   
                    return render(request, 'bidder-application.html', {'var':var})
                
            except ObjectDoesNotExist:
                var= "True"
                
                return render(request, 'bidder-application.html', {'var':var})

        else:
            return redirect('members:home')
    else:
            return redirect('members:home')


def biddersubmit(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)  
        if request.method == 'POST':
            try:
                check = BidderSubmission.objects.get(user_id=id)
                if check.file:
                    messages.success(request, "You have already submitted!")
                    return redirect('members:home')
                    
                else:
                    file = request.FILES.get('file')
                    desc = request.POST.get ('description')
                    check.file = file
                    check.description = desc
                    check.save()
                    messages.success(request, "Succesfully Submitted!")
                    return redirect('members:home')
                    
            
            except ObjectDoesNotExist:
                file = request.FILES.get('file')
                desc = request.POST.get ('description')

                bidadd = BidderSubmission.objects.create(file=file, description=desc, user_id=info)
                bidadd.save()
                messages.success(request, "Succesfully Submitted!")
                return redirect('members:home')
   
    else:
            return redirect('members:home')

def bidderremark(request, bid_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)  
        if request.method == 'POST':
            remark = request.POST.get('remarks')
            
            bidadd = BidderSubmission.objects.get(user_id=bid_id)
            bidadd.comments = remark
            bidadd.save()
            messages.success(request, "Succesfully Added!")
            return HttpResponseRedirect(reverse('IABC_WEB:bidderviewprop', args=(bid_id,)))
   
    else:
            return redirect('members:home')

def bidderstatus(request, bid_id):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)  
        if request.method == 'POST':
            stat = request.POST.get('stat')
            
            bidadd = BidderSubmission.objects.get(user_id=bid_id)
            bidadd.status = stat
            bidadd.save()
            messages.success(request, "Succesfully Changed!")
            return HttpResponseRedirect(reverse('IABC_WEB:bidderviewprop', args=(bid_id,)))
   
    else:
            return redirect('members:home') 
    
def bidderprop_del(request, bid_id):
    if request.method == 'GET':
            bidadd = BidderSubmission.objects.get(user_id=bid_id)
            bidadd.file.delete()
            bidadd.save()
            messages.success(request, "Succesfully Deleted!")
            return HttpResponseRedirect(reverse('IABC_WEB:bidderviewprop', args=(bid_id,)))
    #bidder.delete()
    #return redirect('IABC_WEB:view_bidders')


def user_del(request, user_id):
    person=User.objects.get(pk=user_id)
    person.is_active = False
    person.date_inactive = datetime.datetime.now()
    person.save()
    return redirect('members:logout')
    #bidder.delete()
    #return redirect('IABC_WEB:view_bidders')



def chartA(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_A.objects.all()
            return render(request, 'admin-chartA.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartB(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_B.objects.all()
            return render(request, 'admin-chartB.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartC(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_C.objects.all()
            return render(request, 'admin-chartC.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartD(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_D.objects.all()
            return render(request, 'admin-chartD.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartE(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_E.objects.all()
            return render(request, 'admin-chartE.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartF(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_F.objects.all()
            return render(request, 'admin-chartF.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartG(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            info = Chart_G.objects.all()
            return render(request, 'admin-chartG.html', {'info':info})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chart_Add(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.method == 'GET':
                return render(request, 'admin-chartcrud.html')
            elif request.method == "POST":
                selected = request.POST.get('choice')
                if selected == None:
                    messages.success(request, "Select A field!")
                    return redirect('IABC_WEB:chart_Add')
                if selected == '1':
                    input = request.POST.get('inp1')
                    add = Chart_A.objects.create(industry_Name=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')
                elif selected == '2':
                    input = request.POST.get('inp1')
                    add = Chart_B.objects.create(business_type=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')
                elif selected == '3':
                    input = request.POST.get('inp1')
                    add = Chart_C.objects.create(current_title=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')
                elif selected == '4':
                    input = request.POST.get('inp1')
                    add = Chart_D.objects.create(key_area=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')
                elif selected == '5':
                    input = request.POST.get('inp1')
                    add = Chart_E.objects.create(employee_no=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')
                elif selected == '6':
                    input = request.POST.get('inp1')
                    add = Chart_F.objects.create(experience=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')
                elif selected == '7':
                    input = request.POST.get('inp1')
                    add = Chart_G.objects.create(about=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:chart_Add')

        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def chartA_del(request, cht_id):
    bidder=Chart_A.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartA')

def chartB_del(request, cht_id):
    bidder=Chart_B.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartB')

def chartC_del(request, cht_id):
    bidder=Chart_C.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartC')

def chartD_del(request, cht_id):
    bidder=Chart_D.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartD')

def chartE_del(request, cht_id):
    bidder=Chart_E.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartE')

def chartF_del(request, cht_id):
    bidder=Chart_F.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartF')

def chartG_del(request, cht_id):
    bidder=Chart_G.objects.get(pk=cht_id)
    bidder.delete()
    return redirect('IABC_WEB:chartG')

def awardscrud(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            if request.method == 'GET':
                return render(request, 'admin-awardscrud.html')
            elif request.method == "POST":
                selected = request.POST.get('chart')
                if selected == None:
                    messages.error(request, "Select A field!")
                    return redirect('IABC_WEB:awardscrud')
                if selected == '1':
                    input = request.POST.get('type')
                    add = Division.objects.create(division=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:awardscrud')
                if selected == '2':
                    input = request.POST.get('type')
                    add = Category.objects.create(category=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:awardscrud')
                if selected == '3':
                    input = request.POST.get('type')
                    add = Certification.objects.create(certification=input)
                    add.save()
                    messages.success(request, "Succesfully Added!")
                    return redirect('IABC_WEB:awardscrud')


def category(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            categ = Category.objects.all()
            return render(request, 'admin-awardscategory.html', {'categ':categ})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def certification(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            cert = Certification.objects.all()
            return render(request, 'admin-awardscertificate.html', {'cert':cert})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def division(request):
    if request.user.is_authenticated:
        id = request.user.id
        info = User.objects.get(id=id)
        if info.is_admin == True:
            div = Division.objects.all()
            return render(request, 'admin-awardsdivision.html', {'div':div})
        else:
            return redirect('members:home')
    else:
            return redirect('members:home')

def div_del(request, cht_id):
    div=Division.objects.get(pk=cht_id)
    div.delete()
    return redirect('IABC_WEB:division')

def categ_del(request, cht_id):
    categ=Category.objects.get(pk=cht_id)
    categ.delete()
    return redirect('IABC_WEB:category')

def cert_del(request, cht_id):
    cert=Certification.objects.get(pk=cht_id)
    cert.delete()
    return redirect('IABC_WEB:certification')





#winners table
def winnersCat(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            cat = Category.objects.all()
            context = {'cat':cat}
            return render(request, 'admin-studwinnerscrud.html', context)
        elif request.method == 'POST':
            categ = request.POST.get('categ')
            if categ == "None":
                messages.success(request, "Please Choose a Category")
                return redirect('IABC_WEB:winnersCat')
            else:
                request.session['_category_data'] = request.POST
                return redirect('IABC_WEB:winners')
    else:
        return redirect('IABC_WEB:home')


def winners(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = request.session.get('_category_data')
            checks = data['categ']
            win = Winners.objects.filter(entryCat=checks)
            awa = Awards_student.objects.filter(is_paid=True).filter(category=checks).filter(judged=False)
            cat = Category.objects.all()
            context = {'win':win, 'awa':awa, 'cat':cat}
            return render(request, 'admin-studwinnerscrud2.html', context)
        elif request.method == 'POST':
            ent = request.POST.get('ent')
            awa = Awards_student.objects.get(pk=ent)
            entnum=awa.id
            entname=awa.entry_title
            entcat=awa.category
            entrant=awa.entrant_name
            entcomp = awa.entrant_school
            make = Winners.objects.create(entryNo=entnum,entryName=entname,entryCat=entcat,entrantName=entrant,entryComp=entcomp)
            awa.judged = True
            awa.save()
            return redirect('IABC_WEB:winners')
    else:
        return redirect('IABC_WEB:home')

def winnersdel(request, del_id):
    if request.user.is_authenticated:
        win = Winners.objects.get(pk=del_id)
        win.delete()
        return redirect('IABC_WEB:winners')


#winners table 2
def winnersCat2(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            cat = Category.objects.all()
            context = {'cat':cat}
            return render(request, 'admin-profwinnerscrud.html', context)
        elif request.method == 'POST':
            categ = request.POST.get('categ')
            if categ == "None":
                messages.success(request, "Please Choose a Category")
                return redirect('IABC_WEB:winnersCat2')
            else:
                request.session['_category2_data'] = request.POST
                return redirect('IABC_WEB:winners2')
    else:
        return redirect('IABC_WEB:home')    

def winners2(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = request.session.get('_category2_data')
            checks = data['categ']
            win = Winners2.objects.filter(entryCat=checks)
            awa = Awards_prof.objects.filter(is_paid=True).filter(category=checks).filter(judged=False)
            cat = Category.objects.all()
            context = {'win':win, 'awa':awa, 'cat':cat}
            return render(request, 'admin-profwinnerscrud2.html', context)
        elif request.method == 'POST':
            ent = request.POST.get('ent')
            if ent == "None":
                messages.success(request, "Choose an Entry!")
                return redirect('IABC_WEB:winners2')
            else:
                awa = Awards_prof.objects.get(pk=ent)
                entnum=awa.id
                entname=awa.entry_title
                entcat=awa.category
                entrant=awa.entrant_name
                entcomp = awa.entrant_org
                make = Winners2.objects.create(entryNo=entnum,entryName=entname,entryCat=entcat,entrantName=entrant,entryComp=entcomp)
                awa.judged = True
                awa.save()
                return redirect('IABC_WEB:winners2')
    else:
        return redirect('IABC_WEB:home')

def winnersdel2(request, del_id):
    if request.user.is_authenticated:
        win = Winners2.objects.get(pk=del_id)
        win.delete()
        return redirect('IABC_WEB:winners2')





def price(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            price = Prices.objects.all()
            context = {'price':price}
            return render(request, 'admin-moneycrud.html', context)
        elif request.method == 'POST':
            val = request.POST.get('price')
            name = request.POST.get('name')
            price = Prices.objects.create(priceVal=val,priceName=name)
            return redirect('IABC_WEB:price')
    else:
        return redirect('IABC_WEB:home')


def pricedel(request, del_id):
    if request.user.is_authenticated:
        try:
            price = Prices.objects.get(pk=del_id)
            price.delete()
            return redirect('IABC_WEB:price')
        except:
            return HttpResponse("Invalid Deletion")



def studwinners_pdf(request):
    if request.user.is_authenticated:
        id = request.user.id
        info=User.objects.get(pk=id)
        checker = request.POST.get('filter')
        if checker == "All":
            text = Winners.objects.all() 
        elif checker == "Today":
            text = Winners.objects.filter(windate=date.today())
        elif checker == "7":
            seven = date.today() - relativedelta(days=7)
            text = Winners.objects.filter(windate__gte=seven)
        elif checker == "30":
            thirty = date.today() - relativedelta(days=30)
            text = Winners.objects.filter(windate__gte=thirty)
        template = get_template('form-winners.html')
        context = {'text':text}

        html = template.render(context)
        pdf = render_to_pdf('form-winners.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Student_Winners-%s.pdf" %info.lastName
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")




def profwinners_pdf(request):
    if request.user.is_authenticated:
        id = request.user.id
        info=User.objects.get(pk=id)
        checker = request.POST.get('filter')
        if checker == "All":
            text = Winners2.objects.all() 
        elif checker == "Today":
            text = Winners2.objects.filter(windate=date.today())
        elif checker == "7":
            seven = date.today() - relativedelta(days=7)
            text = Winners2.objects.filter(windate__gte=seven)
        elif checker == "30":
            thirty = date.today() - relativedelta(days=30)
            text = Winners2.objects.filter(windate__gte=thirty)
        template = get_template('form-winners.html')
        context = {'text':text}
        
        html = template.render(context)
        pdf = render_to_pdf('form-winners.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Professional_Winners-%s.pdf" %info.lastName
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def memreport(request):
    if request.user.is_authenticated:
        id = request.user.id
        info=User.objects.get(pk=id)
        try:
            mem=Members.objects.all()
            if request.method == 'POST':
                filt = request.POST.get('filt')
                if filt == "Today":
                    d1 = datetime.date.today()
                    mem1=Members.objects.filter(is_paid=True).filter(join_date__gte=d1) 
                    template = get_template('form-members.html')
                    context={
                         'mem1':mem1,
                    }
                    html = template.render(context)
                    pdf = render_to_pdf('form-members.html', context)

                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "Members Report-%s.pdf" %info.lastName
                        content = "inline; filename=%s" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")
                elif filt == "Last 7 Days":
                    d1 = datetime.date.today()
                    last7 = date.today() - relativedelta(days=7)
                    mem1=Members.objects.filter(is_paid=True).filter(join_date__gte=last7)
                    template = get_template('form-members.html')
                    context={
                         'mem1':mem1,
                    }
                    html = template.render(context)
                    pdf = render_to_pdf('form-members.html', context)

                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "Members Report-%s.pdf" %info.lastName
                        content = "inline; filename=%s" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")

                elif filt == "Last 30 Days":
                    d1 = datetime.date.today()
                    last30 = date.today() - relativedelta(days=30)
                    mem1=Members.objects.filter(is_paid=True).filter(join_date__gte=last30)
                    template = get_template('form-members.html')
                    context={
                         'mem1':mem1,
                    }
                    html = template.render(context)
                    pdf = render_to_pdf('form-members.html', context)

                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "Members Report-%s.pdf" %info.lastName
                        content = "inline; filename=%s" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")

                else:
                    return redirect('IABC_WEB:admember')
            
            #return render(request, 'user-viewwinners.html', context)
        except ObjectDoesNotExist:
            return redirect('IABC_WEB:admember')
            
    else:
        return redirect('IABC_WEB:home')

def pendmemreport(request):
    if request.user.is_authenticated:
        id = request.user.id
        info=User.objects.get(pk=id)
        try:
            mem=Members.objects.all()
            if request.method == 'POST':
                filt = request.POST.get('filt')
                if filt == "Today":
                    d1 = datetime.date.today()
                    mem1=Members.objects.filter(is_paid=False).filter(join_date__gte=d1) 
                    template = get_template('form-non-members.html')
                    context={
                         'mem1':mem1,
                    }
                    html = template.render(context)
                    pdf = render_to_pdf('form-non-members.html', context)

                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "Members Report-%s.pdf" %info.lastName
                        content = "inline; filename=%s" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")
                elif filt == "Last 7 Days":
                    d1 = datetime.date.today()
                    last7 = date.today() - relativedelta(days=7)
                    mem1=Members.objects.filter(is_paid=False).filter(join_date__gte=last7)
                    template = get_template('form-non-members.html')
                    context={
                         'mem1':mem1,
                    }
                    html = template.render(context)
                    pdf = render_to_pdf('form-non-members.html', context)

                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "Members Report-%s.pdf" %info.lastName
                        content = "inline; filename=%s" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")

                elif filt == "Last 30 Days":
                    d1 = datetime.date.today()
                    last30 = date.today() - relativedelta(days=30)
                    mem1=Members.objects.filter(is_paid=False).filter(join_date__gte=last30)
                    template = get_template('form-non-members.html')
                    context={
                         'mem1':mem1,
                    }
                    html = template.render(context)
                    pdf = render_to_pdf('form-non-members.html', context)

                    if pdf:
                        response = HttpResponse(pdf, content_type='application/pdf')
                        filename = "Members Report-%s.pdf" %info.lastName
                        content = "inline; filename=%s" %(filename)
                        download = request.GET.get("download")
                        if download:
                            content = "attachment; filename='%s'" %(filename)
                        response['Content-Disposition'] = content
                        return response
                    return HttpResponse("Not found")
                
                else:
                    return redirect('IABC_WEB:admember')

            
            #return render(request, 'user-viewwinners.html', context)
        except ObjectDoesNotExist:
            return redirect('IABC_WEB:admember')
            
    else:
        return redirect('IABC_WEB:home')











def viewwinners(request):
    if request.user.is_authenticated:
        id = request.user.id
        info=User.objects.get(pk=id)
        try:
            stud=Winners.objects.all()
            prof=Winners2.objects.all()
            context={
                'stud':stud, 'prof':prof
            }
            return render(request, 'user-viewwinners.html', context)
        except ObjectDoesNotExist:
            return render(request, 'user-viewwinners.html')
            
    else:
        return redirect('IABC_WEB:home')
