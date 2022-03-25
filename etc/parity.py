from traitlets import HasTraits, TraitError, Int, Bool, validate


class Parity(HasTraits):
    data = Int()
    parity = Int()

    @validate('data')
    def _valid_data(self, proposal):
        if proposal['value'] % 2 != self.parity:
            raise TraitError('data and parity should be consistent')
        return proposal['value']

    @validate('parity')
    def _valid_parity(self, proposal):
        parity = proposal['value']
        if parity not in [0, 1]:
            raise TraitError('parity should be 0 or 1')
        if self.data % 2 != parity:
            raise TraitError('data and parity should be consistent')
        return proposal['value']


parity_check = Parity(data=2)

# Changing required parity and value together while holding cross validation
with parity_check.hold_trait_notifications():
    parity_check.data = 1
    parity_check.parity = 1
