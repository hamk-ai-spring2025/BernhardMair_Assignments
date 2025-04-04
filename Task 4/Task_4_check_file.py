#Task 4 (Bernhard Mair)
"""
Generate a command line utility program, which feeds the input of one or multiple sources to LLM. The sources you must support,
include text file, URL (html page), csv file, docx file and pdf file.  You can support more input format if you want.
User should be able to provide multiple inputs e.g. local text file and web page, or multiple pdf documents. By default,
if user has not given the query string, the program will perform summarize, but the user can change the query prompt.
By default the output should be printed to standard output, but it should be able to direct it to a file as well.

I recommend to use markitdown or embedchain (for different inputs) and optparse or argparse (to handle command line arguments).
"""

from markitdown import MarkItDown
import argparse
#import pypdf
from openai import OpenAI


# argparse command line arguments
parser = argparse.ArgumentParser(
                    prog='Task_4_check_file.py',
                    description='extracts text from a given file.',
                    epilog='Use with care.')
parser.add_argument('filename',nargs='+',help='Input files or URLs inside quotation marks') # positional argument
parser.add_argument('-q', '--query',type=str,default='Summarize this:',help='Prompt for the LLM, inside quotation marks') # o
parser.add_argument('-f','--file',type=str,help='Optional: write output to file')  # 
args = parser.parse_args()


client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "gemma-3-4b-it"  #small and fast, but limited to 4096 input-tokens
system_prompt = "You are a efficient assistant. Don't use a preamble. " + args.query
print("SYSTEM PROMPT ==> ", system_prompt)

md = MarkItDown(llm_client=client, llm_model=model) #send the source through the LLM
#md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>") #no LLM involved
#md = MarkItDown(enable_plugins=False) # Set to True to enable plugins

#sample files
#input = "Der Zauberlehrling.pdf" #.PFD
#input = "Meeting 24.10.docx" # .DOCX
#input = "https://en.wikipedia.org/wiki/Aurora" # URL
#input = "20250319_222208.jpg" # .JPG
#input = "WorkPlaceSatisfactionSurveyData.xlsx - Data.csv" # .CSV
#input = "data1.xlsx" # .xlsx (too large input for local LLM)

# Process each input file or URL
results = []
for input_source in args.filename:
    result = md.convert(input_source).text_content
    results.append(result)

# Join results from multiple sources
final_result = "\n".join(results)
#print(final_result)

"""
prompt limiting:
1 token ~= 4 chars in English; 100 tokens ~= 75 words;
small local LLM takes ~4096 tokens as input ~= 16000 chars;
2000 chars (500 tokens) for system and 12000 chars (3000 tokens) for content prompt;
output is limited to 500 tokens
XLSX-files need to be limited more, like 5000 chars content prompt
"""
story = [{"role": "system", "content": system_prompt[:2000]},
         {"role": "user", "content": final_result[:12000]}]

summary_response = client.chat.completions.create(
    model=model,
    messages=story,
    temperature=0.7,
    stream=False,
    top_p=0.7,
    presence_penalty=1.0,
    frequency_penalty=1.0,
    max_tokens=5000
        )

# role assistant gives the answer from the model
content_response = summary_response.choices[0].message.content

#save result to file if specified
#f=open('documnet.md','w',encoding="utf-8")
a = 'SHORT SUMMARY\n'
b = '=============\n'
c = '\nFULL CONTENT\n'
d = a + b + str(content_response) + '\n' + c + b + str(final_result)
e = a + b + str(content_response) + '\n'


if args.file:
    with open(args.file, 'w', encoding="utf-8") as f:
        f.write(d)
else:
    print(e)