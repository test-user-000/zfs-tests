import subprocess
import os
# A collection of zfs calls that can be stubed out

def fs_exists(zfs_receive_path):
    """Check if a zfs Filesytem already exists"""
    devnull = open(os.devnull, 'w')
    try:
        subprocess.check_call(['zfs', 'get', 'name', zfs_receive_path],
                stdout=devnull, stderr=devnull)
    except subprocess.CalledProcessError:
        return False
    return True

def zfs_recv(file_to_receive, desitnation_fs):
    """Receive the specified zfs send file to the destination fs"""
    subprocess.check_call('cat ' + file_to_receive + ' | zfs recv ' + desitnation_fs, shell=True)

def get_filesystem_properties(filesystem_name, property_set):
    """Given the name of a filesystem and a list of properties returns a
    dictionary of name value pairs"""
    # Not all properties are valid filesystem properties, some of them are
    # snapshot exclusive or the user could mistype. This section checks that
    # the requested properties exist, and are filesystem properties.
    file_system_proprties = frozenset(
            ['available','compressratio','creation','name',
            'mounted','origin','refcompressratio','referenced','type','used',
            'usedbychildren','usedbydataset','usedbyrefreservation',
            'usedbysnapshots','userrefs','written','aclinherit','atime',
            'canmount','casesensitivity','checksum','compression','copies',
            'dedup','devices','exec','logbias','mountpoint','normalization',
            'primarycache','quota','readonly','recordsize','refquota',
            'refreservation','reservation','secondarycache','setuid',
            'sharenfs','sharesmb','snapdir','sync','utf8only','version'])

    illegal_properties = frozenset(property_set) - file_system_proprties
    if illegal_properties:
        raise ValueError(illegal_properties)
    # -H strips the header, you do not need it since you know the order
    # -p gives you the exact values, so time in UNIX timestamps, size in bytes
    get_response = subprocess.check_output(
            ['zfs', 'get', '-Hp', ','.join(property_set), filesystem_name])
    propery_dictionary = {}
    for line in get_response.splitlines():
        split_line = line.split()
        propery_dictionary[split_line[1]] = split_line[2]
    return propery_dictionary

