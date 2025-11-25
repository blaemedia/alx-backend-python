import django_filters
from django.db.models import Q
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    sender = django_filters.NumberFilter(field_name='sender__id')
    start_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')
    is_read = django_filters.BooleanFilter(field_name='is_read')
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'timestamp', 'is_read']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(content__icontains=value)

class ConversationFilter(django_filters.FilterSet):
    participant = django_filters.NumberFilter(method='filter_by_participant')
    search = django_filters.CharFilter(method='filter_search')
    is_group = django_filters.BooleanFilter(field_name='is_group')
    
    class Meta:
        model = Conversation
        fields = ['is_group']
    
    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(participants__id=value)
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(participants__username__icontains=value) |
            Q(participants__email__icontains=value)
        ).distinct()