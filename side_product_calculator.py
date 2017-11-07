#!/usr/bin/env python

import argparse
from mechanize import Browser

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fin', type=str, dest='file_in',
                        help='file containing list of input files')
    parser.add_argument('--seq', type=str, dest='sequence',
                        help='amino acid sequence (note: use one letter abbreviations)')
    parser.add_argument('--fout', type=str, dest='file_out',
                        help='output file for products')
    args = parser.parse_args()
    return args

def get_products(sequence, file_in):
    # open site and get form
    br = Browser()
    br.open("http://peptide.alexmijalis.com/")
    br.select_form(nr=0) # there's only a single form

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
        map(lambda l: f.write(l + 'n'),
            product_list)


if __name__ == '__main__':
    args = parse_args()
    products = get_products(args.sequence, args.file_in)
    write_output_to_file(args.file_out, products)
