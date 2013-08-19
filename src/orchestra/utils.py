

def to_unicode(data):
    	"""Convert a basestring to unicode

    	:param basestring data: data to decode
    	:return: data as unicode
    	:rtype: unicode

    	"""
    	if not isinstance(data, basestring):
		raise ValueError('Basestring expected')
    	if isinstance(data, unicode):
       		return data
    	for encoding in ('utf-8', 'latin-1'):
		try:
			return unicode(data, encoding)
		except UnicodeDecodeError:
	    		pass
    	return unicode(data, 'utf-8', 'replace')
