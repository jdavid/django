#!/usr/bin/python


from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True),
            dest=dict(),
        )
    )

    name = module.params['name']
    dest = module.params['dest']
    if dest is None:
        dest = name

    rc, out, err = module.run_command(['which', name])
    out = out.strip()

    module.exit_json(changed=False, ansible_facts={dest: out})


if __name__ == '__main__':
    main()
