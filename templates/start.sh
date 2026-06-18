{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{{ dir_bin }}/supervisord -c {{ dir_etc }}/supervisor.conf
