from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from challenge.models import Challenge, StateChallenge
from datetime import datetime, timedelta


def delete_timeout_challenges():
    Challenge.objects.filter(
        state=StateChallenge.IN_CHALLENGE,
        created__lte=datetime.now(tz=pytz.utc) - timedelta(days=1)
    ).update(state=StateChallenge.END_CHALLENGE)


def delete_ended_challenges():
    Challenge.objects.filter(
        state=StateChallenge.END_CHALLENGE,
        ended__lte=datetime.now(tz=pytz.utc) - timedelta(days=2)
    ).update(is_archived=True)


def main():
    scheduler = BackgroundScheduler(timezone='MST')
    scheduler.add_job(delete_timeout_challenges, 'interval', minutes=1)
    scheduler.add_job(delete_ended_challenges, 'interval', minutes=1)
    scheduler.start()
