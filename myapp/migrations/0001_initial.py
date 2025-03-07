# Generated by Django 5.0.6 on 2024-05-23 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=60)),
                ('lname', models.CharField(max_length=50)),
                ('mobile', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proname', models.CharField(max_length=60)),
                ('product_category', models.CharField(choices=[('Zigbee', 'Zigbee'), ('Wifi', 'Wifi'), ('Wired', 'Wired'), ('Security', 'Security'), ('Other', 'Other')], max_length=100)),
                ('qty', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('prodetail', models.TextField()),
                ('product_picture', models.ImageField(default='', upload_to='product_picture/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('mobile', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('usertype', models.CharField(default='staff', max_length=60)),
                ('profile_picture', models.ImageField(default='', upload_to='profile_picture/')),
            ],
        ),
    ]
