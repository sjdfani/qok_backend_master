# Generated by Django 4.0.1 on 2022-02-14 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_remove_account_point_alter_account_image'),
        ('question', '0004_rename_question_question_text_remove_question_status_and_more'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ended', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[('in_challenge', 'In challenge'), ('end_challenge', 'End challenge')], max_length=15)),
                ('account_1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_account_1', to='account.account')),
                ('account_2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_account_2', to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeCategory_CATEGORY', to='category.category')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeCategory_CHALENGE', to='challenge.challenge')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeCategory_accountBy', to='account.account')),
                ('question_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeCategory_question_1', to='question.question')),
                ('question_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeCategory_question_2', to='question.question')),
                ('question_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeCategory_question_3', to='question.question')),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=250)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeAnswer_account', to='account.account')),
                ('challenge_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeAnswer_CHALENGE_CATEGORY', to='challenge.challengecategory')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeAnswer_question', to='question.question')),
            ],
        ),
    ]
