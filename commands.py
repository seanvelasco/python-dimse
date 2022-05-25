import os
from pydicom import dcmread
from pydicom.filewriter import write_file_meta_info
from pydicom.uid import JPEGBaseline, ExplicitVRLittleEndian, ExplicitVRBigEndian, ImplicitVRLittleEndian
from pynetdicom import AE,StoragePresentationContexts, VerificationPresentationContexts, evt, debug_logger, AllStoragePresentationContexts, VerificationPresentationContexts
from pynetdicom.sop_class import CTImageStorage, Verification, StorageCommitmentPushModel, PatientRootQueryRetrieveInformationModelFind
from pydicom.dataset import Dataset

# def default_save(event):
#     # Decode the C-Store request's Data Set parameter to a dict
#     ds = event.dataset

#     # Add the File Meta Information
#     # Ensures the file is conformant with the DICOM File Format
#     ds.file_meta = event.file_meta

#     # write_like_original = False -> Save the DICOM using the SOP Instance UID as the filename
#     # write_like_original = True -> Save the DICOM using the original filename
#     ds.save_as(ds.SOPInstanceUID, write_like_original=True)

def handle_store(event):

    requestor = event.assoc.requestor
    timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        "Received C-ECHO service request from ({}, {}) at {}"
        .format(requestor.address, requestor.port, timestamp)
    )

    print(msg)

    with open(event.request.AffectedSOPInstanceUID, 'wb') as f:
        # Write the preamble and prefix
        f.write(b'\x00' * 128)
        f.write(b'DICM')

        # Add the File Meta Information
        write_file_meta_info(f, event.file_meta)

        # Write encoded dataset
        # Ensures the file is conformant with the DICOM File Format
        f.write(event.request.DataSet.getvalue())

        # Send POST request with binary data as request body
        response = requests.post("https://dicom.sean.ph", data=event.request.DataSet.getvalue())

        print(response.text)
    
    return 0x0000

def handle_echo(event, logger):
    requestor = event.assoc.requestor
    timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        "Received C-ECHO service request from ({}, {}) at {}"
        .format(requestor.address, requestor.port, timestamp)
    )

    print(msg)

    return 0x0000

def handle_commit(event):
    requestor = event.assoc.requestor
    timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        "Received C-STORE service request from ({}, {}) at {}"
        .format(requestor.address, requestor.port, timestamp)
    )

    print(msg)

    return 0x0000
    
def handle_find(event, logger):
    requestor = event.assoc.requestor
    timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        "Received C-FIND service request from ({}, {}) at {}"
        .format(requestor.address, requestor.port, timestamp)
    )

    print(msg)

    ds = event.identifier

    studies = []

    directory = os.getcwd() + "/studies/"
    print(directory)

    for file in os.listdir(directory):
        print(file)
        studies.append(dcmread(os.path.join(directory, file)))

        #if file.endswith(".dcm"):
    print(studies)
            
    if 'QueryRetrieveLevel' not in ds:
        yield 0xC000, None
        return
    
    matching = []
    if ds.QueryRetrieveLevel == 'PATIENT':
        matching = [study for study in studies if study.PatientName == ds.PatientName]
        # if 'PatientName' in ds:
        #     if ds.PatientName not in ['*', '', '?']:
                
    for instance in matching:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return
        identifier = Dataset()
        identifier.PatientName = instance.PatientName
        identifier.QueryRetrieveLevel = ds.QueryRetrieveLevel
        yield (0xFF00, identifier)

    return 0x0000