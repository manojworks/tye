# Generated by Django 3.1.4 on 2021-01-04 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('taxonomy_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('product_description', models.CharField(max_length=200)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='taxonomy.taxonomy')),
            ],
        ),
    ]
