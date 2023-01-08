import setuptools

setuptools.setup(
    data_files=[
        ("settings",  ["settings/settings.cfg", "settings/default_commands.cfg"]),
        ("py_ip_validator",
         ("resources",
          [
              "schemas",
              "schematron"]
          )),
        ("",  ["logging_config.ini"])
    ]
)
