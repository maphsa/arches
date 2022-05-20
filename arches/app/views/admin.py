"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from arches.app.utils.decorators import group_required
from arches.app.utils.index_database import index_resources_by_type
from arches.app.utils.response import JSONResponse
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from django.shortcuts import redirect
from arches.app.models import models
from arches.app.models.system_settings import settings
from django.core.exceptions import PermissionDenied


@method_decorator(group_required("Graph Editor"), name="dispatch")
class ReIndexResources(View):
    def post(self, request):
        data = JSONDeserializer().deserialize(request.body)
        index_resources_by_type(data["graphids"], clear_index=False, batch_size=4000, quiet=True)
        return JSONResponse(data)


class FileView(View):
    def get(self, request, fileid=None):
        file = models.File.objects.get(pk=fileid)
        path = file.path.url
        if settings.RESTRICT_MEDIA_ACCESS:
            permission = request.user.has_perm("read_nodegroup", file.tile.nodegroup)
            permitted = permission is None or permission is True
            if permitted:
                return redirect(path)
            else:
                raise PermissionDenied()
        return redirect(path)
