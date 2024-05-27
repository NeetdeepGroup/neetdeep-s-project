from django.db import models

# Create your models here.
class Contact(models.Model):
	fname=models.CharField(max_length=60)
	lname=models.CharField(max_length=50)
	mobile=models.PositiveIntegerField()
	email=models.EmailField()
	address=models.TextField()
	message=models.TextField()

	def __str__(self):
		return self.fname +' ------------- '+ self.email


class User(models.Model):
	name=models.CharField(max_length=60)
	mobile=models.PositiveIntegerField()
	email=models.EmailField()
	password=models.CharField(max_length=50)
	address=models.TextField()
	usertype=models.CharField(max_length=60,default="staff")
	profile_picture=models.ImageField(upload_to="profile_picture/",default="")

	def __str__(self):
		return self.name

class Product(models.Model):
	category = (
		("Zigbee", "Zigbee"),
		("Wifi", "Wifi"),
		("Wired", "Wired"),
		( "Security", "Security"),
		("Other", "Other"),
	)
	proname=models.CharField(max_length=60)
	product_category=models.CharField(max_length=100,choices=category)
	qty=models.PositiveIntegerField()
	price=models.PositiveIntegerField()
	prodetail=models.TextField()
	product_picture=models.ImageField(upload_to="product_picture/",default="")

	def __str__(self):
		return self.proname

