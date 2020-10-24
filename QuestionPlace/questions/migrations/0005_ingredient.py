# Generated by Django 3.1.2 on 2020-10-24 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_passage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField()),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unity', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='questions.question')),
            ],
        ),
    ]
