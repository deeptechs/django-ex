import os, pandas

AWS_UPLOAD_BUCKET = "photogenius-bucket4"

AWS_UPLOAD_USERNAME = "pg-s3"

AWS_UPLOAD_GROUP = "pg-user-group"

AWS_UPLOAD_REGION = 'us-west-1'


def read_con_arg(cred_file):
    """Read the Access Key Id and Secret Access Key from a csv credential file downloaded from Aws portal.

    Args:
        cred_file: File that consists Aws credentials.

    Returns:
        Connection string dictionary (Keys are aws_access_key_id, aws_secret_access_key, region_name)

    .. warning::

        Set the region default 'eu-central-1'
    """
    df = pandas.read_csv(cred_file, sep=',')

    access_key_id = df.loc[0, 'Access key ID']
    secret_access_key = df.loc[0, 'Secret access key']

    dic = {
        'aws_access_key_id': access_key_id,
        'aws_secret_access_key': secret_access_key,
        'region_name': AWS_UPLOAD_REGION
    }

    return dic


# AWS Settings
conn_args = read_con_arg(os.environ['AWS_CRED_FILE'])
AWS_UPLOAD_SECRET_KEY = conn_args['aws_secret_access_key']
AWS_UPLOAD_ACCESS_KEY_ID = conn_args['aws_access_key_id']
