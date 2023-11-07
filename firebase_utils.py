from firebase_admin import (
    credentials,
    firestore,
    initialize_app,
    auth
)
from utils import *

import threading
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

firebaseConfig = {
    "type": "service_account",
    "project_id": "admin-soeta",
    "private_key_id": "92d3bdb4a8cc1af58f078a6b10d6cc9cd78b61a8",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDqAGwB281Ax5/g\nx/oVchBZAnaKfl71uiVXNyDrjBcue4b1BBPL2Nv8tM+3WLiQV7ZUNg/atPoPtakJ\nIOqyPijAAVOJFcbJ7TBGU1TilNyu88lrUwzq9/eSOtDFWPC/5aK22N3Q/nxamJqY\nkh6zX6AwItxka5oRIGW0AEnJGj5Q3/pbK1JVgxg5FCynLk4itJj2URvPY5WC5do7\ntkOsLD16JyA3fBjcjycfXh4MaMgXjbejcvGCGS/pHhbQ38pdFlMLllxltin1BVuh\nl9sauqmHgGgUr5j6LiTyNeufDDIhghU2/ut6HZv5TLDBkvlRwn6lh0wzTevI6hxt\nwUsMZ5zJAgMBAAECggEAM7IlKmHzXfjcHs4/NyasauWq55zUgMf/gN2ahb88zdWX\ncqDUeMfvjcwqSZCtsaHXE5Kf/QrXZcoVzoD5qKgn24dPe60Wbjza2eaGDcqiWHpe\nSLof0/c1OBaLUdX81gA26ttNYeMe+OrW2JcLdkhNfOTuuLa24kq8fUBFDMsh8j6l\nCi3dB+5oMDVlKp6RDkJv2nxh5pSx/lLrGoJCKj6q1wbRldQPIa81miN59RAISoU9\nXN8lmYvrW34cUayARNGR0CHdvCnvjpgqHjapbJWZtqBDEETTRLMHztQgOLCsGPB0\nzZqQFZg14d3Njhi4ggonj5ihRE7U0P3Ud/4bsbNnSQKBgQD4bXNjYhkKI5AUeGmR\n5/zhtkGxO0f4sDNXLcODVDcwrwTahHeasrCudA7lyAfEehDUdW6M8nH0a7euN8W3\nLbrVQ9Q5IQ0c+MvD6WqQhqEN+UIQW/EnJXPRTYaqyAV5L8HJLrFfIvn1gxJ9LcYi\ndZz4DUYH0k2jPsmktMeD+qPFBQKBgQDxImbjFNeQBcTs7McFnDaEEqQyyRsrU2td\nAWNX5kladJ/3n9/4/ep40njrbpNmWyEI39/ELb4B+U2NSCshMRxXBOW92OOm22VD\nDeQvaB38w4/r1o6Ewip6ytndUtDHwCLgE+C1A34C6pygVlx9af4e+jTbcOLXdhvh\nSt0NB3kD9QKBgQC37vmvDLOzYQ9NSLYJVHVUfMf4vAaWp4brtjN66gCO6Ba0371a\naZENKVraYJb3rtUFKQk4DE25BYQS1rJp5M7fFgBsZ/84gzEDFbBT34ohOXrjd999\n92nf/wGFMuFyj5xwI0UqRlBBqdEno5t+agxVUCaYpenbwyIy87KBEjLtLQKBgGUT\nZYtEPkN5l500dwxL+bIM2lULZV8Y3YUjws+ikRbgkflLQ6fsT2+L0fHl7NVX15YP\nuY1TGzVamf5hxOpp2pZDUEXu9yYHCwA7f227t+4uz1ItIppVhVbpVr9mKmvAhx3k\nVympKBXy3+p5qNVNK58yhBuDyyJDuNYL+nKusjRNAoGAJ4xX+4ShcE2SpUIv7Kue\nwbNnrTrVHyTwP67FK77QEuSRxuJC170EBx2+MoLqjVHkCRixhatDz5K48uLHrHaB\n+mXV5J/ynfXxZFGng5s/vZNVMhFsfFk+tCkFRGTABJv3S4Vdep62JKh/2SxsbXd6\nBmJOAncBfT4aA+Tl3TDu464=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-2oc7h@admin-soeta.iam.gserviceaccount.com",
    "client_id": "107234418637740946261",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2oc7h%40admin-soeta.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(firebaseConfig)
default_app = initialize_app(cred)
db = firestore.client()

db_ref_reports = db.collection('report')
db_ref_employees = db.collection('employees')
db_ref_template = db.collection('template')

nip_name_values_pair = {}
callback_done_api = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot_empnames(doc_snapshot, changes, read_time):
    global nip_name_values_pair
    for change in changes:
        if change.type.name == 'ADDED':
            name = change.document.get("nickname")
            nip  = change.document.get("nip")
            nip_name_values_pair[nip] = name
        elif change.type.name == 'MODIFIED':
            name = change.document.get("nickname")
            nip = change.document.get("nip")
            nip_name_values_pair[nip] = name
        elif change.type.name == 'REMOVED':
            nip_name_values_pair.pop(change.document.get("nip"))

    print(nip_name_values_pair)
    callback_done_api.set()


# Watch the document
doc_watch_doc = db_ref_employees.on_snapshot(on_snapshot_empnames)

def get_name(nip):
    return nip_name_values_pair.get(nip,"")


def get_users(nip=None):
    db_ref_employees = db.collection('employees').order_by("nip")
    if nip is None:
        return list(map(convert_fdoc, db_ref_employees.get()))
    else:
        # asumsi nya nip cuman 1
        return list(map(convert_fdoc, db_ref_employees.where(u'name', u'==', f"{nip}").get()))[0]


def create_employees_document(fields):
    doc_check = db_ref_employees.where(u'nip', u'==', f"{fields['nip']}").get()

    if len(doc_check) > 0:
        return "Already Exist"

    try:
        user = auth.create_user(
            email=f"dummy@gmail.com",
            email_verified=False,
            password=f"123456",
            display_name=f"{fields['nickname']}",
            disabled=False)
    except Exception as e:
        print(e)
        return e

    return db.collection("employees").add(fields)


def create_documents(collections, fields):
    return db.collection(collections).add(fields)


def search_employee_by_name(query: str, N = 10):
    global nip_name_values_pair
    temp_dict = {}
    for nip, name in nip_name_values_pair.items():
        ratio = fuzz.WRatio(query,name)
        temp_dict[nip] = ratio

    print(temp_dict)
    return dict(sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)[:N])


def get_templates(template_name=None):
    """
    :param template_name: if None search all templates , if its available
    :return:
    """
    if template_name is not None:
        return db_ref_template.where(u'title', u'==', f"{template_name}").get()[0].to_dict()
    template = db_ref_template.get()
    template = list(map(convert_fdoc, template))
    return (template)
