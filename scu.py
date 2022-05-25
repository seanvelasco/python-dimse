from pynetdicom.sop_class import CTImageStorage, MRImageStorage, PatientRootQueryRetrieveInformationModelFind

from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, StoragePresentationContexts, debug_logger

# SCU - Service Class User

# ds = dcmread('dicom/covid.dcm')


# debug_logger()

scu = AE() # SCU Application Entitty

# scu.requested_contexts = StoragePresentationContexts
scu.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
# scu.add_requested_context(MRImageStorage)
# scu.add_requested_context(CTImageStorage)
# scu.add_requested_context('1.2.840.10008.1.1')

# 169.254.102.61 - ip address
# 169.254.241.82 - wlan

#ds = dcmread('dicom/covid.dcm')

assoc = scu.associate("127.0.0.1", 1666)

ds = Dataset()
ds.PatientName = ''
ds.QueryRetrieveLevel = 'PATIENT'

# # status = assoc.send_c_store(ds)
# if status:
#     # If the storage request succeeded this will be 0x0000
#     print('C-STORE request status: 0x{0:04x}'.format(status.Status))
# else:
#     print('Connection timed out, was aborted or received invalid response')

if assoc.is_established:
    print('Association established with target SCP')
    
    # Send C-FIND with * as the Patient ID
    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
    for (status, identifier) in responses:
        if status:
            print(identifier)
            #print('C-FIND query status: 0x{0:04X}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')
    

    assoc.release()
else:
    print('Association failed')