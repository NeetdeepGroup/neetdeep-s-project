from django.http import HttpResponse
#from django.http.response import HttpResponse
from django.shortcuts import render , redirect
from .models import Contact,User,Product
import random
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta


def index(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype == 'superadmin':
		return render(request, 'index.html')
	elif user.usertype == 'admin':
		return render(request, 'admin_index.html' )
	elif user.usertype == 'user':
		return render(request, 'user_index.html' )


def login(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(email=request.POST['email'])
			if user.password == request.POST['password']:
				request.session['email'] = user.email
				request.session['name'] = user.name
				request.session['profile_picture']=user.profile_picture.url
				contact = Contact.objects.all()
				if user.usertype=='superadmin':
					return render(request, 'index.html', {'user': user})
				elif user.usertype=='admin':
					return render(request, 'admin_index.html', {'user': user})
				else:
					return render(request, 'user_index.html', {'user': user})
			else:
				alert = True
				msg = 'Wrong Password Please Try Again'
				return render(request, 'login.html', {'msg': msg, "alert": alert})
		except Exception as e:
			print(e)
			alert = True
			msg = 'Your Email Id Not Registered'
			return render(request, 'signup.html', {'msg': msg, "alert": alert})
	else:
		return render(request, 'login.html')

def signup(request):
	user1=User.objects.get(email=request.session['email'])
	if request.method == "POST":
		try:
			user = User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'login.html',{'msg':msg})
		except Exception as e:
			print(e)
			if request.POST['password']==request.POST['conform_password']:
				user=User.objects.create(
						usertype=request.POST['usertype'],
						name=request.POST['name'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_picture=request.FILES['profile_picture']
					)
				subject = 'New User Create'
				message = (f'Hello {user.name}, Well-Come at NEET DEEP GROUP Your Login-Id Has Been Create'
						   f' Your Login Id is {user.email}, '
						   f'And Password Is {user.password} Please First Change Your Password')
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [user.email, ]
				send_mail(subject, message, email_from, recipient_list)
				msg="User Sign Up Successfully"
				if user.usertype=='superadmin':
					return render(request,'signup.html',{'msg':msg})
				elif user.usertype == 'admin':
					return render(request, 'admin_signup.html', {'msg': msg})
				else:
					return render(request, 'user_signup.html', {'msg': msg})
			else:
				msg="Password & Confirm Password Does Not Matched"
				if user.usertype == 'superadmin':
					return render(request, 'signup.html', {'msg': msg})
				elif user.usertype == 'admin':
					return render(request, 'admin_signup.html', {'msg': msg})
				else:
					return render(request, 'user_signup.html' , {'msg': msg})
	else:
		if user1.usertype == 'superadmin':
			return render(request, 'signup.html')
		elif user1.usertype == 'admin':
			return render(request, 'admin_signup.html')
		else:
			return render(request, 'user_signup.html')


def logout(request):
	try:
		del request.session['email']
		del request.session['name']
		del request.session['profile_picture']
		return render(request, 'login.html')
	except:
		return render(request, 'login.html')


def profile(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype == 'superadmin':
		return render(request, 'profile.html', {'user': user})
	elif user.usertype == 'admin':
		return render(request, 'admin_profile.html', {'user': user})
	else:
		return render(request,'user_profile.html',{'user':user})

def profile_update(request):
	user = User.objects.get(email=request.session['email'])
	user.name = request.POST['username']
	user.mobile = request.POST['usermobile']
	user.email = request.POST['useremail']
	user.address = request.POST['useraddress']
	try:
		user.profile_picture = request.FILES['profile_picture']
	except:
		pass
	user.save()
	msg = "Your Profile Has Been Updated"
	if user.usertype == 'superadmin':
		return render(request, 'profile.html', {'user': user, 'msg': msg})
	elif user.usertype == 'admin':
		return render(request, 'admin_profile.html', {'user': user, 'msg': msg})
	else:
		return render(request, 'user_profile.html', {'user': user, 'msg': msg})

def user_info(request):
	user = User.objects.all()
	user1 = User.objects.get(email=request.session['email'])
	if user1.usertype == 'superadmin':
		return render(request, 'user_info.html', {'user': user})
	elif user1.usertype == 'admin':
		return render(request, 'admin_user_info.html', {'user': user})
	else:
		return render(request, 'user_user_info.html', {'user': user})

def user_edit(request,pk):
	user1 = User.objects.get(email=request.session['email'])
	user=User.objects.get(pk=pk)
	if request.method=='POST':
		user.usertype=request.POST['usertype']
		user.save()
		msg='UserType Has Been Updated'
		if user1.usertype == 'superadmin':
			return render(request, 'user_edit.html', {'user': user,'msg':msg})
		elif user1.usertype == 'admin':
			return render(request, 'admin_user_edit.html', {'user': user,'msg':msg})
	else:
		if user1.usertype == 'superadmin':
			return render(request, 'user_edit.html', {'user': user})
		elif user1.usertype == 'admin':
			return render(request, 'admin_user_edit.html', {'user': user})

def user_delete(request,pk):
	user = User.objects.get(email=request.session['email'])
	user=User.objects.get(pk=pk)

	user.delete()
	if user.usertype == 'superadmin':
		return render(request,'signup.html')
	elif user.usertype == 'admin':
		return render(request,'admin_signup.html')



def change_pass(request):
	user = User.objects.get(email=request.session['email'])
	if request.method == 'POST':
		if user.password == request.POST['oldpassword']:
			if request.POST['newpassword'] == request.POST['cpassword']:
				user.password=request.POST['newpassword']
				user.save()
				msg='Your Password Is Change'
				del request.session['email']
				del request.session['name']
				return render(request, 'login.html', {'msg': msg})
			else:
				msg = 'Your New Password And Con Password Is Not Match Please Tray Again'
				if user.usertype == 'superadmin':
					return render(request, 'change_pass.html', {'msg': msg})
				elif user.usertype == 'admin':
					return render(request, 'admin_change_pass.html', {'msg': msg})
				else:
					return render(request, 'user_change_pass.html', {'msg': msg})
		else:
			msg = 'Your Old Password Is Not Correct Please Tray With Correct Password'
			if user.usertype == 'superadmin':
				return render(request, 'change_pass.html', {'msg': msg})
			elif user.usertype == 'admin':
				return render(request, 'admin_change_pass.html', {'msg': msg})
			else:
				return render(request, 'user_change_pass.html', {'msg': msg})

	else:
		if user.usertype == 'superadmin':
			return render(request, 'change_pass.html')
		elif user.usertype == 'admin':
			return render(request, 'admin_change_pass.html')
		else:
			return render(request, 'user_change_pass.html')
def forgot_password(request):
	if request.method=='POST':
		try:
			otp = (random.randint(1000, 9999))
			user=User.objects.get(email=request.POST['email'])
			subject = 'OTP For Forgot Password'
			message = f'Hello {user.name}, Your OTP For Forgot Password Is '+ str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail(subject, message, email_from, recipient_list)
			return render(request, 'otp.html',{'otp':otp,'email':user.email})
		except:
			msg='Email Is Not Registered Please Contact Administrator'
			return render(request, 'forgot_password.html',{'msg':msg})
	else:
		return render(request, 'forgot_password.html')
def verify_otp(request):
	email=request.POST['email']
	otp=int(request.POST['otp'])
	uotp = int(request.POST['uotp'])
	if otp==uotp:
		return render(request, 'new_password.html',{'email':email})
	else:
		msg='Invelid OTP Please Try Again'
		return render(request, 'otp.html', {'msg': msg,'otp':otp,'email':email})
def new_password(request):
	email = request.POST['email']
	np = (request.POST['newpassword'])
	cnp = (request.POST['cnpassword'])
	if np==cnp:
		user=User.objects.get(email=email)
		user.password=np
		user.save()
		msg='Your New Password Is Change'
		return render(request, 'login.html', {'msg': msg})
	else:
		msg = 'Your New Password And Conform New Password Is Not Match'
		return render(request, 'new_password.html', {'msg': msg})


def invoice(request):
	return render(request,'invoice.html')
def icons(request):
	return render(request,'icons.html')
def contact(request):
	return render(request,'contact.html')
def add_product(request):
	user = User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
		product_category = request.POST['product_category'],
		proname =request.POST['proname'],
		qty = request.POST['qty'],
		price = request.POST['price'],
		prodetail = request.POST['prodetail'],
		product_picture = request.FILES['product_picture']
		)
		msg = "Product Added Successfully"
		if user.usertype=='superadmin':
			return render(request, 'add_product.html', {'msg': msg})
		elif user.usertype=='admin':
			return render(request, 'admin_add_product.html', {'msg': msg})
		else:
			return render(request, 'user_add_product.html', {'msg': msg})
	else:
		if user.usertype=='superadmin':
			return render(request,'add_product.html')
		elif user.usertype=='admin':
			return render(request,'admin_add_product.html')
		else:
			return render(request,'user_add_product.html')


def show_product(request):
	user = User.objects.get(email=request.session['email'])
	products=Product.objects.all()
	if user.usertype=='superadmin':
		return render(request,'show_product.html',{'products':products})
	elif user.usertype=='admin':
		return render(request,'admin_show_product.html',{'products':products})
	else:
		return render(request,'user_show_product.html',{'products':products})

def add_Customer(request):
	user = User.objects.get(email=request.session['email'])
	if request.method=='POST':
		contact=Contact.objects.create(
		fname=request.POST['custname'],
		mobile=request.POST['custmobile'],
		email=request.POST['custemail'],
		address=request.POST['custaddress'],
		)
		msg = "Customer Data Save Successfully"
		if user.usertype == 'superadmin':
			return render(request, 'add_Customer.html', {'msg': msg})
		elif user.usertype == 'admin':
			return render(request, 'admin_add_Customer.html', {'msg': msg})
		else:
			return render(request, 'user_add_Customer.html', {'msg': msg})

	else:
		if user.usertype == 'superadmin':
			return render(request,'add_Customer.html')
		elif user.usertype == 'admin':
			return render(request,'admin_add_Customer.html')
		else:
			return render(request,'user_add_Customer.html')


def show_customer(request):
	user = User.objects.get(email=request.session['email'])
	customer=Contact.objects.all()
	if user.usertype=='superadmin':
		return render(request,'show_customer.html',{'customer':customer})
	if user.usertype=='admin':
		return render(request,'admin_show_customer.html',{'customer':customer})
	if user.usertype=='user':
		return render(request,'user_show_customer.html',{'customer':customer})
def edit_cust(request,pk):
	user = User.objects.get(email=request.session['email'])
	customer=Contact.objects.get(pk=pk)
	if request.method=='POST':
		customer.fname = request.POST['custname']
		customer.mobile = request.POST['custmobile']
		customer.address = request.POST['custaddress']
		customer.save()
		msg = "Contact updated successfully"
		if user.usertype == 'superadmin':
			return render(request, 'edit_cust.html', {'customer': customer,'msg': msg})
		elif user.usertype == 'admin':
			return render(request, 'admin_edit_cust.html', {'customer': customer,'msg': msg})
		else:
			return render(request, 'user_edit_cust.html', {'customer': customer,'msg': msg})

	else:
		if user.usertype == 'superadmin':
			return render(request,'edit_cust.html',{'customer':customer})
		elif user.usertype == 'admin':
			return render(request,'admin_edit_cust.html',{'customer':customer})
		else:
			return render(request,'user_edit_cust.html',{'customer':customer})

def backcustpage(request):
	return redirect('show_customer')
def edit_product(request,pk):
	user = User.objects.get(email=request.session['email'])
	product= Product.objects.get(pk=pk)
	if request.method == "POST":
		product.proname = request.POST['proname']
		product.price = request.POST['price']
		product.prodetail = request.POST['prodetail']
		product.save()
		msg = 'Your Produts Details Are Update'
		if user.usertype == 'superadmin':
			return render(request, 'edit_product.html', {'product':product,'msg':msg})
		elif user.usertype == 'admin':
			return render(request, 'admin_edit_product.html', {'product':product,'msg':msg})
		else:
			return render(request, 'user_edit_product.html', {'product':product,'msg':msg})
	else:
		if user.usertype == 'superadmin':
			return render(request, 'edit_product.html', {'product':product})
		elif user.usertype == 'admin':
			return render(request, 'admin_edit_product.html', {'product':product})
		else:
			return render(request, 'user_edit_product.html', {'product':product})

def backpropage(request):
	return redirect('show_product')
def delete_cust(request,pk):
	customer=Contact.objects.get(pk=pk)
	customer.delete()
	return redirect(request,'show_customer')


def delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return render(request,'show_product.html')
def make_quot(request,pk):
	customer=Contact.objects.get(pk=pk)
	product=Product.objects.all()
	invo = str(random.randint(1000, 9999))
	return render(request, 'invoice.html',{'customer':customer,'invo':invo,'product':product})