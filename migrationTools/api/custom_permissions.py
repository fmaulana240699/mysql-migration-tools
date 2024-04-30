from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
   def has_permission(self, request, view):
      if request.user.role == "Admin":
         return True
      return False

class IsViewer(BasePermission):
   def has_permission(self, request, view):
      if request.user.role == "Viewer":
         return True
      return False