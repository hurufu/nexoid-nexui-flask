'''ASN.1'''
from bitstring import BitArray
import asn1tools

asn = asn1tools.compile_files('Scapi.asn1', 'xer')
asn_nexui = asn1tools.compile_files(['Scapi.asn1', 'Nexui.asn1'], 'jer')

def map_cardholder_message(language, msg):
    '''map_cardholder_message'''
    mapping = {
        'crdhldrMsgWelcome': {
            'en': 'Welcome',
            'pl': 'Witamy',
            'fr': 'Bienvenue',
            'de': 'Willkommen'
        },
        'crdhldrEmvPleaseWait': {
            'en': 'Please Wait...',
            'pl': 'Proszę czekać...',
            'fr': "S'il vous plaît, attendez...",
            'de': 'Warten Sie mal...'
        },
        'crdhldrEmvApproved': {
            'en': 'Approved.',
            'pl': 'Zgoda.',
            'fr': 'Approuvée',
            'de': 'Genehmigt'
        },
        'rdhldrMsgTransactionAborted': {
            'en': 'Transaction Aborted!',
            'pl': 'Transakcja przerwana!',
            'fr': 'Transaction abandonnée!',
            'de': 'Transaktion abgebrochen!'
        },
        'crdhldrMsgReceiptPrintingFailed': {
            'en': 'Receipt printing failed!',
            'pl': 'Drukowanie paragonu nie powiodło się!',
            'fr': "L'impression du reçu a échoué!",
            'de': 'Belegdruck fehlgeschlagen!',
        },
        'crdhldrMsgTransactionAborted': {
            'en': 'Transaction Aborted',
            'pl': 'Transakcję przerwano',
            'fr': 'Transaction annulée',
            'de': 'Transaktion abgebrochen',
        }
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
        }
    }
    return mapping[msg][language]

def map_output(language, out):
    '''map_output'''
    mapping = {
        'msg': map_cardholder_message,
        'selectedService': map_selected_service,
        'nokReason': map_nokreason,
    }
    return mapping[out[0]](language, out[1])

def map_entry(language, entry):
    '''map_entry'''
    mapping = {
        'msg': map_cardholder_entry
    }
    return mapping[entry[0]](language, entry[1])

def convert_entry(api, payload):
    '''convert_entry'''
    return [{
        'api': api,
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
    mapping = {
        'output': convert_output,
        'entry': convert_entry,
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
    msg = asn.decode('ScapiRequest', apdu, check_constraints=True)
    return asn_nexui.encode('UiRequest', convert_to_request_log_event(msg), check_constraints=True)

def fromnexui(json_msg):
    '''fromnexui'''
    msg = asn_nexui.decode('UiResponse', json_msg, check_constraints=True)
    return asn.encode('ScapiResponse', msg, check_constraints=True)
