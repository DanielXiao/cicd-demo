#!/usr/bin/python
import sys
import logging
import time

import yaml
from shellutil import shell


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                           '%(message)s', level=logging.DEBUG)
LOG = logging.getLogger(__name__)


def deploy_guestbook(template, name, image_url):
    obj_config = template.format(suffix=name, image_url=image_url)
    file_name = 'guestbook-%s.yaml' % name
    with open(file_name, 'w') as fh:
        fh.write(obj_config)
    LOG.info('Generated guest book configuration file: %s', file_name)
    LOG.info('Start to create service frontend-%s', name)
    shell.local('kubectl create -f %s' % file_name, raise_error=True)
    time.sleep(90)
    while True:
        out = shell.local('kubectl get svc -o yaml -l app=guestbook-%s'
                          % name)[1]
        svc = yaml.load(out)
        lb = svc['items'][0]['status']['loadBalancer']
        ext_lb = None
        if 'ingress' in lb:
            for ingress in lb['ingress']:
                if ingress['ip'].startswith('10.111.108'):
                    ext_lb = ingress['ip']
                    LOG.info('External lb of frontend-%s: %s', name, ext_lb)
                    break
        if ext_lb:
            break
        LOG.info('External lb of frontend-%s is not ready', name)
        time.sleep(15)


def main():
    if len(sys.argv) < 4:
        print 'Usage: python deploy_gb.py <template path> <name> ' \
              '<image url>'
        sys.exit(1)
    with open(sys.argv[1]) as fh:
        template = fh.read()
    name = sys.argv[2]
    image_url = sys.argv[3]
    deploy_guestbook(template, name, image_url)


if __name__ == '__main__':
    main()