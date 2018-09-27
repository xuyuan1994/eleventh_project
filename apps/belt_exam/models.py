from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
password_regex=re.compile(r'\w*[a-zA-Z]\w*')
# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self,form):
        errors=[]
        if len(form['name'])<3:
            errors.append('name must be longer than 3 characters!')
        if len(form['username'])<3:
            errors.append('username must be longer than 3 characters!')
        if not password_regex.match(form['password']):
            errors.append('the password should be at least one character!')
        if form['password']!=form['confirm']:
            errors.append('the confirmed password must match with the the password!')
        try:
            user=self.get(username=form['username'])
            errors.append('the username you used is already registered')
            return (False,errors)
        except:
            if len(errors)>0:
                return (False,errors)
            else:
                return (True,errors)
    def validate_login(self,form):
        errors=[]
        try:
            user=self.get(username=form['username'])
            if bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                return (True,errors)
        except:
            errors.append('this user does not exist')
            return (False,errors)
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=25)
    objects = UserManager()
class Product(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    added_by = models.CharField(max_length=255)
class Wishlist(models.Model):
    
    name = models.CharField(max_length=255)
    product = models.ManyToManyField(Product, related_name="wishlists")
    user= models.ManyToManyField(User, related_name="wishlists")
