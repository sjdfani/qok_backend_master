# Generated by Django 4.0.1 on 2022-02-09 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_remove_question_reports_reportquestion_question_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='question',
            name='status',
        ),
        migrations.AddField(
            model_name='question',
            name='state',
            field=models.CharField(choices=[('accept', 'Accept'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='reportquestion',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='question.question'),
        ),
    ]