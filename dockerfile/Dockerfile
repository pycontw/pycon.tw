FROM python:3.6
##Install nodejs with n
RUN curl -o- -sL https://git.io/n-install | bash -s -- -q
RUN $HOME/n/bin/n 9
##Install yarn
RUN curl -o- -L https://yarnpkg.com/install.sh | bash
##Clone pycontw
WORKDIR /opt
RUN git clone https://github.com/pycontw/pycon.tw.git -b 2019-dev
##Install dependency
WORKDIR pycon.tw
RUN  /bin/bash -c "source ~/.bashrc && pip install -r requirements.txt && yarn install --dev"
WORKDIR src
RUN cp pycontw2016/settings/local.sample.env pycontw2016/settings/local.env
##Replace django seceret key
##you con use http://www.miniwebtool.com/django-secret-key-generator/ to generate new seceret key
##RUN sed -i 's:{{ secret_key }}:{django key you generated}:g' pycontw2016/settings/local.env
RUN sed -i 's:{{ secret_key }}:abvv7p_@am%65!p3$p8o8pk7fa4h(+su8(owx&#q@$t@54pjs8:g' pycontw2016/settings/local.env
RUN python manage.py migrate
EXPOSE 8000