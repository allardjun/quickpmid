import requests
import xml.etree.ElementTree as ET

def fetch_pubmed_data(doi):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': doi,
        'rettype': 'xml',
        'retmode': 'xml'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    article = root.find('.//PubmedArticle')
    if article is None:
        return None

    author_list = article.find('.//AuthorList')
    if author_list is not None:
        authors = ' and '.join([f'{author.find("LastName").text}, {author.find("ForeName").text}' for author in author_list if author.find("LastName") is not None])
    else:
        authors = "Unknown Author"

    article_title = article.find('.//ArticleTitle').text
    journal = article.find('.//Journal/Title').text
    year = article.find('.//PubDate/Year').text
    doi = article.find('.//ArticleId[@IdType="doi"]').text if article.find('.//ArticleId[@IdType="doi"]') is not None else 'N/A'

    return {
        'authors': authors,
        'title': article_title,
        'journal': journal,
        'year': year,
        'DOI': doi
    }

def generate_bibtex(entry):
    bibtex_entry = f"""
@article{{{entry['DOI']},
    author = {{{entry['authors']}}},
    title = {{{entry['title']}}},
    journal = {{{entry['journal']}}},
    year = {{{entry['year']}}},
    DOI = {{{entry['DOI']}}},
}}
"""
    return bibtex_entry.strip()

def generate_markdown(entry):
    first_author = entry['authors'].split(',')[0].strip()
    markdown_entry = f"- **{first_author} et al.** - {entry['title']} - *{entry['journal']}* - {entry['year']}"
    return markdown_entry

def main(dois):
    bib_entries = []
    markdown_entries = []
    for doi in dois:
        xml_data = fetch_pubmed_data(doi)
        if xml_data:
            entry = parse_xml(xml_data)
            if entry:
                bib_entries.append(generate_bibtex(entry))
                markdown_entries.append(generate_markdown(entry))
    
    with open("output.bib", "w") as bib_file:
        bib_file.write("\n\n".join(bib_entries))
    
    with open("output.md", "w") as md_file:
        md_file.write("\n\n".join(markdown_entries))

if __name__ == "__main__":
    dois = ["10.1126/science.adn9560"]  # Example DOIs
    main(dois)
