# coding: utf-8
import logging
from openerp import api, models
from openerp.exceptions import AccessError
from openerp.models import BaseModel, FailedValue, PREFETCH_MAX


@api.multi
def _prefetch_field(self, field):
    """ Slightly modified version of this method in openerp/models.py.
    Modifications are marked as such. """
    if True:  # keep indentation level of original method

        records = self._in_cache_without(field)

        # MODIFICATION START
        prefetch_max = PREFETCH_MAX
        custom_max = self._context.get(
            'prefetch_max_%s' % self._name.replace('.', '_'))
        if custom_max:
            prefetch_max = custom_max
        # MODIFICATION END

        if len(records) > prefetch_max:
            records = records[:prefetch_max] | self

        # determine which fields can be prefetched
        if not self.env.in_draft and \
                self._context.get('prefetch_fields', True) and \
                self._columns[field.name]._prefetch:
            # prefetch all classic and many2one fields that the user can access
            fnames = {fname
                for fname, fcolumn in self._columns.iteritems()
                if fcolumn._prefetch
                if not fcolumn.groups or self.user_has_groups(fcolumn.groups)
            }
        elif self._columns[field.name]._multi:
            # prefetch all function fields with the same value for 'multi'
            multi = self._columns[field.name]._multi
            fnames = {fname
                for fname, fcolumn in self._columns.iteritems()
                if fcolumn._multi == multi
                if not fcolumn.groups or self.user_has_groups(fcolumn.groups)
            }
        else:
            fnames = {field.name}

        # important: never prefetch fields to recompute!
        get_recs_todo = self.env.field_todo
        for fname in list(fnames):
            if get_recs_todo(self._fields[fname]):
                if fname == field.name:
                    records -= get_recs_todo(field)
                else:
                    fnames.discard(fname)

        # fetch records with read()
        assert self in records and field.name in fnames
        result = []
        try:
            result = records.read(list(fnames), load='_classic_write')
        except AccessError:
            # not all records may be accessible, try with only current record
            result = self.read(list(fnames), load='_classic_write')

        # check the cache, and update it if necessary
        if field not in self._cache:
            for values in result:
                record = self.browse(values.pop('id'))
                record._cache.update(record._convert_to_cache(values, validate=False))
            if not self._cache.contains(field):
                e = AccessError("No value found for %s.%s" % (self, field.name))
                self._cache[field] = FailedValue(e)


class BasemodelMonkeyPatchPrefetchField(models.AbstractModel):
    _name = 'monkeypatch.prefetch.field'

    def _register_hook(self, cr):
        """ Replace the core version of BaseModel._prefetch_field with
        our modified version defined above """
        if not hasattr(BaseModel, '_roetz_prefetch_field'):
            logging.getLogger(__name__).info(
                'Installing monkeypatch on BaseModel::_prefetch_field'
            )
            BaseModel._roetz_prefetch_field = \
                BaseModel._prefetch_field
            BaseModel._prefetch_field = _prefetch_field
        return super(BasemodelMonkeyPatchPrefetchField, self)._register_hook(
            cr)
