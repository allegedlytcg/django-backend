# Generated by Django 3.0.1 on 2019-12-28 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodPressure',
            fields=[
                ('bpId', models.AutoField(primary_key=True, serialize=False)),
                ('dPressure', models.IntegerField()),
                ('sPressure', models.IntegerField()),
                ('heartRate', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'BloodPressure post',
                'verbose_name_plural': 'BloodPressure posts',
            },
        ),
    ]
