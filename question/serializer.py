from rest_framework import serializers
from category.models import Category
from .models import Question, ReportQuestion
from category.serializer import CategorySerializer


class CreateQuestionSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    text = serializers.CharField()
    correct_answer = serializers.CharField()
    mistake_answer_1 = serializers.CharField()
    mistake_answer_2 = serializers.CharField()
    mistake_answer_3 = serializers.CharField()

    def user_data(self, obj):
        return {
            'email': obj.user.email,
            'username': obj.user.username
        }
    user = serializers.SerializerMethodField('user_data')

    def create(self, validated_data):
        user = self.context['request'].user
        question = Question.objects.create(
            user=user,
            category=validated_data['category'],
            text=validated_data['text'],
            correct_answer=validated_data['correct_answer'],
            mistake_answer_1=validated_data['mistake_answer_1'],
            mistake_answer_2=validated_data['mistake_answer_2'],
            mistake_answer_3=validated_data['mistake_answer_3']
        )
        return question

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['category'] = CategorySerializer(instance.category).data
        return res


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def user_data(self, obj):
        return {
            'email': obj.user.email,
            'username': obj.user.username
        }
    category = CategorySerializer()
    user = serializers.SerializerMethodField('user_data')


class ReportQuestionSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )
    report = serializers.CharField()

    def create(self, validated_data):
        report_create = ReportQuestion.objects.create(
            question=validated_data['question'],
            report=validated_data['report']
        )
        return report_create
