from .models import Question


COUNT_QUESTIONS = 10


class TredingMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["trending"] = Question.trending(count=COUNT_QUESTIONS)
        return context