from rest_framework import permissions

class IsCompanyRecuiter(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and request.user.type == 'RECUITER'):
            return False
        return hasattr(request.user, 'Recuiter')
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.company == request.user.recuiter.company
    
