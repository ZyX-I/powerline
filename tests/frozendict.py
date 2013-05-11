# From http://code.activestate.com/recipes/414283/, modified


class frozendict(dict):
	def _blocked_attribute(obj):
		raise AttributeError('A frozendict cannot be modified.')

	_blocked_attribute = property(_blocked_attribute)

	__delitem__ = __setitem__ = clear = _blocked_attribute
	pop = popitem = setdefault = update = _blocked_attribute

	def copy(self):
		return dict(self)

	def __new__(cls, *args):
		new = dict.__new__(cls)
		dict.__init__(new, *args)
		return new

	def __init__(self, *args):
		pass

	def __hash__(self):
		try:
			return self._cached_hash
		except AttributeError:
			h = self._cached_hash = hash(frozenset(self.items()))
			return h

	def __repr__(self):
		return 'frozendict({0})'.format(super(frozendict, self).__repr__())


def tofrozen(obj):
	try:
		hash(obj)
		return obj
	except TypeError:
		pass
	if type(obj) is dict:
		r = {}
		for k, v in obj.items():
			r[k] = tofrozen(v)
		return frozendict(r)
	elif type(obj) is list:
		return tuple((tofrozen(i) for i in obj))
	return obj
