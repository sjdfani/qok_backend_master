from .models import Challenge
from account.models import Level, CoinLog


def update_challenge_wins(data, request):
    answer = data['answer']
    correct_answer = data['question']['correct_answer']
    challenge_id = data['challenge_category']['challenge']['id']
    account_1_email = data['challenge_category']['challenge']['account_1']['user']['email']
    account_2_email = data['challenge_category']['challenge']['account_2']['user']['email']
    challenge = Challenge.objects.get(id=challenge_id)
    if answer == correct_answer:
        if request.user.email == account_1_email:
            challenge.wins_account_1 += 1
            challenge.save()
        elif request.user.email == account_2_email:
            challenge.wins_account_2 += 1
            challenge.save()


def update_level(account, amount):
    account_level = Level.objects.get(account=account)
    minimum = account_level.minimum
    maximum = account_level.maximum
    if minimum + amount >= maximum:
        account_level.minimum = (minimum+amount) - maximum
        account_level.maximum += 10
        account_level.stage += 1
        account_level.save()
        if account_level.minimum >= account_level.maximum:
            update_level(account, 0)
    else:
        account_level.minimum += amount
        account_level.save()


def create_coinlog_challenge(account, amount, state, challenge_id):
    description = f'{state} challenge with id={challenge_id}'
    CoinLog.objects.create(
        account=account, amount=amount, description=description)
