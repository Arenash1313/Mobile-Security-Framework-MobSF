from StaticAnalyzer.views.ios.rules.modified import modified_common_rules

from StaticAnalyzer.views.match_strategy import (
    SingleRegex,
    RegexOr,
    RegexAnd,
    SingleString,
    StringOr,
    StringAnd,
    StringAndOr,
    StringAndNot
)
from StaticAnalyzer.views.rules_properties import (
    InputCase,
    Level
)

from StaticAnalyzer.views.standards import (
    CWE,
    OWASP,
    OWASP_MSTG,
)

SWIFT_RULES = modified_common_rules.COMMON_RULES + [
    {
        'desc': ('The App logs information. '
                 'Sensitive information should never be logged.'),
        'type': SingleRegex.__name__,
        'match': r'(print|NSLog|os_log|OSLog|os_signpost)\(.*\)',
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 7.5,
        'cwe': CWE['CWE-532'],
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-3']
    },
    {
        'desc': 'SHA1 is a weak hash known to have hash collisions.',
        'type': RegexOr.__name__,
        'match': [r'(?i)SHA1\(', r'CC_SHA1\('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4']
    },
    {
        'desc': 'MD2 is a weak hash known to have hash collisions.',
        'type': RegexOr.__name__,
        'match': [r'(?i)MD2\(', r'CC_MD2\('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4']
    },
    {
        'desc': 'MD4 is a weak hash known to have hash collisions.',
        'type': RegexOr.__name__,
        'match': [r'(?i)MD4\(', r'CC_MD4\('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4']
    },
    {
        'desc': 'MD5 is a weak hash known to have hash collisions.',
        'type': RegexOr.__name__,
        'match': [r'(?i)MD5\(', r'CC_MD5\('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4']
    },
    {
        'desc': 'MD6 is a weak hash known to have hash collisions.',
        'type': RegexOr.__name__,
        'match': [r'(?i)MD6\(', r'CC_MD6\('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4']
    },
    {
        'desc': 'This App may have custom keyboards disabled.',
        'type': SingleRegex.__name__,
        'match': r'extensionPointIdentifier == .*\.keyboard',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['platform-11']
    },
    {
        'desc': 'Keyboard cache should be disabled for all sensitve data inputs.',
        'type': SingleRegex.__name__,
        'match': r'.autocorrectionType = .no',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-5']
    },
    {
        'desc': ('It is recommended to use WKWebView instead '
                 'of SFSafariViewController or UIViewView.'),
        'type': SingleRegex.__name__,
        'match': r'UIViewView|SFSafariViewController',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-5']
    },
    {
        'desc': 'This App may have Reverse enginering detection capabilities.',
        'type': StringAnd.__name__,
        'match': ['\"FridaGadget\"', '\"cynject\"', '\"libcycript\"', '\"/usr/sbin/frida-server\"'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-4']
    },
    {
        'desc': 'This App may have Emulator detection capabilities.',
        'type': SingleString.__name__,
        'match': '\"SIMULATOR_DEVICE_NAME\"',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-5']
    },
    {
        'desc': ('Biometric authentication should be based '
                 'on Keychain, not based on bool.'),
        'type': SingleRegex.__name__,
        'match': r'\.evaluatePolicy\(.deviceOwnerAuthentication',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['auth-8']
    },
    {
        'desc': 'The file has no special protections associated with it.',
        'type': SingleRegex.__name__,
        'match': r'(?i)\.noFileProtection',
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 4.3,
        'cwe': CWE['CWE-311'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-1']
    },
    {
        'desc': ('This application uses UIPasteboard, improper use '
                 'of this class can lead to security issues.'),
        'type': SingleString.__name__,
        'match': 'UIPasteboard',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-4']
    },
    {
        'desc': 'Usage of generalPasteboard should be avoided.',
        'type': SingleString.__name__,
        'match': 'UIPasteboard.generalPasteboard',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-4']
    },
    {
        'desc': ('The app should not export sensitive functionality via '
                 'custom URL schemes, unless these '
                 'mechanisms are properly protected.'),
        'type': SingleString.__name__,
        'match': 'CFBundleURLSchemes',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-3']
    },
    {
        'desc': 'Some UI controls have secure text entry configured.',
        'type': SingleString.__name__,
        'match': '.secureTextEntry = true',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-5']
    },
    {
        'desc': 'This App may have Certificate Pinning mechanism.',
        'type': StringOr.__name__,
        'match': ['PinnedCertificatesTrustEvaluator', 'TrustKit.initSharedInstance'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': CWE['CWE-295'],
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-4']
    },
    {
        'desc': ('App uses Realm Database. '
                 'Sensitive Information should be encrypted.'),
        'type': SingleString.__name__,
        'match': 'realm.write',
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': CWE['CWE-311'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-14']
    },
    {
        'desc': ('App uses CoreData Database. '
                 'Sensitive Information should be encrypted.'),
        'type': StringAnd.__name__,
        'match': ['NSManagedObjectContext', '.save()'],
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': CWE['CWE-311'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-14']
    },
    {
        'desc': 'Used Realm database has configured encryption.',
        'type': StringAnd.__name__,
        'match': ['Realm.Configuration(encryptionKey:', 'Realm(configuration:'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': CWE['CWE-311'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-14']
    },
    {
        'desc': 'Copy feature may be disabled in some UI controls.',
        'type': RegexAnd.__name__,
        'match': [r'canPerformAction', r'UIResponderStandardEditActions\.copy|\.copy'],
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': ''
    },
    {
        'desc': 'Opening App with URLs can lead to potencial security leaks.',
        'type': SingleRegex.__name__,
        'match': r'func application\(.*open url: URL',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': CWE['CWE-939'],
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-3']
    },
    {
        'desc': ('Sensitive data shouldn\'t be included in backups generated '
                 'by the mobile operating system.'),
        'type': SingleRegex.__name__,
        'match': r'kSecAttrAccessible[a-zA-Z]*ThisDeviceOnly',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-8']
    },
    {
        'desc': ('JavaScript should be disabled in WebViews unless '
                 'explicitly required.'),
        'type': StringAndNot.__name__,
        'match': ['WKWebView', '.javaScriptEnabled = false'],
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['platform-5']
    },
    {
        'desc': 'TLS 1.3 should be used. Detected old version',
        'type': StringAndOr.__name__,
        'match': ['.TLSMinimumSupportedProtocolVersion',
                  ['tls_protocol_version_t.TLSv10', 'tls_protocol_version_t.TLSv11']],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.5,
        'cwe': CWE['CWE-757'],
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-2']
    },
    {
        'desc': 'TLS 1.3 should be used. Detected old version - TLS 1.2.',
        'type': StringAnd.__name__,
        'match': ['.TLSMinimumSupportedProtocolVersion', 'tls_protocol_version_t.TLSv12'],
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-2']
    },
    {
        'desc': 'DTLS 1.2 should be used. Detected old version - DTLS 1.0.',
        'type': StringAnd.__name__,
        'match': ['.TLSMinimumSupportedProtocolVersion', 'tls_protocol_version_t.DTLSv10'],
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-2']
    },
    {
        'desc': ('Use of deprecated property tlsMinimumSupportedProtocol. '
                 'To avoid potential security risks, use '
                 'tlsMinimumSupportedProtocolVersion'),
        'type': SingleString.__name__,
        'match': '.tlsMinimumSupportedProtocol',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0.0,
        'cwe': '',
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-2']
    }
]
