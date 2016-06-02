# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-02 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('projects', '0045_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('color', models.CharField(blank=True, max_length=9, null=True, verbose_name='color')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('modified_date', models.DateTimeField(verbose_name='modified date')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items_tags', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ['project', 'name', 'id'],
            },
        ),
        migrations.CreateModel(
            name='TaggedRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_relations', to='tagging.Tag', verbose_name='tag')),
            ],
            options={
                'verbose_name_plural': 'tagged_relations',
                'verbose_name': 'tagged_relation',
                'ordering': ['tag', 'content_type', 'object_id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='tag',
            index_together=set([('project', 'name')]),
        ),
    ]
