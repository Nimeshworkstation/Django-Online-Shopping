from django.db import models

# Create your models here.from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
	('Madhesh','Madhesh'),
	('Gandaki','Gandaki'),
	('Lumbini','Lumbini'),
	('Karnali','Karnali'),
	('Bagmati','Bagmati'),
	('Sudur Paschim','Sudur Paschim')
)

# Create your models here.

class Customer(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	locality = models.CharField(max_length = 100)
	city = models.CharField(max_length = 100)
	zipcode = models.IntegerField()
	state = models.CharField(max_length = 100, choices=STATE_CHOICES)

	def __str__(self):
		return str(self.id)


CATEGORY = (

	('M','Mobile'),
	('T','Television'),
	('TW','TopWear'),
	('BW', 'BottomWear'),

	)


class Product(models.Model):
	title = models.CharField(max_length = 100)
	selling_price = models.FloatField()
	discounted_price = models.FloatField()
	description = models.TextField()
	brand = models.CharField(max_length = 100)
	category = models.CharField(max_length = 2, choices = CATEGORY)
	product_image = models.ImageField(upload_to = 'prodimg')

	def __str__(self):
		return str(self.id)


class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default = 1)

	def __str__(self):
		return str(self.id)

	@property
	def total_cost(self):
		return self.quantity * self.product.discounted_price
	


	



STATUS_CHOICES =(
		('Accepted','Accepted'),
		('Packed','Packed'),
		('On the Way', 'On the way'),
		('Delivered', 'Delivered'),
		('Cancel','Cancel')

	)

class OrderPlaced(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	ordered_date = models.DateTimeField(auto_now_add = True)
	status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default='Pending')

	def __str__(self):
		return str(self.id)

	@property
	def total_cost(self):
		return self.quantity * self.product.discounted_price



