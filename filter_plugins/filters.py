#!/usr/bin/python3

import itertools

from ansible.errors import AnsibleFilterError

class FilterModule():
    ''' custom filter to check if something is a list '''

    def filters(self):
        return {
            'multiline_indent'  : self.multiline_indent,
            'strip_family'      : self.strip_family,
            'get_rule_names'    : self.get_rule_names,
        }

    def multiline_indent(self, obj, indent=1):
        """ fix jinja multiline indentation """
        out = ""

        if isinstance(obj, list):
            for x in obj:
                out += indent * 4 * ' ' + str(x) + '\n'
            return out

        return indent * 4 * ' ' + str(obj) + '\n'

    def strip_family(self, obj):
        """ strip family from nftable item """
        return obj.split(" ")[-1]

    def get_rule_names(self, obj):
        """ get rule names from nested nftables yaml """

        if not isinstance(obj, dict):
            raise AnsibleFilterError('This only works on dict')

        all_rules = []

        for table in obj:
            for _, rules in obj[table].get('chains').items():
                all_rules.append(rules)

        all_rules = list(itertools.chain(*all_rules))

        return all_rules
