#!/usr/bin/python

import os
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec = dict(
            base=dict(),
            name=dict(required=True),
            dest=dict(),
        )
    )

    base = module.params['base']
    name = module.params['name']
    dest = module.params['dest']
    if dest is None:
        dest = name

    if base:
        # Call which
        rc, out, err = module.run_command(['which', name])
        out = out.strip()
    else:
        # Use base directory directly
        out = os.path.join(base, name)

    # Ok
    module.exit_json(changed=False, ansible_facts={dest: out})


if __name__ == '__main__':
    main()
