import os
import json
from jsonschema import validate as validate_json

class Config:
    _settings = None
    _schema = None
    _base_dir = os.path.dirname(os.path.abspath(__file__))   

    @classmethod
    def __load_defaults(cls):
        if cls._settings is None:     
            settings_file_path = os.path.join( cls._base_dir, "data", "settings.json" )
            if os.path.isfile(settings_file_path):
                with open(settings_file_path, "r") as file:
                    settings = json.load(file)
            cls._settings = settings
        cls.__validate()

    @classmethod
    def update(cls, **kwargs):
        cls.__load_defaults( )
        cls._settings.update( kwargs )
        cls.__validate()

    @classmethod
    def get(cls, key, default=None):
        cls.__load_defaults( )
        return cls._settings.get(key, default)

    @classmethod
    def all(cls):
        cls.__load_defaults( )
        return cls._settings

    @classmethod
    def __validate( cls ):
        try:
            schema_file_path = os.path.join( cls._base_dir, "data", "schema.json" )

            # Load settings from JSON file if it exists, otherwise use default settings
            if cls._schema is None and os.path.isfile(schema_file_path):
                with open(schema_file_path, "r") as file:
                    cls._schema = json.load(file)

            # Validate the JSON object against the schema
            validate_json(instance=cls._settings, schema=cls._schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            sys.exit(f"Invalid settings. Exiting the behave test runner. Validation Error: {err.message}")
        return False