import pytest


@pytest.fixture()
def AnsibleDefaults(Ansible):
    return Ansible("include_vars", "defaults/main.yml")["ansible_facts"]


@pytest.fixture()
def AnsibleVars(Ansible):
    return Ansible("include_vars", "tests/group_vars/aptly.yml")["ansible_facts"]


def test_kafka_user(User, Group, AnsibleDefaults):
    assert User(AnsibleDefaults["aptly_user"]).exists
    assert Group(AnsibleDefaults["aptly_group"]).exists


def test_kafka_conf(File, AnsibleDefaults):
    conf_dir = File(AnsibleDefaults["aptly_conf_path"])
    conf_file = File(AnsibleDefaults["aptly_conf_path"] + "/aptly.conf")
    assert conf_dir.exists
    assert conf_dir.is_directory
    assert conf_dir.user == AnsibleDefaults["aptly_user"]
    assert conf_dir.group == AnsibleDefaults["aptly_group"]
    assert conf_file.exists
    assert conf_file.is_file
    assert conf_file.user == AnsibleDefaults["aptly_user"]
    assert conf_file.group == AnsibleDefaults["aptly_group"]


def test_aptly_service(File, Service, Socket, AnsibleDefaults):
    host = AnsibleDefaults["aptly_host"]
    port = AnsibleDefaults["aptly_port"]
    assert File("/lib/systemd/system/aptly.service").exists
    assert Service("aptly").is_enabled
    assert Service("aptly").is_running
    assert Socket("tcp://" + host + ":" + str(port)).is_listening


def test_aptly_version(Command, AnsibleDefaults):
    aptly_version = AnsibleDefaults["aptly_version"]
    command = Command("aptly version")
    assert command.stdout == 'aptly version: ' + aptly_version
    assert command.rc == 0
