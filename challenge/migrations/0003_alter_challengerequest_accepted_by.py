# Generated by Django 4.0.1 on 2022-02-14 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_accounticons_name'),
        ('challenge', '0002_challengeanswer_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengerequest',
            name='accepted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ChallengeReq_accepted_by', to='account.account'),
        ),
    ]