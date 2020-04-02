"""
Rule Format.

1. desc - Description of the findings

2. type
   a. string
   b. regex

3. match
   a. single_regex - if re.findall(regex1, input)
   b .regex_and - if re.findall(regex1, input) and re.findall(regex2, input)
   c. regex_or - if re.findall(regex1, input) or re.findall(regex2, input)
   d. regex_and_perm - if re.findall(regex, input) and
                       (permission in permission_list_from_manifest)
   e. single_string - if string1 in input
   f. string_and - if (string1 in input) and (string2 in input)
   g. string_or - if (string1 in input) or (string2 in input)
   h. string_and_or -  if (string1 in input) and ((string_or1 in input)
                       or (string_or2 in input))
   i. string_or_and - if (string1 in input) or ((string_and1 in input)
                      and (string_and2 in input))
   j. string_and_perm - if (string1 in input)
                        and (permission in permission_list_from_manifest)
   k. string_or_and_perm - if ((string1 in input) or (string2 in input))
                           and (permission in permission_list_from_manifest)

4. level
   a. high
   b. warning
   c. info
   d. good

5. input_case
   a. upper
   b. lower
   c. exact

6. others
   a. string<no> - string1, string2, string3, string_or1, string_and1
   b. regex<no> - regex1, regex2, regex3
   c. perm - Permission

"""
from StaticAnalyzer.views.matchers import (
    RegexAnd,
    RegexOr,
    SingleRegex,
    SingleString,
    StringAnd,
    StringAndOr,
    StringAndPerm,
    StringOr,
    StringOrAndPerm,
)
from StaticAnalyzer.views.rules_properties import (
    InputCase,
    Level,
)
from StaticAnalyzer.views.standards import (
    CWE,
    OWASP,
    OWASP_MSTG,
)

