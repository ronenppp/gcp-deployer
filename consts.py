ARGS_CLOUD_FUNCTIONS = 'CF'
ARGS_CLOUD_RUN_FUNCTIONS = 'CRF'

DEPLOY_DEFAULT_REGION = 'us-east1'
DEPLOY_DEFAULT_RUNTIME = 'python39'
DEPLOY_DEFAULT_ENTRYPOINT = 'run'
DEPLOY_DEFAULT_TIMEOUT = '180'
DEPLOY_DEFAULT_MEMORY = '512'
DEPLOY_DEFAULT_MEMORY_CR = '512Mi'
DEPLOY_DEFAULT_CPU = '1'
DEPLOY_DEFAULT_MAX_INSTANCES = '1'
DEPLOY_DEFAULT_SERVICE_ACCOUNT = 'cloud-functions@{}.iam.gserviceaccount.com'   # Used by the running function
DEPLOY_DEFAULT_COMPUTE_ACCOUNT = '{}-compute@developer.gserviceaccount.com'     # Used for gcs and pubsub operations
DEPLOY_METHOD_OPTIONS = '(CF|CRF)'
DEPLOY_DEFAULT_LIBRARIES = ['utils']            # Any library you want to include in the running function

COPY_BLACKLIST_FILES = ['.gcloudignore']
TESTS_FOLDER_NAME = 'tests'                     # Top folder for all tests
DEV_FOLDER_NAME = 'PycharmProjects'
REPO_FOLDER_NAME = 'gcp-deployer'

TRIGGER_DEFAULT_PUBSUB_ACK = 600
