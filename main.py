from crewai import Agent, Crew, Process, Task
from agents import *
from tasks import *
from custom_tool import *
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
stable_diffusion_tool = create_stable_diffusion_tool()

crew = Crew(
    agents=[
        plot_weaver_agent,
        character_driver_agent,
        locale_painter_agent,
        story_constructor_agent,
        cover_art_director_agent
    ],
    tasks=[
        plot_weaving_task,
        character_driver_task,
        locale_painter_task,
        story_constructor_task,
        cover_art_director_task
    ],
    verbose=True,
    process=Process.sequential,
)

st.title("Holiday Personalized Story Development")
st.markdown("""This is a simulation of using CrewAI agents to develop a story with a few specialized agents to perform tasks, including:
1. **Develop Plot**: Use the Plot Weaver agent to create the story’s overall structure.  
2. **Drive Characters**: Have the Character Driver agent flesh out characters’ motivations and dialogues.  
3. **Paint Locale**: Let the Locale Painter agent describe rich settings and festive atmospheres.  
4. **Construct Story**: Merge all elements via the Story Constructor agent into a cohesive narrative.  
5. **Direct Cover Art**: Employ the Cover Art Director agent to produce a final, story-consistent cover image.
         """)
christmas_story = st.text_input("Enter your Holiday Story theme", "Christmas Carol")

if st.button("Develop Story"):
    result = crew.kickoff(inputs={"topic": christmas_story})

    st.header("Cover Image")
    st.image('output.png')

    st.header("Main Plot")
    st.text(plot_weaving_task.output.raw)

    st.header("Characters")
    st.text(character_driver_task.output.raw)

    st.header("Scene")
    st.text(locale_painter_task.output.raw)

    st.header("Full Story")
    st.text(story_constructor_task.output.raw)
