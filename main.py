import time
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file and initiate the OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a cover letter for a job advertisement
def create_coverLetter(jobAd, resume, template):
    
    language = "Norwegian"
    rules = "You are a cover letter generator. Use the provided template cover letter and adjust it to the job advert. Reference the resume. Make it ATS-friendly. Language: "+ language + "."
    content = "This is my resume: " + resume + ".\n This is the cover letter template: " + template + ".\n Write a cover letter for the following job adveritsement: " + jobAd + ". "

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": rules},
      {"role": "user", "content": content}
    ]
    )

    return completion.choices[0].message.content, completion.usage.completion_tokens, completion.usage.prompt_tokens, completion.usage.total_tokens


# Open the resume file
with open("resume.txt", "r", encoding="utf8") as file:
    resume = file.read()

with open("template.txt", "r", encoding="utf8") as file:
    template = file.read()

print("\n")
print("Starting cover letter generation...\n")

tokenSum = 0
totalCost = 0
startTime = time.time()

#Parse through the jobAds folder
for filename in os.listdir('jobAds'):
    
    # Start the timer for the generation of the current cover letter
    startGenTime = time.time()

    # Open the job advertisement
    with open('jobAds/' + filename, 'r',  encoding="utf8") as file:
        jobAd = file.read()

    print("Generating application for " + filename.replace(".txt", "").capitalize())

    # Generate the cover letter
    coverLetter, completionTokens, promtTokens, totalTokens = create_coverLetter(jobAd, resume, template)

    print("Completion tokens: " + str(completionTokens) + ", prompt tokens: " + str(promtTokens) + ", total tokens: " + str(totalTokens))
    print("Time used: " + str(round(time.time() - startGenTime, 2)) + " seconds\n")
    print("Cost ≈ " + str(round(totalTokens*0.0000030837, 5)) + "$\n")

    tokenSum += totalTokens
    totalCost += totalTokens*0.0000030837

    #add the generated cover letter to a new txt file in the coverLetters folder:
    with open('coverLetters/' + filename, 'w', encoding="utf8") as file:
        file.write(coverLetter)

endTime = round(time.time() - startTime, 2)

# Print the statistics for the generation of the cover letters
print("Total tokens used: " + str(tokenSum))
print("Total time used: " + str(endTime) + " seconds")
print("Total cost ≈ " + str(round(totalCost, 5)) + "$")
print("Average tokens per application: " + str(round(tokenSum/len(os.listdir('jobAds')), 2)) + " tokens")
print("Average time per application: " + str(round(endTime/len(os.listdir('jobAds')), 2)) + " seconds")
print("\n")