from typing import Dict
from jinja2 import Environment, FileSystemLoader, Template

class Templater:
    def __init__(self, template: Template):
        self.template: Template = template

    def render(self, template_data: Dict[str, str]):
        foo = self.template.render(template_data)
        print(foo)

    @staticmethod
    def new(template_path: str):
        env = Environment(loader=FileSystemLoader('./'))
        template: Template = env.get_template(template_path)

        return Templater(template)

