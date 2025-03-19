from boto3 import client
import time

from src.utils.config import Config

settings = Config()

class SQSService:
    def __init__(self):
        self.client = client('sqs')

    def receive_messages(self):
        while True:
            response = self.client.receive_message(
                QueueUrl=settings.queue_url
            )
            time.sleep(1)
