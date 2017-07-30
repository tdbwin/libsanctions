import os
import json
import logging
from unicodecsv import DictWriter

from libsanctions.config import DATA_PATH
from libsanctions.model import session
from libsanctions.model import Entity, Address, Alias, Nationality
from libsanctions.model import Identifier, BirthDate, BirthPlace

log = logging.getLogger(__name__)
CSV_EXPORTS = (
    (Entity, 'entities'),
    (Address, 'addresses'),
    (Alias, 'aliases'),
    (Identifier, 'identifiers'),
    (BirthDate, 'birthdates'),
    (BirthPlace, 'birthplaces'),
    (Nationality, 'nationalities')
)


def _make_export_path():
    export_path = os.path.join(DATA_PATH, 'exports')
    try:
        os.makedirs(export_path)
    except:
        pass
    return export_path


def export_csv_tables(archive):
    for model, file_name in CSV_EXPORTS:
        export_csv_table(archive, model, file_name)


def export_csv_table(archive, model, name):
    file_path = os.path.join(_make_export_path(), '%s.csv' % name)
    log.info("Exporting CSV to %s...", file_path)
    writer = None
    with open(file_path, 'w') as fh:
        for obj in session.query(model):
            row = obj.to_row()
            if writer is None:
                writer = DictWriter(fh, row.keys())
                writer.writeheader()
            writer.writerow(row)

    url = archive.upload_file(file_path, mime_type='text/csv')
    if url is not None:
        os.unlink(file_path)


def export_isjon_entity(source, entity_id, fh):
    entity = Entity.by_id(source, entity_id)
    line = json.dumps(entity.to_json())
    fh.write('%s\n' % line)


def export_ijson(archive, source):
    file_path = os.path.join(_make_export_path(), '%s.ijson' % source)
    log.info("Exporting iJSON to %s...", file_path)
    with open(file_path, 'w') as fh:
        for (entity_id,) in session.query(Entity.id):
            export_isjon_entity(source, entity_id, fh)

    url = archive.upload_file(file_path, mime_type='application/json')
    if url is not None:
        os.unlink(file_path)
