from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME=re.compile(r"^[\\p{w} .'-]+$")
class UserManager(models.Manager):
    def validCheck(self, form_data):
        print 'You are inside the validCheck'
        result = {"valid": True}
        errors = []
        if len(form_data['name'])<2:
            errors.append("Name must be at least 2 characters long.")
            result["valid"]=False
        if not form_data['name'].isalpha():
            result["valid"]=False
            errors.append("Please enter a name using letters only.")
        if not EMAIL_REGEX.match(form_data['email']):
            result["valid"]=False
            errors.append("Please enter a valid email address.")
        if User.objects.filter(email = form_data['email']).first():
            result["valid"]=False
            errors.append("That email is already taken.")
        if len(form_data['password'])<8:
            result["valid"]=False
            errors.append("Password must be at least 8 characters.")
        if str(form_data['password']) != str(form_data['password_confirmation']):
            result["valid"]=False
            errors.append("Password confirmation does not match password.")
        result['errors'] = errors
        return result

    def createUser(self, form_data):
        password = form_data['password'].encode()
        #Encrypt user's password
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        user=User.objects.create(name=form_data['name'], alias=form_data['alias'], email=form_data['email'], password=encryptedpw, birthdate=form_data['birthdate'])
        return user

    def logging_in(self, form_data):
        result = {"valid": True}
        errors = []
        # print form_data['email']
        user=User.objects.filter(email=form_data['email']).first()

        # print 'this is {}'.format(user)
        if user:

            password=form_data['password'].encode()
            user_pass=user.password.encode()
            if bcrypt.hashpw(password, user_pass) == user_pass:
                result['user']=user
                print 'it worked?'
                return result
        if user == None:
            errors.append("That email does not exist")
        elif bcrypt.hashpw(password, user_pass) != user_pass:
            errors.append('Invalid password')
        result["valid"] = False
        result['errors'] = errors
        return result

class QuoteManager(models.Manager):
    def quoteValidate(self, form_data):
        result = {"valid": True}
        errors = []
        if len(form_data['content'])<11:
            result["valid"]=False
            errors.append("'Message' must be at least 10 characters long.")
        if len(form_data['writer'])<4:
            result["valid"]=False
            errors.append("'Quoted by' must be more than 3 characters long.")
        result['errors'] = errors
        return result




class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirmation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    birthdate=models.DateField()

    objects = UserManager()


class Quote(models.Model):
    content = models.TextField()
    writer = models.CharField(max_length=255)
    submitter= models.ForeignKey(User, related_name='submission')
    favorited_by = models.ManyToManyField(User, related_name='favorites')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Quote contents: {} and the persons that liked {}".format(self.content, self.favorited_by.all)

    objects = QuoteManager()
