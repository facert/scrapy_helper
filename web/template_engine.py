# -*- coding: utf-8 -*-
import os
import zipfile
import shutil
from mako.template import Template
from django.conf import settings


def add_zipfile(source_dir, output_filename):
    f = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()


class BaseTemplate(object):

    def __init__(self, template_name, output_name, template_dir="source/templates", output_dir="outputs"):
        self.template = Template(filename=os.path.join(settings.BASE_DIR, template_dir, template_name))
        self.output_filename = os.path.join(settings.BASE_DIR, output_dir, output_name)

    def render(self, *args, **kwargs):
        with open(self.output_filename, "w+") as f:
            f.write(self.template.render(**kwargs))


class CrawlTemplate(BaseTemplate):

    def render(self, *args, **kwargs):
        super(CrawlTemplate, self).render(*args, **kwargs)


def _generate_crawl_template(project, rule_fields):
    t = CrawlTemplate(template_name="scrapy.cfg.tpl", output_name="scrapy.cfg", output_dir="outputs/"+project.md5)
    t.render(**{"project_name": project.name})

    t = CrawlTemplate(template_name="template/settings.py.tpl", output_name=project.name+"/settings.py", output_dir="outputs/"+project.md5)
    t.render(**{"project": project})

    t = CrawlTemplate(template_name="template/items.py.tpl", output_name=project.name+"/items.py", output_dir="outputs/"+project.md5)
    t.render(**{"rule_fields": rule_fields})

    t = CrawlTemplate(template_name="template/spiders/template.py.tpl", output_name=project.name+"/spiders/"+project.name+".py", output_dir="outputs/"+project.md5)
    t.render(**{"rule_fields": rule_fields, "project": project})

    t = CrawlTemplate(template_name="template/pipelines.py.tpl", output_name=project.name+"/pipelines.py", output_dir="outputs/"+project.md5)
    t.render(**{"rule_fields": rule_fields, "project": project})

    t = CrawlTemplate(template_name="template/middlewares/useragent_middleware.py.tpl", output_name=project.name+"/middlewares/useragent_middleware.py", output_dir="outputs/"+project.md5)
    t.render()
    t = CrawlTemplate(template_name="scripts.py.tpl", output_name="scripts.py", output_dir="outputs/"+project.md5)
    t.render(**{"project": project})


def generate_crawl(project, rule_fields, output_dir="outputs"):
    project_md5_dir = os.path.join(settings.BASE_DIR, output_dir, project.md5)
    if os.path.exists(project_md5_dir):
        shutil.rmtree(project_md5_dir)
    path_dir = os.path.join(project_md5_dir, project.name)
    if os.path.exists(path_dir):
        shutil.rmtree(path_dir)
    os.makedirs(path_dir)
    os.makedirs(os.path.join(path_dir, "spiders"))
    os.makedirs(os.path.join(path_dir, "middlewares"))
    open(os.path.join(path_dir, "__init__.py"), "w").close()
    open(os.path.join(path_dir, "middlewares", "__init__.py"), "w").close()
    open(os.path.join(path_dir, "spiders", "__init__.py"), "w").close()
    _generate_crawl_template(project, rule_fields)

    add_zipfile(os.path.join(output_dir, project.md5), project_md5_dir+".zip")






