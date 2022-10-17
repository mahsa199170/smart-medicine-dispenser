# pylint: disable=missing-module-docstring
# pylint: disable=use-dict-literal

NUM_OF_USERS_SUPPORTED = 5 ##min
NUM_OF_TIME_SLOT_SUPPORTED = 3##maxed
NUM_OF_MEDICINE_SLOT_SUPPORTED = 12##maxed

USER_NUM = 0

# This is the list of keys to the values which will be used in the dictionary created
USERS_DICT_KEY_LIST = ["Name", "Gender", "Contact", "Date of Birth", "Address", "E-Mail", "Disease"]

# List of empty dictionaries of array size NUM_OF_USERS_SUPPORTED to store database of patients
USERS_DB = [dict() for x in range(NUM_OF_USERS_SUPPORTED)]

# List of empty dictionary of size NUM_OF_USERS_SUPPORTED to store database of patient prescription
MEDICINE_DB = [dict() for x in range(NUM_OF_USERS_SUPPORTED)]

# List of empty dictionaries of size NUM_OF_USERS_SUPPORTED to store Login Info of Patients
LOGIN_DB = [dict() for x in range(NUM_OF_USERS_SUPPORTED)]

#List of empty appointments of a patient
APPOINTMENT_DB = ["" for x in range(NUM_OF_USERS_SUPPORTED)]
