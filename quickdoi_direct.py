import requests

def fetch_pubmed_data(doi):
    #base_url = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pmc/"
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    response = requests.get(f"{base_url}?db=pubmed&term=38603491[PMID]&retmode=json")
    print(response)
    print(response.json())  
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_bibtex(entry):
    authors = ' and '.join([f'{a["family"]}, {a["given"]}' for a in entry['author']])
    bibtex_entry = f"""
@article{{{entry['id']},
    author = {{{authors}}},
    title = {{{entry['title']}}},
    journal = {{{entry['container-title']}}},
    year = {{{entry['issued']['date-parts'][0][0]}}},
    DOI = {{{entry['DOI']}}},
}}
"""
    return bibtex_entry

def generate_markdown(entry):
    first_author = f'{entry["author"][0]["family"]}'
    markdown_entry = f"- **{first_author} et al.** - {entry['title']} - *{entry['container-title']}* - {entry['issued']['date-parts'][0][0]}"
    return markdown_entry

def main(dois):
    bib_entries = []
    markdown_entries = []
    for doi in dois:
        print(f"Fetching data for {doi}")
        entry = fetch_pubmed_data(doi)
        if entry:
            bib_entries.append(generate_bibtex(entry))
            markdown_entries.append(generate_markdown(entry))
    
    with open("output.bib", "w") as bib_file:
        bib_file.write("\n".join(bib_entries))
    
    with open("output.md", "w") as md_file:
        md_file.write("\n".join(markdown_entries))

if __name__ == "__main__":
    dois = ["10.1126/science.adn9560", "10.1038/s41556-024-01379-x"]  # DOIs
    main(dois)
