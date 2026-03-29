from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import state


# snapshot
class FullSnapshotView(APIView):
    def get(self, request):
        return Response(state.get_state())


# section
class SectionView(APIView):
    VALID = {"meta", "pump", "ecg", "respiration", "vitals",
             "dialysate", "session", "fluid_balance", "events"}

    def get(self, request, section):
        if section not in self.VALID:
            return Response({"error": "unknown section"}, status=status.HTTP_404_NOT_FOUND)
        snap = state.get_state()
        return Response({section: snap.get(section)})


# stream chunk
class WaveChunkView(APIView):
    def get(self, request):
        chunk = state.generate_wave_chunk(n=int(request.query_params.get("n", 25)))
        return Response(chunk)
