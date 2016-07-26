# -*- coding:utf-8 -*-

import unicodecsv as csv
import json
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models.aggregates import Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import render
from django.template import RequestContext
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from equipment.models import *


def equip_csv(request):
    equipment_code = request.GET.get('equipment_code')
    state_code = request.GET.get('state_code')
    project_code = request.GET.get('project_code')
    user_name = request.GET.get('user_name')

    kwargs = {}
    if equipment_code:
        kwargs.__setitem__('equipment_code__exact', equipment_code)
    if state_code:
        kwargs.__setitem__('state_code__exact', state_code)
    if project_code:
        kwargs.__setitem__('history__project_id__exact', project_code)
    if user_name:
        kwargs.__setitem__('history__user_name__contains', user_name)

    latest_equipment_list = Equipment.objects.all().filter(**kwargs).annotate(max_id=Max('history__end_ymd')).order_by(
        'registered_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response, encoding='utf-8')
    writer.writerow(['자산분류', '제조사', '모델번호', '시리얼번호', '취득가격', '취득일', '폐기(예정)일', '상태', '사용자', '사용종료(예정)일'])
    if latest_equipment_list:
        for equip in latest_equipment_list:
            last_user_name = ''
            last_user_ymd = ''

            for history in equip.history_set.iterator():
                if equip.max_id == history.end_ymd:
                    last_user_name = history.user_name
                    last_user_ymd = history.end_ymd
            writer.writerow([equip.equipment_code.code_name,
                             equip.manufacturer_code.code_name, equip.model_no,
                             equip.serial_no, equip.purchase_price, equip.purchase_ymd, equip.discard_ymd,
                             equip.state_code.code_name, last_user_name, last_user_ymd])
    return response


# @csrf_exempt
def equip_list(request, template='equipment/equip_list.html', page_template='equipment/equip_list_page.html'):
    equipment_code = request.GET.get('equipment_code')
    state_code = request.GET.get('state_code')
    project_code = request.GET.get('project_code')
    user_name = request.GET.get('user_name')
    type_list = Code.objects.filter(code_category_id=1).all()
    state_list = Code.objects.filter(code_category_id=3).all()
    project_list = Project.objects.all().order_by('start_ymd')

    kwargs = {}
    if equipment_code:
        kwargs.__setitem__('equipment_code__exact', equipment_code)
    if state_code:
        kwargs.__setitem__('state_code__exact', state_code)
    if project_code:
        kwargs.__setitem__('history__project_id__exact', project_code)
    if user_name:
        kwargs.__setitem__('history__user_name__contains', user_name)

    total_count = Equipment.objects.all().filter(**kwargs).count()
    latest_equipment_list = Equipment.objects.all().filter(**kwargs).annotate(max_id=Max('history__end_ymd')).order_by(
        'registered_date')

    if request.is_ajax():
        template = page_template

    context = {'latest_equipment_list': latest_equipment_list,
               'total_count': total_count,
               'type_list': type_list,
               'state_list': state_list,
               'project_list': project_list,
               'entries': latest_equipment_list,
               'page_template': page_template,
               'request': request,
               }

    return render_to_response(template, context, context_instance=RequestContext(request))


def equip_addform(request):
    type_list = Code.objects.filter(code_category_id=1).all()
    manufacturer_list = Code.objects.filter(code_category_id=2).all()
    state_list = Code.objects.filter(code_category_id=3).all()
    context = {'type_list': type_list, 'manufacturer_list': manufacturer_list, 'state_list': state_list}
    return render(request, 'equipment/equip_addform.html', context)


# @csrf_exempt
def equip_add(request):
    equip = Equipment()
    equip.management_code = datetime.today().strftime("%Y%m%d%H%M%S")
    equip.equipment_code = Code.objects.get(id=int(request.POST.get('equipment_code')))
    equip.manufacturer_code = Code.objects.get(id=int(request.POST.get('manufacturer_code')))
    equip.state_code = Code.objects.get(id=int(request.POST.get('state_code')))
    equip.model_no = request.POST.get('model_no', '')
    equip.serial_no = request.POST.get('serial_no', '')
    equip.purchase_ymd = request.POST.get('purchase_ymd', '').replace('-', '')
    equip.purchase_price = request.POST.get('purchase_price', '')
    equip.discard_ymd = request.POST.get('discard_ymd', '').replace('-', '')
    equip.detail_info = request.POST.get('detail_info', '')
    equip.save()

    return HttpResponseRedirect(reverse('equipment:equip_view', args=(equip.id,)))


def equip_view(request, sid):
    equipment = get_object_or_404(Equipment, pk=sid)
    return render(request, 'equipment/equip_view.html', {'equipment': equipment})


def equip_updform(request, sid):
    type_list = Code.objects.filter(code_category_id=1).all()
    manufacturer_list = Code.objects.filter(code_category_id=2).all()
    state_list = Code.objects.filter(code_category_id=3).all()
    equipment = get_object_or_404(Equipment, pk=sid)

    context = {'type_list': type_list, 'manufacturer_list': manufacturer_list, 'state_list': state_list, 'equipment': equipment}

    return render(request, 'equipment/equip_updform.html', context)


# @csrf_exempt
def equip_upd(request):
    if request.method != 'POST':
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    sid = request.POST.get('equipment_id')

    if sid != '0':
        equip = Equipment.objects.get(id=sid)
    else:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    try:
        equip.equipment_code = Code.objects.get(id=int(request.POST.get('equipment_code')))
        equip.manufacturer_code = Code.objects.get(id=int(request.POST.get('manufacturer_code')))
        equip.state_code = Code.objects.get(id=int(request.POST.get('state_code')))
        equip.model_no = request.POST.get('model_no', '')
        equip.serial_no = request.POST.get('serial_no', '')
        equip.purchase_ymd = request.POST.get('purchase_ymd', '').replace('-', '')
        equip.purchase_price = request.POST.get('purchase_price', '')
        equip.discard_ymd = request.POST.get('discard_ymd', '').replace('-', '')
        equip.detail_info = request.POST.get('detail_info', '')
        equip.save()

        return HttpResponseRedirect(reverse('equipment:equip_view', args=(sid,)))
    except:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)


