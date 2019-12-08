from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class StatusModel(Model):
    """
    The status of a specific location at a given time.
    """

    class Meta:
        table_name = "RiverTrailAlertsTable"

    pk = UnicodeAttribute(hash_key=True)   # Location
    sk = UnicodeAttribute(range_key=True)  # Time
    status = UnicodeAttribute()            # 'open', 'closed', or 'conditions variable'

