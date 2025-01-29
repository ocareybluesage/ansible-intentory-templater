from typing import Dict
from jinja2 import Environment, FileSystemLoader, Template

class Templater:
    def __init__(self, template: Template):
        self.template: Template = template

    def render(self, template_data: Dict[str, str]) -> str:
        rendered_template = self.template.render(template_data)
        return rendered_template
    
    def write_template(self, rendered_template: str, output_file_path: str):
        
        with open(output_file_path, "w") as f:
            f.write(rendered_template)

    @staticmethod
    def new(template_path: str):
        env = Environment(loader=FileSystemLoader('./'))
        template: Template = env.get_template(template_path)

        return Templater(template)

