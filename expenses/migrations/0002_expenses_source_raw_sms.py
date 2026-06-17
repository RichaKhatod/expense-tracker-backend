from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='source',
            field=models.CharField(
                choices=[('manual', 'Manual'), ('sms', 'SMS')],
                default='manual',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='expenses',
            name='raw_sms',
            field=models.TextField(blank=True, null=True),
        ),
    ]
