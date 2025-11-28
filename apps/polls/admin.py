from django.contrib import admin

from .models import Category, Choice, Poll, Vote


class ChoiceModelAdmin(admin.ModelAdmin):
    list_display = ["text", "poll"]


class PollModelAdmin(admin.ModelAdmin):
    list_display = ["question", "owner", "created_at", "status"]


class VoteModelAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "owner", "created_at"]


admin.site.register(Category)
admin.site.register(Choice, ChoiceModelAdmin)
admin.site.register(Poll, PollModelAdmin)
admin.site.register(Vote, VoteModelAdmin)
