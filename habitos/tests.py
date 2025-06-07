from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from habitos.models import Habito, Stats

class HabitoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ari', password='123456')
        self.outro_user = User.objects.create_user(username='joao', password='123456')
        self.client.login(username='ari', password='123456')

    def test_criar_habito(self):
        response = self.client.post('/habito/', {
            'titulo': 'Beber água',
            'descricao': 'Beber 2L por dia'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habito.objects.count(), 1)
        habito = Habito.objects.first()
        self.assertEqual(habito.responsavel, self.user)
        self.assertFalse(habito.concluida)

    def test_concluir_habito(self):
        habito = Habito.objects.create(
            titulo='Meditar',
            descricao='10 minutos por dia',
            responsavel=self.user
        )
        response = self.client.patch(f'/habito/{habito.id}/concluir/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habito.refresh_from_db()
        self.assertTrue(habito.concluida)

        stats = Stats.objects.get(usuario=self.user)
        self.assertEqual(stats.streak, 1)
        self.assertGreater(stats.percentual_conclusao_mes, 0)

    def test_concluir_habito_de_outro_usuario(self):
        habito = Habito.objects.create(
            titulo='Ler',
            descricao='15 minutos de leitura',
            responsavel=self.outro_user
        )
        response = self.client.patch(f'/habito/{habito.id}/concluir/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        habito.refresh_from_db()
        self.assertFalse(habito.concluida)

    def test_stats_criado_automaticamente(self):
        self.assertEqual(Stats.objects.filter(usuario=self.user).count(), 0)
        self.client.post('/habito/', {
            'titulo': 'Estudar',
            'descricao': 'Estudar Python'
        })
        self.client.patch('/habito/1/concluir/')
        self.assertEqual(Stats.objects.filter(usuario=self.user).count(), 1)