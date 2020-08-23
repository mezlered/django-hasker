from django.contrib.auth import get_user_model
from rest_framework import serializers

from questions.models import Answer, AnswerVote, Question, QuestionVote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class QuestionSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = [
            'date_publication',
            'rating',
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        new_question = super().create(validated_data)
        new_question.add_tags(tags)
        return new_question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = [
            'author',
            'is_accepted',
            'posted',
            'question',
            'rating',
        ]


class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = [
            'author',
            'content',
            'description',
            'question',
            'rating',
        ]


class QuestionVoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuestionVote
        exclude = ['to']
        read_only_fields = [
            'user',
        ]

    def validate(self, data):
        question_pk = self.context['view'].kwargs['pk']
        user = self.context['request'].user

        if QuestionVote.objects.filter(to=question_pk, author=user).exists():
            raise serializers.ValidationError('Vote already exists.')
        return data


class AnswerVoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnswerVote
        exclude = ['to']
        read_only_fields = [
            'user',
        ]

    def validate(self, data):
        answer_pk = self.context['view'].kwargs['pk']
        user = self.context['request'].user

        if AnswerVote.objects.filter(to=answer_pk, author=user).exists():
            raise serializers.ValidationError('Vote already exists.')
        return data
