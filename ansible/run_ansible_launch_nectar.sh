#!/bin/bash
. ./openrc.sh; ansible-playbook -i hosts --ask-become-pass run_nectar.yaml -e'ansible_python_interpreter=/usr/bin/python3'