RULES = [
    {
        'desc': ('Files may contain hardcoded sensitive '
                 'informations like usernames, passwords, keys etc.'),
        'type': SingleRegex.__name__,
        'match': (r'(password\s*=\s*[\'|\"].+[\'|\"]\s{0,5})|'
                  r'(pass\s*=\s*[\'|\"].+[\'|\"]\s{0,5})|'
                  r'(username\s*=\s*[\'|\"].+[\'|\"]\s{0,5})|'
                  r'(secret\s*=\s*[\'|\"].+[\'|\"]\s{0,5})|'
                  r'(key\s*=\s*[\'|\"].+[\'|\"]\s{0,5})'),
        'level': Level.high,
        'input_case': InputCase.lower,
        'cvss': 7.4,
        'cwe': CWE['CWE-312'],
        'owasp': OWASP['m9'],
        'owasp-mstg': OWASP_MSTG['storage-14'],
    },
    {
        'desc': 'IP Address disclosure',
        'type': SingleRegex.__name__,
        'match': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 4.3,
        'cwe': CWE['CWE-200'],
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['code-2'],
    },
    {
        'desc': ('Hidden elements in view can be used to hide'
                 ' data from user. But this data can be leaked'),
        'type': SingleRegex.__name__,
        'match': (r'setVisibility\(View\.GONE\)|'
                  r'setVisibility\(View\.INVISIBLE\)'),
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 4.3,
        'cwe': CWE['CWE-919'],
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['storage-7'],
    },
    {
        'desc': ('The App uses ECB mode in Cryptographic encryption algorithm.'
                 ' ECB mode is known to be weak as it results in the same'
                 ' ciphertext for identical blocks of plaintext.'),
        'type': SingleRegex.__name__,
        'match': r'Cipher\.getInstance\(\s*"\s*AES\/ECB',
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-2'],
    },
    {
        'desc': ('This App uses RSA Crypto without OAEP padding. The purpose'
                 ' of the padding scheme is to prevent a number of attacks on'
                 ' RSA that only work when the encryption is performed'
                 ' without padding.'),
        'type': SingleRegex.__name__,
        'match': r'cipher\.getinstance\(\s*"rsa/.+/nopadding',
        'level': Level.high,
        'input_case': InputCase.lower,
        'cvss': 5.9,
        'cwe': CWE['CWE-780'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-3'],
    },
    {
        'desc': ('Insecure Implementation of SSL. Trusting all the '
                 'certificates or accepting self signed certificates'
                 ' is a critical Security Hole. This application is'
                 ' vulnerable to MITM attacks'),
        'type': RegexAnd.__name__,
        'match': [r'javax\.net\.ssl',
                  (r'TrustAllSSLSocket-Factory|AllTrustSSLSocketFactory|'
                   r'NonValidatingSSLSocketFactory|'
                   r'net\.SSLCertificateSocketFactory|'
                   r'ALLOW_ALL_HOSTNAME_VERIFIER|'
                   r'\.setDefaultHostnameVerifier\(|'
                   r'NullHostnameVerifier\(')],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.4,
        'cwe': CWE['CWE-295'],
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-3'],
    },
    {
        'desc': ('WebView load files from external storage. Files in external'
                 ' storage can be modified by any application.'),
        'type': RegexAnd.__name__,
        'match': [r'\.loadUrl\(.*getExternalStorageDirectory\(',
                  r'webkit\.WebView'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.0,
        'cwe': CWE['CWE-919'],
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-6'],
    },
    {
        'desc': 'The file is World Readable. Any App can read from the file',
        'type': RegexOr.__name__,
        'match': [r'MODE_WORLD_READABLE|Context\.MODE_WORLD_READABLE',
                  r'openFileOutput\(\s*".+"\s*,\s*1\s*\)'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 4.0,
        'cwe': CWE['CWE-276'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-2'],
    },
    {
        'desc': 'The file is World Writable. Any App can write to the file',
        'type': RegexOr.__name__,
        'match': [r'MODE_WORLD_WRITABLE|Context\.MODE_WORLD_WRITABLE',
                  r'openFileOutput\(\s*".+"\s*,\s*2\s*\)'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 6.0,
        'cwe': CWE['CWE-276'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-2'],
    },
    {
        'desc': ('The file is World Readable and Writable. '
                 'Any App can read/write to the file'),
        'type': SingleRegex.__name__,
        'match': r'openFileOutput\(\s*".+"\s*,\s*3\s*\)',
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 6.0,
        'cwe': CWE['CWE-276'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-2'],
    },
    {
        'desc': 'Weak Hash algorithm used',
        'type': SingleRegex.__name__,
        'match': (r'getInstance(\"md4\")|getInstance(\"rc2\")|'
                  r'getInstance(\"rc4\")|getInstance(\"RC4\")|'
                  r'getInstance(\"RC2\")|getInstance(\"MD4\")'),
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.4,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4'],
    },
    {
        'desc': 'MD5 is a weak hash known to have hash collisions.',
        'type': SingleRegex.__name__,
        'match': (r'MessageDigest\.getInstance\(\"*MD5\"*\)|'
                  r'MessageDigest\.getInstance\(\"*md5\"*\)|'
                  r'DigestUtils\.md5\('),
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.4,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4'],
    },
    {
        'desc': 'SHA-1 is a weak hash known to have hash collisions.',
        'type': SingleRegex.__name__,
        'match': (r'MessageDigest\.getInstance\(\"*SHA-1\"*\)|'
                  r'MessageDigest\.getInstance\(\"*sha-1\"*\)|'
                  r'DigestUtils\.sha\('),
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-327'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-4'],
    },
    {
        'desc': ('App can write to App Directory. '
                 'Sensitive Information should be encrypted.'),
        'type': SingleRegex.__name__,
        'match': r'MODE_PRIVATE|Context\.MODE_PRIVATE',
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 3.9,
        'cwe': CWE['CWE-276'],
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-14'],
    },
    {
        'desc': 'The App uses an insecure Random Number Generator.',
        'type': SingleRegex.__name__,
        'match': r'\bjava\.util\.Random\b',
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.5,
        'cwe': CWE['CWE-330'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-6'],
    },
    {
        'desc': ('The App logs information. '
                 'Sensitive information should never be logged.'),
        'type': SingleRegex.__name__,
        'match': (r'Log\.(v|d|i|w|e|f|s)|'
                  r'System\.out\.print|System\.err\.print'),
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 7.5,
        'cwe': CWE['CWE-532'],
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-3'],
    },
    {
        'desc': ('This App uses Java Hash Code. It\'s a weak hash function and'
                 ' should never be used in Secure Crypto Implementation.'),
        'type': SingleString.__name__,
        'match': '.hashCode()',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 2.3,
        'cwe': CWE['CWE-327'],
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['crypto-4'],
    },
    {
        'desc': ('These activities prevent '
                 'screenshot when they go to background.'),
        'type': SingleString.__name__,
        'match': 'LayoutParams.FLAG_SECURE',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-9'],
    },
    {
        'desc': 'This App uses SQL Cipher. But the secret may be hardcoded.',
        'type': SingleString.__name__,
        'match': 'SQLiteOpenHelper.getWritableDatabase(',
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['crypto-1'],
    },
    {
        'desc': 'This app has capabilities to prevent tapjacking attacks.',
        'type': SingleString.__name__,
        'match': 'setFilterTouchesWhenObscured(true)',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['platform-9'],
    },
    {
        'desc': ('App can read/write to External Storage. '
                 'Any App can read data written to External Storage.'),
        'type': StringOrAndPerm.__name__,
        'match': ['.getExternalStorage', '.getExternalFilesDir('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.5,
        'perm': 'android.permission.WRITE_EXTERNAL_STORAGE',
        'cwe': CWE['CWE-276'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-2'],
    },
    {
        'desc': ('App creates temp file. Sensitive '
                 'information should never be written into a temp file.'),
        'type': StringAndPerm.__name__,
        'match': '.createTempFile(',
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.5,
        'perm': 'android.permission.WRITE_EXTERNAL_STORAGE',
        'cwe': CWE['CWE-276'],
        'owasp': OWASP['m2'],
        'owasp-mstg': OWASP_MSTG['storage-2'],
    },
    {
        'desc': ('Insecure WebView Implementation. Execution of user'
                 ' controlled code in WebView is a critical Security Hole.'),
        'type': StringAnd.__name__,
        'match': ['setJavaScriptEnabled(true)', '.addJavascriptInterface('],
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 8.8,
        'cwe': CWE['CWE-749'],
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['platform-7'],
    },
    {
        'desc': ('This App uses SQL Cipher. SQLCipher '
                 'provides 256-bit AES encryption to sqlite database files.'),
        'type': StringAnd.__name__,
        'match': ['SQLiteDatabase.loadLibs(', 'net.sqlcipher.'],
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['crypto-1'],
    },
    {
        'desc': 'This App download files using Android Download Manager',
        'type': StringAnd.__name__,
        'match': ['android.app.DownloadManager',
                  'getSystemService(DOWNLOAD_SERVICE)'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': '',
    },
    {
        'desc': 'This App use Realm Database with encryption.',
        'type': StringAnd.__name__,
        'match': ['io.realm.Realm', '.encryptionKey('],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['crypto-1'],
    },
    {
        'desc': ('The App may use weak IVs like '
                 '"0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00" or '
                 '"0x01,0x02,0x03,0x04,0x05,0x06,0x07". '
                 'Not using a random IV makes the resulting '
                 'ciphertext much more predictable and '
                 'susceptible to a dictionary attack.'),
        'type': StringOr.__name__,
        'match': ['0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00',
                  '0x01,0x02,0x03,0x04,0x05,0x06,0x07'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 9.8,
        'cwe': CWE['CWE-329'],
        'owasp': OWASP['m5'],
        'owasp-mstg': OWASP_MSTG['crypto-3'],
    },
    {
        'desc': 'Remote WebView debugging is enabled.',
        'type': StringAnd.__name__,
        'match': ['.setWebContentsDebuggingEnabled(true)', 'WebView'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.4,
        'cwe': CWE['CWE-919'],
        'owasp': OWASP['m1'],
        'owasp-mstg': OWASP_MSTG['resilience-2'],
    },
    {
        'desc': ('This app listens to Clipboard changes.'
                 ' Some malwares also listen to Clipboard changes.'),
        'type': StringAnd.__name__,
        'match': ['content.ClipboardManager', 'OnPrimaryClipChangedListener'],
        'level': Level.warning,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['platform-4'],
    },
    {
        'desc': ('This App copies data to clipboard. Sensitive data should'
                 ' not be copied to clipboard as other'
                 ' applications can access it.'),
        'type': StringAnd.__name__,
        'match': ['content.ClipboardManager', 'setPrimaryClip('],
        'level': Level.info,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-10'],
    },
    {
        'desc': ('Insecure WebView Implementation. WebView ignores SSL'
                 ' Certificate errors and accept any SSL Certificate.'
                 ' This application is vulnerable to MITM attacks'),
        'type': StringAnd.__name__,
        'match': ['onReceivedSslError(WebView', '.proceed();'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.4,
        'cwe': CWE['CWE-295'],
        'owasp': OWASP['m3'],
        'owasp-mstg': OWASP_MSTG['network-3'],
    },
    {
        'desc': ('App uses SQLite Database and execute raw SQL query. '
                 'Untrusted user input in raw SQL queries can cause'
                 ' SQL Injection. Also sensitive information should'
                 ' be encrypted and written to the database.'),
        'type': StringAndOr.__name__,
        'match': ['android.database.sqlite', ['rawQuery(', 'execSQL(']],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 5.9,
        'cwe': CWE['CWE-89'],
        'owasp': OWASP['m7'],
        'owasp-mstg': '',
    },
    {
        'desc': 'This App detects frida server.',
        'type': StringAndOr.__name__,
        'match': ['fridaserver', ['27047', 'REJECT', 'LIBFRIDA']],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-4'],
    },
    {
        'desc': ('This App uses an SSL Pinning Library '
                 '(org.thoughtcrime.ssl.pinning) to '
                 'prevent MITM attacks in secure'
                 ' communication channel.'),
        'type': StringAndOr.__name__,
        'match': ['org.thoughtcrime.ssl.pinning',
                  ['PinningHelper.getPinnedHttpsURLConnection',
                   'PinningHelper.getPinnedHttpClient',
                   'PinningSSLSocketFactory(']],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['network-4'],
    },
    {
        'desc': ('This App has capabilities to prevent against'
                 ' Screenshots from Recent Task History/ Now On Tap etc.'),
        'type': StringAndOr.__name__,
        'match': ['.FLAG_SECURE',
                  ['getWindow().setFlags(', 'getWindow().addFlags(']],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['storage-9'],
    },
    {
        'desc': ('DexGuard Debug Detection code to detect'
                 ' whether an App is debuggable or not is identified.'),
        'type': StringAnd.__name__,
        'match': ['import dexguard.util', 'DebugDetector.isDebuggable'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-2'],
    },
    {
        'desc': 'DexGuard Debugger Detection code is identified.',
        'type': StringAnd.__name__,
        'match': ['import dexguard.util', 'DebugDetector.isDebuggerConnected'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-2'],
    },
    {
        'desc': 'DexGuard Emulator Detection code is identified.',
        'type': StringAnd.__name__,
        'match': ['import dexguard.util',
                  'EmulatorDetector.isRunningInEmulator'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-5'],
    },
    {
        'desc': ('DexGuard code to detect whether the App'
                 ' is signed with a debug key or not is identified.'),
        'type': StringAnd.__name__,
        'match': ['import dexguard.util',
                  'DebugDetector.isSignedWithDebugKey'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['code-2'],
    },
    {
        'desc': 'DexGuard Root Detection code is identified.',
        'type': StringAnd.__name__,
        'match': ['import dexguard.util', 'RootDetector.isDeviceRooted'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-1'],
    },
    {
        'desc': 'DexGuard App Tamper Detection code is identified.',
        'type': StringAnd.__name__,
        'match': ['import dexguard.util', 'TamperDetector.checkApk'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-3'],
    },
    {
        'desc': ('DexGuard Signer Certificate'
                 ' Tamper Detection code is identified.'),
        'type': StringAnd.__name__,
        'match': ['import dexguard.util',
                  'TCertificateChecker.checkCertificate'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-3'],
    },
    {
        'desc': 'The App may use package signature for tamper detection.',
        'type': StringAnd.__name__,
        'match': ['PackageManager.GET_SIGNATURES', 'getPackageName('],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-3'],
    },
    {
        'desc': 'This App uses SafetyNet API.',
        'type': SingleString.__name__,
        'match': 'com.google.android.gms.safetynet.SafetyNetApi',
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-7'],
    },
    {
        'desc': 'This App may request root (Super User) privileges.',
        'type': StringOr.__name__,
        'match': ['com.noshufou.android.su',
                  'com.thirdparty.superuser',
                  'eu.chainfire.supersu',
                  'com.koushikdutta.superuser',
                  'eu.chainfire.'],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': CWE['CWE-250'],
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-1'],
    },
    {
        'desc': 'This App may have root detection capabilities.',
        'type': StringOr.__name__,
        'match': ['.contains("test-keys")',
                  '/system/app/Superuser.apk',
                  'isDeviceRooted()',
                  '/system/bin/failsafe/su',
                  '/system/sd/xbin/su',
                  '"/system/xbin/which", "su"',
                  'RootTools.isAccessGiven()'],
        'level': Level.good,
        'input_case': InputCase.exact,
        'cvss': 0,
        'cwe': '',
        'owasp': '',
        'owasp-mstg': OWASP_MSTG['resilience-1'],
    },
    {
        'desc': ('The app uses jackson deserialization library'
                 'Deserialization of untrusted input can result in'
                 'arbitary code execution'),
        'type': StringAnd.__name__,
        'match': ['com.fasterxml.jackson.databind.ObjectMapper',
                  '.enableDefaultTyping('],
        'level': Level.high,
        'input_case': InputCase.exact,
        'cvss': 7.5,
        'cwe': CWE['CWE-502'],
        'owasp': OWASP['m7'],
        'owasp-mstg': OWASP_MSTG['platform-8'],
    },
]