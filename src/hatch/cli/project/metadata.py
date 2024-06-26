import click


@click.command(short_help='Display project metadata')
@click.argument('field', required=False)
@click.pass_obj
def metadata(app, field):
    """Display project metadata."""
    import json

    from hatchling.dep.core import dependencies_in_sync

    if dependencies_in_sync(app.project.metadata.build.requires_complex):
        from hatchling.metadata.utils import resolve_metadata_fields

        with app.project.location.as_cwd():
            project_metadata = resolve_metadata_fields(app.project.metadata)
    else:
        with app.project.location.as_cwd():
            environment = app.get_environment()

            with app.status_waiting('Setting up build environment for missing dependencies') as status:
                with environment.build_environment(app.project.metadata.build.requires):
                    status.stop()

                    command = ['python', '-u', '-m', 'hatchling', 'metadata', '--app', '--compact']
                    process = app.platform.capture_process(command)
                    project_metadata = json.loads(app.read_builder(process))

    if field:
        if field not in project_metadata:
            app.abort(f'Unknown metadata field: {field}')
        elif field == 'readme':
            if project_metadata[field]['content-type'] == 'text/markdown':  # no cov
                app.display_markdown(project_metadata[field]['text'])
            else:
                app.display_info(project_metadata[field]['text'])
        elif isinstance(project_metadata[field], str):
            app.display_info(project_metadata[field])
        else:
            app.display_info(json.dumps(project_metadata[field], indent=4))
    else:
        for key, value in list(project_metadata.items()):
            if not value:
                project_metadata.pop(key)

        app.display_info(json.dumps(project_metadata, indent=4))
