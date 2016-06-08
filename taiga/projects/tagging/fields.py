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

from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from taiga.base.api import serializers


from django.core.exceptions import ValidationError


class TagsAndTagsColorsField(serializers.WritableField):
    """
    Pickle objects serializer fior stories, tasks and issues tags.
    """
    def __init__(self, *args, **kwargs):
        def _validate_tag_field(value):
            for tag in value:
                if isinstance(tag, str):
                    continue
                if isinstance(tag, (list, tuple)) and len(tag) == 2:
                    continue
                raise ValidationError(_("Invalid tag '{value}'. It must be the name or a pair "
                                        "'[\"name\", \"hex color\"]'.").format(value=tag))

        super().__init__(*args, **kwargs)
        self.validators.append(_validate_tag_field)

    def to_native(self, obj):
        return obj

    def from_native(self, data):
        # The supported imput to this field is:
        #   - ['tag1', 'tag2', 'tag3'] -> ['tag1', 'tag2', 'tag3']
        #   - ['tag1', 'tag2,tag3'] -> ['tag1', 'tag2', 'tag3']
        #   - ['tag1', ['tag2', '#ffffff'], 'tag3'] -> ['tag1', ['tag2', '#ffffff'], 'tag3']
        if not data:
            return data

        ret = []
        for tag in data:
            if isinstance(tag, str):
                ret += tag.split(",")
            else:
                ret.append(tag)

        return ret


class TagsField(serializers.WritableField):
    """
    Pickle objects serializer for tags names.
    """
    def __init__(self, *args, **kwargs):
        def _validate_tag_field(value):
            for tag in value:
                if isinstance(tag, str):
                    continue
                raise ValidationError(_("Invalid tag '{value}'. It must be the tag name.").format(value=tag))

        super().__init__(*args, **kwargs)
        self.validators.append(_validate_tag_field)

    def to_native(self, obj):
        return obj

    def from_native(self, data):
        if not data:
            return data

        ret = sum([tag.split(",") for tag in data], [])

        return ret


class TagsColorsField(serializers.WritableField):
    """
    PgArray objects serializer.
    """
    widget = widgets.Textarea

    def to_native(self, obj):
        return dict(obj)

    def from_native(self, data):
        return list(data.items())
