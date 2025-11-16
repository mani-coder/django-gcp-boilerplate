# Generated migration to rename firebase_uid to workos_user_id

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firebase_uid',
            new_name='workos_user_id',
        ),
        migrations.RenameField(
            model_name='historicaluser',
            old_name='firebase_uid',
            new_name='workos_user_id',
        ),
    ]
