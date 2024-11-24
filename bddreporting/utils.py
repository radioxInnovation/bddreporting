import os
from jinja2.sandbox import SandboxedEnvironment
from jinja2 import DictLoader, FileSystemLoader, ChoiceLoader
import yaml
import pypandoc
import sys
import logging
from .config import Config
from datetime import datetime

def extract_multiline_string(arr):
    arr = arr if arr else []
    in_multiline = False
    result = []

    for line in arr:
        # Check for the first """
        if '"""' in line and not in_multiline:
            in_multiline = True
            result.append(line.split('"""', 1)[-1])  # Append content after """
        # Check for the second """
        elif '"""' in line and in_multiline:
            result.append(line.split('"""', 1)[0])  # Append content before """
            break  # Stop after the second """
        # Collect the lines between the """
        elif in_multiline:
            result.append(line)

    # Join the result lines into a single string
    return "\n".join(result).strip()

def applyJinja2Template(template_str, context_dict = {}):
    # Dictionary loader for the provided template string
    string_loader = DictLoader({
        'input_template': template_str
    })

    # Create a sandboxed Jinja2 environment with both loaders (string and file-based templates)
    env = SandboxedEnvironment(
        loader=ChoiceLoader([string_loader])
    )

    # Load the input template from the string loader
    template = env.get_template('input_template')

    # Render the template with the provided context dictionary
    try:
        rendered_content = template.render(context_dict)
        return rendered_content
    except Exception as e:
        loggig.error(f"An error occurred during template rendering: {e}")
        return ""

def write_text( text, filename, feature_name, scenario_name, tags):

    if len( text ) > 0:
        feature_file_directory = os.path.dirname( filename )
        feature_file_directory = os.path.abspath(feature_file_directory)

        path_dict = { "filename": os.path.basename( filename ), "feature": feature_name, "scenario": scenario_name }

        report_dir = applyJinja2Template( Config.get("report_dir", "reports" ), path_dict )    

        directory_path = os.path.join(feature_file_directory, report_dir )

        os.makedirs( directory_path, exist_ok=True )

        # Convert tags to lowercase
        lower_tags = [tag.lower() for tag in tags]

        # Filter valid formats based on the tags
        known_formats = Config.get("formats", {} ).keys()
        valid_formats = [ext for ext in known_formats if ext.lower() in lower_tags]

        if len( valid_formats ) == 0:
            default_formats = Config.get("default_formats", [])
            for f in default_formats:
                if f in known_formats:
                    valid_formats.append( f )

        for ext in valid_formats:
            output_file = os.path.join( directory_path, applyJinja2Template( Config.get("report_file_basename", "{{scenario}}"), path_dict ) + "." + ext )
            format_dict = Config.get("formats", {})
            format_data = format_dict[ext]

            module_name = format_data.get( "module", False )

            if not module_name:
                # no module, use pypandoc
                front_matter = parse_front_matter( text )
                extra_args = format_data["extra_args"]
                to = format_data.get("to", ext )

                if front_matter and "extra_args" in front_matter:
                    extra_args = front_matter.get("extra_args", [])

                try:
                    original_working_directory = os.getcwd()
                    os.chdir( feature_file_directory )
                    output = pypandoc.convert_text(text, to, format='md', extra_args = extra_args, outputfile = output_file )
                    os.chdir( original_working_directory )
                except Exception as e:
                    logging.error("Failed to generate report: %s", e)
            else:
                module_dir = format_data.get( "dir", False )
                if module_dir and module_dir not in sys.path:
                    sys.path.append( module_dir ) 

                import importlib

                try:
                    module = importlib.import_module( module_name )
                    logging.debug(f"Successfully imported module '{module_name}' for format '{ext}'.")
                except ImportError as e:
                    logging.warning(f"Could not import module '{module_name}' for format '{ext}': {e}")
                    module = None

                try:
                    if module:
                        module.convert( text, output_file, **format_data )
                except ImportError as e:
                    logging.warning(f"Could call convert function of module: '{module_name}' for format '{ext}': {e}")

        if len ( valid_formats ) == 0:
            # Create file path for the scenario log
            log_file_path = os.path.join( directory_path, f"{scenario_name}.md" )

            # Write the log content to the file
            with open(log_file_path, "w", encoding="utf-8") as log_file:
                log_file.write( text.strip() )

def parse_front_matter(content):
    try:
        if content.startswith("---"):
            end_of_front_matter = content.find("---", 3)
            if end_of_front_matter != -1:
                yaml_header = content[3:end_of_front_matter].strip()
                
                # Parse the YAML header
                front_matter_data = yaml.safe_load(yaml_header)
                return front_matter_data
    except:
        pass

    return None

def get_current_date_time():
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')  # Standard date format
    current_time = now.strftime('%H-%M-%S')  # Replace colons with dashes
    return current_date, current_time