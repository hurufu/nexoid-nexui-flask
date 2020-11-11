'''ASN.1'''
import json
from bitstring import BitArray
import asn1tools

asn = asn1tools.compile_files('Scapi.asn1', 'xer')

def map_cardholder_message(language, msg):
    '''map_cardholder_message'''
    mapping = {
        'crdhldrMsgWelcome': { 'en': 'Welcome' },
        'crdhldrEmvPleaseWait': { 'en': 'Please Wait...' },
        'crdhldrEmvApproved': { 'en': 'Approved.' },
        'rdhldrMsgTransactionAborted': { 'en': 'Transaction Aborted!' }
    }
    return mapping[msg][language]

def map_selected_service(language, srv):
    '''map_selected_service'''
    mapping = {
        'none': { 'en': 'None' },
        'payment': { 'en': 'Sale' },
        'refund': { 'en': 'Refund' },
        'cancellation': { 'en': 'Cancellation' },
        'preauth': { 'en': 'Pre-Authorisation' },
        'updatePreauth': { 'en': 'Update Pre-Auth.' },
        'completion': { 'en': 'Pre-Auth. Completion' },
        'cashAdvance': { 'en': 'Cash Advance' },
        'deferredPayment': { 'en': 'Deffered Payment' },
        'deferredPaymentCompletion': { 'en': 'Deffered Payment Completion' },
        'voiceAuthorisation': { 'en': 'Voice Auth.' },
        'cardholderDetection': { 'en': 'Cardholder Detection' },
        'cardValidityCheck': { 'en': 'Card Validity Check' },
        'noShow': { 'en': 'No-show' },
    }
    return mapping[srv][language]

def map_sale_system_notification(language, ssn):
    '''map_sale_system_notification'''
    mapping = {
        'crdhldrSsnCardRemovalRequested': { 'en': 'Remove Card' },
        'crdhldrSsnCardRemoved': { 'en': 'Card Removed' },
        'crdhldrSsnRequestSignature': { 'en': 'Request Signature' },
        'crdhldrSsnReceiptPrintingFailed': { 'en': 'Printing Failed' },
    }
    return mapping[ssn][language]

def map_output(language, out):
    '''map_output'''
    mapping = {
        'msg': map_cardholder_message,
        'selectedService': map_selected_service,
        'ssn': map_sale_system_notification,
    }
    return mapping[out[0]](language, out[1])

def convert_output(api, payload):
    '''convert_output'''
    def map_all_outputs(language, what):
        return [map_output(language, w) for w in what]
    return {
        'api': api,
        'line': ' '.join(map_all_outputs(payload['language'], payload['what'])),
    }

def convert_interfaces(_, payload):
    '''convert_interfaces'''
    return {
        'api': 'interface',
        'line': BitArray(payload['interfaceStatus'][0]).bin,
    }

def convert_print(api, _):
    '''convert_print'''
    return {
        'api': api,
    }

def convert_to_request_log_event(msg):
    '''convert_to_request_log_event'''
    mapping = {
        'output': convert_output,
        'updateInterfaces': convert_interfaces,
        'print': convert_print
    }
    return mapping[msg[0]](msg[0], msg[1])

def tonexui(apdu):
    '''tonexui'''
    msg = asn.decode('ScapiRequest', apdu, check_constraints=True)
    return json.dumps(convert_to_request_log_event(msg))

def fromnexui(json_msg):
    '''fromnexui'''
    tmp = json.loads(json_msg)
    if 'ack' in tmp:
        return asn.encode('ScapiResponse', ('ack', None), check_constraints=True)
    raise NotImplementedError
