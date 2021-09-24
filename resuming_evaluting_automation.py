# -*- coding: utf-8 -*-


#Requirements To be install new
pip install pdfminer.six
pip install spacy #because spacy itself has many nlp structures means already pretrained models
python3 -m spacy download en_core_web_sm #english model
pip3 install pandas #data manipulation

#importing libraries
import spacy
nlp = spacy.load('en_core_web_sm')
text = "Iron Man is a superhero machine learning appearing in American comic books published by Marvel Comics. The character was co-created by writer and editor Stan Lee, developed by scripter Larry Lieber, and designed by artists Don Heck and Jack Kirby. The character made his first appearance in Tales of Suspense #39 (cover dated March 1963), and received his own title in Iron Man #1 (May 1968). Also in 1963, the character founded the Avengers alongside Thor, Ant-Man, Wasp and the Hulk. publication history, Iron Man has been a founding member of the superhero team the Avengers and has been featured in several incarnations of his own various comic book series. Iron Man has been adapted for several animated TV shows and films. In the Marvel Cinematic Universe, the character was portrayed by Robert Downey Jr., appearing in the films Iron Man (2008), "
words = nlp(text) #load the text with spacy language model then only we can do tokenize tagging parsing etc...

#little spacy falvours because nlp is wide in research so we cant cover fully here
for token in words:
  print(token)

#now we are going to take the noun words (if we leave to annotate the language model to read the paragraph it opens which is adjective,noun and opening and closing all that....)

for token in words:
  if token.pos_ == "NOUN":
    print(token)

#(named entity recongintion) it shows for ex google => organization , August => date like that whether it is noun,adjective etc..
for namedentity in words.ents:
  print(namedentity.text,namedentity.label_)

#resume automation starts here!!
#Collecting requirement
#https://raw.githubusercontent.com/pdfminer/pdfminer.six/develop/tools/pdf2txt.py => pdftotxt.py

import pandas as pd #csv tabular 
import spacy #nlp
import pdfminer # pdftotext
import re #regex
import os #file maupulation
import pdf2txt

#converting pdf to text

def convert_to_pdf(f):
  output_filename = os.path.basename(os.path.splitext(f)[0])+".txt" #hello.pdf => hello.txt because python has 0 index language
  filepath = os.path.join("output/txt/",output_filename)
  pdf2txt.main(args=[f,"--outfile",filepath]) #the main function in pdf2txt takes multiple *args 
  print(filepath + "Saved successfully")
  return open(filepath).read()

#loading the language model
nlp = spacy.load("en_core_web_sm")

#declaring the variables for extraction
# why we are doing this means when we getting more files it will stores all information into structure format
result = {'name':[],'phone':[],'email':[],'skills':[]}
names=[]
phones = []
emails =[]
skills =[]

def parse_content(text):
  skillset = re.compile("python|java|sql|tableau|hadoop|big data") #skillset is defined in the basics of position for ex in this case we defined for data science role so we want skills like python, sql etc...
  phone_num = re.compile("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})") #for matching mobile numbers
  doc = nlp(text) #annotating the text => spacy
  name = [candidate.text for candidate in doc.ents if candidate.label_ is "PERSON"][0] #all resumes contains name at first so i used [0] like first occurence  
  email = [word for word in doc if word.like_email == True] #=>like_email is a spacy inbuilt return boolean
  phone = re.findall(phone_num,text.lower())
  skills_list = re.findall(skillset,text.lower())
  unique_skills_list = str(set(skills_list)) # because if they use python in skills and they will tell the project section the name python again so we want to reduce it so we can use this set method because set method removes the duplicates 
  names.append(name)
  phones.append(phone)
  emails.append(email)
  skills.append(unique_skills_list)
  result['name'] = names
  result['email'] = emails
  result['phone'] = phones
  result['skills'] = skills
  print("Extraction Completed from the resume......")
  convertingtocsv()

def convertingtocsv():
  result_df = pd.DataFrame(result) #df => data frame used to see in strucutre prefect format
  result_df.to_csv('output/csv/extractedinfo.csv')
  print("Completed check on csv folder thank you for using me!!")

def main():
  for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
      print("reading file.....",file)
      txt = convert_to_pdf(os.path.join('resumes/',file))
      parse_content(txt)

main()
