import pysam
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scripts.helper_scripts.run_suprocess import run_cmd

def run_analysis_and_filtering(variant_vcf, min_depth, min_qual, spike_start, spike_end, not_filtered_data, filtered_data, analysed_variants, png_mutation_types, png_depth_distr, png_spike_occurence):
    
    print(f"Start loading vcf file: {variant_vcf}")
    load_vcf(variant_vcf, not_filtered_data)
    print(f"Stored output csv here:{not_filtered_data}")

    print(f"Start filtering data frame based on depth and quality.")
    filter_low_quality(min_depth, min_qual, not_filtered_data, filtered_data)
    print(f"Stored output csv here:{filtered_data}")
    
    print(f"Start filtering based on spike position")
    analyse_spike_mutations(spike_start, spike_end, filtered_data, analysed_variants)
    print(f"Stored output csv here:{analysed_variants}")

    print(f"Start creating analysis plots.")
    cretae_plots(analysed_variants, png_mutation_types, png_depth_distr, png_spike_occurence)

    return 0

def load_vcf(variant_vcf, not_filtered_data):
    # cerate empty list
    variants = []

    # load input data
    vcf = pysam.VariantFile(variant_vcf)

    # load data into dctionary
    for rec in vcf:
        alt_str = None if not rec.alts else str(rec.alts[0]) # get alternative allele(S) else none
        variants.append({
            "pos": rec.pos,                 # position
            "ref": rec.ref,                 # reference allele
            "alts": alt_str,                # alternative allele(S)
            "qual": rec.qual,               # Phred-scaled probability that REF/ALT polymorphism exists at at this site
            "depth": rec.info.get("DP", 0)  # depth of coverage 
        })


    # create data frame of dictionary
    df = pd.DataFrame(variants)

    df_variants = df[~df["alts"].str.contains("<*>", na=False)]
    # safe dataframe to csv file
    df_variants.to_csv(not_filtered_data, index=False)


def filter_low_quality(min_depth, min_qual, not_filtered_data, filtered_data):
    # load data from file
    df = pd.read_csv(not_filtered_data)
    
    # filter dataframe
    df_filt = df[
        (df["depth"] >= min_depth) &
        (df["qual"] >= min_qual)]

    # safe dataframe to csv file
    df_filt.to_csv(filtered_data, index=False)

def analyse_spike_mutations(spike_start, spike_end, filtered_data, analysed_variants):
    # load data from file
    df_filt = pd.read_csv(filtered_data)

    # get only data within spike gene
    df_filt["in_spike"] = (
        (df_filt["pos"] >= spike_start) &
        (df_filt["pos"] <= spike_end)
    )

    # count mutations by type
    df_filt["mutation"] = df_filt["ref"] + "-->" + df_filt["alts"]

    # safe dataframe to csv file
    df_filt.to_csv(analysed_variants, index=False)



def cretae_plots(analysed_variants, png_mutation_types, png_depth_distr, png_spike_occurence):
    # load data from file
    df_filt = pd.read_csv(analysed_variants)

    # print to png file
    plt.figure()
    df_filt["mutation"].value_counts().plot.bar()
    plt.title("Count of occuring Variants")
    plt.ylabel("Count")
    plt.xlabel("Mutation")
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.15)
    plt.savefig(png_mutation_types)
    plt.close()

    # create histogram for depth distribution
    # print to png file
    plt.figure()
    df_filt["depth"].plot.hist(bins=30, edgecolor='black')
    plt.title("Depth distribution")
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.15)
    plt.savefig(png_depth_distr)
    plt.close()

    # compare spike vs non_spike
    # print to png file
    plt.figure(constrained_layout=True)
    legend = ['outside_spike', 'inside_spike']
    df_filt["in_spike"].value_counts().plot.pie(labels =None, autopct='%1.1f%%', startangle=90)
    plt.title("Variants inside and outside of spike region")
    plt.legend(legend, title='Variants')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(png_spike_occurence)
    plt.close()




