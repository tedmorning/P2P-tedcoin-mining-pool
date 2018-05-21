ident = '$Id: Config.py 1298 2006-11-07 00:54:15Z sanxiyn $'
from version import __version__

import socket
from types import *

from NS import NS

################################################################################
# Configuration class
################################################################################


class SOAPConfig:
    __readonly = ('SSLserver', 'SSLclient', 'GSIserver', 'GSIclient')
    class SSLconfig:
        __slots__ = ('key_file', 'cert_file')
        key_file = None
        cert_file = None

    def __init__(self, config = None, **kw):
        d = self.__dict__

        if config:
            if not isinstance(config, SOAPConfig):
                raise AttributeError, \
                    "initializer must be SOAPConfig instance"

            s = config.__dict__

            for k, v in s.items():
                if k[0] != '_':
                    d[k] = v
        else:
            # Setting debug also sets returnFaultInfo,
            # dumpHeadersIn, dumpHeadersOut, dumpSOAPIn, and dumpSOAPOut
            self.debug = 0
            self.dumpFaultInfo = 1
            # Setting namespaceStyle sets typesNamespace, typesNamespaceURI,
            # schemaNamespace, and schemaNamespaceURI
            self.namespaceStyle = '1999'
            self.strictNamespaces = 0
            self.typed = 1
            self.buildWithNamespacePrefix = 1
            self.returnAllAttrs = 0

            # Strict checking of range for floats and doubles
            self.strict_range = 0

            # Default encoding for dictionary keys
            self.dict_encoding = 'ascii'

            # New argument name handling mechanism.  See
            # README.MethodParameterNaming for details
            self.specialArgs = 1

            # If unwrap_results=1 and there is only element in the struct,
            # SOAPProxy will assume that this element is the result
            # and return it rather than the struct containing it.
            # Otherwise SOAPproxy will return the struct with all the
            # elements as attributes.
            self.unwrap_results = 1

            # Automatically convert SOAP complex types, and
            # (recursively) public contents into the corresponding
            # python types. (Private subobjects have names that start
            # with '_'.)
            #
            # Conversions:
            # - faultType    --> raise python exception
            # - arrayType    --> array
            # - compoundType --> dictionary
            #
            self.simplify_objects = 0

            # Per-class authorization method.  If this is set, before
            # calling a any class method, the specified authorization
            # method will be called.  If it returns 1, the method call
            # will proceed, otherwise the call will throw with an
            # authorization error.
            self.authMethod = None

            # Globus Support if pyGlobus.io available
            try:
                from pyGlobus import io;
                d['GSIserver'] = 1
                d['GSIclient'] = 1
            except:
                d['GSIserver'] = 0
                d['GSIclient'] = 0


            # Server SSL support if M2Crypto.SSL available
            try:
                from M2Crypto import SSL
                d['SSLserver'] = 1
            except:
                d['SSLserver'] = 0

            # Client SSL support if socket.ssl available
            try:
                from socket import ssl
                d['SSLclient'] = 1
            except:
                d['SSLclient'] = 0

            # Cert support
            if d['SSLclient'] or d['SSLserver']:
                d['SSL'] = self.SSLconfig()

        for k, v in kw.items():
            if k[0] != '_':
                setattr(self, k, v)

    def __setattr__(self, name, value):
        if name in self.__readonly:
            raise AttributeError, "readonly configuration setting"

        d = self.__dict__

        if name in ('typesNamespace', 'typesNamespaceURI',
                    'schemaNamespace', 'schemaNamespaceURI'):

            if name[-3:] == 'URI':
                base, uri = name[:-3], 1
            else:
                base, uri = name, 0

            if type(value) == StringType:
                if NS.NSMAP.has_key(value):
                    n = (value, NS.NSMAP[value])
                elif NS.NSMAP_R.has_key(value):
                    n = (NS.NSMAP_R[value], value)
                else:
                    raise AttributeError, "unknown namespace"
            elif type(value) in (ListType, TupleType):
                if uri:
                    n = (value[1], value[0])
                else:
                    n = (value[0], value[1])
            else:
                raise AttributeError, "unknown namespace type"

            d[base], d[base + 'URI'] = n

            try:
                d['namespaceStyle'] = \
                    NS.STMAP_R[(d['typesNamespace'], d['schemaNamespace'])]
            except:
                d['namespaceStyle'] = ''

        elif name == 'namespaceStyle':
            value = str(value)

            if not NS.STMAP.has_key(value):
                raise AttributeError, "unknown namespace style"

            d[name] = value
            n = d['typesNamespace'] = NS.STMAP[value][0]
            d['typesNamespaceURI'] = NS.NSMAP[n]
            n = d['schemaNamespace'] = NS.STMAP[value][1]
            d['schemaNamespaceURI'] = NS.NSMAP[n]

        elif name == 'debug':
            d[name]                     = \
                d['returnFaultInfo']    = \
                d['dumpHeadersIn']      = \
                d['dumpHeadersOut']     = \
                d['dumpSOAPIn']         = \
                d['dumpSOAPOut']        = value

        else:
            d[name] = value


Config = SOAPConfig()
