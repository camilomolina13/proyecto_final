# Generated by Django 3.1.12 on 2024-12-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0002_curso_inscripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
