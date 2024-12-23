# Generated by Django 5.1.4 on 2024-12-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0003_auto_20241223_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='correo',
        ),
        migrations.AddField(
            model_name='estudiante',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='curso',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='Inscripcion',
        ),
    ]
