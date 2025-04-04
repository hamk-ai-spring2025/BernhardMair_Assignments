#Task 5 (Bernhard Mair)
"""
Image-to-text-to-image generator. Generate a command line or GUI program, which reads an image and uses AI to generate
textual description of it. It prints the description to standard output, but also attempts to generate image using the
description of image as input prompt for the image generation. You can use OpenAI Vision API and Dall-E 3 or some other
if you want. However: this assignment is not supposed to be real image-to-image model, but really image-to-text and then
feed that text output to text-to-image model.
"""

from markitdown import MarkItDown
from openai import OpenAI
import replicate
#import argparse


#sample files
#image_input = "20230430_143716.jpg" # .JPG flower & field
#image_input = "20230528_003912.jpg" # .JPG pink tractor
image_input = "20240723_190211.jpg" # .JPG smallest petrol station
#image_input = "20240729_214652.jpg" # .JPG special rainbow/halo
#image_input = "20250319_222208.jpg" # .JPG food in fridge
#image_input = "DSC7946.jpg" # .JPG blueberries
#image_input = "DSC8817.jpg" # .JPG tree with yellow leaves
#image_input = "look_super_intelligent.png" # .PNG self

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "gemma-3-4b-it"  #small and fast, but limited to 4096 input-tokens
system_prompt = "You analyze images efficiently and accurately. Don't use any preamble. Describe the image in detail."
# print("SYSTEM PROMPT ==> ", system_prompt)

md = MarkItDown(llm_client=client, llm_model=model) #send the source through the LLM

# Process each input file or URL
result = md.convert(image_input).text_content
    
#print(result)

story = [{"role": "system", "content": system_prompt},
         {"role": "user", "content": result}]

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

print("Prompt:\n",content_response)
print("\n==========")

with open('output.txt', 'w', encoding="utf-8") as f:
        f.write(content_response)

print("The following code will generate a new image using Replicate.")
print("Costs will occur if you continue!!!")
wait = input("Hit ENTER to continue. Hit Q to end the program and get the prompt only.")

if wait == "q" or wait =="Q":
    print("\n==========")
    print(f"Prompt saved as output.txt")
    exit()
    
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": content_response,
        "go_fast": True,
        "megapixels": "1",
        "num_outputs": 1,
        "aspect_ratio": "1:1",
        "output_format": "png",
        "output_quality": 80,
        "num_inference_steps": 4
    }
)
print(output)

# Save the generated image
with open('output.png', 'wb') as f:
    f.write(output[0].read())

print("\n==========")
print(f"Image saved as output.png")
print(f"Prompt saved as output.txt")
