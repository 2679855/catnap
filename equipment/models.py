from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CodeCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):  # __str__ on Python 3
        return str(self.id) + ' ' + self.category_name

    def serialize(self):
        data = {
            'id': self.id,
            'category_name': self.category_name,
        }
        return data


class Code(models.Model):
    code_category = models.ForeignKey(CodeCategory)
    code_name = models.CharField(max_length=100)

    def __unicode__(self):  # __str__ on Python 3
        return str(self.id) + ' ' + self.code_name

    def serialize(self):
        data = {
            'id': self.id,
            'category_id': self.code_category_id,
            'category_name': self.code_category.category_name,
            'code_name': self.code_name,
        }
        return data


class Equipment(models.Model):
    management_code = models.CharField(max_length=14, unique=True, help_text='yyyymmddhhmiss')
    equipment_code = models.ForeignKey(Code, related_name='equipment_code')
    model_no = models.CharField(max_length=200)
    serial_no = models.CharField(max_length=200, unique=True)
    purchase_ymd = models.CharField(max_length=10)
    purchase_price = models.IntegerField()
    discard_ymd = models.CharField(max_length=10)
    manufacturer_code = models.ForeignKey(Code, related_name='manufacturer_code')
    detail_info = models.TextField(blank=True)
    state_code = models.ForeignKey(Code, related_name='state_code')
    registered_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # __str__ on Python 3
        return self.model_no + ' : ' + self.serial_no


class Project(models.Model):
    project_name = models.CharField(max_length=200, unique=True)
    start_ymd = models.CharField(max_length=8)
    end_ymd = models.CharField(max_length=8)
    registered_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # __str__ on Python 3
        return self.project_name

    def serialize(self):
        data = {
            'id': self.id,
            'project_name': self.project_name,
            'start_ymd': self.start_ymd,
            'end_ymd': self.end_ymd,
        }
        return data


class History(models.Model):
    equipment = models.ForeignKey(Equipment)
    user_name = models.CharField(max_length=100)
    start_ymd = models.CharField(max_length=8)
    end_ymd = models.CharField(max_length=8)
    project = models.ForeignKey(Project)
    registered_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # __str__ on Python 3
        return self.user_name

    def serialize(self):
        data = {
            'id': self.id,
            'user_name': self.user_name,
            'start_ymd': self.start_ymd,
            'end_ymd': self.end_ymd,
            'registered_date': self.registered_date.__str__(),
            'equipment_name': self.equipment.__str__(),
            'project_name': self.project.project_name,
            'project_id': self.project_id,
        }
        return data
