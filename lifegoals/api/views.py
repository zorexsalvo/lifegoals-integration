from api.serializers import WalletSerializer
from api.config import CHANNEL_ID, CLIENT_ID, CLIENT_SECRET, LIFE_GOALS_ACCOUNT
from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging
import requests


class WalletDetail(APIView):
    def post(self, request):
        try:
            type = request.data['type']

            if type == 'COINS':
                access_token = request.data['access_token']
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

            elif type == 'UBANK':
                account_no = request.data['account_no']
                url = 'https://api.us.apiconnect.ibmcloud.com/ubpapi-dev/sb/api/RESTs/getAccount'

                headers = {
                    'x-ibm-client-id': CLIENT_ID,
                    'x-ibm-client-secret': CLIENT_SECRET,
                    'content-type': 'application/json',
                    'accept': 'application/json'
                    }

                account = {'account_no': account_no}

                r = requests.get(url, params=account, headers=headers)
                return Response(r.json())

            else:
                raise Http404
        except KeyError as e:
            logging.error(e)
            raise Http404


class FundTransfer(APIView):
    def get_account(self, access_token):
        url = 'https://coins.ph/api/v3/crypto-accounts'
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        r = requests.get(url, headers=headers)
        try:
            wallet_detail = r.json()['crypto-accounts'][0]
            return wallet_detail.get('id')
        except KeyError:
            logging.error('Account ID not found.')

    def post(self, request):
        try:
            type = request.data['type']

            if type == 'COINS':
                access_token = request.data['access_token']
                url = 'https://coins.ph/api/v3/transfers/'
                headers = {
                            'Authorization': 'Bearer {}'.format(access_token),
                            'Content-Type': 'application/json;charset=UTF-8',
                            'Accept': 'application/json'
                          }

                account = self.get_account(access_token)
                amount = request.data['amount']
                target_address = request.data['target_address']
                body = json.dumps({
                                    'account': account,
                                    'target_address': target_address,
                                    'amount': amount
                                 })
                r = requests.post(url, data=body, headers=headers)
                return Response(r.json())

            elif type == 'UBANK':
                amount = request.data['amount']
                source_account = request.data['source_address']
                target_account = request.data['target_address']
                transaction_id = request.data['transaction_id']

                url = 'https://api.us.apiconnect.ibmcloud.com/ubpapi-dev/sb/api/RESTs/transfer'
                headers = {
                    'x-ibm-client-id': CLIENT_ID,
                    'x-ibm-client-secret': CLIENT_SECRET,
                    'content-type': 'application/json',
                    'accept': 'application/json'
                }
                payload = {
                            'channel_id': CHANNEL_ID,
                            'transaction_id': transaction_id,
                            'source_account': source_account,
                            'source_currency': 'php',
                            'target_account': target_account,
                            'target_currency': 'php', 
                            'amount': amount
                          }
                r = requests.post(url, json=payload, headers=headers,)
                return Response(r.json())

            else:
                raise Http404
        except KeyError as e:
            logging.error(str(e))
            raise Http404
        

