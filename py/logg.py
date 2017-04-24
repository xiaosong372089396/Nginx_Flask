#!/usr/bin/env python

import logging
import traceback

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    #debug, info, error
    #logging.basicConfig(level=logging.INFO, filemode="w",filename="./log.txt")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s:%(message)s")
    logger.debug('xxxx')
    logger.info('info')
    logger.error('error')
    try:
       1 / 0
    except BaseException as e:
        logger.error(traceback.format_exc())
        logger.error(e)
    pass
                                                            ~           
