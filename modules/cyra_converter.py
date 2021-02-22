import difflib
import re
import discord
from discord.ext import commands
import modules.custom_exceptions as custom_exceptions
from modules.cyra_constants import hero_synonyms, ability_synonyms, hero_list, achievements, achievement_synonyms

def find_closest(word, word_list):
  close_word = difflib.get_close_matches(word, word_list, n=1)
  if close_word:
    return close_word[0]
  return None
  
def find_hero_from_emoji(ctx, argument):
  # read a hero emoji
  match = re.match(r'<(a?):hero_([a-zA-Z]+)([0-9]+):([0-9]+)>$', argument)
  if match:
    hero_name = match.group(2).lower()
    if hero_name not in hero_list:
      raise custom_exceptions.HeroNotFound(hero_name.title())
    emoji_id = int(match.group(4))
    emoji = discord.utils.get(ctx.guild.emojis, id=emoji_id)
    if not emoji:
      emoji = ctx.bot.get_emoji(ctx.guild, hero_name)
    return hero_name, emoji
  raise custom_exceptions.HeroNotFound(argument.title())

class find_hero(commands.Converter):
  # convert a hero input to a string
  async def convert(self, ctx, word):
    try:
      hero, _ = find_hero_from_emoji(ctx, word)
      return hero
    except:
      word = word.lower()
      close_word = find_closest(word, list(hero_synonyms))
      if close_word:
        return hero_synonyms[close_word]
      raise custom_exceptions.HeroNotFound(word.title())
  
class hero_emoji_converter(find_hero):
  # convert a hero input to an emoji, can be used to distinguish skins
  async def convert(self, ctx, argument):
    try:
      _, emoji = find_hero_from_emoji(ctx, word)
    except:
      hero = await super().convert(ctx, argument)
      emoji = ctx.bot.get_emoji(ctx.guild, hero)
    if emoji:
      return emoji
    raise custom_exceptions.HeroNotFound(argument.title())
  
def find_ability(word):
  word = word.lower()
  if word.split(" ", 1)[0] in ["rank1", "rank2", "rank3", "rank4", "rank5", "rank6", "rank7"]:
    return word.replace("rank", "r", 1)
  if word in ability_synonyms:
    return ability_synonyms[word]
  return word
  
def find_achievement(name):
  name = name.lower()
  close_word = find_closest(name, list(achievement_synonyms))
  if close_word:
    return achievement_synonyms[close_word]
  raise custom_exceptions.DataNotFound("Achievement", name.title())
  
def toMode(argument):
  argument = argument.lower()
  if argument in ["legend", "legendary"]:
    return "legendary"
  elif argument in ["camp", "campaign"]:
    return "campaign"
  raise custom_exceptions.DataNotFound("Mode", argument.title())

def toWorld(argument):
  world = argument.lower()
  if world.startswith("world"):
    world = world.replace("world", "", 1)
  elif world.startswith("w"):
    world = world.replace("w", "", 1)
  world = world.strip()
  return int(world)
  
def toLevelWorld(argument):
  world = argument.lower()
  if world.startswith("world"):
    return int(world[5:].strip())
  elif world.startswith("w"):
    return int(world[1:].strip())
  elif world in ["s", "sr", "shattered realms", "shatteredrealms"]:
    return "S"
  elif world in ["a", "arcade", "arcades"]:
    return "A"
  elif world in ["e", "endless"]:
    return "E"
  elif world in ["c", "challenge", "challenges"]:
    return "C"
  elif world in ["connie", "connie story", "conniestrory"]:
    return "Connie"
  raise custom_exceptions.DataNotFound("World", argument.title())
  
def numberComparisonConverter(argument):
  if "->" in argument:
    numbers = argument.split("->")
    return int(numbers[0]), int(numbers[1])
  else:
    return int(argument)
