#!/usr/bin/python

from pathlib import Path
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec = dict(
            base=dict(type=str, required=True),
            dirs=dict(type=list, required=True),
            name=dict(type=str, required=True),
            dest=dict(type=str, required=True),
        )
    )

    base = module.params['base']
    dirs = module.params['dirs'] # ['mods/admin', 'mods/dotenv', 'mods/sendfile', 'mods/vite']
    name = module.params['name'] # urls.py
    dest = module.params['dest']

    base = Path(base)

    out = []
    for subdir in dirs:
        filepath = base / subdir / name
        if filepath.exists():
            out.append(subdir)

    # Ok
    module.exit_json(changed=False, ansible_facts={dest: out})


if __name__ == '__main__':
    main()
