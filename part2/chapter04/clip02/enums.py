from enum import Enum


class Dalles(str, Enum):
    IMAGE_PROMPT = """
  please draw an image of the cover of the children's book based on the characters and the requirements and the children's book title below. In a waterolor style.
  """


class PromptTemplates(str, Enum):
    TITLE_PROMPT = """please write a title for a children's book base on the characters and requirements below
    
    [characters] 
    {characters}
    
    [requirements]
    {requirements}
    
    title : 
  """

    PLOT_PROMPT = """please write a plot for a children's book base on the characters and requirements and title below
    
    [characters] 
    {characters}
    
    [requirements]
    {requirements}
    
    [title]
    {title}
    
    plot : 
  """
