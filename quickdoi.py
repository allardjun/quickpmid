from pymed import PubMed
import json

def generate_bibtex(article):
    authors = ' and '.join([f'{a.lastname}' for a in article.authors])
    bibtex_entry = f"""
@article{{{article.pubmedId},
    author = {{{authors}}},
    title = {{{article.title}}},
    journal = {{{article.journal}}},
    year = {{{article.publicationDate.year}}},
    DOI = {{{article.doi or 'N/A'}}},
}}
"""
    return bibtex_entry.strip()

def generate_markdown(article):
    if article.authors:
        first_author = f'{article.authors[0].lastname}'
    else:
        first_author = "Unknown Author"
    markdown_entry = f"- **{first_author} et al.** - {article.title} - *{article.journal}* - {article.publicationDate.year}"
    return markdown_entry

def main(dois):
    pubmed = PubMed(tool="for_my_lab", email="jun.allard@uci.edu")
    bib_entries = []
    markdown_entries = []

    for doi in dois:
        query = f"{doi}[DOI]"  # Corrected query format
        results = pubmed.query(query, max_results=1)
        for article in results:
            print(article.doi)
            bib_entries.append(generate_bibtex(article))
            markdown_entries.append(generate_markdown(article))
    
    with open("output.bib", "w") as bib_file:
        bib_file.write("\n\n".join(bib_entries))
    
    with open("output.md", "w") as md_file:
        md_file.write("\n\n".join(markdown_entries))

if __name__ == "__main__":
    dois = ["10.1126/science.adn9560", "10.1038/s41556-024-01379-x"]  # DOIs
    main(dois)
