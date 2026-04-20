from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class DataSource(TextChoices):
    IMF = 'IMF', _('International Monetary Fund')
    WORLD_BANK = 'WORLD_BANK', _('World Bank')
