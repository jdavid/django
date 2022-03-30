{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
kill -TERM `cat {{ file_pid }}`
