from dbmanager import *
import sys

print("Initiating user with the following data.", f"Username:{sys.argv[1]}", f"Password:{sys.argv[2]}")
su = add_superuser(username=sys.argv[1], password=sys.argv[2])
commit()
