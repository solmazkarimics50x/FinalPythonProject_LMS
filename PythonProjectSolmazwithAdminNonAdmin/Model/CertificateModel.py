class Certificate:
    def __init__(self,certificate_id = None,certificate_title='',vendor = ''):
        self.certificate_id = certificate_id
        self.certificate_title = certificate_title
        self.vendor = vendor




class CertificateIdDelete:
    def __init__(self, certificate_id = None):
        self.certificate_id = certificate_id