# Generated by Django 4.0.1 on 2022-02-14 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_accounticons_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
    ]