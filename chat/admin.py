from django.contrib import admin
from .models import Contact,  Conversation,  Message, ChatRoom


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'profile', 'phone_number']
    list_edit = ['user', 'profile', 'phone_number']
    search_fields = ['user__username', 'phone_number']
    list_filter = ['user__first_name', 'user__username']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id',   'started_at']
    filter_horizontal = ('participants',)
    search_field = ['participants__contact__user__username', 'groups__name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation',  'sender', 'timestamp', 'message', 'message']
    search_fields = ['message', 'sender__user__username', 'conversation__chat__name']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_on']
    filter_horizontal = ('members',)
    list_editable = ['name']
    search_fields = ['name']








