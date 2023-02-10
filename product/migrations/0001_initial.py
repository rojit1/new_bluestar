# Generated by Django 4.0.6 on 2022-07-22 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, verbose_name='Category Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Category Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Product Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Product Description')),
                ('is_taxable', models.BooleanField(default=True)),
                ('price', models.FloatField(default=0.0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/images/')),
                ('product_id', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productcategory')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
