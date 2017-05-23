#!/usr/bin/env python

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Test a Fast R-CNN network on an image database."""
import sys,os
this_dir = os.path.dirname(__file__)
sys.path.insert(0, this_dir + '/..')
# import _init_paths
from lib.fast_rcnn.test import test_net
from lib.fast_rcnn.config import cfg, cfg_from_file
from lib.datasets.factory import get_imdb
from lib.networks.factory import get_network
import argparse
import pprint
import time
import tensorflow as tf

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Test a Fast R-CNN network')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU id to use',
                        default=0, type=int)
    parser.add_argument('--def', dest='prototxt',
                        help='prototxt file defining the network',
                        default=None, type=str)
    parser.add_argument('--weights', dest='model',
                        help='model to test',
                        default=None, type=str)
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file', default=None, type=str)
    parser.add_argument('--wait', dest='wait',
                        help='wait until net file exists',
                        default=True, type=bool)
    parser.add_argument('--imdb', dest='imdb_name',
                        help='dataset to test',
                        default='voc_2007_test', type=str)
    parser.add_argument('--comp', dest='comp_mode', help='competition mode',
                        action='store_true')
    parser.add_argument('--network', dest='network_name',
                        help='name of the network',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)

    print('Using config:')
    pprint.pprint(cfg)

    while not os.path.exists(args.model) and args.wait:
        print(('Waiting for {} to exist...'.format(args.model)))
        time.sleep(1000)

    weights_filename = os.path.splitext(os.path.basename(args.model))[0]

    imdb = get_imdb(args.imdb_name)
    imdb.competition_mode(args.comp_mode)

    device_name = '/gpu:{:d}'.format(args.gpu_id)
    print(device_name)

    network = get_network(args.network_name)
    print(('Use network `{:s}` in training'.format(args.network_name)))

    cfg.GPU_ID = args.gpu_id

    # start a session
    saver = tf.train.Saver()
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    saver.restore(sess, args.model)
    print((('Loading model weights from {:s}').format(args.model)))

    test_net(sess, network, imdb, weights_filename)
