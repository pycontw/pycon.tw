if [ "$TRAVIS_BRANCH" == "master" ] && [ "$TRAVIS_PULL_REQUEST" == "false" ]
then
    openssl aes-256-cbc -K $encrypted_6c2822a03f14_key \
        -iv $encrypted_6c2822a03f14_iv -in secrets.tar.enc -out secrets.tar -d
    tar xvf secrets.tar
    cp ./deploy_key ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    eval $(ssh-agent)
    ssh-add ~/.ssh/id_rsa
    chmod 755 ./deploy_staging.sh
fi
