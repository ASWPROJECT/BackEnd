# Generated by Django 4.1.7 on 2023-03-21 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_issue_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='Priority',
            field=models.CharField(blank=True, choices=[('Low', 'Low'), ('Normal', 'Normal'), ('High', 'High')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='Severity',
            field=models.CharField(blank=True, choices=[('Wishlist', 'Wishlist'), ('Minor', 'Minor'), ('Normal', 'Normal'), ('Important', 'Important'), ('Critical', 'Critical')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='Type',
            field=models.CharField(blank=True, choices=[('Bug', 'Bug'), ('Question', 'Question'), ('Enhancement', 'Enhancement')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='Status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('In progress', 'In progress'), ('Ready for test', 'Ready for test'), ('Closed', 'Closed'), ('Needs info', 'Needs info'), ('Rejected', 'Rejected'), ('Posponed', 'Rejected')], max_length=50, null=True),
        ),
    ]
