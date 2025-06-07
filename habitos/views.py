from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import time
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Habito, Stats
from .serializer import UserSerializer, HabitoSerializer, StatSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class StatsViewset(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stats, created = Stats.objects.get_or_create(usuario=self.request.user)
        return Stats.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user, streak=0, percentual_conclusao_mes=0.00)


class HabitoViewSet(viewsets.ModelViewSet):
    queryset = Habito.objects.all()
    serializer_class = HabitoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], url_path='concluir')
    def concluir_habito(self, request, pk=None):
        habito = self.get_object()

        if habito.responsavel != request.user:
            return Response({'detail': 'Apenas o responsável pode concluir este hábito.'},
                            status=status.HTTP_403_FORBIDDEN)

        habito.concluida = True
        habito.data_conclusao = timezone.now()
        habito.save()

        stats, _ = Stats.objects.get_or_create(usuario=request.user)
        stats.streak += 1
        dias_do_mes = timezone.now().day
        stats.percentual_conclusao_mes = round((stats.streak / dias_do_mes) * 100, 2)
        stats.save()

        return Response({'detail': 'Hábito concluído com sucesso!'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='deletar')
    def deletar_habito(self, request, pk=None):
        habito = self.get_object()

        if habito.responsavel != request.user:
            return Response({'detail': 'Apenas o responsável pode deletar este hábito.'},
                            status=status.HTTP_403_FORBIDDEN)

        habito.delete()
        return Response({'detail': 'Hábito Deletado!'}, status=status.HTTP_200_OK)
