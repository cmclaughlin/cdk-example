#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput

from cdktf_cdktf_provider_aws import AwsProvider
from cdktf_cdktf_provider_aws import S3Bucket, S3BucketWebsite, S3BucketObject


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        region = 'us-east-1'
        bucket_name = 'cdktest-cmclaughlin'

        AwsProvider(self, 'aws', region=region)

        website = S3BucketWebsite(index_document='index.html',
                                  error_document='error.html')

        bucket = S3Bucket(self, 'bucket', bucket=bucket_name, region=region,
                          website=[website])

        S3BucketObject(self, 'upload', bucket=bucket_name,
                       key='index.html', source='../index.html',
                       acl='public-read',
                       content_type='text/html',
                       depends_on=[bucket])

        TerraformOutput(self, 'endpoint', value=bucket.website_endpoint)


app = App()
MyStack(app, "example")

app.synth()
