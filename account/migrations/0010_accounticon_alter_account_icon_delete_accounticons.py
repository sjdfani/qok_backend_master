# Generated by Django 4.0.1 on 2022-02-16 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_rename_uploaded_accounticons_uploaded_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='icons/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Icon',
            },
        ),
        migrations.AlterField(
            model_name='account',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.accounticon'),
        ),
        migrations.DeleteModel(
            name='AccountIcons',
        ),
    ]
