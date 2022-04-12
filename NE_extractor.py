#!/usr/bin/python3

import argparse
from collections import OrderedDict    
import nltk 

def generate_pairs(source):
    result = []
    for p1 in range(len(source)):
        for p2 in range(p1+1,len(source)):
            result.append([source[p1],source[p2]])
    return result

def handle_text(fp):
    edges = {}
    nodes = {}
    mapping = {}
    counter = 0
    for text in fp:
        sentences = nltk.sent_tokenize(text)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

        for tree in chunked_sentences:
            entities = extract_entity_names(tree)
            for n in entities:
                if n not in mapping:
                    mapping[n] = counter
                    nodes[mapping[n]] = 1
                    counter += 1
                else:
                    nodes[mapping[n]] += 1
            if len(entities) >= 2:
                pairs = generate_pairs(entities)
                for pair in pairs:
                    edge = (mapping[pair[0]], mapping[pair[1]])
                    if edge not in edges:
                        edges[edge] = 1
                    else:
                        edges[edge] += 1
    return (mapping, nodes, edges)

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            ne = ' '.join([child[0] for child in t])
            if not ne.isupper():
                entity_names.append(ne)
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    return entity_names

def filter_data(mapping, nodes, edges, max_nodes):
    new_nodes = {}
    new_edges = {}
    new_mapping = {}
    ordered_edges = OrderedDict(sorted(edges.items(), key=lambda t: t[1], reverse=True))
    nr_nodes = 0
    for e in ordered_edges:
        if nr_nodes < max_nodes:
            if e[0] in new_nodes and e[1] in new_nodes:
                None
            elif e[0] in new_nodes:
                new_nodes[e[1]] = nodes[e[1]]
                nr_nodes += 1
            elif e[1] in new_nodes:
                new_nodes[e[0]] = nodes[e[0]]
                nr_nodes += 1
            else:
                new_nodes[e[1]] = nodes[e[1]]
                new_nodes[e[0]] = nodes[e[0]]
                nr_nodes += 2
            new_edges[e] = ordered_edges[e]
    for m in mapping:
        if mapping[m] in new_nodes:
            new_mapping[m] = mapping[m]
    return (new_mapping, new_nodes, new_edges)

def print_nodes(mapping, nodes, output):
    output.write("id,label,weight\n")
    for k in mapping:
        output.write(str(mapping[k]) + "," + str(k) + "," + str(nodes[mapping[k]]) + "\n")

def print_edges(edges, output):
    output.write("source,target,weight\n")
    for k in edges:
        output.write(str(k[0]) + "," + str(k[1]) + "," + str(edges[k]) + "\n")


def main():
    parser = argparse.ArgumentParser(description='Extract NE from text in file.')
    parser.add_argument("-i", "--input", help='input file', required=True)
    parser.add_argument("-n", "--nodes", help='nodes output file', required=True)
    parser.add_argument("-e", "--edges", help='edges output file', required=True)
    parser.add_argument("-m", "--max", help='max nr of nodes', default=200)

    args = parser.parse_args()

    with open(args.input, 'r') as i:
        (mapping, nodes, edges) = handle_text(i)
        (mapping, nodes, edges) = filter_data(mapping, nodes, edges, args.max)
        with open(args.nodes, "w") as n:
            print_nodes(mapping, nodes, n)
            with open(args.edges, "w") as e:
                print_edges(edges, e)

if __name__ == '__main__':
    main()
