import discord
from discord.ext import commands
import random
import json
import os
import time
import random
#get all the important packages, ya know
client = commands.Bot(command_prefix = "/")

@client.event
async def on_ready():
  print("Ready")
#defines the client and puts it up online
  
@client.command()
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  wallet_amt = users[str(user.id)]["wallet"]
#this will get the data from the .json file
  em = discord.Embed(title = f"{ctx.author.name}'s balance", color =random.randint(0, 16777215) )
  em.add_field(name = "Wallet balance",value = wallet_amt)
  await ctx.send(embed = em)

@client.command()
async def dice(ctx, bet: int):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author    
    d1 = ['1', '2', '3', '4', '5', '6']
    d2 = ['1', '2', '3', '4', '5', '6']   
    r1 = random.choice(d1)
    r2 = random.choice(d2)


    embed1=discord.Embed(title="Dices", color =random.randint(0, 16777215) )
    embed1.add_field(name="You rolled", value=r1, inline=False)
    embed1.set_footer(text="Made by Lb")
    embed2=discord.Embed(title="Dices")
    embed2.add_field(name="You rolled", value=r1, inline=False)
    embed2.add_field(name="Bot rolled", value=r2, inline=False)
    embed2.set_footer(text="Made by Lb")
    

    betwin = bet*2
    if users[str(user.id)]["wallet"] < bet:
      await ctx.send("You do not have enough money to make this bet.")
      return False
    users[str(user.id)]["wallet"] -= bet
    await ctx.send("Rolling...")
    time.sleep(2)
    msg = await ctx.send(embed=embed1)
    time.sleep(2)
    await msg.edit(embed=embed2)
    if r1 > r2:
      users[str(user.id)]["wallet"] += bet*2
      await ctx.send("Congratulations! You won " + str(betwin) + " Coins!")
    if r2 > r1:
      await ctx.send("You lost " + str(bet) + " Coins!")

    if r1 == r2:
      users[str(user.id)]["wallet"] += bet
    with open("users.json", "w") as f:
      json.dump(users, f)


@client.command()
async def coinflip(ctx, side: str, bet: int):
  await open_account(ctx.author)
  users = await get_bank_data()
  user = ctx.author  
  sides = ["Heads", "Tails"]
  res = random.choice(sides)
  if users[str(user.id)]["wallet"] < bet:
      await ctx.send("You do not have enough money to make this bet.")
      return False
  #Flipping coin
  fc=discord.Embed(title="Coin Flip")
  fc.add_field(name="Flipping Coin..", value= "flipping...", inline=False)

  #flipping coins Heads
  fch=discord.Embed(title="Coin Flip")
  fch.add_field(name="Coin landed on " , value= res, inline=False)

  #Flipping coin headwin
  fchw=discord.Embed(title="Coin Flip")
  fchw.add_field(name="Coin landed on ", value= "Heads", inline=False)
  fchw.add_field(name="You won ", value= str(bet*2), inline=False)

  #Flipping coins Tails
  #fct=discord.Embed(title="Coin Flip")
  #fct.add_field(name="Coin landed on Tails", value= ".", inline=False)

  #Flipping coins Tails win
  fctw=discord.Embed(title="Coin Flip")
  fctw.add_field(name="Coin landed on ", value= "Tails", inline=False)
  fctw.add_field(name="You won " , value= str(bet*2), inline=False)
  #Flipping coin tailsloose
  fctf=discord.Embed(title="Coin Flip")
  fctf.add_field(name="Coin landed on ", value= "Tails", inline=False)
  fctf.add_field(name="You lost ", value= str(bet), inline=False)
  #Flipping coin headloose
  fchl=discord.Embed(title="Coin Flip")
  fchl.add_field(name="Coin landed on ", value= "Heads", inline=False)
  fchl.add_field(name="You lost ", value=str(bet), inline=False)


  users[str(user.id)]["wallet"] -= bet
  msg = await ctx.send(embed=fc)
  time.sleep(1)
  await msg.edit(embed=fch)
  time.sleep(3)
  if res == "Heads":
    if side == "Heads":
      time.sleep(1)
      await msg.edit(embed=fchw)
      users[str(user.id)]["wallet"] += bet*2
  if res == "Tails":
    if side == "Heads":
      time.sleep(1)
      await msg.edit(embed=fchl)
      

  if res == "Heads":
    if side == "Tails":
      time.sleep(1)
      await msg.edit(embed=fctl)
      
  if res == "Tails":
    if side == "Tails":
      time.sleep(1)
      await msg.edit(embed=fctw)
      users[str(user.id)]["wallet"] += bet*2
  with open("users.json", "w") as f:
    json.dump(users, f)    



  



@client.command()
async def add(ctx, a: int):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    users[str(user.id)]["wallet"] += a
    with open("users.json", "w") as f:
        json.dump(users, f)

@client.command()
async def remove(ctx, b: int):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    users[str(user.id)]["wallet"] -= b
    with open("users.json", "w") as f:
        json.dump(users, f)

@client.command()
async def beg(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()
#fetches the data for the author
  user = ctx.author

  earnings = random.randrange(101)

  await ctx.send(f"Someone gave you {earnings} coins!!")
#randomizes the earnings and tells you
  users[str(user.id)]["wallet"] += earnings

  with open("users.json", "w") as f:
    json.dump(users, f)

async def open_account(user):

  users = await get_bank_data()

  if str(user.id) in users:
    return False
  with open("users.json","r") as f:
    users = json.load(f)
  
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
  
  with open("users.json", "w") as f:
    json.dump(users,f)
  return True

async def get_bank_data():
  with open("users.json", "r") as f:
    users = json.load(f)
  return users

client.run('')
