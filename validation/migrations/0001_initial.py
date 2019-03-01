# Generated by Django 2.1.2 on 2019-01-21 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ivoid', models.TextField()),
                ('url', models.TextField()),
                ('svc_type', models.TextField()),
                ('date', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('msg', models.TextField(blank=True, null=True)),
                ('section', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'errors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ivoid', models.TextField()),
                ('url', models.TextField()),
                ('title', models.TextField(blank=True, null=True)),
                ('short_name', models.TextField(blank=True, null=True)),
                ('date_insert', models.TextField(blank=True, null=True)),
                ('date_update', models.TextField(blank=True, null=True)),
                ('vor_status', models.TextField(blank=True, null=True)),
                ('vor_created', models.TextField(blank=True, null=True)),
                ('vor_updated', models.TextField(blank=True, null=True)),
                ('contact_name', models.TextField(blank=True, null=True)),
                ('contact_email', models.TextField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
                ('xsi_type', models.TextField(blank=True, null=True)),
                ('spec', models.TextField(blank=True, null=True)),
                ('specv', models.TextField(blank=True, null=True)),
                ('params', models.TextField(blank=True, null=True)),
                ('val_mode', models.TextField(blank=True, null=True)),
                ('result_vot', models.TextField(blank=True, null=True)),
                ('result_spec', models.TextField(blank=True, null=True)),
                ('nb_warn', models.IntegerField(blank=True, null=True)),
                ('nb_err', models.IntegerField(blank=True, null=True)),
                ('nb_fatal', models.IntegerField(blank=True, null=True)),
                ('days_same', models.IntegerField(blank=True, null=True)),
                ('nb_fail', models.IntegerField(blank=True, null=True)),
                ('provenance', models.TextField(blank=True, null=True)),
                ('standard_id', models.TextField(blank=True, null=True)),
                ('svc_type', models.TextField()),
            ],
            options={
                'db_table': 'services',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='services',
            unique_together={('ivoid', 'url')},
        ),
    ]
