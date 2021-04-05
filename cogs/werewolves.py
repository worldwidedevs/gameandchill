import discord
from discord.ext import commands
import random

class Werewolve(commands.Cog, name="Werewolves (ww.[command])"):

  def __init__(self, bot):
    self.bot = bot

  roles = [
        ["Villager", # Villager
        "Your goal is to kill all werewolves by voting.",
        "The most commonplace role, a simple Villager, spends the game trying to root out who they believe the werewolves (and other villagers) are. While they do not need to lie, the role requires players to keenly sense and point out the flaws or mistakes of their fellow players. Someone is speaking too much? Could mean they're a werewolf. Someone isn't speaking enough? Could mean the same thing. It all depends on the people you're playing with, and how well you know them."],
        ["Witch", # Witch
        "You have a heal potion which can revive the victim and a deadly potion, which can kill anybody. Be careful, both can only be used once",
        "This role, while first and foremost taking on all the elements of a regular Villager throughout the game, also has the additional powers of one potion and one poison, which they may use at any point throughout the game. When the Witch is added, the Moderator will wake them up separately during the night with, “The Witch comes awake…” and follows this with “The Witch brings someone back to life.” and “The Witch poisons someone.” The Witch will then point to the person they want to poison or bring back to life."],
        ["Hunter", # Hunter
        "When you die, you can take a person of your choice with you.",
        "Known amongst the villagers, the Hunter is the one providing fresh meat to the village. Also respected for his aim and because he could easily kill someone if he desires to do so."],
        ["Seer" # Seer
        ,"You're able to see the role of a person of your choice every night",
        "Provided with inhuman powers, she usually these powers for the village. As one of the mightiest roles, she can detect the will of people and seperate between good and evil. The village respects her as the most known elder and always takes her decisions into consideration."],
        ["Guardian", # Guardian
        "You must protect a person of your choice every night. That person will not die for that night.","Trained from a very young age, this role was always decided to become the villages Guardian. Rough training steeled his reflexes so now he could be considered a fighting machine. He still is only able to defend one person at a time, so i may be risky for him to defend someone else, as he might die himself. Furthermore his mindset restricts him to never defend the same person twice in a row."],
        ["Hoe", # Hoe
        "You can decide to sleep with anyone you choose every night. When you would be the victim while sleeping somewhere else you will not die. However, if the person you sleep with dies, you also die.",
        "Well . . . what am I gonna say . . .\nYou have been teached in the arts of seduction in order to survive. The women of the village disregard you and treat you shamefully, but their husbands would secretly take you over them hundred times.\nBONK!"],
        ["Armor", # Armor
        "You can make 2 people fall in love in the first night. If one of them dies, the other one will do so too. They can also accomplish the love-victory. If only those two survive, they also won the game, and the werewolves and villagers lost.",
        "The God of Love is amongst the villagers. As he desires love, he can make two people fall in love. This does not exluce himself, so if he wants he can also fall in love. Whether you want to play as a normal villager or want to win as a part of the couple, is in your hands."],
        ["Doctor", # Doctor
        "Your can heal one person every night and protect them from dieing that night.",
        "Also a villager, the Doctor has the ability to heal themselves or another villager when called awake by the Moderator during the night. Should they heal themselves, then will be safe from being killed by the werewolves, or should they want to prove themselves the Doctor or fear the death of a fellow villager, can opt to heal them instead. Again, the strategy here is up to you."]
      ] 

  # Start_Game______________________________________________________________
  @commands.command(aliases=["sw", "pw", "start werewolve", "play werewolves"], pass_context=True)
  async def start_werewolve(self, ctx):
    if ctx.prefix != "ww.": return

    global roles

    # playerlist erstellen
    try:
        playerlist = ctx.author.voice.channel.members
    except AttributeError:
        await ctx.send("You can only start a game while you're on a server, in a voice channel together with your friends.")
        return

    playercount = len(playerlist)

    # Fehlerabfang
    # if playercount < 5: # -> 0 werewolves and no fun
      # await ctx.send("You should be at least 5 players, else there is no fun.")
      # return
    for player in playerlist: # Bot im Channel -> removen
      if player.bot == True:
        playerlist.remove(player)


    # Werwolanzahl in Rollen einrechnen bzw. Liste an gebrauchten Rollen erstellen
    werewolvecount = round(playercount/5)
    calc_roles = []
    random_role_count = playercount - werewolvecount
    for role in range(random_role_count): # Calculate Rolelist
      random_role = random.choice(roles)
      calc_roles.append(random_role)
      roles.remove(random_role)
    for werewolve in range(werewolvecount): # Add Werewolves
      calc_roles.append(["Werewolve","Your goal is to kill everybody until there are only werewolves left.","The goal of the werewolves is to decide together on one villager to secretly kill off during the night, while posing as villagers during the day so they're not killed off themselves. One by one they'll kill off villagers and win when there are either the same number of villagers and werewolves left, or all the villagers have died."])

    playerlist_copy = playerlist.copy()

    for role in calc_roles:
      print(role[0])

    for role in calc_roles:
      print("") # leerzeile

      random_player = random.choice(playerlist_copy)
      playerlist_copy.remove(random_player)

      # Role Printen
      print(f"Random_Player: {random_player}")
      print(f"Role: {role[0]}")

      # messaged player his role
      await ctx.send(f"Sending role to {random_player}")
      dm_channel = await random_player.create_dm()
      embed=discord.Embed(title=role[0], description="A new game has started!", color=0x8f2c01)
      embed.add_field(name="Task", value=role[1], inline=True)
      embed.add_field(name="Description", value=role[2], inline=False)
      await dm_channel.send(embed=embed)

    # ________________________Nacht__________________________
    '''
    reihenfolge = ["Hoe","Werewolve",""]
    
    if "Hoe" in calc_roles:
      # Get Player for Hoe and dmchannel
      await dmchannel.send("Do you want to sleep with someone this night? If so please type his name.")
    '''

def setup(bot):
  bot.add_cog(Werewolve(bot))