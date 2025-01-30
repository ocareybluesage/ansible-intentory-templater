from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, Template
from src import OUTPUT_DIR, is_prod

class Templater:
    def __init__(self, template: Template):
        self.template: Template = template

    def render(self, template_data: Dict[str, str]) -> str:
        rendered_template = self.template.render(template_data)
        return rendered_template
    
    def write_template(self, rendered_template: str, client_name):

        output_file_path = self.get_output_file_path(client_name=client_name)
        
        with open(output_file_path, "w") as f:
            f.write(rendered_template)
    
    def get_output_file_path(self, client_name: str):

        env = "lower"
        if "prod" in self.template.filename:
            env = "prod"

        output_file_path = f"{OUTPUT_DIR}/{env}/01-{client_name}.yml"

        return output_file_path

    @staticmethod
    def new(environments: List[str]):
        env = "lower"
        if is_prod(environments):
            env = "prod"

        template_path = f"templates/{env}_inventory.yml.jinja"
        environment = Environment(loader=FileSystemLoader('./'))
        template: Template = environment.get_template(template_path)

        return Templater(template=template)

