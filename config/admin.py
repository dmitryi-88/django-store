from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = 'Панель управления Django Store'
    site_title = 'Django Store'
    index_title = 'Управление проектом'