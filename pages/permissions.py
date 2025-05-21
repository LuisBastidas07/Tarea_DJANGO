from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios de un libro editarlo o eliminarlo.
    Los administradores tienen acceso total.
    """
    def has_permission(self, request, view):
        # Permitir métodos de solo lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        # Si el usuario es admin, tiene todos los permisos
        if request.user and request.user.is_staff:
            return True
        # Si el usuario está autenticado, puede crear/editar
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Si el usuario es admin, tiene todos los permisos
        if request.user and request.user.is_staff:
            return True
        # Permitir métodos de solo lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        # Los permisos de escritura solo están permitidos al propietario del libro
        return obj.owner == request.user
