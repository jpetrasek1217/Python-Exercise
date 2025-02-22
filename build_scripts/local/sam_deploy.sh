#!/bin/bash

echo "started at $(date +"%T.%N")"

set -e

OPTS=`getopt -o p: --long profile: -n 'parse-options' -- "$@"`

if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi

echo "$OPTS"
eval set -- "$OPTS"

PROFILE=''

while true; do
  case "$1" in
    -p | --profile ) PROFILE="$2"; shift; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

PROFILE_REGION=$(aws configure get region --profile $PROFILE)
REGION=${PROFILE_REGION:-${AWS_REGION:-${AWS_DEFAULT_REGION:-us-east-1}}}

echo "Start deploying stack"
sam deploy \
    --profile $PROFILE \
    --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
    --no-confirm-changeset \
    --stack-name cookiecutter-$USER \
    --s3-bucket evertz-io-artifacts-bucket-$REGION \
    --s3-prefix cookiecutter-$USER/Artifacts/Templates \
    --parameter-overrides \
        Project=cookiecutter-$USER \
        Owner=$USER@evertz.com Name=cookiecutter-$USER \
        BasePath=cookiecutter-$USER

echo "finished at $(date +"%T.%N")"
echo "All done"
