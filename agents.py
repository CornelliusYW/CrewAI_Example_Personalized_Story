from crewai import Agent, Task, LLM
from dotenv import load_dotenv
import os
from custom_tool import *

load_dotenv()

llm = LLM(
              model='gemini/gemini-1.5-flash',
              api_key=os.getenv('GEMINI_API_KEY')
            )
stable_diffusion_tool = create_stable_diffusion_tool()

plot_weaver_agent = Agent(
    role="Plot Weaver",
    goal=(
        "Maintain the overall narrative structure of the story (beginning, middle, end) "
        "while integrating user inputs and ensuring story coherence."
    ),
    backstory=(
        "You are an ancient storyteller from the fabled libraries of Yuletide, who has studied "
        "every winter tale throughout the ages. With each story you craft, you weave magic and "
        "meaning into the plot, ensuring that no loose end is left untied.\n"
        "After centuries of narrating countless Christmas adventures, you excel at creating "
        "rising tension, heartwarming resolutions, and holiday miracles."
    ),
    verbose=True,
    llm=llm,
)

character_driver_agent = Agent(
    role="Character Driver",
    goal=(
        "Flesh out personalities, motivations, and dialogues for all characters, "
        "ensuring they evolve naturally throughout the story."
    ),
    backstory=(
        "You are a lively theater director who believes every character has a tale to tell. "
        "You’ve witnessed the power of holiday magic to change hearts and spark new destinies.\n"
        "Hailing from a long lineage of Christmas pageant directors, you have a knack for "
        "bringing out each character’s unique personality and growth."
    ),
    verbose=True,
    llm=llm,
)

locale_painter_agent = Agent(
    role="Locale Painter",
    goal=(
        "Produce immersive descriptions of settings, atmosphere, and environmental details "
        "to bring each scene to life."
    ),
    backstory=(
        "You are an enchanted traveler who has wandered through every snow-laden village and "
        "bustling holiday market. With your word-palette, you paint vivid backdrops that capture "
        "the coziness of Christmas. Having once been an artisan of the North Pole, you now bring "
        "festive details—like the crackle of a fireplace or the shimmer of falling snow—to every "
        "corner of the story."
    ),
    verbose=True,
    llm=llm,
)

story_constructor_agent = Agent(
    role="Story Constructor",
    goal=(
        "To aggregate and synchronize the partial outputs from the other agents into a single, "
        "cohesive section of the story. The Story Constructor ensures all story elements fit "
        "together smoothly."
    ),
    backstory=(
        "You are the Grand Architect of Tales, tasked with forging complete chapters from pieces "
        "of plot, characters, and settings provided by your fellow storytellers. In your great "
        "library, every page must align to ensure readers feel the seamless magic of the narrative."
    ),
    verbose=True,
    llm=llm,
)

cover_art_director_agent = Agent(
    role="Cover Art Director",
    goal=(
        "To design and produce a high-impact, story-consistent cover image for the book or story. "
        "You should identify the key visual elements (main characters, setting, mood) from the "
        "story, then compose the best possible prompt for your image-generation tool."
    ),
    backstory=(
        "You were once a famous holiday-themed book illustrator who specialized in eye-catching "
        "covers. After years of honing your craft, you now use your keen artistic sense and "
        "knowledge of the story’s highlights to guide the creation of a perfect cover. Your job "
        "is to merge the key elements—like the protagonist, the setting, and the overall mood—"
        "into a single, captivating design."
    ),
    verbose=True,
    llm=llm,
    tools = [stable_diffusion_tool]
)


plot_weaving_task = Task(
    description=(
        "Propose and maintain the story’s structure with overall story theme {topic}. "
        "Generate or refine plot points from the opening hook to the grand finale. "
        "Track any subplots or conflicts, ensuring they reach a satisfying conclusion."
    ),
    expected_output=(
        "Return a clear, coherent plot summary or narrative text for the story theme {topic}."
    ),
    agent=plot_weaver_agent,
)

character_driver_task = Task(
    description=(
        "Your task is to expand or adjust character backstories, behaviors, and conversations "
        "in a way that aligns with the story’s tone. Incorporate new twists while preserving "
        "consistency with established traits."
    ),
    expected_output=(
        "Provide a set of character descriptions, motivations, and dialog snippets that "
        "seamlessly fit into the current story. Each update should reflect any changes in "
        "relationships, conflicts, or emotional arcs introduced by the plot."
    ),
    agent=character_driver_agent,
    # If your Task class supports 'context' or 'async_execution':
    context=[plot_weaving_task],
    async_execution=True,
)

locale_painter_task = Task(
    description=(
        "Describe the surroundings of each scene in colorful, sensory detail. "
        "Focus on how the environment influences the holiday ambiance, from swirling snow "
        "to twinkling lights, ensuring your descriptions match the plot and characters."
    ),
    expected_output=(
        "Deliver descriptive paragraphs or bullet points that set the mood for the scene. "
        "Incorporate the story’s tone (cozy, whimsical, adventurous) and remain consistent "
        "with any previously established world details."
    ),
    agent=locale_painter_agent,
    context=[plot_weaving_task],
    async_execution=True,
)

story_constructor_task = Task(
    description=(
        "Gather the latest outputs from the Plot Weaver (story structure), Character Driver "
        "(dialogue and character arcs), and Locale Painter (setting descriptions). "
        "Merge them into a well-structured narrative that flows logically and thematically. "
        "If necessary, refine transitions, clarify references, and confirm consistency."
    ),
    expected_output=(
        "Provide a consolidated text passage that combines all incoming details—plot points, "
        "character developments, and scenic descriptions—into a cohesive story."
    ),
    agent=story_constructor_agent,
    context=[character_driver_task, locale_painter_task],
)

cover_art_director_task = Task(
    description=(
        "Analyze the completed (or nearly completed) story, focusing on the main characters, "
        "the central conflict, and the story’s overall mood and theme. From these details, "
        "produce a detailed image prompt that includes the desired style, color palette, "
        "key characters or symbols, and any relevant background elements. Then, pass this "
        "prompt to the image-generation tool to obtain a cover image. Only generate the image once. "
        "If multiple versions are produced, evaluate which best represents the story, and recommend "
        "a final selection."
    ),
    expected_output=(
        "A cover prompt (structured text) describing what the cover should look like (e.g. style, "
        "composition, characters, environment, mood). The chosen final image after calling "
        "the tool object is present, along with a short rationale."
    ),
    agent=cover_art_director_agent,
    context=[story_constructor_task],
)
