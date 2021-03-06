from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Department(models.Model):
    user = models.ManyToManyField(User, through='Association')
    name = models.CharField(max_length=255, unique = True)
    def __str__(self):
        return self.name

class Product(models.Model):
    cas = models.CharField('CAS number', max_length=12, unique=True)
    name = models.CharField(max_length=255)
    min_temp = models.DecimalField('Minimum Temperature', max_digits=6, decimal_places=3, default = 25)
    max_temp = models.DecimalField('Maximum Temperature', max_digits=6, decimal_places=3, default = 25)
    ispoison_nonvol = models.BooleanField('poison - non-volatile')
    isreactive = models.BooleanField('reactive')
    issolid = models.BooleanField('solid')
    isoxidliq = models.BooleanField('oxidizing liquid')
    isflammable = models.BooleanField('flammable')
    isbaseliq = models.BooleanField('base liquid')
    isorgminacid = models.BooleanField('organic and mineral acid')
    isoxidacid = models.BooleanField('oxidizing acid')
    ispois_vol = models.BooleanField('poison - volatile')
    def __str__(self):
        return self.name

class Room(models.Model):
    room_name = models.CharField(max_length=255)
    building_name = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.room_name

class Location(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    temperature = models.DecimalField('Temperature', max_digits=10, decimal_places=4, default = 25)
    description = models.TextField(blank=True)
    ispoison_nonvol = models.BooleanField('poison - non-volatile', default = False)
    ispois_vol = models.BooleanField('poison - volatile', default = False)
    isreactive = models.BooleanField('reactive', default = False)
    issolid = models.BooleanField('solid', default = False)
    isbaseliq = models.BooleanField('base liquid', default = False)
    isorgminacid = models.BooleanField('organic and mineral acid', default = False)
    isoxidliq = models.BooleanField('oxidizing liquid', default = False)
    isoxidacid = models.BooleanField('oxidizing acid', default = False)
    isorgminacid = models.BooleanField('organic and mineral acid', default = False)
    isflammable = models.BooleanField('flammable', default = False)

    def is_valid(self, Product):
        if (self.ispois_vol == Product.ispoison_nonvol and self.ispoison_nonvol == Product.ispoison_nonvol and self.issolid == Product.issolid):
            return True
        else:
            return False
    def __str__(self):
        return self.name

class Product_Unit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    in_house_no = models.CharField('In House ID', max_length=255, blank = True )
    del_date = models.DateField('delivery date')
    company = models.CharField(max_length=255)
    cat_num = models.CharField('catalog number', max_length=255, blank = True)
    description = models.CharField(max_length=255)
    batch = models.CharField('Batch Number', max_length=255, blank = True )
    init_amount = models.DecimalField('initial amount', max_digits=10, decimal_places=4, default = 0, validators = [MinValueValidator(0.0000)])
    m_unit = models.CharField('measuring units', max_length=4, null=True, blank = True)
    purity = models.CharField('purity/percentage', max_length = 255, null=True, blank = True)
    exp_date = models.DateField('expiration date', null=True, blank = True)
    ret_date = models.DateField('retest date', null=True, blank = True)
    open_date = models.DateField('date opened', null=True, blank = True)
    used_amount = models.DecimalField('amount used', max_digits=10, decimal_places=4, default=0, validators = [MinValueValidator(0.0000)])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    reservation = models.ManyToManyField(User, through='Reserve')
    is_inactive = models.BooleanField('Archived', default = False)
    curr_amount = models.DecimalField('current amount', max_digits=10, decimal_places=4, default=0, blank = True, validators = [MinValueValidator(0.0000)])
    department = models.ManyToManyField(Department, through="Watching", default=None, blank=True)
    def curr_am(self):
        init = float(self.init_amount)
        used = float(self.used_amount)
        return round((init - used), 3)
    @property
    def perc_left(self):
        return round((self.curr_amount/self.init_amount)*100, 3)

    def __str__(self):
        return self.description

class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_un = models.ForeignKey(Product_Unit, verbose_name='description', on_delete=models.CASCADE)
    amount_res = models.DecimalField('Amount to Reserve', max_digits=10, decimal_places=4)
    date_res = models.DateField('Reservation Date')
    is_complete = models.BooleanField(null=True)
    res_name = models.CharField('Reservation Name', max_length=255, unique=True, default="Reservation")
    def _str_(self):
        return self.prod_un

class Uses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_un = models.ForeignKey(Product_Unit, verbose_name='description',  on_delete=models.CASCADE)
    amount_used = models.DecimalField('amount used', max_digits=10, decimal_places=4)
    date_used = models.DateField('date of use')

class Watching(models.Model):
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    prod_un = models.ForeignKey(Product_Unit, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    low_warn = models.BooleanField('Running Low Warning')

class Association(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, verbose_name = 'department', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'dept',)
