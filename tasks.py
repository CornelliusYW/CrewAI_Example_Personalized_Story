from crewai import  Task
from agents import *
from dotenv import load_dotenv
load_dotenv()

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
