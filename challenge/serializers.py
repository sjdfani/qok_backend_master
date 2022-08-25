from rest_framework import serializers
from .models import ChallengeAnswer, ChallengeRequest, Challenge, ChallengeCategory, StateChallenge, ChallengeResult, StateChallengeResult
from account.models import Account
from account.serializers import AccountSerializer
from django.db.models import Q
from question.models import Question
import random
from question.serializer import QuestionSerializer
from category.serializer import CategorySerializer
from .utils import update_level, update_challenge_wins, create_coinlog_challenge


class RetrieveChallengeReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeRequest
        fields = '__all__'


class ChallengeReqSerializer(serializers.Serializer):

    def get_free_challenge_request(self):
        user = self.context['request'].user
        account = Account.objects.filter(user=user).first()
        lookup = Q(accepted_by=None) & ~Q(account=account)
        try:
            challenge_req = ChallengeRequest.objects.get(lookup)
        except:
            challenge_req = None
        return challenge_req

    def create_challenge(self, challenge_request):
        user = self.context['request'].user
        accepting_account = Account.objects.filter(
            user=user
        ).first()
        challenge_request.accepted_by = accepting_account
        challenge_request.save()
        challenge_serializer = ChallengeSerializer(data={
            'account_1': challenge_request.account.pk,
            'account_2': challenge_request.accepted_by.pk,
            'state': StateChallenge.IN_CHALLENGE
        })
        if challenge_serializer.is_valid(raise_exception=True):
            challenge = challenge_serializer.save()
            return challenge

    def create(self):
        user = self.context['request'].user
        account = Account.objects.filter(user=user).first()
        challenge_req = ChallengeRequest.objects.create(account=account)
        return challenge_req

    def save(self, **kwargs):
        challenge_request_found = False
        challenge_request = self.get_free_challenge_request()
        if challenge_request:
            challenge_request_found = True
            return (self.create_challenge(challenge_request), challenge_request_found)
        else:
            return (self.create(), challenge_request_found)


class ChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context['request']
        res = super().to_representation(instance)
        res['account_1'] = AccountSerializer(
            instance.account_1, context={'request': request}).data
        res['account_2'] = AccountSerializer(
            instance.account_2, context={'request': request}).data
        return res


class ChallengeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeCategory
        fields = '__all__'
        extra_kwargs = {
            'created_by': {
                'required': False
            }
        }

    def random_questions(self):
        category = self.validated_data['category']
        questions = list(Question.objects.filter(category=category))
        questions = random.sample(questions, 4)
        return questions

    def create(self, validated_data):
        user = self.context['request'].user
        account = Account.objects.filter(user=user).first()
        random_question = self.random_questions()
        challenge_category = ChallengeCategory.objects.create(
            challenge=validated_data['challenge'],
            category=validated_data['category'],
            created_by=account,
            question_1=random_question[0],
            question_2=random_question[1],
            question_3=random_question[2],
            question_4=random_question[3],
        )
        return challenge_category

    def to_representation(self, instance):
        request = self.context['request']
        res = super().to_representation(instance)
        res['challenge'] = ChallengeSerializer(
            instance.challenge, context={'request': request}
        ).data
        res['created_by'] = AccountSerializer(instance.created_by, context={'request': request}
                                              ).data
        res['question_1'] = QuestionSerializer(instance.question_1, context={'request': request}
                                               ).data
        res['question_2'] = QuestionSerializer(instance.question_2, context={'request': request}
                                               ).data
        res['question_3'] = QuestionSerializer(instance.question_3, context={'request': request}
                                               ).data
        res['question_4'] = QuestionSerializer(instance.question_4, context={'request': request}
                                               ).data
        res['category'] = CategorySerializer(
            instance.category, context={'request': request}).data
        return res


class ChallengeAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeAnswer
        exclude = ['created_at']

    def to_representation(self, instance):
        request = self.context['request']
        res = super().to_representation(instance)
        res['challenge_category'] = ChallengeCategorySerializer(
            instance.challenge_category, context={'request': request}).data
        res['account'] = AccountSerializer(
            instance.account, context={'request': request}).data
        res['question'] = QuestionSerializer(
            instance.question, context={'request': request}).data
        return res

    def end_challenge_process(self, challenge_id):
        request = self.context['request']
        serializer = EndChallengeSerializer(
            data={'challenge': challenge_id}, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    def save(self, **kwargs):
        request = self.context['request']
        challenge_answer = super().save(**kwargs)
        update_challenge_wins(self.data, request)
        challenge_id = self.validated_data['challenge_category'].challenge.pk
        challenge_answer_count = ChallengeAnswer.objects.filter(
            challenge_category__challenge=challenge_id).count()
        if challenge_answer_count == 48:
            self.end_challenge_process(challenge_id)
        return challenge_answer


class EndChallengeSerializer(serializers.Serializer):
    challenge = serializers.PrimaryKeyRelatedField(
        queryset=Challenge.objects.all())

    def calculate_level(self, amount_account_1, amount_account_2):
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        update_level(account_1, amount_account_1)
        update_level(account_2, amount_account_2)

    def calculate_coin(self, amount_account_1, amount_account_2):
        wins_account_1 = self.validated_data['challenge'].wins_account_1
        wins_account_2 = self.validated_data['challenge'].wins_account_2
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        challenge = self.validated_data['challenge']
        if wins_account_1 > wins_account_2:
            account_1.coin += amount_account_1
            account_1.save()
            create_coinlog_challenge(
                account_1, amount_account_1, 'win', challenge.id
            )
        elif wins_account_1 < wins_account_2:
            account_2.coin += amount_account_2
            account_2.save()
            create_coinlog_challenge(
                account_2, amount_account_2, 'win', challenge.id
            )
        else:
            account_1.coin += amount_account_1
            account_1.save()
            create_coinlog_challenge(
                account_1, amount_account_1, 'equal', challenge.id
            )
            account_2.coin += amount_account_2
            account_2.save()
            create_coinlog_challenge(
                account_2, amount_account_2, 'equal', challenge.id
            )

    def identifyـwinner(self):
        wins_account_1 = self.validated_data['challenge'].wins_account_1
        wins_account_2 = self.validated_data['challenge'].wins_account_2
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        if wins_account_1 > wins_account_2:
            return (account_1, None)
        elif wins_account_1 < wins_account_2:
            return (account_2, None)
        else:
            return (account_1, account_2)

    def calculate_reward(self):
        wins_account_1 = self.validated_data['challenge'].wins_account_1
        wins_account_2 = self.validated_data['challenge'].wins_account_2
        reward_account_1 = int(wins_account_1 * 1.5)
        reward_account_2 = int(wins_account_2 * 1.5)
        return (reward_account_1, reward_account_2)

    def save(self, **kwargs):
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        challenge = self.validated_data['challenge']
        challenge.state = StateChallenge.END_CHALLENGE
        challenge.save()
        reward_account_1, reward_account_2 = self.calculate_reward()
        self.calculate_level(reward_account_1, reward_account_2)
        self.calculate_coin(reward_account_1, reward_account_2)
        winner_1, winner_2 = self.identifyـwinner()
        if winner_2:
            ChallengeResult.objects.create(
                challenge=challenge, account=account_1, state=StateChallengeResult.EQUAL_CHALLENGE, coin=reward_account_1, xp=reward_account_1)
            ChallengeResult.objects.create(
                challenge=challenge, account=account_2, state=StateChallengeResult.EQUAL_CHALLENGE, coin=reward_account_2, xp=reward_account_2)
        else:
            if winner_1 == account_1:
                ChallengeResult.objects.create(
                    challenge=challenge, account=account_1, state=StateChallengeResult.WIN_CHALLENGE, coin=reward_account_1, xp=reward_account_1)
                ChallengeResult.objects.create(
                    challenge=challenge, account=account_2, state=StateChallengeResult.LOSS_CHALLENGE, coin=0, xp=reward_account_2)
            elif winner_1 == account_2:
                ChallengeResult.objects.create(
                    challenge=challenge, account=account_2, state=StateChallengeResult.WIN_CHALLENGE, coin=reward_account_2, xp=reward_account_2)
                ChallengeResult.objects.create(
                    challenge=challenge, account=account_1, state=StateChallengeResult.LOSS_CHALLENGE, coin=0, xp=reward_account_1)


class ChallengeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeResult
        fields = '__all__'


class ChallengeGiveUpSerializer(serializers.Serializer):
    challenge = serializers.PrimaryKeyRelatedField(
        queryset=Challenge.objects.all()
    )

    def calculate_level(self, amount_account_1, amount_account_2):
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        update_level(account_1, amount_account_1)
        update_level(account_2, amount_account_2)

    def calculate_coin(self, request, amount_account_1, amount_account_2):
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        challenge = self.validated_data['challenge']
        remaining = None
        if request.user == account_1.user:
            if account_1.coin - 50 <= 0:
                remaining = 50 - account_1.coin
                account_1.coin -= remaining
                account_1.save()
                create_coinlog_challenge(
                    account_1, remaining, 'loss', challenge.id
                )
            else:
                account_1.coin -= 50
                account_1.save()
                create_coinlog_challenge(
                    account_1, -50, 'loss', challenge.id
                )
            account_2.coin += amount_account_2
            account_2.save()
            create_coinlog_challenge(
                account_2, amount_account_2, 'win', challenge.id
            )
        elif request.user == account_2.user:
            if account_2.coin - 50 <= 0:
                remaining = 50 - account_2.coin
                account_2.coin -= remaining
                account_2.save()
                create_coinlog_challenge(
                    account_2, remaining, 'loss', challenge.id
                )
            else:
                account_2.coin -= 50
                account_2.save()
                create_coinlog_challenge(
                    account_2, -50, 'loss', challenge.id
                )
            account_1.coin += amount_account_1
            account_1.save()
            create_coinlog_challenge(
                account_1, amount_account_1, 'win', challenge.id
            )
        return remaining

    def calculate_reward(self):
        wins_account_1 = self.validated_data['challenge'].wins_account_1
        wins_account_2 = self.validated_data['challenge'].wins_account_2
        reward_account_1 = int(wins_account_1 * 1.5)
        reward_account_2 = int(wins_account_2 * 1.5)
        return (reward_account_1, reward_account_2)

    def save(self, **kwargs):
        request = self.context['request']
        account_1 = self.validated_data['challenge'].account_1
        account_2 = self.validated_data['challenge'].account_2
        challenge = self.validated_data['challenge']
        challenge.state = StateChallenge.END_CHALLENGE
        challenge.save()
        reward_account_1, reward_account_2 = self.calculate_reward()
        self.calculate_level(reward_account_1, reward_account_2)
        remaining = self.calculate_coin(
            request, reward_account_1, reward_account_2)
        coin_amount = remaining if remaining else -50
        if account_1.user == request.user:
            ChallengeResult.objects.create(
                challenge=challenge, account=account_1, state=StateChallengeResult.LOSS_CHALLENGE, coin=coin_amount, xp=reward_account_1)
            ChallengeResult.objects.create(
                challenge=challenge, account=account_2, state=StateChallengeResult.WIN_CHALLENGE, coin=reward_account_2, xp=reward_account_2)
        elif account_2.user == request.user:
            ChallengeResult.objects.create(
                challenge=challenge, account=account_2, state=StateChallengeResult.LOSS_CHALLENGE, coin=coin_amount, xp=reward_account_2)
            ChallengeResult.objects.create(
                challenge=challenge, account=account_1, state=StateChallengeResult.WIN_CHALLENGE, coin=reward_account_1, xp=reward_account_1)
