from rest_framework import serializers
from .models import Producto, Usuario, Mascota, ArticuloInformativo, SolicitudAdopcion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ArticuloInformativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloInformativo
        fields = '__all__'

class SolicitudAdopcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudAdopcion
        fields = '__all__'
