import uuid
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Poll(models.Model):
    STATUS_CHOICES = (
        ("ready", "ativo"),
        ("draft", "rascunho"),
    )
    DURATION_CHOICES = (
        ("1d", "1 dia"),
        ("7d", "7 dias"),
        ("0d", "indeterminado"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    question = models.CharField(max_length=256, null=False)
    description = models.CharField(max_length=256, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_polls"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="categorized_polls"
    )
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="ready")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "enquete"
        verbose_name_plural = "enquetes"
        ordering = ("-created_at",)

    def __str__(self):
        return self.question


class Choice(models.Model):
    text = models.CharField(max_length=256)
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="poll_choices"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "escolha"
        verbose_name_plural = "escolhas"
        ordering = ("-poll",)

    def __str__(self):
        return self.text


class Vote(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="poll_votes"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="choice_votes"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "voto"
        verbose_name_plural = "votos"
        ordering = ("-created_at",)
        unique_together = ("owner", "poll")

    def __str__(self):
        return f"{self.choice}: {self.poll}"

