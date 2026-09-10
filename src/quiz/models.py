from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name="Exam"
    )
    text = models.CharField(max_length=500, verbose_name="Question Text")

    class Meta:
        ordering = ['id']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f"{self.exam.title} - {self.text[:30]}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='choices', 
        verbose_name="Question"
    )
    text = models.CharField(max_length=200, verbose_name="Choice Text")
    is_correct = models.BooleanField(default=False, verbose_name="Is Correct")

    class Meta:
        ordering = ['id']
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    def __str__(self):
        return f"{self.question.text[:20]} - {self.text}"