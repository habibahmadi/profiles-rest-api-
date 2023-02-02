from django.db import models
#we need to import some classes
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.
#modify this file to enclude our user provfile model.


class userProfileManager(BaseUserManager):
    """Manager for user profiles"""
    #add some function to maniputed the model the manager is for.
    def create_user(self, email, name, password=None):
        """create a new user profile"""
        #making sure the user have an email address
        if not email:
            raise ValueError('users must have an email address')

        #normalize the email address (make the second half of the email lower case)
        email = self.normalize_email(email)
        #create a new model that the userProfileManager representing
        user = self.model(email=email, name=name)
        #set password, this way the password is hashed not a clear text. django encrypts password with set
        #set password function.
        user = set_password(password)
        #same the user. Use <using=self._dd> this will make sure that the user will be saved on multiple
        #database.
        user.save()
        #return the user
        return user
    #the next functino we need to create is superUser function
    #this will user our create_user function to create a new user but also assign super_user status.
    #like admin user in the system.
    #we want the password not be none. so that all super user have one.
    def create_superuser(self, name, password):
        """Create and save a new superuser with given detail"""
        user =self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
        """Database model for users in the system"""
        email = models.EmailField(max_length=225, unique=True)
        name = models.CharField(max_length=225)
        #add fieldds for the opermission system.
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False )
        #specify the model manager for the user model so it know how to create a user.
        objects = userProfileManager()
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['name']

        #these fileds are required by django model to interact with our custom model.
        def get_full_name(staff):
            """Retrieve full name of user"""
            return self.name

        def get_short_name(self):
            """Retrieve short name of the user"""
            return self.name

        #specify the string representation of our model.
        #this is the item that we watn tot return when we convert user profile opbject to a stirng
        # in python
        def __str__(self):
            """Return the string representation of our user"""
            return self.email
        #now create a manager
        # by default when creating a user django looks for a username but we have changed that to email.
        # for that we need to create a custome user manager to work with these users.
