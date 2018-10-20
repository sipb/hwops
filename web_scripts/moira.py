import subprocess

devnull = open("/dev/null", "r")

def scan_acl(acl_name, strip_instance=True):
    try:
        assert acl_name[0:1].isalpha()
        members = set()
        for line in subprocess.check_output(["/mit/ops/bin/qy", "-n", "-s", "geml", acl_name], stderr=devnull).split("\n"):
            if not line.strip(): continue
            mem_type, mem_name = line.strip().split(", ")
            if mem_type == "USER":
                members.add(mem_name)
            elif mem_type == "KERBEROS" and mem_name.endswith("@ATHENA.MIT.EDU"):
                user = mem_name.rsplit("@", 1)[0]
                if strip_instance:
                    user = user.split("/")[0]
                members.add(user)
        return members
    except subprocess.CalledProcessError:
        return set()

def list_exists(list_name):
    try:
        return list_name[0:1].isalpha() and subprocess.check_output(["/mit/ops/bin/qy", "-n", "-s", "-f", "active", "glin", list_name], stderr=devnull).strip() == "1"
    except subprocess.CalledProcessError:
        return False

def email_to_user(email):
    try:
        kv = subprocess.check_output(["/mit/consult/bin/ldaps", "--", "mail=%s" % email, "uid"], stderr=devnull).strip().split("\n")[-1].split(": ",1)
        return (kv[1:] and kv[1]) or None
    except subprocess.CalledProcessError:
        return None

def user_to_email(name):
    try:
        kv = subprocess.check_output(["/mit/consult/bin/ldaps", "--", "uid=%s" % name, "mail"], stderr=devnull).strip().split("\n")[-1].split(": ",1)
        return (kv[1:] and kv[1]) or None
    except subprocess.CalledProcessError:
        return None

def is_email_valid_for_owner(email):
    if email.endswith("@mit.edu"):
        if list_exists(email.rsplit("@", 1)[0]):
            return True
    return email_to_user(email) is not None

def has_access(user, mailing_list):
    if not user:
        return False
    if mailing_list.endswith("@mit.edu"):
        if user in scan_acl(mailing_list.rsplit("@", 1)[0]):
            return True
    if email_to_user(mailing_list) == user:
        return True
    return False

def stella(hostname):
    if hostname[0:1] == "-":
        return "-- no invocation; invalid hostname --"
    so, se = subprocess.Popen(["stella", "-noauth", hostname], stdin=devnull, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if se:
        if so:
            so += "\n -- stderr --\n" + se
        else:
            so = se
    return so
