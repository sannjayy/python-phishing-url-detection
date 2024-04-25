import whois
from urllib.parse import urlparse
import httpx
import pickle as pk
import pandas as pd
import extractorFunctions as ef

#Function to extract features
def featureExtraction(url):

  features = []
  #Address bar based features (12)
  features.append(ef.getLength(url))
  features.append(ef.getDepth(url))
  features.append(ef.tinyURL(url))
  features.append(ef.prefixSuffix(url))
  features.append(ef.no_of_dots(url))
  features.append(ef.sensitive_word(url))


  domain_name = ''
  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(1 if dns == 1 else ef.domainAge(domain_name))
  features.append(1 if dns == 1 else ef.domainEnd(domain_name))

  # HTML & Javascript based features (4)
  dom = []
  try:
    response = httpx.get(url)
  except:
    response = ""

  dom.append(ef.iframe(response))
  dom.append(ef.mouseOver(response))
  dom.append(ef.forwarding(response))

  features.append(ef.has_unicode(url)+ef.haveAtSign(url)+ef.havingIP(url))

  with open('model/pca_model.pkl', 'rb') as file:
    pca = pk.load(file)

  #converting the list to dataframe
  feature_names = ['URL_Length', 'URL_Depth', 'TinyURL', 'Prefix/Suffix', 'No_Of_Dots', 'Sensitive_Words',
                       'Domain_Age', 'Domain_End', 'Have_Symbol','domain_att']
  dom_pd = pd.DataFrame([dom], columns = ['iFrame','Web_Forwards','Mouse_Over'])
  features.append(pca.transform(dom_pd)[0][0])

  row = pd.DataFrame([features], columns= feature_names)

  return row