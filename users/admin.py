from django.contrib import admin
from users.models import Profile, Category, Relationship, Invitation

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class RelationshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(Relationship, RelationshipAdmin)

class InvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Invitation, InvitationAdmin)
