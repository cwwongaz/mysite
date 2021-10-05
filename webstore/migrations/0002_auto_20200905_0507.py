# Generated by Django 3.0.8 on 2020-09-05 05:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_price',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='item',
            name='picture',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='item_Description',
            field=models.TextField(max_length=5000),
        ),
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rater', models.ManyToManyField(related_name='user_rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='rating',
            field=models.ManyToManyField(blank=True, related_name='item', to='webstore.rating'),
        ),
    ]
