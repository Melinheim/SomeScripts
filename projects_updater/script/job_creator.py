import yaml

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

with open('mirror_config.yaml') as mirror_config:
    mirrors = yaml.full_load(mirror_config)

with open('./ci_include/project_update_jobs.yml', 'w') as project_update_jobs_file:
    stages = {
        'stages': [
            'project_update'
        ]
    }

    yaml.dump(stages, project_update_jobs_file, Dumper=Dumper, width=200)

    default = {
        'default': {
            'before_script': [
                'git config --global user.email "user@domain.com"',
                'git config --global user.name "GitLab Runner"',
                'git config user.email "user@domain.com',
                'git config user.name "GitLab Runner"'
            ]
        }
    }

    yaml.dump(default, project_update_jobs_file, Dumper=Dumper, width=200)

    for project_name, project_data in mirrors.items():
        clone_origin = project_data.get('clone_origin')
        clone_branch = project_data.get('clone_branch')
        push_origin = project_data.get('push_origin')
        push_branch = project_data.get('push_branch')

        job = {
            project_name: {
                'stage': 'project_update',
                'tags': ['work'],
                'script': [
                    'git clone ' + clone_origin + ' --branch ' + clone_branch + ' ' + project_name,
                    'cd ' + project_name,
                    'git pull ' + push_origin + ' ' + push_branch + ' --allow-unrelated-histories --no-edit -s ours || true',
                    'git remote add -f mirror_origin ' + push_origin,
                    'git remote update',
                    'git_diff=$(git diff ' + clone_branch + ' remotes/mirror_origin/' + push_branch + ')',
                    'if [[ $git_diff != \'\' ]]; then ' + \
                        'echo "There is diff"; ' + \
                        'git push '+ push_origin + ' ' + clone_branch + ':' + push_branch + ';' + \
                        'else echo "There is no diff"; fi',
                ],
                'rules': [
                    {'if': '$CI_PIPELINE_SOURCE == "schedule"'}
                ]
            }
        }

        yaml.dump(job, project_update_jobs_file, Dumper=Dumper, width=200)
