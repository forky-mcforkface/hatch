# Builder plugins

-----

See the documentation for [build configuration](../../config/build.md).

## Known third-party

- [hatch-aws](https://github.com/aka-raccoon/hatch-aws) - used for building AWS Lambda functions with SAM

::: hatchling.builders.plugin.interface.BuilderInterface
    options:
      members:
      - PLUGIN_NAME
      - app
      - root
      - build_config
      - target_config
      - config
      - get_config_class
      - get_version_api
      - get_default_versions
      - clean
      - recurse_included_files
      - get_default_build_data
