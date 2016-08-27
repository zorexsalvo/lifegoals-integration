from api.serializers import WalletSerializer
from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging
import requests


class WalletDetail(APIView):
    def post(self, request):
        access_token = request.data['access_token']
        type = request.data['type']

        if type == 'COINS':
            url = 'https://coins.ph/api/v3/crypto-accounts'
            headers = {'Authorization': 'Bearer {}'.format(access_token)}

            r = requests.get(url, headers=headers)
            try:
                wallet_detail = r.json()['crypto-accounts'][0]
                serializer = WalletSerializer(wallet_detail)
                return Response(serializer.data)
            except KeyError as e:
                logging.error(str(e))
                return Response(r.json())


