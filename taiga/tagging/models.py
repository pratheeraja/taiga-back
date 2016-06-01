# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from hashlib import sha1


def generate_color(tag_name):
    return "#{}".format(sha1(tag_name.encode("utf-8")).hexdigest()[0:6])


class Tag(models.Model):
    name = models.CharField(null=False, blank=False, max_length=128, verbose_name=_("name"))
    color = models.CharField(max_length=9, null=True, blank=True, verbose_name=_("color"))
    project = models.ForeignKey("projects.Project", null=True, blank=True, related_name="items_tags",
                                verbose_name=_("project"))

    created_date = models.DateTimeField(null=False, blank=False, default=timezone.now,
                                        verbose_name=_("created date"))
    modified_date = models.DateTimeField(null=False, blank=False, verbose_name=_("modified date"))

    _importing = None

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        unique_together = (("project", "name"),)
        index_together = ("project", "name")
        ordering = ["project", "name", "id"]

    def __str__(self):
        return "[{}]".format(self.name)

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = generate_color(self.name)

        if not self._importing or not self.modified_date:
            self.modified_date = timezone.now()

        return super().save(*args, **kwargs)


class TaggedRelation(models.Model):
    tag = models.ForeignKey("tagging.Tag", null=False, blank=False, related_name="tagged_relations",
                            verbose_name=_("tag"))

    content_type = models.ForeignKey(ContentType, null=False, blank=False, verbose_name=_("content type"))
    object_id = models.PositiveIntegerField(null=False, blank=False, verbose_name=_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")

