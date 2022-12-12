import csv
import os
import datetime as dt

files_path = os.getcwd() + os.path.sep + "files" + os.path.sep

appts_fieldnames = ["Appt_id", "Patient Name", "Doctor Name", "Time Slot", "Status"]
doctors_fieldnames = ["Doctor Name", "Specialty", "Time Start", "Time End"]
patients_fieldnames = ["Patient Name", "Age", "Sex", "Phone No."]
admin_fieldnames = ["id", "password"]

global appts_file
global doctors_file
global patients_file
global admin_file

doctors_file = None
appts_file = None
admin_file = None
patients_file = None


def time_fmt(time_string):
    try:
        h, m = (int(t.strip()) for t in time_string.split(":"))
        return h, m
    except:
        return "err: incorrect time entered"


def in_time_slot(t, start_time, end_time):
    t = time_fmt(t)
    start_time = time_fmt(start_time)
    end_time = time_fmt(end_time)

    # hour comparison
    if t[0] >= start_time[0] and t[0] <= end_time[0]:
        # minute comprison
        if (t[1] >= start_time[1] and t[1] <= end_time[1]) or (
            t[0] > start_time[0] and t[0] < end_time[0]
        ):
            return True
        else:
            return False
    else:
        return False


def start():
    """Starts the backend and loads all the necessary file objects"""
    global appts_file
    global doctors_file
    global patients_file
    global admin_file

    if not os.path.isdir(files_path):
        os.mkdir(files_path)

    admin_file = open(files_path + "admin.csv", "a+", newline="")
    appts_file = open(files_path + "appts.csv", "a+", newline="")
    doctors_file = open(files_path + "docs.csv", "a+", newline="")
    patients_file = open(files_path + "patients.csv", "a+", newline="")


def change_mode(mode):
    """Changes the access mode of all the files

    Args:
        mode (str): _description_
    """
    global appts_file
    global doctors_file
    global patients_file
    global admin_file

    if appts_file is not None:
        if not appts_file.closed:
            appts_file.close()
        appts_file = open(files_path + "appts.csv", mode, newline="")
    else:
        appts_file = open(files_path + "appts.csv", mode, newline="")

    if doctors_file is not None:
        if not doctors_file.closed:
            doctors_file.close()
        doctors_file = open(files_path + "docs.csv", mode, newline="")
    else:
        doctors_file = open(files_path + "docs.csv", mode, newline="")

    if patients_file is not None:
        if not patients_file.closed:
            patients_file.close()
        patients_file = open(files_path + "patients.csv", mode, newline="")
    else:
        patients_file = open(files_path + "patients.csv", mode, newline="")

    if admin_file is not None:
        if not admin_file.closed:
            admin_file.close()
        admin_file = open(files_path + "admin.csv", mode, newline="")
    else:
        admin_file = open(files_path + "admin.csv", mode, newline="")


def stop():
    global appts_file
    global doctors_file
    global patients_file
    global admin_file

    admin_file.close()
    appts_file.close()
    doctors_file.close()
    patients_file.close()


def add_doctor(doc_name, specialty, start_time, end_time):
    change_mode("a+")
    global doctors_file
    global doctors_fieldnames
    data = [doc_name, specialty, start_time, end_time]
    w = csv.writer(doctors_file)
    if len(data) != len(doctors_fieldnames):
        return "err: unequal fields"
    else:
        w.writerow(data)
        return "succ: data written"


def get_specialties():
    change_mode("r+")
    global doctors_file
    r = csv.reader(doctors_file)
    specs = []
    for row in r:
        if row[1] not in specs:
            specs.append(row[1])
    change_mode("a+")
    return specs


def get_doc_names():
    change_mode("r+")
    global doctors_file
    r = csv.reader(doctors_file)
    names = []
    for row in r:
        names.append(row[0].strip())
    change_mode("a+")
    return names


def get_doc_names_by_spec(spec):
    change_mode("r+")
    global doctors_file
    r = csv.reader(doctors_file)
    names = []
    for row in r:
        if row[1].strip() == spec.strip():
            names.append(row[0])
    change_mode("a+")
    return names


def get_doc_time_slot(doc_name):
    change_mode("r+")
    global doctors_file
    r = csv.reader(doctors_file)
    for row in r:
        if row[0] == doc_name:
            change_mode("a+")
            return row[2], row[3]
            break
    else:
        change_mode("a+")


def not_in_appts_time_slot(doc_name, appt_time):
    appts = get_appts_by_doc(doc_name)
    for appt in appts:
        if appt[4] != "Canceled":
            if in_time_slot(appt_time, appt[3], appt[3][:-2] + "15"):
                return False
                break
    else:
        return True


def get_appts_by_doc(doc_name):
    change_mode("r+")
    global appts_file
    r = csv.reader(appts_file)
    appts = []
    for row in r:
        if row[2].strip() == doc_name.strip():
            appts.append(row)
    change_mode("a+")
    return appts


def add_patient(name, age, sex, ph_no):
    change_mode("a+")
    global patients_file
    global patients_fieldnames
    data = [name, age, sex, ph_no]
    w = csv.writer(patients_file)
    if len(data) != len(patients_fieldnames):
        return "err: unequal fields"
    else:
        w.writerow(data)
        return "succ: data written"


