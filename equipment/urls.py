from django.conf.urls import patterns, url 
from equipment import views

urlpatterns = [
    url(r'^equip/list/$', views.equip_list, name='equip_list'),
    url(r'^equip/addform/$', views.equip_addform, name='equip_addform'),
    url(r'^equip/add/$', views.equip_add, name='equip_add'),
    url(r'^equip/view/(?P<sid>\d+)/$', views.equip_view, name='equip_view'),
    url(r'^equip/updform/(?P<sid>\d+)/$', views.equip_updform, name='equip_updform'),
    url(r'^equip/upd/$', views.equip_upd, name='equip_upd'),
    url(r'^equip/history/view/(?P<sid>\d+)/$', views.equip_history_view, name='equip_history_view'),
    url(r'^equip/history/upd/(?P<sid>\d+)/$', views.equip_history_upd, name='equip_history_upd'),
    url(r'^equip/csv/$', views.equip_csv, name='equip_csv'),

    url(r'^code/list/$', views.code_list, name='code_list'),
    url(r'^code/addform/$', views.code_addform, name='code_addform'),
    url(r'^code/add/$', views.code_add, name='code_add'),
    url(r'^code/updform/(?P<sid>\d+)/$', views.code_updform, name='code_updform'),
    url(r'^code/upd/$', views.code_upd, name='code_upd'),

    url(r'^pjt/list/$', views.pjt_list, name='pjt_list'),
    url(r'^pjt/addform/$', views.pjt_addform, name='pjt_addform'),
    url(r'^pjt/add/$', views.pjt_add, name='pjt_add'),
    url(r'^pjt/updform/(?P<sid>\d+)/$', views.pjt_updform, name='pjt_updform'),
    url(r'^pjt/upd/$', views.project_upd, name='project_upd'),
]
