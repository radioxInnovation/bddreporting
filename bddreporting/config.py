import jsonschema
import sys
from jsonschema import validate as validate_json

class Config:
    _settings = {
        "report_tag": None,
        "report_dir": "reports/{{filename}}/",
        "report_file_basename": "{{scenario}}",
        "process_gherkin_doc_string": True,
        "scenario_header": "## {{scenario}}\n\n",
        "feature_header": "# {{feature}}\n\n",
        "export_scenario": False,
        "halt_execution_on_failure": False,
        "default_formats": [ "docx", "txt"],
        "formats": {
            "docx": {
                "extra_args": [
                    "--toc"
                ]
            },
            "pptx": {
                "extra_args": [
                    "--toc"
                ]
            },
            "html": {
                "extra_args": []
            },
            "md": {
                "extra_args": []
            },
            "txt": {
                "to": "plain",
                "extra_args": []
            }
        }
    }

    _schema = {
        "type": "object",
        "properties": {
            "report_tag": {
                "type": ["string", "null"],
                "description": "Tag used to identify reports. null means no filter, report every scenario"
            },
            "report_dir": {
                "type": "string",
                "description": "Directory where reports are stored"
            },
            "report_file_basename": {
                "type": "string",
                "description": "base name of a report file"
            },
            "process_gherkin_doc_string": {
                "type": "boolean",
                "description": "Flag to enable or disable processing of Gherkin doc strings"
            },
            "scenario_header": {
                "type": ["string", "boolean", "null"],
                "description": "Template for the scenario header"
            },
            "feature_header": {
                "type": ["string", "boolean", "null"],
                "description": "Template for the feature header"
            },
            "export_scenario": {
                "type": "boolean",
                "description": "export scenario"
            },
            "halt_execution_on_failure": {
                "type": "boolean",
                "description": "Flag to determine whether to exit on step failure"
            },
            "default_formats": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9_]+$"
                },
                "description": "Default formats, must be null or an array of strings matching the keys in the formats dictionary."
            },
            "formats": {
                "type": "object",
                "description": "Extra arguments for different formats.",
                "patternProperties": {
                    "^[a-zA-Z0-9_]+$": {
                    "type": "object",
                    "description": "Additional arguments for any format."
                    }
                }
            }
        },
        "required": [
            "report_tag",
            "report_dir",
            "process_gherkin_doc_string",
            "scenario_header",
            "halt_execution_on_failure",
            "default_formats",
            "formats"
        ],
        "additionalProperties": False
    }

    @classmethod
    def update(cls, **kwargs):
        cls._settings.update( kwargs )
        cls.__validate()

    @classmethod
    def get(cls, key, default=None):
        cls.__validate()
        return cls._settings.get(key, default)

    @classmethod
    def all(cls):
        cls.__validate()
        return cls._settings

    @classmethod
    def __validate( cls ):
        try:
            # Validate the JSON object against the schema
            validate_json(instance=cls._settings, schema=cls._schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            sys.exit(f"Invalid settings. Exiting the behave test runner. Validation Error: {err.message}")
        return False
