# **`bddreporting` Overview**

`bddreporting` is a Python package designed to enhance Behavior-Driven Development (BDD) with [`behave`](https://github.com/behave/behave) by providing comprehensive logging and reporting tools. The package simplifies the process of generating detailed, customizable reports for each feature, scenario, and step execution.

---

## **Installation**

Install `bddreporting` directly from GitHub using the following command:

```bash
pip install git+https://github.com/radioxInnovation/bddreporting.git
```

---

## **Features**

- Automatically logs execution details at the feature, scenario, and step levels.
- Supports flexible log customization using decorators.
- Allows integration of log messages into feature files or step definitions.
- Enables template-based reporting with variable interpolation.

---

## **Setup**

### **Directory Structure of a Behave Project**

A typical `behave` project follows a standardized directory structure:

```
my_behave_project/
│
├── features/
│   ├── steps/                   # Contains step definitions
│   │   ├── __init__.py
│   │   ├── sample_steps.py
│   │
│   ├── environment.py           # Hooks for setup and teardown
│   ├── example.feature          # Feature files
│
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

- **Feature files (`*.feature`)**: Define the test cases in plain language.
- **Step files (`steps/*.py`)**: Contain the Python implementations of the steps.
- **`environment.py`**: Provides hooks to execute custom logic during test setup and teardown.

### **Setting Up `environment.py` with Decorators**

To use `bddreporting`, define hooks in `environment.py` for logging or additional setup. Below is a template demonstrating the available hooks:

```python
from bddreporting import before_feature, after_feature, before_step, after_step, before_scenario, after_scenario, Config

@before_feature
def before_feature(context, feature):
    """Logic to execute before a feature starts."""
    pass

@after_feature
def after_feature(context, feature):
    """Logic to execute after a feature finishes."""
    pass

@before_step
def before_step(context, step):
    """Logic to execute before a step starts."""
    pass

@after_step
def after_step(context, step):
    """Logic to execute after a step finishes."""
    pass

@before_scenario
def before_scenario(context, scenario):
    """Logic to execute before a scenario starts."""
    pass

@after_scenario
def after_scenario(context, scenario):
    """Logic to execute after a scenario finishes."""
    pass
```

Each hook receives `context` (shared across the tests) and the corresponding test artifact (e.g., `feature`, `scenario`, or `step`). This allows for fine-grained control of pre- and post-execution behaviors.

---

## **Step Definitions with Logging**

The `@report` decorator enables reporting for individual steps with flexible log generation options. Here's an example:

```python
import os
from bddreporting import report
from behave import step

@given('the test stand is turned on')
@report('some log text (option 1)')
def step_turn_on(context):
    pass

@when('the test is executed with "{frequency} Hz, amplitude {amplitude} mm, and duration {duration} seconds"')
@report()
def step_execute_test(context, frequency, amplitude, duration):
    """
    some log text (option 2)
    the frequency is ${frequency} 
    the time is: ${time}
    """
    pass

@then('test stand is turned off')
@report(filename="template.txt")
def step_turn_off(context):
    pass
```

### **Options for Log String Definitions in `@report`**

There are three main ways to define log strings in the `@report` decorator:

1. **Inline Definition**:
   - Define the log message directly within the decorator.
   - Example:
     ```python
     @report('Log: The test stand is turned on.')
     ```

2. **Docstring-Based Definition**:
   - Define the log message within the step’s docstring.
   - Variables from the step definition (e.g., `frequency`, `amplitude`, `duration`) and additional variables like `time` and `date` (from `context`) are available for interpolation.
   - Example:
     ```python
     """
     Executing the test:
     Frequency: ${frequency} Hz
     Time: ${time}
     """
     ```

3. **Template File**:
   - Reference an external template file using the `filename` parameter.
   - Example:
     ```python
     @report(filename="log_template.txt")
     ```

   The specified file can include placeholders for variables available in the `context` or step.

#### **Available Variables**

- **Step-Specific Variables**: Defined directly in the step definition, such as `frequency`, `amplitude`, and `duration`.
- **Global Variables**: Available globally in all steps:
  - `time`: Current time.
  - `date`: Current date.

---

## **Logging Directly from Feature Files**

`bddreporting` supports logging output directly from feature files using Jinja2 syntax for placeholders. 

### **Syntax for Placeholders**

- **Supported Placeholders**:
  - `{{time}}`: Inserts the current time.
  - `{{date}}`: Inserts the current date.
  
> **Note**: Unlike Mako templates used in step definitions, Jinja2 templates are used in feature files for security reasons, as they do not allow executable Python code.
> 
> **Note**: While feature files use [Jinja2 templates](https://jinja.palletsprojects.com/), step definitions leverage [Mako templates](https://www.makotemplates.org/) for enhanced functionality.


### **Example Feature File**

```gherkin
Feature: Execute breathing curves
  """
  This feature demonstrates the logging capabilities.
  """

  Scenario: Normal breathing curve
    """
    Normal breathing curve
    Date: {{date}}
    """

    Given the test stand is turned on

    When the test is executed with "0.25" Hz, amplitude "30" mm, and duration "8" seconds
    
    Then test stand is turned off
```

# **Configuration**

The `bddreporting.Config` class provides a flexible way to configure the behavior of the `bddreporting` library. It includes methods for updating, retrieving, and validating settings based on a predefined schema, ensuring robust and predictable functionality.

---

## **Methods**

1. **`Config.update(**kwargs)`**
   - Updates the configuration settings with the provided key-value pairs.
   - Automatically validates the new settings against the schema.

   **Example:**
   ```python
   Config.update(report_dir="reports/{{filename}}/")
   ```

2. **`Config.get(key, default=None)`**
   - Retrieves the value for a specified configuration key.
   - If the key does not exist, the provided default value is returned.

   **Example:**
   ```python
   report_dir = Config.get("report_dir")
   ```

3. **`Config.all()`**
   - Returns the complete configuration as a dictionary.

   **Example:**
   ```python
   settings = Config.all()
   ```

---

## **Configuration Options**

The following table summarizes the available configuration options, their purposes, and default values:

| **Key**                        | **Description**                                                                                         | **Default Value**               |
|--------------------------------|---------------------------------------------------------------------------------------------------------|----------------------------------|
| `report_tag`                   | A tag to filter scenarios for reporting. Use `null` to include all scenarios.                          | `None`                          |
| `report_dir`                   | Directory where reports are stored. Variables like `{{filename}}` can be used in the path.             | `reports/{{filename}}/`         |
| `report_file_basename`         | Base name for the report file. Variables like `{{scenario}}` are supported.                            | `{{scenario}}`                  |
| `process_gherkin_doc_string`   | Enables or disables processing of Gherkin doc strings.                                                 | `True`                          |
| `scenario_header`              | Template for the scenario header in the report. Use `null` to omit.                                    | `## {{scenario}}\n\n`           |
| `feature_header`               | Template for the feature header in the report. Use `null` to omit.                                     | `# {{feature}}\n\n`             |
| `export_scenario`              | Enables or disables scenario export in the report.                                                     | `False`                         |
| `halt_execution_on_failure`    | Halts execution of tests on the first step failure if set to `True`.                                   | `False`                         |
| `default_formats`              | Default output formats for reports. Must match keys in the `formats` dictionary.                      | `["docx", "txt"]`               |
| `formats`                      | Additional arguments for different output formats (e.g., `docx`, `pptx`, `html`).                     | See default schema below.       |

---

## **Default Formats Configuration**

The `formats` configuration allows customization for various output formats. The default configuration is as follows:

```json
"formats": {
    "docx": {
        "extra_args": ["--toc"]
    },
    "pptx": {
        "extra_args": ["--toc"]
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
```

- **Pandoc Integration**:  
  The library uses the **Pandoc** document converter to export reports to the desired formats. The `formats` dictionary defines the command-line options for Pandoc, ensuring compatibility with all supported formats.

- **Key Parameters**:
  - **`extra_args`**: A list of additional arguments specific to each format.
  - **`to`**: Specifies the target format explicitly (e.g., `"plain"` for `txt`).

---

# Custom Formats

In cases where conversion is not possible via [Pandoc](https://pandoc.org/), a custom converter can be implemented. Below is an example of a configuration for a custom format:

```json
{
    "formats": {
        "log": {
            "module": "custom_log",
            "dir": "formats"
        }
    }
}
```

- **`module`**: The name of the module that implements the custom converter (e.g., `custom_log`).
- **`dir`**: The directory where the module (e.g., `custom_log.py`) must be located.

The module must define a `convert` function using the following template:

```python
def convert(text, outputfile, **kwargs):
    """
    Convert the input text into a custom log file format and write it to the output file.

    Args:
        text (str): The input text to be converted.
        outputfile (str): The path to the output file.
        kwargs: Additional keyword arguments for customization.

    Returns:
        None
    """
    # Example implementation of custom log file conversion
    with open(outputfile, "w", encoding="utf-8") as file:
        file.write(text)
```

This template ensures that the custom conversion logic is flexible and adaptable to various requirements.

## **Format Selection via Tags**

The desired output format can be selected directly within the Gherkin feature file using tags. Each feature or scenario can include one or more format-specific tags (e.g., `@docx`, `@pptx`), which determine the export formats.

### **Example:**

```gherkin
  @docx @pptx
  Scenario: Normal breathing curve

    Given the test stand is turned on
```

In this example, the scenario will be exported to both `docx` and `pptx` formats.

---

## **Summary**

- The configuration system is highly flexible, allowing control over every aspect of logging, reporting, and output format.
- Integration with **Pandoc** ensures a wide range of supported formats and customization options.
- By using tags in Gherkin files, users can dynamically select the desired export formats for features and scenarios.

This robust configuration setup empowers teams to tailor `bddreporting` to meet diverse project needs.

### **Key Points**

- Feature-level and scenario-level comments can include Jinja2 placeholders.
- These placeholders are replaced with their values at runtime, ensuring dynamic content in logs.

---

## **Conclusion**

`bddreporting` bridges the gap between BDD practices and detailed reporting. By integrating seamlessly with [`behave`](https://github.com/behave/behave), it provides a robust toolset for generating structured, customizable logs and templates for enhanced test reporting. Its use of [Pandoc](https://pandoc.org/) for format conversion ensures compatibility with a wide range of formats, and the integration of [Mako templates](https://www.makotemplates.org/) and Jinja2 templates offers powerful customization options.

