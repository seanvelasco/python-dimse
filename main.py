import logging
from pydicom import dcmread
from pydicom.filewriter import write_file_meta_info
from pydicom.uid import JPEGBaseline, ExplicitVRLittleEndian, ExplicitVRBigEndian, ImplicitVRLittleEndian
from pynetdicom import AE,StoragePresentationContexts, VerificationPresentationContexts, evt, debug_logger, AllStoragePresentationContexts, VerificationPresentationContexts
from pynetdicom.sop_class import CTImageStorage, Verification, StorageCommitmentPushModel, PatientRootQueryRetrieveInformationModelFind
from pydicom.dataset import Dataset

from commands import *

# debug_logger()

ADDRESS = "0.0.0.0"
PORT = 1666

# Bind C-STORE, C-ECHO handlers

handlers = [
    (evt.EVT_C_STORE, handle_store),
    (evt.EVT_C_ECHO, handle_echo, [logging.getLogger('pynetdicom')]),
    (evt.EVT_C_FIND, handle_find, [logging.getLogger('pynetdicom')]),
]

# Create application entity
scp = AE(ae_title='SCP') # Must not exceed 16 characters

# Maximum size per transfer (default: 16384, unlimited: 0)
scp.maximum_pdu_size = 0

# Add support for all Storage SOP Classes & transfer syntaxes
# Add support for Verification SOP Class
scp.supported_contexts = (
    StoragePresentationContexts +
    VerificationPresentationContexts
)

# Add support for C-FIND
scp.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

print("Starting DIMSE in SCP mode at " + ADDRESS + ":" + str(PORT))

scp.start_server((ADDRESS, PORT), block=True, evt_handlers=handlers)