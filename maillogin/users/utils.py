from .models import WhitelistDomain,BlacklistDomain
from validate_email import validate_email_or_fail
from validate_email.exceptions import SMTPTemporaryError,DomainNotFoundError


def EmailCheck(email):
    domain = email.split('@')[-1].strip()
    if(BlacklistDomain.objects.filter(pk=domain).exists()):
        print(f'domain {domain},false')
        return False,False,'Non Institutional Email Used'
    else:
        print(f'domain {domain},true')
        return True,False,"Registration Successful, however we couldn't check the validity of your email ID. Validation email sent. Please check inbox to validate and activate account."
    # if(WhitelistDomain.objects.filter(pk=domain).exists() or True):
    #     try:
    #         if(validate_email_or_fail(email)):
    #             return True,True,'Successfully Registered'
    #         else:
    #             return False,False,'Invalid Email Id'
    #     except SMTPTemporaryError:
    #         return True,False,"Registration Successful, however we couldn't check the validity of your email ID. Validation email sent. Please check inbox to validate and activate account."
    #     except DomainNotFoundError:
    #         return False,False,'Invalid Email Domain'
    #     except:
    #         return False,False,'Unknown Error'


        
    
    