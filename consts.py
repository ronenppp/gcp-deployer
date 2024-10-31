ARGS_CLOUD_FUNCTIONS = 'CF'
ARGS_CLOUD_RUN_FUNCTIONS = 'CRF'

DEPLOY_DEFAULT_REGION = 'us-east1'
DEPLOY_DEFAULT_RUNTIME = 'python39'
DEPLOY_DEFAULT_ENTRYPOINT = 'run'
DEPLOY_DEFAULT_TIMEOUT = '180'
DEPLOY_DEFAULT_MEMORY = '512'
DEPLOY_DEFAULT_MAX_INSTANCES = '1'
DEPLOY_DEFAULT_SERVICE_ACCOUNT = 'cloud-functions@{}.iam.gserviceaccount.com'
DEPLOY_METHOD_OPTIONS = '(CF|CRF)'
DEPLOY_DEFAULT_LIBRARIES = ['utils']

COPY_BLACKLIST_FILES = ['.gcloudignore']
TESTS_FOLDER_NAME = 'tests'
DEV_FOLDER_NAME = 'PycharmProjects'
REPO_FOLDER_NAME = 'gcp-deployer'
