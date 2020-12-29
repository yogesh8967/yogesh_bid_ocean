from django.db import models
# Create your models here.

class Dish(models.Model):
    def __str__(self):
        return self.Dish_Name
    d_type = (
        ('Indian','Indian'),
        ('Chinesse','Chinesse'),
        ('Western','Western'),
        ('Beverages', 'Beverages'),
    )
    Dish_Name = models.CharField(max_length=200, null=True)
    Dish_Discription = models.CharField(max_length=200, null=True)
    Dish_Type = models.CharField(max_length=200, null=True, choices=d_type)
    Price = models.FloatField(max_length=200, null=True)
    Offer = models.IntegerField(null=True)
    Date = models.DateTimeField(auto_now_add=True, null=True)
    Total_Sold = models.IntegerField(null=True)
    Dish_File_Path = models.ImageField(null=True, blank = True)

class Profile(models.Model):
    def __str__(self):
        return self.User_ID
    User_ID = models.CharField(max_length=200, null=True)
    Password = models.CharField(max_length=200, null=True)
    Ph_no = models.CharField(max_length=12, null=True)
    E_Mail = models.CharField(max_length=200, null=True)
    Address = models.CharField(max_length=200, null=True)
    Role = models.CharField(max_length=200, null=True)

class Order(models.Model):
    O_Type = (
        ('Take-away','Take-away'),
        ('Delivery', 'Delivery'),
    )
    Pay_Status = (
        ('Pending','Pending'),
        ('Recieved','Recieved')
    )
    #Order_ID = models.CharField(max_length=200, null=True)
    User_ID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True, null=True)
    Order_Type = models.CharField(max_length=200, null=True, choices=O_Type)
    Payment_Status = models.CharField(max_length=200, null=True, choices=Pay_Status)
    Destination = models.CharField(max_length=200, null=True)
    Tax = models.FloatField(max_length=200, null=True, default = 0.0)
    Overdue = models.FloatField(max_length=200, null=True, default = 0.0)
    Total_Amount = models.FloatField(max_length=200, null=True)

class Cart(models.Model):
    User_ID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    Quantity = models.IntegerField(null=True, default = 0)

class Intermediate(models.Model):
    Order_ID = models.ForeignKey(Order, on_delete=models.CASCADE)
    Dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    Quantity = models.IntegerField(null=True)