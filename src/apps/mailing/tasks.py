from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail

from apps.users.models import CustomUser
from apps.mailing.models import Template


@shared_task(bind=True)
def send_email_task(self, ids: list[int], template_id: int, to_everyone: bool):
    channel_layer = get_channel_layer()
    task_id = self.request.id
    template_object = Template.objects.get(pk=template_id)
    template_file = open(template_object.file.path, "r")
    template = template_file.read()
    users = CustomUser.objects.all() if to_everyone else CustomUser.objects.filter(id__in=ids)

    sent = 0
    total = len(users)

    async_to_sync(channel_layer.group_send)(
        task_id,
        {
            "type": "celery_task_update",
            "message": {"progress": 0.0, "status": "start"},
        },
    )

    for user in users:
        send_mail(
            subject="KinoCMS",
            html_message=template,
            message="KinoCMS",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        sent += 1
        progress = sent / total
        status = "progress" if progress < 1.0 else "complete"

        async_to_sync(channel_layer.group_send)(
            task_id,
            {
                "type": "celery_task_update",
                "message": {"progress": progress, "status": status},
            },
        )
