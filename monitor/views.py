from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import access, state
from .role import get_role
from .role_config import DOCTOR_SECTIONS


# dashboard (role-shaped)
class DashboardView(APIView):
    """
    Replaces "/snapshot", role based dashboard-payload.

    Returns {"role": <role>, "data": {...}} where the contents of
    'data' depend on the callers role.
    """

    def get(self, request):
        role = get_role(request)
        return Response(access.build_dashboard_payload(role))



'''
# snapshot (replaced it with 'dashboard')
class FullSnapshotView(APIView):
    def get(self, request):
        role = get_role(request)
        snap = state.get_state()
        if role == "doctor":
            snap = {k: snap[k] for k in DOCTOR_SECTIONS if k in snap}
        return Response(snap)

'''



# section
class SectionView(APIView):
    VALID = {"meta", "pump", "ecg", "respiration", "vitals",
             "dialysate", "session", "fluid_balance", "events"}

    def get(self, request, section):
        if section not in self.VALID:
            return Response(
                {"error": "unknown section"},
                status=status.HTTP_404_NOT_FOUND,
            )

        role = get_role(request)
        if not access.is_section_allowed(role, section):
            return Response(
                {"error": "not permitted for this role"},
                status=status.HTTP_403_FORBIDDEN,
            )

        snap = state.get_state()
        return Response({section: snap.get(section)})


# stream chunk
class WaveChunkView(APIView):
    def get(self, request):
        role = get_role(request)
        if role != "technician":
            return Response(
                {"error": "not permitted for this role"},
                status=status.HTTP_403_FORBIDDEN,
            )
        chunk = state.generate_wave_chunk(
            n=int(request.query_params.get("n", 25))
        )
        return Response(chunk)
