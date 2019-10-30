from Bio import SeqIO


def contig_filter(input_path, filtered_path, min_length):
    # Inside {username}ContigFilterImpl#run_{username}ContigFilter_max, after you have fetched the fasta file:
    # Parse the downloaded file in FASTA format
    parsed_assembly = SeqIO.parse(input_path, 'fasta')
    min_length = min_length
    # Keep a list of contigs greater than min_length
    good_contigs = []
    # total contigs regardless of length
    n_total = 0
    # total contigs over the min_length
    n_remaining = 0
    for record in list(parsed_assembly):
        n_total += 1
        if len(record.seq) >= min_length:
            good_contigs.append(record)
            n_remaining += 1
    output = {
        'n_total': n_total,
        'n_remaining': n_remaining
    }
    SeqIO.write(good_contigs, filtered_path, 'fasta')
    return output
