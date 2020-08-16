from rest_framework import serializers


class FilteredListSerializerByUser(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(user=self.context.get('request').user)
        return super(FilteredListSerializerByUser, self).to_representation(data)
