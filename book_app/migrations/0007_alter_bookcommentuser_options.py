# Generated by Django 4.2.5 on 2023-10-02 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0006_bookcommentuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookcommentuser',
            options={'verbose_name': 'Комментарий к книге', 'verbose_name_plural': 'Комментарии к книгам'},
        ),
    ]