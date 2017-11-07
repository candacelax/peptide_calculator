#!/usr/bin/env python

import argparse
from mechanize import Browser
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fin', type=str, dest='file_in',
                        help='file containing list of input files')
    parser.add_argument('--seq', type=str, dest='sequence',
                        help='amino acid sequence (note: use one letter abbreviations)')
    parser.add_argument('--fout', type=str, dest='file_out',
                        help='output file for products')
    args = parser.parse_args()

    # check file type of input file
    if not re.match('.*\.cef', args.file_in):
        raise ValueError('Invalid input file type')
    return args


def get_products(sequence, file_in):
    # open site and get form
    br = Browser()
    br.open("http://peptide.alexmijalis.com/")
    br.select_form(nr=0) # there's only a single form

    # get response
    # TODO make action statement for input arg

    br['text'] = sequence
    br.add_file(open(file_in, 'r'),
                'text/plain/',
                file_in,
                name='file')

    
    response = br.submit()
    return response.readlines()


def write_output_to_file(file_out, product_list):
    column_counter=1
    with open(file_out, 'w') as f:
        for l in product_list:
            if re.match('.*<td>.*', l):
                cleaned = clean_results(l) \
                        + ('\n' \
                           if column_counter % 6 == 0 \
                           else ',')
                f.write(cleaned)
                column_counter+=1


def clean_results(line):
    # remove table formatting
    return re.sub('<td>|</td>|^\s+|$\s+', '', line)
    
        
if __name__ == '__main__':
    args = parse_args()
    products = get_products(args.sequence, args.file_in)
    write_output_to_file(args.file_out, products)
