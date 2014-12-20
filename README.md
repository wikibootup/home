Homepage for see
=======
```
It's the hompage for 'see'
```
- 서버는 기본적으로 자동으로 실행되도록 설정을 해두었습니다. ( /etc/init/wsgi.conf ) 
  하지만 어떤 이유로 당장 자동실행이 안될 경우 아래 방법으로 수동 실행 가능합니다.


* 서버를 수동으로 켜는 방법

 * 1. nginx + uwsgi를 이용한 실행 
```
$ uwsgi --wsgi-file /home/seebuntu/github/home/seeseehome/seeseehome/wsgi.py --http-socket 0.0.0.0:80
```

 * 2. apache2 + django app을 이용한 실행 
```
$ ~/github/home/seeseehome
$ ./manage.py runserver 0.0.0.0:80 --insecure
```
( * 만약 ssh로 접속 중이라면  $ screen 을 먼저 입력하시기 바랍니다. )
