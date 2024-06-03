from django.db import models


# Create your models here.

class Users(models.Model):
    type = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"type: {self.type},username: {self.username}, email: {self.email}, password: {self.password}"

    class Meta:
        db_table = 'users'


class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Measure_units(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100)
    def __str__(self):
        return f"name: {self.name}, abbreviation: {self.abbreviation}"

    class Meta:
        db_table = 'measure_units'


class Subcategories(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"name= {self.name}, category: {self.category}"

    class Meta:
        db_table = 'subcategories'


class Store(models.Model):
    available_quantity = models.IntegerField()
    price_product = models.DecimalField(max_digits=10, decimal_places=2)
    desc_prod = models.CharField(max_length=100)
    discount = models.IntegerField()
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE)  # Modificato
    provider = models.ForeignKey('Providers', on_delete=models.CASCADE)  # Modificato
    measure_units = models.ForeignKey(Measure_units, on_delete=models.CASCADE)

    def __str__(self):
        return f"available_quantity= {self.available_quantity}, discount: {self.discount}, price_product: {self.price_product}, desc_prod: {self.desc_prod}, provider: {self.provider}, subcategory: {self.subcategory}, measure_units: {self.measure_units}"

    class Meta:
        db_table = 'store'


class Providers(models.Model):
    type = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return f"type: {self.type},password: {self.password}, email: {self.email}, username: {self.username}"

    class Meta:
        db_table = 'providers'


class Cart(models.Model):
    quantity = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"quantity: {self.quantity}, store: {self.store}, user: {self.user}"

    class Meta:
        db_table = 'cart'


class Orders(models.Model):
    status = models.CharField(max_length=100)
    date_order = models.CharField(max_length=100)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"status: {self.status}, date_order: {self.date_order}, user: {self.user}"

    class Meta:
        db_table = 'orders'


class OrderDetails(models.Model):
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"quantity: {self.quantity},status:{self.status}, order: {self.order}, store: {self.store}"

    class Meta:
        db_table = 'orders_details'




