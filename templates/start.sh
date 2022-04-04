{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{{ dir_bin }}/gunicorn -c {{ dir_etc }}/gunicorn.conf.py
