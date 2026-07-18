    # Code reference https://stackoverflow.com/questions/51462947/manage-py-createsuperuser-is-not-working-with-custom-user-model

# from django.contrib.auth.base_user import BaseUserManager

# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):

#         # make sure the username is provided
#         if username is None:
#             raise ValueError('Please provide Username')

#         # creates a user model
#         user = self.model(username=username, **extra_fields)
#         # sets password
#         user.set_password(password)
#         # saves instance
#         user.save(using=self._db)
#         return user


    # def create_superuser(self, email, username, password):

    #     if password is None:
    #         raise TypeError('Provide password')

    #     user = self.create_user(
    #         email=email, 
    #         username=username,
    #         password=password
    #         )
    #     user.is_superuser = True
    #     user.save()

    #     return user