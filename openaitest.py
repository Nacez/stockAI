from openai import OpenAI
from docx import Document
from docx2pdf import convert
from category_list import seek_categories, seek_categories_test
from skills import skill_list

catgeoriesstr = ", ".join(seek_categories)



messages = [{"role": "system", "content": """
You are a resume analysing tool thats only role is to analyse resumes and output all of the matching tags
             Your output is only in list form. You MUST ONLY use the tags given to you within the system.
"""},
{"role": "system", "content": f""" ONLY USE TAGS WITHIN THIS LIST AND THAT ARE RELATABLE TO THE RESUME | TAGS ARE: {catgeoriesstr}
"""},
    {"role": "user", "content": """
 Kane Rayner is an experienced communications officer with a robust background in public relations and media relations, adept at aligning communication strategies with brand values. 
     He possesses solid skills in networking with media outlets and leveraging social media for positive engagement. Kane has diverse experience in the construction industry, including carpentry and project management, and holds relevant qualifications such as a white card and a driver's license. His recent employment includes part-time roles at Safari Music Records as an A&R and video creator, and at M Group, where he managed stakeholder engagement and recruitment. Previously, he served as a manager at Loukamades,
      overseeing a team and handling customer engagement and business development. Kane has coordinated events like the Sole Sonic Festival and Paradise Music Festival, gaining experience in logistics, budget management, and artist relations. As a former managing director of Darwin Carpentry Services, he established an Indigenous building company and focused on community engagement. His background includes presenting for Hashtag Darwin TV and support roles in radio broadcasting, showcasing his versatility across media and event coordination.
     
"""},
    {"role": "assistant", "content": """
Marketing & Communications, Public Relations, Experience in Marketing & Communications, Experience in Construction, Project Management, Administrative Assistants, Event Coordination, Experience in Community Services & Development, Experience in CEO & General Management, Experience in Advertising, Arts & Media,"""},

]
messages2 = [
    {"role": "system", "content": """
your only job is to summarise the given resume, summarising all key expeirience, skills and roles and to output the sumarrisation into a paragraph.
"""},
]

skillmessages = [
    {"role": "system", "content": """
you will be given a work related key phrase/word. you need to then list 5 skills that have connection to in the python format stored within the system.
"""},
    {"role": "user", "content": """
Project Management
"""},
    {"role": "assistant", "content": """
     {
     "skillcat":"Project Management",
     "skills":[
"Time Management", "Communication Skills","Risk Management", "Budgeting and Financial Management", "Leadership and Team Management"]}

"""},
    {"role": "user", "content": """
Hotel Management
"""},
    {"role": "assistant", "content": """
{
    "skillcat": "Hotel Management",
    "skills": [
        "Customer Service Skills",
        "Operations Management",
        "Revenue Management",
        "Staff Training and Development",
        "Event Planning"
    ]
}

"""},
]

messages3 = [
    {"role": "system", "content": """
    You are a resume analysing tool thats only role is to analyse resumes and output all of the matching tags
             Your output is only in list form. You MUST ONLY use the tags given to you within the system.
     you have 5 tags of choice you can pick more then one. ONLY PICK NECCASARY TAGS.
"""},
    {"role": "user", "content": """
 Darren Andy is an experienced Trade Assistant and Laborer with a strong background in construction and project support. He possesses a variety of safety certifications including RIW Rail Ticket, EWP ticket, confined spaces, and working at heights. Currently, he is employed at UGL on the Sydney Metro Line-wide project, where he specializes in cable running and earth bar connections. Previous roles include laboring and plastering at Brighton Ceilings, skilled laboring and framing at Brighton (CPB Contractors) for NEPEAN HOSPITAL, and assisting trades at Downer, including boiler makers and fitters. Earlier in his career, he gained experience in scaffolding and field assistance, with a focus on measuring and surveying. Darren is recognized for his analytical thinking, attention to detail, time management, and teamwork skills, further supplemented by over a decade of experience in various labor-intensive roles. References are available from UGL and Jim McDonald Building Group.
"""},
    {"role": "assistant", "content": """
Safety Compliance, Construction Methods and Materials Knowledge, Team Coordination
    """},
]

def resume_summariser(prompt):
    messages2.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages2,
        stream=True
    )
    generated_response = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            generated_response += chunk.choices[0].delta.content
    messages2.append({"role": "assistant", "content": generated_response})
    return generated_response.strip()


def summarise_tagger(prompt):
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    generated_response = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            generated_response += chunk.choices[0].delta.content
    messages.append({"role": "assistant", "content": generated_response})
    return generated_response.strip()


def skill_tagger(skill_list,prompt):
    messages3.append({"role": "system", "content": f"You must pick from this list: {skill_list}"})
    messages3.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages3,
        stream=True
    )
    generated_response = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            generated_response += chunk.choices[0].delta.content
    messages3.append({"role": "assistant", "content": generated_response})
    messages3.pop()
    messages3.pop()
    messages3.pop()

    return generated_response.strip()




def temp_skiller(prompt):
    skillmessages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=skillmessages,
        stream=True
    )
    generated_response = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            generated_response += chunk.choices[0].delta.content
    skillmessages.append({"role": "assistant", "content": generated_response})
    return generated_response.strip()

#while True:
 #   user_input = input("You: ")
  #  if user_input.lower() in ["quit", "bye", "q", "exit"]:
   #     break
    #response = chat_with_gpt(user_input)
    #print("ChatBot:", response)

temp_skill = []
while True:
    user_input = input("You: ")
    if user_input =="q":
        break

    response = resume_summariser(user_input)  

    print(f"\n {response}  \n")  
    tag = summarise_tagger(response)
    print("ChatBot:", tag)
    tag_list = tag.split(", ")
    print(tag_list)

    for tag in tag_list:
        for skill in skill_list:
            if tag == skill["skillcat"]:
                skillstring = ", ".join(skill["skills"])

                moretags = skill_tagger(skillstring,response)
                moretags_list = moretags.split(", ")
                tag_list.extend(moretags_list)
                print(tag_list)
                print("done")
    
    unique_tag_list = list(set(tag_list))
    print(unique_tag_list)





# import os

# def open_and_write_notepad(filename, text):
#     """Opens Notepad and writes text into a file."""
#     with open(filename, "w") as file:
#         file.write(text)
    
#     os.system(f'notepad {filename}')

# for x in seek_categories_test:
#         response = temp_skiller(x)  
#         temp_skill.append(response)
#         print("ChatBot:", response)

# catgeoriesstr1 = ", ".join(temp_skill)

# print(f"skill_list = [{catgeoriesstr1}]")
# open_and_write_notepad("skills.txt", f"skill_list = [{catgeoriesstr1}]")


