from core.models import CompareProduto
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class ProdutTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.compare_url = reverse("token_obtain_pair")

        self.user_data = {
            "preco_produto": "R$ 100,00",
            "promocao": "False",
            "loja": "Kanui",
            "Produto": "camisa",
        }

        return super().setUp()

    def test_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_compare(self):
        response = self.client.post(self.register_url, self.user_data)

        response = self.client.post(
            self.compare_url,
            {
                "produto": self.user_data["produto"],
                "loja": self.user_data["loja"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_produto(self):
        response = self.client.post(self.produto_url, self.compare_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_produto(self):
        self.test_create_produto()

        response = self.client.get(self.produto_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_details_produto(self):
        produto = CompareProduto.objects.create(**self.produto_data)
        response = self.client.get(self.employee_url + str(produto.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_produto(self):
        produto = CompareProduto.objects.create(**self.produto_data)
        response = self.client.put(
            self.produto_url + str(produto.id) + "/", self.produto_data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_produto(self):
        produto = CompareProduto.objects.create(**self.produto_data)
        response = self.client.delete(self.produto_url + str(produto.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

