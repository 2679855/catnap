# 개요
자산 관리 

# 프로젝트 사전 설정

## virtualenv 생성
requirements.txt 참조

## Django 프로젝트와 App 생성
- Project name: catnap
- App Name: equipment
- 샘플
```bash
django-admin startproject catnap
manage.py startapp equipment
manage.py migrate
manage.py createsuperuser
manage.py runserver 0.0.0.0:8000
manage.py makemigrations
manage.py migrate myapp 0001
```

## DB
기본 설정은 sqlite3 

## logging
logs 디렉토리 생성

# 실행
manage.py runserver 0.0.0.0:8000 --noreload