def get_patient_names():
    change_mode("r+")
    global patients_file
    r = csv.reader(patients_file)
    names = []
    for row in r:
        names.append(row[0].strip())
    change_mode("a+")
    return names


def get_patient_ph_no():
    change_mode("r+")
    global patients_file
    r = csv.reader(patients_file)
    ph_no = []
    for row in r:
        ph_no.append(row[-1].strip())
    change_mode("a+")
    return ph_no


def add_appointment(patient_name, doctor_name, time_slot):
    global appts_file
    change_mode("r+")
    r = csv.reader(appts_file)

    appt_ids = get_appt_ids()
    appt_id = max(appt_ids) + 1 if not appt_ids == [] else 0

    change_mode("a+")

    if patient_name in get_patient_names():
        if doctor_name in get_doc_names():
            timing = get_doc_time_slot(doctor_name)
            if in_time_slot(time_slot, timing[0], timing[1]):
                if not_in_appts_time_slot(doctor_name, time_slot):
                    w = csv.writer(appts_file)
                    w.writerow(
                        [appt_id, patient_name, doctor_name, time_slot, "Booked"]
                    )

                    return "succ: appointment booked"
                else:
                    return "err: error! conflict with another appointment"
            else:
                return "err: error! wrong time slot"
        else:
            return "err: error! doctor not registered"
    else:
        return "err: error! patient not registered"


def get_appts_by_patient(name):
    change_mode("r+")
    global appts_file
    r = csv.reader(appts_file)
    appts = []
    for row in r:
        if row[1] == name:
            appts.append(row)
    change_mode("a+")
    return appts


def get_appt_ids():
    change_mode("r+")
    global appts_file
    r = csv.reader(appts_file)
    appt_ids = []
    try:
        for row in r:
            appt_ids.append(int(row[0]))
    except Exception:
        appt_ids = []
    change_mode("a+")
    return appt_ids


def modify_appointment_status(appt_id, status):
    global appts_file

    change_mode("r+")
    r = csv.reader(appts_file)
    mod_appts = []
    for row in r:
        if int(row[0].strip()) == appt_id:
            appt = row.copy()
            appt[4] = status
            mod_appts.append(appt)
        else:
            mod_appts.append(row)

    if not appts_file.closed:
        appts_file.close()
    appts_file = open(files_path + "appts.csv", "w", newline="")
    w = csv.writer(appts_file)
    w.writerows(mod_appts)
    appts_file.close()

    change_mode("a+")


def modify_doc_time_slot(doc_name, start_time, end_time):
    change_mode("r+")
    global doctors_file
    r = csv.reader(doctors_file)
    mod_recs = []
    for row in r:
        if row[0].strip() == doc_name.strip():
            rec = row.copy()
            rec[2] = start_time
            rec[3] = end_time
            mod_recs.append(rec)
        else:
            mod_recs.append(row)

    if not doctors_file.closed:
        doctors_file.close()
    doctors_file = open(files_path + "docs.csv", "w", newline="")
    w = csv.writer(doctors_file)
    w.writerows(mod_recs)
    doctors_file.close()

    change_mode("a+")

    return "succ"


def remove_doc(doc_name):
    change_mode("r+")
    global doctors_file
    r = csv.reader(doctors_file)
    mod_recs = []
    for row in r:
        if row[0].strip() != doc_name.strip():
            mod_recs.append(row)

    if not doctors_file.closed:
        doctors_file.close()
    doctors_file = open(files_path + "docs.csv", "w", newline="")
    w = csv.writer(doctors_file)
    w.writerows(mod_recs)
    doctors_file.close()

    change_mode("a+")


def is_admin(adm_id, password):
    change_mode("r+")
    global admin_file
    r = csv.reader(admin_file)

    for row in r:
        if row[0].strip() == adm_id:
            return password == row[1].strip()
            break
    else:
        return False


def add_admin(adm_id, password):
    change_mode("a+")
    global admin_file
    w = csv.writer(admin_file)
    w.writerow([adm_id, password])


def remove_admin(u_id, password):
    change_mode("r+")
    global admin_file
    r = csv.reader(admin_file)
    mod_recs = []
    for row in r:
        if row[0].strip() != u_id.strip() and row[1].strip() != password.strip():
            rec = row.copy()
            mod_recs.append(rec)

    if not admin_file.closed:
        admin_file.close()

    admin_file = open(files_path + "admin.csv", "w", newline="")
    w = csv.writer(admin_file)
    w.writerows(mod_recs)
    admin_file.close()

    change_mode("a+")
    return "succ"


if __name__ != "__main__" and not os.path.isfile(files_path + "admin.csv"):
    add_admin("admin", "1234")
    add_doctor("A. Kumar", "Cardiology", "10:00", "14:00")
    add_doctor("C.K. Goyal", "Cardiology", "10:30", "13:00")
    add_doctor("B. Pal", "Cardiology", "13:00", "17:00")
    add_doctor("K.J. Jain", "Orthopaedic", "09:00", "14:30")
    add_doctor("J. Shah", "Orthopaedic", "19:00", "21:30")
    add_doctor("S. Agarwal", "ENT", "16:00", "18:00")
    add_doctor("A. Pote", "Dermatology", "12:00", "16:00")
