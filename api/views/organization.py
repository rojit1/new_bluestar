from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.serializers.organization import BranchSerializer, OrganizationSerializer

from organization.models import Branch, Organization


class OrganizationApi(ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.active()

    def list(self, request, *args, **kwargs):
        instance = Organization.objects.last()
        serializer_data = self.get_serializer(instance).data
        return Response(serializer_data)


class BranchApi(ReadOnlyModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.active()
