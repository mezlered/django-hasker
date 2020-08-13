from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Question, Answer, VOTE_CHOICES


MAX_COUNT_POST_TAGS = 3
MAX_LENGTH_POST_TAGS = 15

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("description",)


class SearchForm(forms.Form):
    search_ = forms.CharField(max_length = 254)


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=254, required=False)

    class Meta:
        model = Question
        fields = ("title", "description",)

    def clean_title(self):
        title = self.cleaned_data["title"]

        try:
            Question.objects.get(title__iexact=title.strip())
        except ObjectDoesNotExist:
            return title
        raise forms.ValidationError(
            "A topic with the same name already exists.")

    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        tags = [tag.lower().strip() for tag in tags.split(',') if tag]

        if len(tags) > MAX_COUNT_POST_TAGS:
            raise forms.ValidationError(
                f"You cannot post more than {MAX_COUNT_POST_TAGS} tags")

        if tags and max(map(len, tags)) > MAX_LENGTH_POST_TAGS:
            raise forms.ValidationError(
                f"Maximum tag length no more than {MAX_LENGTH_POST_TAGS} characters")

        return tags


class VoteForm(forms.Form):
    target_id = forms.IntegerField()
    value = forms.TypedChoiceField(choices=VOTE_CHOICES, coerce=int)
