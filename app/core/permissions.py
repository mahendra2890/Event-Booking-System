# permissions.py

from rest_framework import permissions

class IsEventOrganizer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow any user to create an event
        if request.method == 'POST':
            return True
        # Restrict other actions to event organizers
        return obj.organizer == request.user

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'customer'




# from rest_framework import permissions

# class IsEventOrganizer(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Check if the user is an organizer for the given event
#         return obj.organizer.user == request.user

# class IsTicketBooker(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Check if the user is the one who made the booking for the ticket
#         return obj.customer.user == request.user
