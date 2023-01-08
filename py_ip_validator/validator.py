#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Core package and command line utility for E-ARK Information Package validation. """
import argparse
import datetime
import json
import os

# using absolute imports, therefore adding root to python path
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))  # NOQA

from py_ip_validator.mets import MetsValidator
from py_ip_validator.rules import ValidationProfile


from py_ip_validator import LOGGER
from py_ip_validator import information_package as IP


def get_report(details, schema_result, schema_errors, prof_names, schematron_result, profile_results):

    prof_results_basic = {key: value.is_valid for key, value in profile_results.items()}

    error_details = [
        {"rule_id": error.rule_id,
         "severity": error.severity.name,
         "message": error.message,
         "sub_message": error.sub_message}
        for error in details.errors]

    def get_issues(items):
        def get_items(item_list):
            for item in item_list:
                return [{
                    "rule_id": item.rule_id,
                    "severity": item.severity.name,
                    "location": item.location.location,
                    "test": item.location.test,
                    "message": item.message
                }]
        for key, value in items:
            return (get_items(value.warnings) or []) + (get_items(value.failures) or [])

    schematron_issues = get_issues(profile_results.items())

    return {
        "validation_report": {
            "package_id": details.name,
            "report_created": datetime.datetime.now().isoformat(),
            "package_status": details.package_status.name,
            "error_details": error_details,
            "structure_checks": prof_results_basic,
            "metadata_checks": {
                "schema": {
                    "valid": schema_result,
                    "errors": schema_errors
                },
                "schematron": {
                    "valid": schematron_result,
                    "validity_per_section": prof_results_basic
                },
                "schematron_issues": schematron_issues

            }
        }
    }


def validate(directory):
    """Display validation results."""
    # Get the validation path ready
    to_validate = directory
    # Validate package structure
    struct_details = IP.validate_package_structure(to_validate)
    # Schema and schematron validation to be factored out.
    # initialise schema and schematron validation structures
    schema_result = None
    prof_results = {}
    schema_errors = []
    # Schematron validation profile
    profile = ValidationProfile()
    # IF package is well formed then we can validate it.
    if struct_details.package_status == IP.PackageStatus.WellFormed:
        # Schema based METS validation first
        validator = MetsValidator(struct_details.path)
        mets_path = os.path.join(struct_details.path, 'METS.xml')
        schema_result = validator.validate_mets(mets_path)
        # Now grab any errors
        schema_errors = validator.validation_errors
        if schema_result is True:
            profile.validate(mets_path)
            prof_results = profile.get_results()

    return (get_report(details=struct_details, schema_result=schema_result,
                     schema_errors=schema_errors, prof_names=ValidationProfile.NAMES,
                     schematron_result=profile.is_valid, profile_results=prof_results))


def main():
    parser = argparse.ArgumentParser(description='E-ARK Python Information Package validation')

    parser.add_argument('--input', "-i", type=str, help='Information package name', required=True)
    parser.add_argument('--output', "-o", type=str, help='Report result file (JSON format)', required=False)

    args = parser.parse_args()

    if not os.path.exists(args.input):
        msg = "The input (directory or file) does not exist: %s" % args.input
        LOGGER.error(msg)
        raise FileNotFoundError(msg)
    else:
        result = validate(args.input)
        if args.output:
            with open(args.output, "w") as outfile:
                outfile.write(json.dumps(result, indent=4))
            print("Result file created: %s" % args.output)
        else:
            print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
