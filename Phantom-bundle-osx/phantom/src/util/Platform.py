import sys
import logging


def setMaxfilesopened(limit):
    try:
        if sys.platform == "win32":
            return True
        else:
            import resource
            soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            if soft < limit:
                logging.debug("Current RLIMIT_NOFILE: %s, changing to %s..." % (soft, limit))
                resource.setrlimit(resource.RLIMIT_NOFILE, (soft, hard))
                return True

    except Exception, err:
        logging.error("Failed to modify max files open limit: %s" % err)
        return False
