#!/usr/bin/python

from pathlib import Path
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec = dict(
            base=dict(),
            path=dict(required=True),
        )
    )

    base = module.params['base']
    path = Path(module.params['path'])

    if base:
        path = Path(base) / path
    
    realpath = str(path.resolve())

    # Ok
    module.exit_json(changed=False, realpath=realpath)


if __name__ == '__main__':
    main()
