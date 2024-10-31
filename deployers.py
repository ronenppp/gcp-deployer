import argparse

from abc import ABCMeta, abstractmethod
from typing import Union
from consts import *
from utils import *


class Deployer(metaclass=ABCMeta):
    def __init__(self):
        self._args = None

    @abstractmethod
    def validate_input(self):
        """Validate the input commands from the user"""

    @abstractmethod
    def deploy(self):
        """Issues deployment commands to GCP cloud"""


class CloudFunctionsGen1Deployer(Deployer):
    def validate_input(self) -> bool:
        parser = argparse.ArgumentParser()
        parser.add_argument('function_name', type=str, help='function name')
        parser.add_argument('project', type=str, help='target project name')
        parser.add_argument('deploy_method', type=str, help=f'specify deployment type {DEPLOY_METHOD_OPTIONS}')
        parser.add_argument('-t', '--topic', type=str, help='specify pubsub topic')
        parser.add_argument('-b', '--bucket', type=str, help='specify bucket')
        parser.add_argument('-s', '--secret', type=str, help='specify secrets from secret manager')
        parser.add_argument('-o', '--timeout', type=str, help='specify max timeout')
        parser.add_argument('-m', '--memory', type=str, help='specify memory size')
        parser.add_argument('-i', '--instances', type=str, help='specify number of parallel instance runs')
        parser.add_argument('-u', '--unittest', action="store_true", help='run unit testing with pytest')
        self._args = parser.parse_args()
        return True

    def _prepare_deployment_config(self, deployment_folder: str) -> dict:
        deploy_conf = {
            'function_name': self._args.function_name,
            'region': DEPLOY_DEFAULT_REGION,
            'runtime': DEPLOY_DEFAULT_RUNTIME,
            'source': deployment_folder,
            'entry-point': DEPLOY_DEFAULT_ENTRYPOINT,
            'service-account': DEPLOY_DEFAULT_SERVICE_ACCOUNT.format(self._args.project),
            'timeout': self._args.timeout or DEPLOY_DEFAULT_TIMEOUT,
            'memory': self._args.memory or DEPLOY_DEFAULT_MEMORY,
            'max-instances': self._args.instances or DEPLOY_DEFAULT_MAX_INSTANCES,
            'project': self._args.project,
        }
        deploy_conf.update({'set-secrets': self._args.secret} if self._args.secret else {})
        deploy_conf.update({'security-level': 'secure-always'} if not self._args.topic and not self._args.bucket else {})
        return deploy_conf

    def _get_trigger_commands(self) -> list:
        if self._args.topic:
            return ['--trigger-topic', self._args.topic]
        elif self._args.bucket:
            return ['--trigger-bucket', self._args.bucket]
        else:
            return ['--trigger-http']

    def _deploy_function(self, deploy_conf) -> None:
        commands = ['gcloud', 'functions', 'deploy', deploy_conf['function_name'],
                    '--region', deploy_conf['region'],
                    '--runtime', deploy_conf['runtime'],
                    '--source', deploy_conf['source'],
                    '--entry-point', deploy_conf['entry-point'],
                    '--service-account', deploy_conf['service-account'],
                    '--timeout', deploy_conf['timeout'],
                    '--memory', deploy_conf['memory'],
                    '--max-instances', deploy_conf['max-instances'],
                    '--no-allow-unauthenticated',
                    '--project', deploy_conf['project'],
                    '--no-gen2'
                    ] + self._get_trigger_commands()
        if 'set-secrets' in deploy_conf:
            commands += ['--set-secrets', deploy_conf['set-secrets']]
        if 'security-level' in deploy_conf:
            commands += ['--security-level', deploy_conf['security-level']]

        print(f'About to deploy with the following configuration: {commands}')
        subprocess.run(commands, shell=True)

    def deploy(self):
        repo_root = get_local_repo_path()

        # Run tests
        if self._args.unittest and not run_tests(repo_root):
            raise RuntimeError('Some or all tests have failed. Aborting deployment')

        deployment_folder = prepare_deployment_folder(self._args.function_name)
        deployment_config = self._prepare_deployment_config(deployment_folder)

        # Deploy to the cloud
        self._deploy_function(deployment_config)


class CloudRunFunctionsDeployer(Deployer):
    def validate_input(self):
        pass

    def deploy(self):
        pass


def get_deployer(args: list) -> Union[Deployer, None]:
    if ARGS_CLOUD_FUNCTIONS in args:
        return CloudFunctionsGen1Deployer()
    if ARGS_CLOUD_RUN_FUNCTIONS in args:
        return CloudRunFunctionsDeployer()
    print(f'Please specify a valid deploy method {DEPLOY_METHOD_OPTIONS}')
    return None
