from django.core.management.utils import get_random_secret_key

#KEYGEN
def KEYGEN():
    return get_random_secret_key()

print(KEYGEN())