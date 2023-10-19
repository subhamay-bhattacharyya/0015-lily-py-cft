# diagram.py
from diagrams import Diagram
from diagrams.aws.compute import EC2ElasticIpAddress,LambdaFunction


with Diagram("Release EIP", show=False):
    LambdaFunction("Release Unattached IP") >> EC2ElasticIpAddress("EPI")