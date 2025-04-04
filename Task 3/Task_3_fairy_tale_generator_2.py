# Task #3 (Bernhard Mair)
"""
Create a standalone program (command line application), which is uses large language model (LLM) to be a creative writer 
e.g. marketing materials, memes, song lyrics, poems or blog posts, which are search engine optimized (SEO) by using as
many possible synonyms as possible. The program should by default produce 3 different versions from the same prompt. 
Try adjusting the system prompt, temperature, top-p, presence penalty and frequency penalty for best possible results. 
Use OpenAI API. You are free to use any version of LLM you want, but try to choose a one suitable for the project 
(e.g. gpt-4o-mini is most likely not ideal).
"""

from openai import OpenAI

# LM Studio is running on localhost:1234
# Make sure to start LM Studio first

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# system prompt
system_prompt = "You write fairy tales for children's bedtime. Write a short fairy tale no longer than 100 words. Use the topic given below. Always start with 'Once upon a time ...' and end with 'THE END and sleep well'. Don't use a preamble."

print("FAIRY TALE GENERATOR")
print("====================")

#define LLM model; REMINDER: start server in LM Studio first !!
model = "gemma-3-4b-it"  #small and fast

print(f"Give a topic, {model} generates a tiny fairy tale for you.")
print(" --> Enter 'exit' or 'quit' to say happily-ever-after.")
print("-----------------------------------------------------------")

#Chat-loop
while True:
    prompt = input("\nWhat is the topic? ... ")
    if prompt == "exit" or prompt == "quit" or len(prompt) == 0 or prompt == "no":
        print("\nFarewell and Happily Ever After")
        break

    # while loop: creates 3 different versions of the same prompt in this loop
    i = 0
    while (i < 3):

        story = [{"role": "system","content": system_prompt},
                   {"role": "user", "content": prompt}]

        completion = client.chat.completions.create(
            model=model,
            messages=story,
            temperature=1.5,
            stream=True,
            top_p=1,
            presence_penalty=1.0,
            frequency_penalty=1.0,
        )

        print (f"\nStory {i+1}:")

        # role assistant gives the answer from the model
        story_response = {"role": "assistant", "content": ""}
   
        # print the answer as it comes, chunk by chunk
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                story_response["content"] += chunk.choices[0].delta.content

        print()

        i+=1







