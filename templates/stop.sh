{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
kill -TERM `cat {{ supervisord_pidfile }}`
