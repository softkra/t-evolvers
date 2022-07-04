from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.db.models import IntegerField, UUIDField, DateTimeField, TextField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Create your models here.
class Metrics(TimeStampedModel):

    """Model for managing Metrics

    Attributes:
        device_id: ID device
        metric: Metric number
        report: date metric reported
    """

    device_id = UUIDField(verbose_name=_('Dispositivo'))
    metric = IntegerField(verbose_name=_('Metrica'))
    report = DateTimeField(verbose_name=_('Fecha de reporte'))

    class Meta:
        verbose_name = _('Metrics')
        verbose_name_plural = _('Metrics')

    """def __str__(self):
        return '{} {} {}'.format(self.device_id, self.metric, self.report)"""

class Notifications(TimeStampedModel):

    """Model for managing Notifications

    Attributes:
        message: message notification
    """

    message = TextField(verbose_name=_('Notificacion'))

    class Meta:
        verbose_name = _('Notifications')
        verbose_name_plural = _('Notifications')