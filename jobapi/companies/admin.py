from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from unicodedata import category

from companies.models import Category, Company, Job, Tag, Comment, User
from django.contrib import admin
from django.urls import path

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class JobForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Job
        fields = '__all__'

class MyJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_date']
    search_fields = ['name', 'salary', 'address']
    list_filter = ['id', 'created_date']
    list_editable = ['name']
    readonly_fields = ['image_view']
    form = JobForm

    def image_view(self, job):
        if job:
            return mark_safe(f"<img src='/static/{job.image.name}' width='200' />")

    class Media:
        css = {
            'all': ('/static/css/styles.css', )
        }


class MyAdminSite(admin.AdminSite):
    site_header = 'JOB24h'

    def get_urls(self):
        return [path('company-stats/', self.company_stats), path('job-stats1/', self.job_stats1), ] + super().get_urls()

    def company_stats(self, request):
        stats = Category.objects.annotate(company_count = Count('company__id')).values('id', 'name', 'company_count')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })

    def job_stats1(self, request):
        stats1 = Tag.objects.annotate(job_count = Count('job__id')).values('id', 'name', 'job_count')
        return TemplateResponse(request, 'admin/stats1.html', {
            'stats1': stats1
        })





    # def get_urls(self):
    #     return [path('job-stats/', self.job_stats), ] + super().get_urls()
    #
    # def job_stats(self, request):
    #     stats = .objects.annotate(job_count = Count('job__id')).values('id', 'name', 'job_count')
    #     return TemplateResponse(request, 'admin/stats.html', {
    #         'stats': stats
    #     })


admin_site = MyAdminSite(name='ViecLam')



admin_site.register(Category)
admin_site.register(Company)
admin_site.register(Job, MyJobAdmin)
admin_site.register(Tag)
admin_site.register(Comment)


#
# admin_site.register(Post)
admin_site.register(User, UserAdmin)

