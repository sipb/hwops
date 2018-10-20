import os

def get_kerberos():
    email = os.getenv("SSL_CLIENT_S_DN_Email")
    if email is None or not email.lower().endswith("@mit.edu") or email.count("@") != 1:
        return None
    return email[:email.index("@")]
