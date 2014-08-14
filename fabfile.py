from fabric.api import run, local, env, sudo, cd


def vagrant():
    # todo: path to vagrant
    result = local('vagrant ssh_config | grep IdentityFile', capture=True)
    _run('vagrant', '127.0.0.1:2222', result.split()[1])


def remote(user, host, key):
    raise NotImplementedError


def _run(user, host, key):
    # todo: use password also
    # change from the default user to 'vagrant'
    env.user = user
    # connect to the port-forwarded ssh
    env.hosts = [host]
    # use vagrant ssh key
    env.key_filename = key

    path_to_toster = '/var/www/toster'
    path_to_venv = '/var/www/venv'

    sudo('mkdir -p {}'.format(path_to_toster))
    sudo('mkdir -p {}'.format(path_to_venv))
    sudo('chmod 755 {}'.format(path_to_toster))
    sudo('chmod 755 {}'.format(path_to_venv))

    run('git clone https://github.com/nyddle/toster.git {}'.format(
        path_to_toster))

    sudo('add-apt-repository ppa:webupd8team/java')
    sudo('apt-get update')
    sudo('apt-get install software-properties-common python3-dev postgresql libpq-dev git')
    sudo('wget https://download.elasticsearch.org/elasticsearch/'
         'elasticsearch/elasticsearch-1.3.1.deb')
    sudo('dpkg -i elasticsearch-1.3.1.deb')
    sudo('update-rc.d elasticsearch defaults 95 10')
    sudo('/etc/init.d/elasticsearch start')
    sudo('/etc/init.d/elasticsearch status')

    # todo: create venv
    # todo: create postgres DB

    with cd(path_to_toster):
        run('./manage.py syncdb')
