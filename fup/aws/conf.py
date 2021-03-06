import datetime, boto3, configparser
from botocore.client import Config

keys = configparser.ConfigParser()
keys.read('./.env')
aws = keys['aws']

# s3 = boto3.resource(
#     's3',
#     aws_access_key_id='',
#     aws_secret_access_key='',
#     config=Config(signature_version='s3v4')
# )

AWS_GROUP_NAME          = aws.AWS_GROUP
AWS_USERNAME            = aws.AWS_USERNAME
AWS_ACCESS_KEY_ID       = aws.AWS_ACCESS
AWS_SECRET_ACCESS_KEY   = aws.AWS_SECRET
AWS_FILE_EXPIRE         = 200
AWS_PRELOAD_METADATA    = True
AWS_QUERYSTRING_AUTH    = True

AWS_S3_SIGNATURE_VERSION = "s3v4"

DEFAULT_FILE_STORAGE = 'fup.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'fup.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'my-buck0'
S3DIRECT_REGION = 'ap-south-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
