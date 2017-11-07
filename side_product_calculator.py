#!/usr/bin/env python

# command to run
# confused? run ./side_product_calculator.py --help

# python SCRIPT_NAME ARGS..
# python side_product_calculator.py --seq 'AAAAA' --fin FILE_IN --fout FILE_OUT

import argparse
import re
from mechanize import Browser

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fin', type=str, dest='file_in',
                        help='input file TODO')
    parser.add_argument('--seq', type=str, dest='sequence',
                        help='input file TODO')
    parser.add_argument('--fout', type=str, dest='file_out')
    args = parser.parse_args()
    return args

def get_products(sequence, file_in):
    # open site and get form
    br = Browser()
    br.open("http://peptide.alexmijalis.com/")
    br.select_form(nr=0)


    # get response
    br['text'] = sequence
    br.add_file(open(file_in, 'r'),
                'text/plain/',
                file_in,
                name='file')

    response = br.submit()
    return response.readlines()


def write_output_to_file(file_out, product_list):
    with open(file_out, 'w') as f:
        for line in product_list:
            f.write(line + '\n')


if __name__ == '__main__':
    args = parse_args()

    products = get_products(args.sequence, args.file_in)
    write_output_to_file(args.file_out, products)


    # for list of input, output files
    # with open(file_in, 'r') as f:
    #     for filename in f:
    #         products = get-prof(file)
    #         write(prod)
