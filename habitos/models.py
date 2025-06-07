from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Habito(models.Model):
    titulo = models.CharField(max_length=100, blank=False)
    concluida = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Stats(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    streak = models.IntegerField(default=0, null=False)
    percentual_conclusao_mes = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.percentual_conclusao_mes}% concluído no mês"