from django.core.files import File
from django.db import models

from io import BytesIO
from PIL import Image

class Category(models.TextChoices):
    WOMEN = "WOMEN"
    MEN = "MEN"
    KIDS = "KIDS"

class Type(models.TextChoices):
    CASUAL = "CASUAL"
    COOPERATE = "COOPERATE"

class LabelColor(models.TextChoices):
    green = 'new'
    grey = 'stockout'
    blue = 'stockblue'
    red = 'sale'

def compress(image):
    img = Image.open(image)
    im_io = BytesIO()
    img.save(im_io, 'png', quality=70)
    img.close()
    new_image = File(im_io, name=image.name)
    return new_image

def listRating(rating):
    final = ""
    for n in range(rating):
        final += 'x'
    return final

class Product(models.Model):
    name = models.CharField(max_length=15, null=True)
    category = models.CharField(max_length=5, choices=Category.choices, null=True)
    productType = models.CharField(max_length=9, choices=Type.choices, null=True)
    rating = models.IntegerField(default=0, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    ratingList = models.CharField(max_length=5, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)
    image = models.ImageField(default="default.jpeg", upload_to="images/")
    label = models.CharField(max_length=20, null=True, blank=True)
    labelColor = models.CharField(max_length=10, choices=LabelColor.choices, null=True, blank=True)
    labelClass = models.CharField(max_length=5, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        if self.label:
            self.label = self.label.upper()
            if self.labelColor.lower() == 'green':
                self.labelClass = 'new'
            elif self.labelColor.lower() == 'grey':
                self.labelClass = 'stockout'
            elif self.labelColor.lower() == 'blue':
                self.labelClass = 'stockblue'
            elif self.labelColor.lower() == 'red':
                self.labelClass = 'sale'
        self.ratingList = listRating(self.rating)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    cart_order = models.ForeignKey('main.Order', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey('main.UserData', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f'qty: {self.qty}, {self.product.name}'

    def save(self, *args, **kwargs):
        self.cost = self.product.price * self.qty
        return super().save(*args, **kwargs)


class UserData(models.Model):
    ip = models.CharField(max_length=20, unique=True, null=True)
    cart = models.ManyToManyField(CartItem)
    totalCost = models.IntegerField(default=0, null=True, blank=True)
    firstname = models.CharField(max_length=20, default='', null=True, blank=True)
    lastname = models.CharField(max_length=20, default='', null=True, blank=True)
    address = models.CharField(max_length=50, default='', null=True, blank=True)
    apartment = models.CharField(max_length=30, default='', null=True, blank=True)
    city = models.CharField(max_length=20, default='', null=True, blank=True)
    state = models.CharField(max_length=30, default='', null=True, blank=True)
    phone = models.CharField(max_length=15, default='', null=True, blank=True)
    email = models.EmailField(default='', null=True, blank=True)
    display_order_taken_notification = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        if self.firstname:
            return f'{self.firstname} {self.lastname}'
        return f'IP - {self.ip}, no-name-yet'

    def fullname(self):
        if self.firstname:
            return f'{self.firstname} {self.lastname}'
        return ''

    def save(self, *args, **kwargs):
        totalCost = 0
        if self.id:
            for item in self.cart.all():
                totalCost += item.cost
        self.totalCost = totalCost
        super().save(*args, **kwargs)

class OrderStatus(models.TextChoices):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN PROGRESS'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'

class Order(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, default='', null=True, blank=True)
    apartment = models.CharField(max_length=30, default='', null=True, blank=True)
    city = models.CharField(max_length=20, default='', null=True, blank=True)
    state = models.CharField(max_length=30, default='', null=True, blank=True)
    phone = models.CharField(max_length=15, default='', null=True, blank=True)
    email = models.EmailField(default='', null=True, blank=True)
    cart = models.ManyToManyField(CartItem)
    products = models.TextField(null=True, blank=True, default='')
    totalCost = models.IntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=11, choices=OrderStatus.choices, default=OrderStatus.CREATED)

    def get_products(self):
        self.products = ''
        for idx,item in enumerate(list(self.cart.all())):
            self.products += f'({idx+1}) {item.qty} qty of {item.product.name} at {item.product.price} = {item.cost} total \n\n'
        return self.products

    def save(self, *args, **kwargs):
        if self.id:
            self.products = self.get_products()
            totalCost = 0
            for item in self.cart.all():
                totalCost += item.cost
            self.totalCost = totalCost
        super().save(*args, **kwargs)

    def __str__(self):
        if self.user.firstname:
            return f'order by {self.user.firstname} {self.user.lastname}'
        return f'IP - {self.user.ip}, no-name-yet'

class MessageStatus(models.TextChoices):
    NEW = 'NEW'
    WAITING = 'WAITING'
    FINISHED = 'FINISHED'

class Message(models.Model):
    name = models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True)
    content = models.TextField(null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=MessageStatus.choices, default=MessageStatus.NEW)

    def __str__(self):
        return f'{self.name} on {self.date_sent}'