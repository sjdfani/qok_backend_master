from rest_framework import serializers
from user.models import CustomUser
from .models import Account, Level, CoinLog, AccountIcon
from challenge.models import Challenge, ChallengeAnswer, ChallengeResult, StateChallengeResult
from django.db.models import Q


class AccountIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountIcon
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        exclude = ['account']


class AccountSerializer(serializers.ModelSerializer):

    def user_data(self, obj):
        return {
            'email': obj.user.email,
            'username': obj.user.username
        }
    user = serializers.SerializerMethodField('user_data')
    level = LevelSerializer()

    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'icon': {
                'required': False
            }
        }

    def create(self, validated_data):
        user = self.context['request'].user
        level = validated_data.pop('level')
        account = Account.objects.create(user=user, **validated_data)
        Level.objects.create(account=account, **level)
        return account

    def update(self, instance, validated_data):
        level_data = validated_data.pop('level')
        level = instance.level
        level.stage = level_data.get('stage', level.stage)
        level.minimum = level_data.get('minimum', level.minimum)
        level.maximum = level_data.get('maximum', level.maximum)
        level.save()
        instance.coin = validated_data.get('coin', instance.coin)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['icon'] = AccountIconSerializer(instance.icon).data
        return res


class CoinLogSerializer(serializers.ModelSerializer):
    def account_data(self, obj):
        return {
            'email': obj.account.user.email,
            'username': obj.account.user.username
        }
    account = serializers.SerializerMethodField('account_data')

    class Meta:
        model = CoinLog
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        account = Account.objects.filter(user=user).first()
        coin_log = CoinLog.objects.create(account=account, **validated_data)
        return coin_log


class UpdateAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    icon = serializers.PrimaryKeyRelatedField(
        queryset=AccountIcon.objects.all())

    def save(self, **kwargs):
        user = self.context['request'].user
        username = self.validated_data['username']
        try:
            account = Account.objects.get(user=user)
            user = CustomUser.objects.get(email=user.email)
        except:
            account = None
            user = None
        if account and user:
            account.icon = self.validated_data['icon']
            account.save()
            user.username = username
            user.save()
        return account


class UpdateIconAccountSerializer(serializers.Serializer):
    icon = serializers.PrimaryKeyRelatedField(
        queryset=AccountIcon.objects.all())

    def save(self, **kwargs):
        user = self.context['request'].user
        try:
            account = Account.objects.get(user=user)
        except:
            account = None
        account.icon = self.validated_data['icon']
        account.save()
        return account


class TotalGamesSerializer(serializers.Serializer):

    def save(self, **kwargs):
        user = self.context['request'].user
        lookup = Q(account_1__user=user) | Q(account_2__user=user)
        total_challenge_count = Challenge.objects.filter(lookup).count()
        lookup = Q(account__user=user) & Q(
            state=StateChallengeResult.WIN_CHALLENGE)
        wins_challenge_count = ChallengeResult.objects.filter(lookup).count()
        lookup = Q(account__user=user) & Q(
            state=StateChallengeResult.LOSS_CHALLENGE)
        loss_challenge_count = ChallengeResult.objects.filter(lookup).count()
        lookup = Q(account__user=user) & Q(
            state=StateChallengeResult.EQUAL_CHALLENGE)
        equal_challenge_count = ChallengeResult.objects.filter(lookup).count()
        message = {
            'total': total_challenge_count,
            'wins': wins_challenge_count,
            'equal': equal_challenge_count,
            'loss': loss_challenge_count
        }
        return message


class SummaryCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    total_answers = serializers.SerializerMethodField()

    class Meta:
        model = ChallengeAnswer
        fields = ['category', 'correct_answers', 'total_answers']

    def get_category(self, obj):
        return obj.get('challenge_category__category__name')

    def get_correct_answers(self, obj):
        return obj.get('correct_answers')

    def get_total_answers(self, obj):
        return obj.get('total_answers')
