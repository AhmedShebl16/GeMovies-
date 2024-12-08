# Generated by Django 4.2.4 on 2024-02-07 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_terms_and_condition'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-date_joined', '-update_at'), 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Admin'), (1, 'Customer'), (2, 'Company'), (3, 'Other')], default=3, null=True, verbose_name='Role'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('is_superuser', True), ('role', 0)), ('is_superuser', False), _connector='OR'), name='superuser_must_be_admin', violation_error_message="Superusers must have the 'Admin' role."),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('terms_and_condition', True)), name='terms_and_conditions_must_be_true', violation_error_message='Our terms and condition must be accepted.'),
        ),
    ]