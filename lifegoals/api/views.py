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


class FundTransfer(APIView):
    def get_account(self, access_token):
        url = 'https://coins.ph/api/v3/crypto-accounts'
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        r = requests.get(url, headers=headers)
        try:
            wallet_detail = r.json()['crypto-accounts'][0]
            logging.error(wallet_detail)
            logging.error(wallet_detail.get('id'))
            return wallet_detail.get('id')
        except KeyError:
            logging.error('Account ID not found.')

    def post(self, request):
        access_token = request.data['access_token']
        amount = request.data['amount']
        target_address = request.data['target_address']
        type = request.data['type']

        url = 'https://coins.ph/api/v3/transfers/'
        headers = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Accept': 'application/json'
                  }

        if type == 'COINS':
            account = self.get_account(access_token)
            body = json.dumps({
                                'account': account,
                                'target_address': target_address,
                                'amount': amount
                             })
            r = requests.post(url, data=body, headers=headers)
            return Response(r.json())
        raise Http404
