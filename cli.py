import backend
import sys
import os


def clr():
    print("\033[H\033[2J", end="")


def is_backend_success(msg):
    if isinstance(msg, str):
        status, sep, message = msg.partition(":")
        if status == "succ":
            return True
        else:
            print(message.capitalize())
            input("\n(Press ENTER to continue)")
            return False


def menuprint(*args):
    for i, arg in enumerate(args):
        print(f"{i+1}. {arg}")


def patient_menu(patient):
    """Displays and handles the menu for patients

    Args:
        patient (str): name of patient logged in
    """
    while True:
        try:
            clr()
            print("PATIENT MENU")
            menuprint(
                "Book Appointment",
                "View All Appointments",
                "Cancel Appointment",
                "Back",
            )
            opt = int(input("Enter an option: "))
            if opt == 4:
                break
            elif opt == 1:

                print("\nSelect specialty:")
                menuprint(*backend.get_specialties())
                opt_s = int(input("Enter option: "))
                spec = backend.get_specialties()[opt_s - 1]

                docs = backend.get_doc_names_by_spec(spec)
                print("\nSelect doctor:")
                menuprint(*docs)
                opt_o = int(input("Enter option: "))
                doctor = docs[opt_o - 1]

                timing = input("Enter appointment time in 24-hour format(HH:MM): ")

                if is_backend_success(backend.add_appointment(patient, doctor, timing)):
                    print("Appointment booked!")
                    input("\n(Press ENTER to continue)")

            elif opt == 2:
                appts = [" ".join(row) for row in backend.get_appts_by_patient(patient)]
                menuprint(*appts)
                input("\n(Press ENTER to continue)")
            elif opt == 3:
                print(" ".join(backend.appts_fieldnames))
                appts = [" ".join(row) for row in backend.get_appts_by_patient(patient)]
                menuprint(*appts)
                opt_t = int(input("Select an appointment id: "))
                stat = input("Do you wish to cancel the appointment?(Y/N): ").lower()
                if stat == "y":
                    stat = "Canceled"
                    if is_backend_success(
                        backend.modify_appointment_status(
                            backend.get_appt_ids()[opt_t], stat
                        )
                    ):
                        print("Appointment canceled!!")
                        input("\n(Press ENTER to continue)")
            else:
                print("Invalid option!")
        except:
            pass


def doctor_menu(doctor):
    """Prints and handles menu for doctors of the hospital

    Args:
        doctor (str): name of the doctor logged in
    """
    while True:
        try:
            clr()
            print("DOCTOR MENU")
            menuprint(
                "View Appointments", "Cancel Appointment", "Change Time Slot", "Back"
            )
            opt = int(input("Enter an option: "))
            if opt == 4:
                break
            elif opt == 1:
                print(" ".join(backend.appts_fieldnames))
                appts = [" ".join(row) for row in backend.get_appts_by_doc(doctor)]
                menuprint(*appts)
                input("\n(Press ENTER to continue)")

            elif opt == 2:
                print(" ".join(backend.appts_fieldnames))
                appts = [" ".join(row) for row in backend.get_appts_by_doc(doctor)]
                menuprint(*appts)
                opt_t = int(input("Select an appointment id: "))
                stat = input("Do you wish to cancel the appointment?(Y/N): ").lower()
                if stat == "y":
                    stat = "Canceled"
                    if is_backend_success(
                        backend.modify_appointment_status(
                            backend.get_appt_ids()[opt_t], stat
                        )
                    ):
                        print("Appointment canceled!!")
                        input("\n(Press ENTER to continue)")

            elif opt == 3:
                st = input("Enter start time in 24-hour format(HH:MM): ")
                et = input("Enter end time in 24-hour format(HH:MM): ")
                if is_backend_success(backend.modify_doc_time_slot(doctor, st, et)):
                    print("Time slot changed!")
                    input("\n(Press ENTER to continue)")
            else:
                print("Invalid option!")
        except:
            pass


def admin_menu():
    """Prints menu for hospital administration"""
    while True:
        try:
            clr()
            print("ADMIN MENU")
            menuprint(
                "Add Doctor", "Remove Doctor", "Add Admin", "Remove Admin", "Back"
            )
            opt = int(input("Enter an option: "))
            if opt == 5:
                break
            elif opt == 1:
                doc_name = input("Enter doctor name: ")
                spec = input("Enter doctor specialty: ")
                st = input("Enter start time: ")
                et = input("Enter end time: ")
                if is_backend_success(backend.add_doctor(doc_name, spec, st, et)):
                    print("Doctor added!")
                    input("\n(Press ENTER to continue)")
            elif opt == 2:
                menuprint(*backend.get_doc_names())
                doc_name = input("Enter doctor name: ")
                if is_backend_success(backend.remove_doc(doc_name)):
                    print("Doctor removed!")
                    input("\n(Press ENTER to continue)")
            elif opt == 3:
                user_id = input("Enter admin ID: ")
                pswd = input("Enter admin password: ")
                if is_backend_success(backend.add_admin(user_id, pswd)):
                    print("Admin added!")
                input("\n(Press ENTER to continue)")
            elif opt == 4:
                user_id = input("Enter admin ID: ")
                pswd = input("Enter admin password: ")
                if is_backend_success(backend.remove_admin(user_id, pswd)):
                    print("Admin removed!")
                input("\n(Press ENTER to continue)")
            else:
                print("Invalid option!")
        except:
            pass


def main():
    backend.start()
    while True:
        try:
            clr()
            print("HOSPITAL MANAGEMENT SYSTEM")
            print()
            print()
            print("MAIN MENU")
            print("1. Patient Login")
            print("2. Doctor Login")
            print("3. Management Login")
            print("4. Quit")
            opt = int(input("Enter an option: "))
            print()
            if opt == 4:
                break
            elif opt == 1:
                pname = input("Enter patient name: ")
                ph_no = int(input("Enter patient phone no.: "))

                if (
                    pname in backend.get_patient_names()
                    and ph_no in backend.get_patient_ph_no()
                ):
                    patient_menu(pname)
                else:
                    new_patient = input(
                        "Patient not registered. Do you wish to register a new patient?(Y/N): "
                    ).lower()
                    if new_patient == "y":
                        age = int(input("Enter patient age: "))
                        sex = input("Enter patient sex: ")
                        if is_backend_success(
                            backend.add_patient(pname, age, sex, ph_no)
                        ):
                            print("Patient registered!")
                            input("\n(Press ENTER to continue)")
                            patient_menu(pname)

            elif opt == 2:
                dname = input("Enter doctor name: ")
                if dname in backend.get_doc_names():
                    print(backend.get_doc_names())
                    doctor_menu(dname)
                else:
                    print("Doctor not registered!")
                    print(backend.get_doc_names())
                    input("\n(Press ENTER to continue)")

            elif opt == 3:
                adm_id = input("Enter admin id: ")
                pswd = input("Enter admin password: ")
                if backend.is_admin(adm_id, pswd):
                    admin_menu(adm_id)
                else:
                    print("Invalid admin!")
                    input("\n(Press ENTER to continue)")

            else:
                print("Invalid option!")
        except:
            pass
    backend.stop()


if __name__ == "__main__":
    main()
