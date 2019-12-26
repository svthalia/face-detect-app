from .default import *

environment = os.environ.get('ENVIRONMENT', 'LOCAL')

if environment == 'AWS_EB':
    from .elastic_beanstalk import *