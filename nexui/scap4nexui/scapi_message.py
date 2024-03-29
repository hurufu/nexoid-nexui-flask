'''ASN.1'''
import os
import threading
from datetime import datetime

from dateutil.tz import tzlocal
from bitstring import BitArray
import asn1tools
from babel.numbers import format_currency

ASN_SCAPI_MODULE_PATH = os.path.join(os.path.dirname(__file__), 'asn1/Scapi.asn1')
ASN_SCNNG_MODULE_PATH = os.path.join(os.path.dirname(__file__), 'asn1/ScapiNngClient.asn1')
ASN_NEXUI_MODULE_PATH = os.path.join(os.path.dirname(__file__), 'asn1/Nexui.asn1')
ASN_EVENT_LOG_MODULE_PATH = os.path.join(os.path.dirname(__file__), 'asn1/EventLog.asn1')

asn = asn1tools.compile_files([ASN_SCAPI_MODULE_PATH, ASN_SCNNG_MODULE_PATH], 'xer')
asn_nexui = asn1tools.compile_files([ASN_SCAPI_MODULE_PATH, ASN_NEXUI_MODULE_PATH], 'jer')
asn_event_log = asn1tools.compile_files([ASN_SCAPI_MODULE_PATH, ASN_EVENT_LOG_MODULE_PATH], 'xer')

class Counter:
    '''The simplest possible thread-safe counter'''
    def __init__(self, start):
        self.value = start
        self._lock = threading.Lock()

    def pre_incr(self):
        '''Increment counter and return new value'''
        with self._lock:
            self.value += 1
            return self.value

    def post_incr(self):
        '''Increment counter and return previous value'''
        with self._lock:
            ret = self.value
            self.value -= 1
            return ret

