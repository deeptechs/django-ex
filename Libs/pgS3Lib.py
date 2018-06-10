import boto3
import pandas
from PhotoGenius import config_aws
import botocore


# For detailed logs
# boto3.set_stream_logger('')


class PgS3:
    _s3 = None

    def __init__(self):

        """Initialize the aws service objects with the provided environmental variable.

        """

        self.s3 = boto3.resource('s3', **config_aws.conn_args)

    @staticmethod
    def _read_con_arg(cred_file):

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
            'region_name': config_aws.AWS_UPLOAD_REGION
        }

        return dic

    def get_bucket_by_name(self, bname):

        bucket = self.s3.Bucket(bname)
        exists = True
        try:
            self.s3.meta.client.head_bucket(Bucket=bname)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False

        if exists is True:
            return bucket
        else:
            return None

    def get_user_photo_urls_by_bucket_name(self, bname, email):

        # if blank prefix is given, return everything)
        bucket = self.get_bucket_by_name(bname)
        objs = bucket.objects.filter(Prefix=email)
        urls = []

        for object in objs:
            urls.append(self.s3.meta.client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': config_aws.AWS_UPLOAD_BUCKET,
                    'Key': object.key,
                })
            )
        return urls
