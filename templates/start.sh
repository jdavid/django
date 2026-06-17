{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{{ django_root }}/ansible/rotate-logs.sh || true
{{ dir_bin }}/supervisord -c {{ dir_etc }}/supervisor.conf
{{ django_root }}/ansible/rotate-logs.sh --compress || true
