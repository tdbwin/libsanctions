import logging
import warnings
# from sqlalchemy.exc import SAWarning

from libsanctions.source import Source  # noqa
from libsanctions.model import Identifier, Entity, Alias, Address, Birth  # noqa

warnings.simplefilter("ignore")

fmt = '[%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=fmt)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
