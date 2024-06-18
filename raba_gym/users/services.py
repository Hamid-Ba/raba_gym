from random import randint
from django.db import transaction 

from .models import User, Profile


def create_profile(*, user:User, bio:str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)

def create_user(*, phone:str, password:str) -> User:
    # for Test
    return User.objects.create_user(phone=phone, password=password, full_name=password)


@transaction.atomic
def register(*, phone:str, bio:str|None) -> User:

    otp = str(randint(100000, 999999))
    user = create_user(phone=phone, password=otp)
    create_profile(user=user, bio=bio)

    return user