def synchronized(func):
    '''Decorator that adds lock around a function call'''
    func.__lock__ = threading.Lock()
    def synchronized_function(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return synchronized_function

def map_cardholder_message(language, msg):
    '''map_cardholder_message'''
    icon_please_wait = '⏳	'
    icon_approved = '✔️	'
    icon_aborted = '🚫	'
    mapping = {
        'crdhldrMsgWelcome': {
            'en': 'Welcome',
            'pl': 'Witamy',
            'fr': 'Bienvenue',
            'de': 'Willkommen'
        },
        'crdhldrEmvPleaseWait': {
            'en': icon_please_wait + 'Please Wait...',
            'pl': icon_please_wait + 'Proszę czekać...',
            'fr': icon_please_wait + "S'il vous plaît, attendez...",
            'de': icon_please_wait + 'Warten Sie mal...'
        },
        'crdhldrEmvApproved': {
            'en': icon_approved + 'Approved.',
            'pl': icon_approved + 'Zgoda.',
            'fr': icon_approved + 'Approuvée',
            'de': icon_approved + 'Genehmigt'
        },
        'crdhldrMsgReceiptPrintingFailed': {
            'en': 'Receipt printing failed!',
            'pl': 'Drukowanie paragonu nie powiodło się!',
            'fr': "L'impression du reçu a échoué!",
            'de': 'Belegdruck fehlgeschlagen!',
        },
        'crdhldrMsgTransactionAborted': {
            'en': icon_aborted + 'Transaction Aborted',
            'pl': icon_aborted + 'Transakcję przerwano',
            'fr': icon_aborted + 'Transaction annulée',
            'de': icon_aborted + 'Transaktion abgebrochen',
        },
        'crdhldrMsgCashbackNotAllowed': {
            'en': 'Cashback Not Allowed',
            'pl': 'Wypłata gotówki niedozwolona',
            'fr': 'Cashback non autorisé',
            'de': 'Cashback nicht erlaubt',
        },
        'crdhldrEmvUseMagStripe': {
            'en': 'USE MAG STRIPE',
            'pl': 'UŻYJ PASKA MAGNETYCZNEGO',
            'fr': 'UTILISER UNE BANDE MAGNÉTIQUE',
            'de': 'MAGNETSTREIFEN VERWENDEN',
        },
        'crdhldrEmvInsertCard': {
            'en': 'INSERT CARD',
            'pl': 'WŁÓŻ KARTĘ',
            'fr': 'INSÉRER LA CARTE',
            'de': 'KARTE EINFÜHREN',
        },
        'crdhldrMsgSupplementaryAmountNotAllowed': {
            'en': "Supplementary amount isn't allowed",
            'pl': 'Napiwek niedozwolony',
            'fr': "Le montant supplémentaire n'est pas autorisé",
            'de': 'Ergänzungsbetrag ist nicht zulässig',
        },
    }
    return mapping[msg][language]

def map_selected_service(language, srv):
    '''map_selected_service'''
    mapping = {
        'none': {
            'en': 'None',
            'pl': 'Żaden',
            'fr': 'Aucune',
            'de': 'Keiner',
        },
        'payment': {
            'en': 'Sale',
            'pl': 'Sprzedaż',
            'fr': 'Vente',
            'de': 'Verkauf',
        },
        'refund': {
            'en': 'Refund',
            'pl': 'Zwrot',
            'fr': 'Rembourser',
            'de': 'Rückerstattung',
        },
        'cancellation': {
            'en': 'Cancellation',
            'pl': 'Unieważnienie',
            'fr': 'Annulation',
            'de': 'Stornierung',
        },
        'preauth': {
            'en': 'Pre-Authorisation',
            'pl': 'Preautoryzacja',
            'fr': 'Pré-autorisation',
            'de': 'Vorautorisierung',
        },
        'updatePreauth': {
            'en': 'Update Pre-Auth.',
            'pl': 'Zaktualizuj preautoryzację',
            'fr': 'Mettre à jour la pré-autorisation',
            'de': 'Vorautorisierung aktualisieren',
        },
        'completion': {
            'en': 'Pre-Auth. Completion',
            'pl': 'Zakończenie pre-autoryzacji',
            'fr': 'Achèvement de la pré-autorisation',
            'de': 'Abschluss der Vorautorisierung',
        },
        'cashAdvance': {
            'en': 'Cash Advance',
            'pl': 'Zaliczki pieniężne',
            'fr': 'Avance de fonds',
            'de': 'Vorauszahlung',
        },
        'deferredPayment': {
            'en': 'Deffered Payment',
            'pl': 'Opóźniona płatność',
            'fr': 'Paiement différé',
            'de': 'Zahlungsaufschub',
        },
        'deferredPaymentCompletion': {
            'en': 'Deffered Payment Completion',
            'pl': 'Zakończenie odroczonej płatności',
            'fr': 'Achèvement du paiement différé',
            'de': 'Abschluss der Zahlungsaufschub',
        },
        'voiceAuthorisation': {
            'en': 'Voice Auth.',
            'pl': 'Autoryzacja głosowa',
            'fr': 'Autorisation vocale',
            'de': 'Sprachautorisierung',
        },
        'cardholderDetection': {
            'en': 'Cardholder Detection',
            'pl': 'Wykrywanie posiadacza karty',
            'fr': 'Détection des titulaires de carte',
            'de': 'Karteninhabererkennung',
        },
        'cardValidityCheck': {
            'en': 'Card Validity Check',
            'pl': 'Sprawdzanie ważności karty',
            'fr': 'Vérification de la validité de la carte',
            'de': 'Überprüfung der Kartengültigkeit',
        },
        'noShow': {
            'en': 'No-show',
            'pl': 'Brak pokazu',
            'fr': 'Non-présentation',
            'de': 'No-show',
        },
    }
    return mapping[srv][language]

def map_sale_system_notification(language, ssn):
    '''map_sale_system_notification'''
    mapping = {
        'crdhldrSsnCardRemovalRequested': {
            'en': 'Remove Card',
            'pl': 'Usuń kartę',
            'fr': 'Retirer la carte',
            'de': 'Karte entfernen',
        },
        'crdhldrSsnCardRemoved': {
            'en': 'Card Removed',
            'pl': 'Karta usunięta',
            'fr': 'Carte supprimée',
            'de': 'Karte entfernt',
        },
        'crdhldrSsnRequestSignature': {
            'en': 'Request Signature',
            'pl': 'Poproś o podpis',
            'fr': 'Demande de signature',
            'de': 'Unterschrift anfordern',
        },
        'crdhldrSsnReceiptPrintingFailed': {
            'en': 'Printing Failed',
            'pl': 'Drukowanie nie powiodło się',
            'fr': "L'impression a échoué",
            'de': 'Druck fehlgeschlagen',
        },
    }
    return mapping[ssn][language]

def map_nokreason(language, nok):
    '''map_nokreason'''
    mapping = {
        'none': {
            'en': 'None',
            'pl': 'Brak',
            'fr': 'Aucune',
            'de': 'Keiner',
        },
        'notImplemented': {
            'en': 'Not implemented',
            'pl': 'Nie zaimplementowano',
            'fr': 'Pas mis en œuvre',
            'de': 'Nicht implementiert',
        },
        'originalTrxNotFound': {
            'en': 'Original transaction not found',
            'pl': 'Nie znaleziono oryginalnej transakcji',
            'fr': 'Transaction originale introuvable',
            'de': 'Ursprüngliche Transaktion nicht gefunden',
        },
        'technicalError': {
            'en': 'Technical Error',
            'pl': 'Błąd techniczny',
            'fr': 'Erreur technique',
            'de': 'Technischer Fehler',
        },
        'missingData': {
            'en': 'Missing Data',
            'pl': 'Brakujące dane',
            'fr': 'Données manquantes',
            'de': 'Fehlende Daten',
        },
        'confError': {
            'en': 'Conf. Error',
            'pl': '',
            'fr': '',
            'de': '',
        },
        'noPermission': {
            'en': 'No permission',
            'pl': 'Brak pozwolenia',
            'fr': 'Aucune autorisation',
            'de': 'Keine Erlaubnis',
        },
        'configurationError': {
            'en': 'Configuration Error',
            'pl': 'Błąd konfiguracji',
            'fr': 'Erreur de configuration',
            'de': 'Konfigurationsfehler',
        },
        'amountError': {
            'en': 'Amount Error',
            'pl': 'Błąd kwoty',
            'fr': 'Erreur de montant',
            'de': 'Betrag Fehler',
        },
        'kernelError': {
            'en': 'Kernel Error',
            'pl': 'Błąd jądra',
            'fr': 'Erreur de noyau',
            'de': 'Kernelfehler',
        },
        'dataError': {
            'en': 'Data Error',
            'pl': 'Błąd danych',
            'fr': 'Erreur de donnée',
            'de': 'Datenfehler',
        },
        'noCardInserted': {
            'en': 'No Card Inserted',
            'pl': 'Nie włożono karty',
            'fr': 'Aucune carte insérée',
            'de': 'Keine Karte eingelegt',
        },
        'cancelled': {
            'en': 'Cancelled',
            'pl': 'Anulowany',
            'fr': 'Annulé',
            'de': 'Abgesagt',
        },
        'aborted': {
            'en': 'Aborted',
            'pl': 'Przerwano',
            'fr': 'Interrompu',
            'de': 'Unterbrochen',
        },
        'timeout': {
            'en': 'Timeout',
            'pl': 'Koniec czasu',
            'fr': 'Temps libre',
            'de': 'Auszeit',
        },
        'cardMissing': {
            'en': 'Card Missing',
            'pl': 'Brak karty',
            'fr': 'Carte manquante',
            'de': 'Karte fehlt',
        },
        'chipError': {
            'en': 'Chip Error',
            'pl': 'Błąd chipa',
            'fr': 'Erreur de puce',
            'de': 'Chipfehler',
        },
        'noProfile': {
            'en': 'No Profile',
            'pl': 'Brak profilu',
            'fr': 'Aucun profil',
            'de': 'Kein Profil',
        },
        'fallbackProhibited': {
            'en': 'Fallback Prohibited',
            'pl': 'Zabronione zastępowanie',
            'fr': 'Repli interdit',
            'de': 'Fallback verboten',
        },
        'technologyNotSupported': {
            'en': 'Technology Not Supported',
            'pl': 'Technologia nie jest obsługiwana',
            'fr': 'Technologie non prise en charge',
            'de': 'Technologie wird nicht unterstützt',
        },
        'gpo6985': {
            'en': 'GPO6985',
            'pl': 'GPO6985',
            'fr': 'GPO6985',
            'de': 'GPO6985',
        },
        'cardBlocked': {
            'en': 'Card Blocked',
            'pl': 'Karta zablokowana',
            'fr': 'Carte bloquée',
            'de': 'Karte gesperrt',
        },
        'emptyList': {
            'en': 'Empty List',
            'pl': 'Pusta lista',
            'fr': 'Liste vide',
            'de': 'Leere Liste',
        }
    }
    return mapping[nok][language]

def map_cardholder_entry(language, msg):
    '''map_cardholder_entry'''
    mapping = {
        'crdhldrEntCvdPresence': {
            'en': 'Is CVD Present?',
            'pl': 'Czy podano CVD?',
            'fr': 'Le CVD est-il présent?',
            'de': 'Ist CVD vorhanden?',
        },
        'crdhldrEntEnterExpiryDate': {
            'en': 'Enter expiry date',
            'pl': 'Karta ważna do:',
            'fr': "Entrer la date d'expiration",
            'de': 'Ablaufdatum eingeben',
        },
        'crdhldrEntEnterPan': {
            'en': 'Enter PAN',
            'pl': 'Wprowadź numer karty',
            'fr': 'Entrer le numéro de carte',
            'de': 'Kartennummer eingeben',
        },
        'crdhldrMsgEnterPin': {
            'en': 'Enter PIN',
            'pl': 'Wprowadź PIN',
            'fr': 'Entrer le code PIN',
            'de': 'Pin eingeben',
        },
        'crdhldrMsgNoPin': {
            'en': 'Bypass PIN entry',
            'pl': 'Pomiń PIN',
            'fr': 'Ignorer la saisie du code PIN',
            'de': 'PIN-Eingabe umgehen',
        },
        'crdhldrMsgAmount': {
            'en': 'Amount:',
            'pl': 'Kwota:',
            'fr': 'Montant:',
            'de': 'Betrag',
        },
    }
    return mapping[msg][language]

def map_missing_parameters(language, msg):
    '''map_missing_parameters'''
    mapping = {
        'en': 'Missing parameters: ',
        'pl': 'Brakujące parametry: ',
        'fr': 'Paramètres manquants: ',
        'de': 'Fehlende Parameter: ',
    }
    return mapping[language] + ' '.join(msg)

def noop(_lang, out):
    '''noop'''
    return out

def map_output(language, out):
    '''map_output'''
    mapping = {
        'msg': map_cardholder_message,
        'selectedService': map_selected_service,
        'nokReason': map_nokreason,
        'formattedTrxAmount': noop,
        'missingParameters': map_missing_parameters,
        'status': noop,
    }
    return mapping[out[0]](language, out[1])

def map_entry(language, entry):
    '''map_entry'''
    mapping = {
        'msg': map_cardholder_entry,
        'applicationLabelDisplayed': noop,
        'commandKeyEnterLabel': noop,
        'commandKeyPinBypassLabel': noop,
        'selectedService': noop,
        'formattedTrxAmount': noop,
    }
    return mapping[entry[0]](language, entry[1])

def convert_entry(api, payload):
    '''convert_entry'''
    def choose_api():
        return 'pin' if any(x[1] == 'crdhldrMsgEnterPin' for x in payload['what']) else api

    return [{
        'api': choose_api(),
        'line': [ map_entry(payload['language'], what) for what in payload['what'] ]
    }]

def convert_output(api, payload):
    '''convert_output'''
    language = payload['language']
    ssn = []
    crd = []
    for what in payload['what']:
        if what[0] == 'ssn':
            ssn.append(map_sale_system_notification(language, what[1]))
        else:
            crd.append(map_output(language, what))
    ret = []
    if len(ssn) != 0:
        ret.append({'api': 'ssn', 'line': ssn})
    if len(crd) != 0:
        ret.append({'api': api, 'line': crd})
    return ret

def format_trx_amount(language, amount_data):
    '''Formats amount according to received language and currency specifiers'''
    def get_locale():
        mapping = {
            'en': 'en_GB',
            'pl': 'pl_PL',
            'fr': 'fr_FR',
            'de': 'de_DE',
        }
        return mapping[language]

    amount = amount_data['trxAmount'] / 10 ** amount_data['trxCurrencyExponent']
    currency = amount_data['trxCurrencyAlpha3']
    formatted_amount = format_currency(amount, currency, locale=get_locale())
    return ('formattedTrxAmount', formatted_amount)

def convert_filter(payload):
    '''convert_output_filter
    Refactor this function! It's ugly AF
    '''
    def contains_trx_amount(payload_element):
        parts = ['trxAmount', 'trxCurrencyAlpha3', 'trxCurrencyExponent']
        return any(payload_element == x for x in parts)

    language = payload['language']
    filtered = list((n[0], n[1]) for n in payload['what'] if not contains_trx_amount(n[0]))

    amount_data = {}
    amount_flag = 0
    for what in payload['what']:
        if what[0] == 'trxAmount':
            amount_data['trxAmount'] = what[1]
            amount_flag |= 1
        elif what[0] == 'trxCurrencyAlpha3':
            amount_data['trxCurrencyAlpha3'] = what[1]
            amount_flag |= 2
        elif what[0] == 'trxCurrencyExponent':
            amount_data['trxCurrencyExponent'] = what[1]
            amount_flag |= 4

    if amount_data:
        if amount_flag == 7:
            filtered.append(format_trx_amount(language, amount_data))
        else:
            filtered.append(('formattedTrxAmount', 'Not enough data to format amount'))

    payload['what'] = filtered
    return payload

def convert_output_filter(api, payload):
    '''convert_output_filter'''
    return convert_output(api, convert_filter(payload))

def convert_entry_filter(api, payload):
    '''convert_entry_filter'''
    return convert_entry(api, convert_filter(payload))

def convert_interfaces(_, payload):
    '''convert_interfaces'''
    return [{
        'api': 'interface',
        'line': [BitArray(payload['interfaceStatus'][0]).bin],
    }]

def convert_print(api, payload):
    '''convert_print'''
    return [{
        'api': api,
        'line': [payload['type']]
    }]

def convert_to_request_log_event(msg):
    '''convert_to_request_log_event'''
    print(msg)
    mapping = {
        'output': convert_output_filter,
        'entry': convert_entry_filter,
        'updateInterfaces': convert_interfaces,
        'print': convert_print
    }
    return {
        'source': {
            'type': 'scap'
        },
        'payload': mapping[msg[0]](msg[0], msg[1])
    }

def tonexui(apdu):
    '''tonexui'''
    msg = asn.decode('ScapiNngRequest', apdu, check_constraints=True)
    ui_msg = convert_to_request_log_event(msg['req'])
    return asn_nexui.encode('UiRequest', ui_msg, check_constraints=True)

def fromnexui(json_msg):
    '''fromnexui'''
    msg = asn_nexui.decode('UiResponse', json_msg, check_constraints=True)
    nng_msg = {
        'rsp': msg,
        'id': fromnexui.msg_counter.pre_incr(),
    }
    return asn.encode('ScapiNngResponse', nng_msg, check_constraints=True)

fromnexui.msg_counter = Counter(0)

def append_to_event_log(root, apdu):
    '''Appends APDU to the event log'''
    @synchronized
    def write(file, data):
        file.write(data)
    with open('/tmp/events', mode='ab', buffering=0) as event_log:
        write(event_log, apdu_to_event_log(root, apdu))

def apdu_to_event_log(root, apdu):
    '''any_totest'''
    mapping = {
        'ScapiNngRequest': 'req',
        'ScapiNngResponse': 'rsp',
        'ScapiNngNotification': 'ntf'
    }
    msg = asn.decode(root, apdu, check_constraints=True)
    test_mesg = {
        'ts': datetime.now(tzlocal()),
        'ev': {
            'id': msg['id'],
            'pd': (
                mapping[root], msg[mapping[root]]
            )
        }
    }
    return asn_event_log.encode('EventLogRecord', test_mesg, check_constraints=True) + b'\n'
