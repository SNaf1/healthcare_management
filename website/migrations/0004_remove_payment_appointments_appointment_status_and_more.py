# Generated by Django 4.2.7 on 2023-12-02 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_schedule_slot_alter_schedule_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='appointments',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='appointment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.appointment'),
        ),
    ]
