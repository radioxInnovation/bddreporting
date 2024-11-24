import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup
from functools import wraps
import logging
from datetime import datetime
from behave.model_core import Status
from .utils import applyJinja2Template, get_current_date_time
from .config import Config

def report(template = None, filename = None):
    def decorator(func):
        @wraps(func)
        def wrapper(context, *args, **kwargs):
            result = None
            try:
                # Call the original function
                result = func(context, *args, **kwargs)
            except:
                pass

            # Log the doc string if needed after successful execution
            report_tag = Config.get("report_tag", "report")
            if not report_tag or report_tag in context.scenario.tags:
                doc_string_to_log( context, func, args, kwargs, template, filename )
            return result
        return wrapper
    return decorator

def doc_string_to_log(context, func,  args, kwargs, template, filename):
    text = ""
    scenario = context.scenario

    if Config.get("process_gherkin_doc_string", True) and hasattr(context, 'text') and isinstance(context.text, str) and context.text:
        # use Jinja2 template
        try:
            current_date, current_time = get_current_date_time()
            rendered_content = applyJinja2Template(context.text, { "scenario": scenario.name , "feature": scenario.feature.name, "date": current_date, "time": current_time } )            
            logging.info(f"Template rendered successfully.")
            text += rendered_content + "\n" * 2

        except Exception as e:
            pass

    # pocess the python step definition
    if template:
        template_text = str( template )
    elif filename:
        full_path = os.path.join( scenario.feature.feature_file_abspath , filename)
        if os.path.exists( full_path ):
            with open(full_path, 'r', encoding='utf-8') as file:
                template_text = file.read()
        else:
            template_text = f"**missing template file: {full_path}**"
    elif inspect.getdoc(func):
        # Get the docstring of the function
        template_text = inspect.getdoc(func)
    else:
        template_text = ""
        for step in context.scenario.steps:
            if step.status == Status.untested:
                with open( os.path.join( scenario.feature.feature_file_abspath, os.path.basename(step.filename)), "r", encoding="utf-8") as file:                                
                    lines = file.read().splitlines()
                    words = lines[step.line - 1].split()
                    template_text = " ".join(words[1:])
                    break

    if template_text:
        lookup = TemplateLookup(directories=[scenario.feature.feature_file_abspath])
        template = Template( template_text, lookup=lookup )
        if "id" in kwargs.keys():
            id_parameter = kwargs["id"] 
            logging.warning("step contains id parameter {id_parameter}. This conficts with auto generated step id: {context.current_step_id}")
        render_args = { "id": context.current_step_id } | kwargs
        if hasattr(context, "report") and isinstance(context.report, dict) and context.report:
            render_args = render_args | {"report": context.report }
        rendered_content = template.render(**render_args)
        text += rendered_content + "\n"
        
    if len( text ) > 0:
        if not hasattr(context, 'log'):
            context.log = ""
        context.log += text + "\n"
