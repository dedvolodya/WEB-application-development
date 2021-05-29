import datetime
from time import sleep
from celery import shared_task, Task
from django.core.mail import send_mail
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CallbackTask(Task):
    def on_success(self, retval, task_id, *args, **kwargs):
        channel_layer = get_channel_layer()
        if not channel_layer:
            print("Not found")
            return

        async_to_sync(channel_layer.group_send)(
            "finished_tasks",
            {
                'type': 'task_message',
                'message': f'Finished Task {task_id}.  Result is {retval}, Args is {args} Current time is {datetime.datetime.now()}'
            }
        )
        print("success")


@shared_task(name="send_email")
def send_email(emails: list):
    send_mail("Celery test!", "Great!", 'vlad81boiko@gmail.com', emails)
    return None


@shared_task(name="long_work")
def long_work(time):
    sleep(time)
    return None