def to_json(objs, status=200):
    json_str = json.dumps(objs, ensure_ascii=False)
    return HttpResponse(json_str, status=status, content_type='application/json; charset=utf-8')


def serialize(objs):
    return map(lambda x: x.serialize(), objs)


def equip_history_view(request, sid):
    project_list = Project.objects.all().order_by('start_ymd')
    serial = []

    if project_list:
        for p in project_list:
            serial.append(p.serialize())

    if sid != '0':
        history = get_object_or_404(History, pk=sid)
        return to_json({'history': history.serialize(), 'project_list': serial})
    else:
        return to_json({'history': {}, 'project_list': serial})


# @csrf_exempt
def equip_history_upd(request, sid):
    if request.method != 'POST':
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    if sid != '0':
        history = History.objects.get(id=sid)
    else:
        history = History()

    try:
        history.equipment = Equipment.objects.get(id=int(request.POST.get('equipment_id')))
        history.user_name = request.POST.get('user_name', '')
        history.start_ymd = request.POST.get('start_ymd', '').replace('-', '')
        history.end_ymd = request.POST.get('end_ymd', '').replace('-', '')
        history.project = Project.objects.get(id=int(request.POST.get('project_id')))
        history.save()
        return to_json({'status': 'create success'})
    except:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)


def code_updform(request, sid):
    code_category_list = CodeCategory.objects.all().order_by('category_name')
    serial = []

    if code_category_list:
        for p in code_category_list:
            serial.append(p.serialize())

    if sid != '0':
        code = get_object_or_404(Code, pk=sid)
        return to_json({'code': code.serialize(), 'code_category_list': serial})
    else:
        return to_json({'code': {}, 'code_category_list': serial})


