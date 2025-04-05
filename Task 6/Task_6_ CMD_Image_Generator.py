#Task 6 (Bernhard Mair)
"""
Generate a versatile command line utility for image generator using your favorite image generator.
User should be able to adjust the prompt, possible negative prompt (if the image generator supports it),
seed (if the image generator supports it) and aspect ratio of the image (e.g. square 1:1, 16:9, 4:3, 3:4).
You can add more parameters if you want. User can also define the number of images it generates.
The program will print out the URL where they can be downloaded, but it will also download them and save
into current directory with automatically generated file names and prints out those file names.
"""

#Import libraries
import argparse
import replicate

#Setup argparse
parser = argparse.ArgumentParser(
                    prog='Task_6_CMD_Image_Generator.py',
                    description='Generate images via the command line',
                    epilog='Use with care.')
parser.add_argument('-p','--prompt', type=str, default='Snowman in summer, sunbathing at the beach and wearing sunglasses.',help='Prompt for generated image.') # prompt
parser.add_argument('-s', '--seed',type=int,help='Random seed. Set for reproducible generation.') # seed
parser.add_argument('-a','--aspect',type=str,default='1:1',help='Aspect ratio for the generated image: e.g. 16:9, 4:3, 3:4. Default is 1:1')  # aspect ratio
parser.add_argument('-n','--number',type=int,choices=[1,2,3,4],default=1,help='Number of outputs to generate. Default is 1.')
parser.add_argument('-f','--format',type=str,choices=['png','jpg','webp'],default='png',help='Format of the output images - png, jpg or webp. Default is png')
parser.add_argument('-m','--megapixel',type=str,default='1',help='Approximate number of megapixels for generated image. Default is 1')
parser.add_argument('-q','--quality',type=int,default=80,help='Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs')
parser.add_argument('-i','--iteration',type=int,choices=[1,2,3,4],default=4,help='Number of denoising steps. 4 is recommended, and lower number of steps produce lower quality outputs, faster.. Values 1-4. Default is 4.')
args = parser.parse_args()

#Create prompt and other parameters
query_prompt = args.prompt
query_seed = args.seed
query_aspectratio = args.aspect
query_number = args.number
query_format = args.format
query_megapixel = args.megapixel
query_quality = args.quality
query_steps = args.iteration
model = 'black-forest-labs/flux-schnell'

#Print query values
print('==========')
print('Query values using '+model+':')
print('----------')
print('Prompt:                    ',query_prompt)
print('megapixel:                 ',query_megapixel)
print('Number of outputs:         ',query_number)
print('Aspect ratio:              ',query_aspectratio)
print('Output format:             ',query_format)
print('Output quality:            ',query_quality,'%')
print('Number of interface steps: ',query_steps)
print('Seed:                      ',query_seed, ' (Not in use!)')
print('==========')

#Generate output
output = replicate.run(
    model,
    input={
        "prompt": query_prompt,
        "go_fast": True,
        "megapixels": query_megapixel,
        "num_outputs": query_number,
        "aspect_ratio": query_aspectratio,
        "output_format": query_format,
        "output_quality": query_quality,
        "num_inference_steps": query_steps
    }
)

#Store output in file(s)
print("Output files for each image")
print('----------')
for idx, file_output in enumerate(output):
    with open(f'output_{idx+1}.'+query_format, 'wb') as f:
        f.write(file_output.read())
        print(f"Image {idx+1} stored locally in file: output_{idx+1}."+query_format)
print('==========')

#Provide URL to file(s)
print("Output files for each image")
print('----------')
for i in range(query_number):
    url = output[i].url
    print(f"File {i+1} available at: {url}")
print('==========')
print("\nOnline files are available for 1 hour before they are deleted automatically.")