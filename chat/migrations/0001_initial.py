# Generated by Django 5.1.2 on 2024-10-30 17:55

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ImageField(default='images/placeholder.jfif', upload_to='images/')),
                ('phone_number', models.CharField(blank=True, default='images/placeholder.jfif', max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(related_name='chat_rooms', to='chat.contact')),
            ],
            options={
                'verbose_name': 'Chat Room',
                'verbose_name_plural': 'Chat Rooms',
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='chat.chatroom')),
                ('participants', models.ManyToManyField(related_name='conversations', to='chat.contact')),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
                'ordering': ['-started_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('message_type', models.CharField(choices=[('private', 'Private'), ('group', 'Group'), ('public', 'Public')], default='public', max_length=10)),
                ('conversation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.conversation')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.contact')),
            ],
            options={
                'verbose_name': 'Messages',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]