from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, Template

class Templater:
    def __init__(self, template: Template, is_prod_template: bool):
        self.template: Template = template
        self.is_prod: bool = is_prod_template

    def render(self, template_data: Dict[str, str]) -> str:
        rendered_template = self.template.render(template_data)
        return rendered_template
    
    def write_template(self, rendered_template: str, output_directory: str):

        output_file_path = self.get_output_file_path(output_directory=output_directory)
        
        with open(output_file_path, "w") as f:
            f.write(rendered_template)
    
    def get_output_file_path(self, output_directory: str):

        output_file_path = f"{output_directory}"

        if self.is_prod_template():
            output_file_path = f"{output_file_path}/prod/prod.yml"
        else:
            output_file_path = f"{output_file_path}/lower/lower.yml"

        return output_file_path

    def is_prod_template(self) -> bool:
        return self.is_prod

    @staticmethod
    def new(environments: List[str]):
        is_prod_template = False
        if "prod" in environments:
            template_path = "templates/prod_inventory.yml.jinja"
            is_prod_template = True
        else:
            template_path = "templates/lower_inventory.yml.jinja"

        env = Environment(loader=FileSystemLoader('./'))
        template: Template = env.get_template(template_path)

        return Templater(template=template, is_prod_template=is_prod_template)

