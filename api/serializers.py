from rest_framework import serializers
from care.models import Category, Download


class CategorySerializer(serializers.ModelSerializer):
	download = DownloadSerializer(many=True)(many=True)

	class Meta:
		model = Category
		fields = ('category_name',)

class CategorySerializer(serializers.ModelSerializer):
	download = serializers.RelatedField(many=True)

	class Meta:
		model = Category
		fields = ('category_name',)


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title')

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')