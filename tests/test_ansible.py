import pytest


@pytest.fixture()
def AnsibleDefaults(Ansible):
    return Ansible("include_vars", "defaults/main.yml")["ansible_facts"]


@pytest.fixture()
def AnsibleVars(Ansible):
    return Ansible("include_vars", "tests/group_vars/aptly.yml")["ansible_facts"]


def test_aptly_user(User, Group, AnsibleDefaults):
    assert User(AnsibleDefaults["aptly_user"]).exists
    assert Group(AnsibleDefaults["aptly_group"]).exists


def test_aptly_service(File, Service, Socket, AnsibleDefaults):
    host = AnsibleDefaults["aptly_host"]
    port = AnsibleDefaults["aptly_port"]
    assert File("/lib/systemd/system/aptly.service").exists
    assert Service("aptly").is_enabled
    assert Service("aptly").is_running
    assert Socket("tcp://" + host + ":" + str(port)).is_listening


def test_aptly_api_service(File, Service, Socket, AnsibleDefaults):
    host = AnsibleDefaults["aptly_host"]
    port = AnsibleDefaults["aptly_api_port"]
    assert File("/lib/systemd/system/aptly-api.service").exists
    assert Service("aptly-api").is_enabled
    assert Service("aptly-api").is_running
    assert Socket("tcp://" + host + ":" + str(port)).is_listening


def test_aptly_version(Command, AnsibleDefaults):
    aptly_version = AnsibleDefaults["aptly_version"]
    command = Command("aptly version")
    assert command.stdout == 'aptly version: ' + aptly_version
    assert command.rc == 0
