from rest_framework import serializers

class WalletSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    total_received = serializers.DecimalField(decimal_places=3, max_digits=9)
    currency = serializers.CharField(max_length=100)
    default_address = serializers.CharField(max_length=100)
    balance = serializers.DecimalField(decimal_places=3, max_digits=9)
    id = serializers.CharField(max_length=200)
    pending_balance = serializers.DecimalField(decimal_places=3, max_digits=9)

