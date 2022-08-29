import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from users.models import BlacklistDomain,WhitelistDomain

with open('static/all_email_provider_domains.txt','r') as f:
    domains = f.readlines()

data_list = [{'domain':x.strip()} for x in domains]
obj_list = [BlacklistDomain(**data_dict) for data_dict in data_list]
objs = BlacklistDomain.objects.bulk_create(obj_list)
# print(content_list[0])

