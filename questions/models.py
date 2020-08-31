from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count

from config.base import VOTE_DOWN, VOTE_UP

User = get_user_model()


VOTE_CHOICES = ((VOTE_UP, "Vote Up"), (VOTE_DOWN, "Vote Down"))


class AbstactPost(models.Model):
    """
    Abstract model that defines common fields and methods
    for Question / Answer models.
    """
    
    class Meta:
        abstract = True
        ordering = ["-date_publication"]

    vote_class = None
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s",
    )
    description = models.TextField(blank=False)
    date_publication = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


    def change_vote(self, user, value):
        """Add, cancel, delete vote to current rating."""

        try:
            current = self.vote_class.objects.get(to=self, author=user)
        except ObjectDoesNotExist:
            self.vote_class.objects.create(to=self, author=user, value_vote=value)
            current = self.vote_class.objects.get(to=self, author=user)
            self.rating += value
            return self.rating

        if current.value_vote == value:
            return self.rating

        self.vote_class.objects.filter(to=self, author=user).delete()
        self.rating += value
        return self.rating


class AbstractVote(models.Model):
    """
    Abstract model that defines common fields and methods
    for QuestionVote / AnswerVote models.
    """

    class Meta:
        abstract = True

    time_vote = models.DateField(auto_now=True)
    value_vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s",
    )


class QuestionVote(AbstractVote):
    to = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="votes",
        related_query_name="votes",
    )


class AnswerVote(AbstractVote):
    to = models.ForeignKey(
        "Answer",
        on_delete=models.CASCADE,
        related_name="votes",
        related_query_name="votes",
    )


class QuestionManager(models.Manager):
    def get_queryset(self):
        """ Returns annotated qweryset: answers_count."""
        queryset = super().get_queryset().annotate(
            answers_count=Count("answer")
        )
        return queryset


class Question(AbstactPost):
    vote_class = QuestionVote
    title = models.CharField(blank=False, max_length=256)
    tags = models.ManyToManyField("Tag", blank=True)

    objects = models.Manager()
    hewy = QuestionManager()

    def __str__(self):
        return self.title

    @classmethod
    def trending(cls, count = 10):
        """ Returns a query set of trending questions."""

        return cls.objects.order_by("-rating")[:count]

    def add_tags(self, tags):
        for tag in set(tags):
            try:
                tag = Tag.objects.get(name=tag)
            except ObjectDoesNotExist:
                tag = Tag.objects.create(name=tag)
            self.tags.add(tag)


class Answer(AbstactPost):
    vote_class = AnswerVote
    question = models.ForeignKey(
        Question,
        related_name="answer",
        on_delete=models.CASCADE,
    )
    is_accepted = models.BooleanField(default=False)


    def accepted(self):
        """Accept answer"""

        self.question.answer.update(is_accepted=False)
        self.is_accepted = True
        self.save(update_fields=["is_accepted"])


    def unaccepted(self):
        """Cansel answer"""

        self.is_accepted = False
        self.save(update_fields=["is_accepted"])

    def __str__(self):
        return self.question.title


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=15)

    def __str__(self):
        return self.name