# @csrf_exempt
def code_upd(request):

    if request.method != 'POST':
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    sid = request.POST.get('modal_code_id')

    if sid != '0':
        code = Code.objects.get(id=sid)
    else:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    try:
        code.code_category = CodeCategory.objects.get(id=int(request.POST.get('modal_code_category_id')))
        code.code_name = request.POST.get('modal_code_name')
        code.save()
        return to_json({'status': 'create success'})
    except:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)


# @csrf_exempt
def code_add(request):
    code = Code()
    code.code_category = CodeCategory.objects.get(id=int(request.POST.get('code_category_id')))
    code.code_name = request.POST.get('code_name', '')
    code.save()

    return HttpResponseRedirect(reverse('equipment:code_list', args=()))


def code_addform(request):
    code_category_list = CodeCategory.objects.all()
    context = {'code_category_list': code_category_list}
    return render(request, 'equipment/code_addform.html', context)


# @csrf_exempt
def code_list(request, template='equipment/code_list.html', page_template='equipment/code_list_page.html'):

    code_category_list = CodeCategory.objects.all()
    code_category_id = request.GET.get('code_category_id')
    code_name = request.GET.get('code_name')

    kwargs = {}
    if code_category_id:
        kwargs.__setitem__('code_category_id__exact', code_category_id)
    if code_name:
        kwargs.__setitem__('code_name__contains', code_name)

    total_count = Code.objects.all().filter(**kwargs).count()
    list = Code.objects.all().filter(**kwargs).order_by('code_category__category_name', 'code_name')

    if request.is_ajax():
        template = page_template

    context = {'list': list,
               'total_count': total_count,
               'code_category_list': code_category_list,
               'page_template': page_template,
               'request': request,
               }

    return render_to_response(template, context, context_instance=RequestContext(request))


# @csrf_exempt
def pjt_list(request, template='equipment/pjt_list.html', page_template='equipment/pjt_list_page.html'):
    project_name = request.GET.get('project_name')

    kwargs = {}
    if project_name:
        kwargs.__setitem__('project_name__contains', project_name)

    total_count = Project.objects.all().filter(**kwargs).count()
    list = Project.objects.all().filter(**kwargs).order_by('-end_ymd')

    if request.is_ajax():
        template = page_template

    context = {'list': list,
               'total_count': total_count,
               'page_template': page_template,
               'request': request,
               }

    return render_to_response(template, context, context_instance=RequestContext(request))


def pjt_addform(request):
    context = {'null': {}}
    return render(request, 'equipment/pjt_addform.html', context)


# @csrf_exempt
def pjt_add(request):
    project = Project()

    project.project_name = request.POST.get('project_name', '')
    project.start_ymd = request.POST.get('start_ymd', '').replace('-', '')
    project.end_ymd = request.POST.get('end_ymd', '').replace('-', '')
    project.save()

    return HttpResponseRedirect(reverse('equipment:pjt_list', args=()))


def pjt_updform(request, sid):

    if sid != '0':
        project = get_object_or_404(Project, pk=sid)
        return to_json({'project': project.serialize()})
    else:
        return to_json({'project': {}})


# @csrf_exempt
def project_upd(request):
    if request.method != 'POST':
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    sid = request.POST.get('modal_project_id')

    if sid != '0':
        project = Project.objects.get(id=sid)
    else:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)

    try:
        project.project_name = request.POST.get('modal_project_name')
        project.start_ymd = request.POST.get('modal_start_ymd').replace('-', '')
        project.end_ymd = request.POST.get('modal_end_ymd').replace('-', '')
        project.save()
        return to_json({'status': 'create success'})
    except:
        resp = {
            'status': 'bad request'
        }
        return to_json(resp, 400)
